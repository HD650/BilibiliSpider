from scrapy_redis.scheduler import Scheduler
from rediscluster import StrictRedisCluster
import importlib
import six


class ClusterScheduler(Scheduler):
    @classmethod
    def from_settings(cls, settings):
        kwargs = {
            'persist': settings.getbool('SCHEDULER_PERSIST'),
            'flush_on_start': settings.getbool('SCHEDULER_FLUSH_ON_START'),
            'idle_before_close': settings.getint('SCHEDULER_IDLE_BEFORE_CLOSE'),
        }

        optional = {
            'queue_key': 'SCHEDULER_QUEUE_KEY',
            'queue_cls': 'SCHEDULER_QUEUE_CLASS',
            'dupefilter_key': 'SCHEDULER_DUPEFILTER_KEY',
            'dupefilter_cls': 'DUPEFILTER_CLASS',
            'serializer': 'SCHEDULER_SERIALIZER',
        }
        for name, setting_name in optional.items():
            val = settings.get(setting_name)
            if val:
                kwargs[name] = val

        # Support serializer as a path to a module.
        if isinstance(kwargs.get('serializer'), six.string_types):
            kwargs['serializer'] = importlib.import_module(kwargs['serializer'])

        try:
            start_node = [settings.getdict('REDIS_CLUSTER_START_NODE')]
        except Exception:
            raise ValueError("redis cluster start node required")
        server = StrictRedisCluster(startup_nodes=start_node)
        connection_state = server.ping()
        cluster_num = 0
        for key in connection_state:
            if connection_state[key] is True:
                cluster_num += 1
                print("Connected to node "+str(key)+" successfully!")
            else:
                print("Failed to connect to node "+str(key)+"!")
        if cluster_num <= 2:
            print("No enough nodes found in cluster! Exiting...")
            exit()
        print("Connected to the redis cluster finished! Working with "+str(cluster_num)+" nodes")
        return cls(server=server, **kwargs)