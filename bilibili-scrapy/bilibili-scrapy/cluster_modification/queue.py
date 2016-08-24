from scrapy_redis.queue import SpiderPriorityQueue, SpiderQueue, SpiderStack


class ClusterSpiderPriorityQueue(SpiderPriorityQueue):
    def pop(self, timeout=0):
        """优先级队列中使用了redis的事物功能，但是redis-cluster不支持事物，我们只能这里取消事物，损失了一定原子性"""
        # use atomic range/remove using multi/exec
        pipe = self.server.pipeline()
        # this access to redis is not atomic but cluster doesn't support transaction
        # 不使用multi损失了原子性，但是集群不支持事物
        # pipe.multi()
        pipe.zrange(self.key, 0, 0).zremrangebyrank(self.key, 0, 0)
        results, count = pipe.execute()
        if results:
            return self._decode_request(results[0])


class ClusterSpiderQueue(SpiderQueue):
    pass


class ClusterSpiderStack(SpiderStack):
    pass