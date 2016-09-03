import re
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.http import Request
import urllib.request
import json
from scrapy import signals
from rediscluster import StrictRedisCluster
from scrapy_redis import connection
import sys
sys.path.append(r'..')
sys.path.append(r'.\bilibili-scrapy')
from items import BilibiliVideo


video_classifier = re.compile("http://.*/video/av[\d]*/")
category_extractor = re.compile("http://www.bilibili.com/list/default-(\d*)-")
number_identifier = re.compile("\d+")


class VideoSpider(RedisCrawlSpider):
    """爬取视频信息的爬虫，目前不支持番剧分类的视频爬取."""
    name = 'video_spider'
    redis_key = 'video_spider:start_urls'

    def setup_redis(self, crawler=None):
        """重写该函数以支持redis集群模式"""
        if self.server is not None and isinstance(self.server, StrictRedisCluster):
            return

        if crawler is None:
            crawler = getattr(self, 'crawler', None)

        if crawler is None:
            raise ValueError("crawler is required")

        settings = crawler.settings

        if self.redis_key is None:
            self.redis_key = settings.get(
                'REDIS_START_URLS_KEY', '%(name)s:start_urls',
            )

        self.redis_key = self.redis_key % {'name': self.name}

        if not self.redis_key.strip():
            raise ValueError("redis_key must not be empty")

        if self.redis_batch_size is None:
            self.redis_batch_size = settings.getint(
                'REDIS_START_URLS_BATCH_SIZE', 1,
            )

        try:
            self.redis_batch_size = int(self.redis_batch_size)
        except (TypeError, ValueError):
            raise ValueError("redis_batch_size must be an integer")

        self.logger.info("Reading start URLs from redis key '%(redis_key)s' "
                         "(batch size: %(redis_batch_size)s)", self.__dict__)
        if settings.getbool('REDIS_IS_CLUSTER', True):
            try:
                start_node = [settings.getdict('REDIS_CLUSTER_START_NODE')]
            except Exception:
                raise ValueError("redis cluster start node required")
            self.server = StrictRedisCluster(startup_nodes=start_node)
        else:
            self.server = connection.from_settings(crawler.settings)
        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

    # 测试用初始url
    # def start_requests(self):
    #     return [Request("http://www.bilibili.com/video/ent.html")]
    #     return [Request("http://www.bilibili.com/video/game.html")]
    #     return [Request("http://www.bilibili.com/video/bangumi-two-1.html")]
    #     return [Request("http://www.bilibili.com/video/av142153/", callback=self.parse_page)]

    def next_requests(self):
        """因为原版实现会出现解码错误，我们重写这个函数把他修正"""
        use_set = self.settings.getbool('REDIS_START_URLS_AS_SET')
        fetch_one = self.server.spop if use_set else self.server.lpop
        # XXX: Do we need to use a timeout here?
        found = 0
        while found < self.redis_batch_size:
            data = fetch_one(self.redis_key).decode('utf8')
            if not data:
                # Queue empty.
                break
            req = self.make_request_from_data(data)
            if req:
                yield req
                found += 1
            else:
                self.logger.debug("Request not made from data: %r", data)

        if found:
            self.logger.debug("Read %s requests from '%s'", found, self.redis_key)

    def parse(self, response):
        """爬取首页"""
        # 找到大分类下的小分类目录页面
        category_href = response.xpath("//ul[@class='n_num']//a/@href").extract()
        if category_href:
            for category in category_href:
                href = 'http://www.bilibili.com' + category
                yield Request(href, callback=self.parse_index)

        # 无论是目录还是首页，都有其他视频的超链接，我们也爬取他们
        raw_href = response.xpath("//a[contains(@href,'/video/av')]/@href").extract()
        if raw_href:
            for href in raw_href:
                if not video_classifier.match(href):
                    href = 'http://www.bilibili.com' + href
                yield Request(href, callback=self.parse_item)

    def parse_index(self, response):
        """爬取目录页，bilibili目录页在开发过程中，其结构似乎做了修改，pagelist不是随html直接返回的了，
        所以爬取变得困难，需要伪造请求"""
        page_num = response.xpath("//div[@class='pagelistbox']//a/text()").extract()
        current_category = response.xpath("//ul[@class='n_num']//li[@class='on']//@tid").extract()
        if current_category:
            current_category = current_category[0]
        else:
            raw = category_extractor.search(response.url)
            if raw:
                current_category = raw.groups()[0]
            else:
                current_category = ''
        # 老pagelist页面中，翻页超链接是渲染在html中的，现在似乎是在js中动态创建的
        if page_num:
            for num in page_num:
                if number_identifier.match(num):
                    href = "http://www.bilibili.com/list/default-" + str(current_category) \
                           + "-" + str(num) + "-2016-08-07~2016-08-14.html"
                    temp_request = Request(href, callback=self.parse_index)
                    temp_request.category = current_category
                    yield temp_request
        # 通过抓包我们可以发现，新翻页是通过动态请求达到的，但是新情求的视频似乎不全，我们还是使用老方法
        else:
            # raw_url = "http://api.bilibili.com/archive_rank/getarchiverankbypartion?type=jsonp&" \
            #           "tid="+str(current_category)+"&pn=1"
            # response = urllib.request.urlopen(raw_url, timeout=10)
            # raw_data = json.loads(response.read().decode("utf8"))
            # if raw_data['message'] == 'ok':
            #     video_amount = raw_data['data']['page']['count']
            #     page_size = raw_data['data']['page']['size']
            href = "http://www.bilibili.com/list/default-" + str(current_category) \
                           + "-" + str(1) + "-2016-08-07~2016-08-14.html"
            temp_request = Request(href, callback=self.parse_index)
            temp_request.category = current_category
            yield temp_request

        # 无论是目录还是首页，都有其他视频的超链接，我们也爬取他们
        raw_href = response.xpath("//a[contains(@href,'/video/av')]/@href").extract()
        if raw_href:
            for href in raw_href:
                if not video_classifier.match(href):
                    href = 'http://www.bilibili.com' + href
                yield Request(href, callback=self.parse_item)

    def parse_item(self, response):
        """从视频页爬取其他视频页，并爬取信息"""
        # 爬取视频页面的其他视频超链接
        raw_href = response.xpath("//a[contains(@href,'/video/av')]/@href").extract()
        if raw_href:
            for href in raw_href:
                if not video_classifier.match(href):
                    href = 'http://www.bilibili.com' + href
                yield Request(href, callback=self.parse_item)

        # 爬取视频主要信息
        item = BilibiliVideo()
        raw_av = response.url.split("/")
        if raw_av[-1] is "":
            av_num = raw_av[-2]
        else:
            av_num = raw_av[-1]
        item['av'] = av_num.lstrip("av")
        item['url'] = response.url
        item['name'] = response.xpath("//div[@class='v-title']/h1/text()").extract()
        if item['name']:
            item['name'] = item['name'][0]
        item['category'] = response.xpath("//a[@property='v:title']/text()").extract()
        if item['category']:
            item['category'] = item['category'][2]
        item['date'] = response.xpath("//time/i/text()").extract()
        if item['date']:
            item['date'] = item['date'][0]
        item['author'] = response.xpath("//div[@class='usname']//a[@class='name']/text()").extract()
        if item['author']:
            item['author'] = item['author'][0]
        raw_url = "http://api.bilibili.com/archive_stat/stat?aid="+str(item['av'])+"&type=jsonp"
        result = urllib.request.urlopen(raw_url, timeout=10)
        raw_data = json.loads(result.read().decode("utf8"))
        item['plays'] = raw_data['data']['view']
        item['barrages'] = raw_data['data']['danmaku']
        item['coins'] = raw_data['data']['coin']
        item['replys'] = raw_data['data']['reply']
        item['favorites'] = raw_data['data']['favorite']
        yield item

