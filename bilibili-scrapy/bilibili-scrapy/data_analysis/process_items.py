#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""用于将redis中的数据转存至sql数据库，注意sql中必须有insert_procedure存储过程"""
from __future__ import print_function, unicode_literals
import argparse
import json
import time
import datetime
from rediscluster import StrictRedisCluster
from redis import StrictRedis
import pymysql.connections
import sys
sys.path.append(r'.\bilibili-scrapy')
import settings

first_connection = True
host = settings.SQL_HOST
port = settings.SQL_PORT
user = settings.SQL_USER
password = settings.SQL_PASSWORD
database = settings.SQL_DATABASE
table = settings.SQL_TABLE

def get_cursor():
    """通过settings的配置，链接到SQL数据库，通过cursor写入数据"""
    global first_connection
    conn = pymysql.connections.Connection(host=host, port=port, user=user, passwd=password,
                                          database=database, connect_timeout=5, charset='utf8')
    cur = conn.cursor()
    if first_connection is True:
        first_connection = False
        query = '''SELECT COUNT(1)
                    FROM information_schema.TABLES
                    WHERE TABLE_SCHEMA = '{0}' AND TABLE_NAME = '{1}' '''.format(str(database),str(table))
        cur.execute(query)
        count = cur.fetchone()[0]
        if count == 0:
            query = '''CREATE TABLE `{0}` (
                          `id` int(11) NOT NULL,
                          `name` varchar(512) DEFAULT NULL,
                          `av` int(11) DEFAULT NULL,
                          `author` varchar(512) DEFAULT NULL,
                          `plays` int(11) DEFAULT NULL,
                          `barrages` int(11) DEFAULT NULL,
                          `coins` int(11) DEFAULT NULL,
                          `favorites` int(11) DEFAULT NULL,
                          `replys` int(11) DEFAULT NULL,
                          `category` varchar(512) DEFAULT NULL,
                          `url` varchar(512) DEFAULT NULL,
                          `update_time` datetime DEFAULT NULL,
                          `update_time_short` date DEFAULT NULL,
                          `last_crawled` date DEFAULT NULL,
                          PRIMARY KEY (`id`),
                          KEY `date` (`update_time_short`),
                          KEY `author` (`author`),
                          KEY `category` (`category`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''.format(table)
    return cur, conn

def get_safe_item(item):
    """因为拼接sql时使用了单引号，item中的字符串不能出现单引号，将所有单引号转义为双引号"""
    if item['author'].find("'") is not -1:
        item['author'] = item['author'].replace("'",'''"''')
    if item['name'].find("'") is not -1:
        item['name'] = item['name'].replace("'",'''"''')
    if item['category'].find("'") is not -1:
        item['category'] = item['category'].replace("'",'''"''')
    return item

def insert_data(buffer):
    """用于把buffer中的数据写入sql数据库内，buffer每积攒到一定数量的item，才会触发这个函数，缓解sql数据库的压力"""
    try:
        cur, conn = get_cursor()
        for i in range(0,len(buffer)):
            temp = buffer.pop()
            query = '''CALL {0}.insert_procedure'''.format(database)
            query += '''({av},'{name}',{av},'{author}',{plays},{barrages},{coins},'{date}',
            '{date_short}','{category}',{favorites},{replys},'{update_time}','{url}');'''.format_map(temp)
            result = cur.execute(query)
            print('insert ',result)
        print("Inserted {0} items!".format(str(i+1)))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as err:
        print("Error when inserting:"+str(err))
        cur.close()
        conn.close()
        pass

def process_items(r, key, limit=0, log_every=1000, wait=.1):
    """通关set容器访问到所有的av号，之后通过av号来访问redis中的数据将他们转存到sql中"""
    limit = limit or float('inf')
    processed = 0
    buffer = list()
    while processed < limit:
        ret = r.spop(key)
        if ret is None:
            if len(buffer) is not 0:
                insert_data(buffer)
            else:
                time.sleep(wait)
            print("Found no item in set, waiting...")
            continue

        av = ret.decode('utf8')
        print("Get an item, av number:"+str(av))
        try:
            data = r.get(av).decode('utf8')
            item = json.loads(data)
            item = get_safe_item(item)
            if item is not None:
                r.delete(av)
            else:
                print("Av number %s not found in redis" % str(av))
        except Exception:
            print("Failed to load item, av number:"+str(av))
            continue

        try:
            date = time.strptime(item.get('date'), '%Y-%m-%d %H:%M')
            buffer.append({
                'name' : item.get('name'),
                'av' : item.get('av'),
                'url' : item.get('url'),
                'plays' : item.get('plays'),
                'barrages' : item.get('barrages'),
                'coins' : item.get('coins'),
                'date' : item.get('date'),
                'date_short' : datetime.datetime(date[0], date[1], date[2]),
                'author' : item.get('author'),
                'category' : item.get('category'),
                'replys' : item.get('replys'),
                'favorites' : item.get('favorites'),
                'update_time' : item.get('update_time')})
        except KeyError:
            print("Failed to process item, av number: "+str(av))
            continue

        processed += 1
        if processed % log_every == 0:
            print("Processed %s items", processed)
            print("Start to insert...")
            insert_data(buffer)
            buffer = list()
            print("Inserting finished!")



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit', type=int, default=0)
    parser.add_argument('--progress-every', type=int, default=100)

    args = parser.parse_args()

    if settings.REDIS_IS_CLUSTER:
        start_node = [settings.REDIS_CLUSTER_START_NODE]
        r = StrictRedisCluster(startup_nodes=start_node)
    else:
        r = StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    kwargs = {
        'key': settings.REDIS_ITEMS_KEY,
        'limit': args.limit,
        'log_every': args.progress_every,
    }
    try:
        process_items(r, **kwargs)
        retcode = 0  # ok
    except KeyboardInterrupt:
        retcode = 0  # ok
    except Exception as err:
        print("Unhandled exception!\n")
        print(str(err))
        retcode = 2

    return retcode


if __name__ == '__main__':
    sys.exit(main())
