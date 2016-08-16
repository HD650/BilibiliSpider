# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy.utils.misc import load_object
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet.threads import deferToThread
from scrapy_redis import connection
import datetime


# 我们使用和scrapy-redis默认一样的串行化类，将item串行化为json格式的字符串
default_serialize = ScrapyJSONEncoder().encode


class VideoInfoPipeline(object):
    """将爬取的item存储到redis中，我们不直接存储到sql数据库中，主要因为sql多次写入的性能问题
       同时，因为bilibili的各种视频参数会随时间而变动，我们需要不断爬取更新数据，所以这里重写
       管道的存入函数，通过hash判断视频信息是否存在，如存在则更新，不然则创建"""

    def __init__(self, server,
                 key='%(spider)s:items',
                 serialize_func=default_serialize):
        self.server = server
        self.key = key
        self.serialize = serialize_func

    @classmethod
    def from_settings(cls, settings):
        params = {
            'server': connection.from_settings(settings),
        }
        if settings.get('REDIS_ITEMS_KEY'):
            params['key'] = settings['REDIS_ITEMS_KEY']
        if settings.get('REDIS_ITEMS_SERIALIZER'):
            params['serialize_func'] = load_object(
                settings['REDIS_ITEMS_SERIALIZER']
            )

        return cls(**params)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        """使用twisted的defer功能以达到最高的性能，当写入的时候，不会阻塞我们的主线程"""
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        """不适用list来存储item信息，因为我们需要大量的查找操作，所以我们使用hash"""
        key = self.item_key(item, spider)
        item["update_time"] = datetime.datetime.now()
        data = self.serialize(item)
        self.server.hset(key, str(item["av"]), data)
        return item

    def item_key(self, item, spider):
        """如没有在setting中配置key，则使用spider的名字"""
        return self.key % {'spider': spider.name}
