# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

# 添加正确的目录防止import失败
import sys
sys.path.append(r'..')
sys.path.append(r'.\bilibili-scrapy')

SPIDER_MODULES = ['bilibili-scrapy.spiders']
NEWSPIDER_MODULE = 'bilibili-scrapy.spiders'

# 设置是否使用redis的集群模式
REDIS_IS_CLUSTER = False

# 伪装成浏览器
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/32.0.1667.0 Safari/537.36'

# 使用支持redis集群的判重池和调度池
if REDIS_IS_CLUSTER:
    DUPEFILTER_CLASS = "cluster_modification.dupefilter.ClusterDupeFilter"
    SCHEDULER = "cluster_modification.scheduler.ClusterScheduler"
    SCHEDULER_PERSIST = True
    # SCHEDULER_QUEUE_CLASS = "cluster_modification.queue.ClusterSpiderPriorityQueue"
    SCHEDULER_QUEUE_CLASS = "cluster_modification.queue.ClusterSpiderQueue"
    # SCHEDULER_QUEUE_CLASS = "cluster_modification.queue.ClusterSpiderStack"
else:
    DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
    SCHEDULER = "scrapy_redis.scheduler.Scheduler"
    SCHEDULER_PERSIST = True
    # SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
    SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
    # SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"


# 使用pipeline将爬取的数据存入redis数据库中
ITEM_PIPELINES = {
    'bilibili-scrapy.pipelines.RedisItemPipeline': 300,
    # 'scrapy_redis.pipelines.RedisPipeline': 400,
}

LOG_LEVEL = 'DEBUG'

# 下载的延迟，减轻服务器端的负担，同时因为能并行化，爬取会更快（?）
DOWNLOAD_DELAY = 1

# 配置我们的redis集群的入口，事实上只要一个结点就可以连接到整个集群
if not REDIS_IS_CLUSTER:
    REDIS_HOST = '192.168.253.2'
    REDIS_PORT = 7000
else:
    REDIS_CLUSTER_START_NODE = {'host': 'localhost', 'port': 7000}

# 配置SQL数据库的入口
SQL_HOST = '192.168.253.2'
SQL_PORT = 8000
SQL_USER = 'zzk'
SQL_PASSWORD = 'zzk'
SQL_DATABASE = 'bilibili'
SQL_TABLE = 'video'

# 每个爬虫只从初始url池中拿取一个连接
REDIS_START_URLS_BATCH_SIZE = 1

# 存储item的key，这个要改，以把key分散在hash池中
REDIS_ITEMS_KEY = 'video_info'

# 储存错误的item的key，错误item主要指需要登录的页面
REDIS_ERROR_ITEMS_KEY = 'video_error'

