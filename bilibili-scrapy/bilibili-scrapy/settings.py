# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
SPIDER_MODULES = ['bilibili-scrapy.spiders']
NEWSPIDER_MODULE = 'bilibili-scrapy.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/32.0.1667.0 Safari/537.36'

DUPEFILTER_CLASS = "cluster-modification.dupefilter.ClusterDupeFilter"
SCHEDULER = "cluster-modification.scheduler.ClusterScheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = "cluster-modification.queue.ClusterSpiderPriorityQueue"
# SCHEDULER_QUEUE_CLASS = "cluster-modification.queue.ClusterSpiderQueue"
# SCHEDULER_QUEUE_CLASS = "cluster-modification.queue.ClusterSpiderStack"

ITEM_PIPELINES = {
    'bilibili-scrapy.pipelines.VideoInfoPipeline': 300,
    # 'scrapy_redis.pipelines.RedisPipeline': 400,
}

LOG_LEVEL = 'DEBUG'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 1

# REDIS_HOST = 'localhost'
# REDIS_PORT = 7000
REDIS_CLUSTER_START_NODE = {'host': 'localhost', 'port': 7000}
REDIS_START_URLS_BATCH_SIZE = 1
REDIS_ITEMS_KEY = 'video_info'

