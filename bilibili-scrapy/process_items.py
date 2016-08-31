#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""A script to process items from a redis queue."""
from __future__ import print_function, unicode_literals
import argparse
import json
import time
from rediscluster import StrictRedisCluster
from redis import StrictRedis
import sys
sys.path.append(r'.\bilibili-scrapy')
import settings


def process_items(r, key, limit=0, log_every=1000, wait=.1):
    """通关set容器访问到所有的av号，之后通过av号来访问redis中的数据"""
    limit = limit or float('inf')
    processed = 0
    while processed < limit:
        ret = r.spop(key)
        if ret is None:
            time.sleep(wait)
            print("Found no item in set, waiting...")
            continue

        av = ret.decode('utf8')
        print("Get an item, av number:"+str(av))
        try:
            data = r.get(av).decode('utf8')
            item = json.loads(data)
            if item is not None:
                r.delete(av)
            else:
                print("Av number %s not found in redis" % str(av))
        except Exception:
            print("Failed to load item, av number:"+str(av))
            continue

        try:
            name = item.get('name')
            av = item.get('av')
            coins = item.get('coins')
            plays = item.get('plays')
            author = item.get('author')
            print("DEBUG: title: "+str(name)+"\nauthor: "+str(author)+"\nplay: "+str(plays)+"\ncoins: "+str(coins))
        except KeyError:
            print("Failed to process item, av number: "+str(av))
            continue

        processed += 1
        if processed % log_every == 0:
            print("Processed %s items", processed)


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
    except Exception:
        print("Unhandled exception! ")
        retcode = 2

    return retcode


if __name__ == '__main__':
    sys.exit(main())
