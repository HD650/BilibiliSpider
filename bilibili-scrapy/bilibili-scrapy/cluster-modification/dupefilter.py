from scrapy_redis.dupefilter import RFPDupeFilter, DEFAULT_DUPEFILTER_KEY
from rediscluster import StrictRedisCluster
import time


class ClusterDupeFilter(RFPDupeFilter):
    @classmethod
    def from_settings(cls, settings):
        try:
            start_node = [settings.getdict('REDIS_CLUSTER_START_NODE')]
        except Exception:
            raise ValueError("redis cluster start node required")
        server = StrictRedisCluster(startup_nodes=start_node)
        key = DEFAULT_DUPEFILTER_KEY % {'timestamp': int(time.time())}
        debug = settings.getbool('DUPEFILTER_DEBUG')
        return cls(server, key=key, debug=debug)