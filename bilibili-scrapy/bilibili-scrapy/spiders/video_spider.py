import re
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.http import Request
import urllib.request
import json
from scrapy.item import Item, Field


class BilibiliVideo(Item):
    """需要记录的video的主要参数，item先辈存储在redis中，后被导入到sql中进行处理"""
    name = Field()
    av = Field()
    plays = Field()
    barrages = Field()
    coins = Field()
    date = Field()
    author = Field()
    category = Field()
    replys = Field()
    favorites = Field()
    update_time = Field()

video_classifier = re.compile("http://.*/video/av[\d]*/")
category_extractor = re.compile("http://www.bilibili.com/list/default-(\d*)-")
number_identifier = re.compile("\d+")


class VideoSpider(RedisCrawlSpider):
    """爬取视频信息的爬虫，目前不支持番剧分类的视频爬取."""
    name = 'video_spider'
    redis_key = 'video_spider:start_urls'

    # def start_requests(self):
    #     return [Request("http://www.bilibili.com/video/game.html")]
    #     return [Request("http://www.bilibili.com/video/bangumi-two-1.html")]
    #     return [Request("http://www.bilibili.com/video/av142153/", callback=self.parse_page)]

    def next_requests(self):
        """因为原版实现会出现错误，我们重写这个函数把他修正"""
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
        """爬取目录或者首页"""
        # 找到大分类下的小分类目录页面
        category_href = response.xpath("//ul[@class='n_num']//a/@href").extract()
        if category_href:
            for category in category_href:
                href = 'http://www.bilibili.com' + category
                yield Request(href, callback=self.parse)

        # 如果发现是一个目录页面，就构造请求，遍历目录
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
        if page_num:
            for num in page_num:
                if number_identifier.match(num):
                    href = "http://www.bilibili.com/list/default-" + str(current_category) \
                           + "-" + str(num) + "-2016-08-07~2016-08-14.html"
                    temp_request = Request(href, callback=self.parse)
                    temp_request.category = current_category
                    yield temp_request

        # 无论是目录还是首页，都有其他视频的超链接，我们也爬取他们
        raw_href = response.xpath("//a[contains(@href,'/video/av')]/@href").extract()
        if raw_href:
            for href in raw_href:
                if not video_classifier.match(href):
                    href = 'http://www.bilibili.com' + href
                yield Request(href, callback=self.parse_page)

    def parse_page(self, response):
        """从视频页爬取其他视频页，并爬取信息"""
        # 爬取视频页面的其他视频超链接
        raw_href = response.xpath("//a[contains(@href,'/video/av')]/@href").extract()
        if raw_href:
            for href in raw_href:
                if not video_classifier.match(href):
                    href = 'http://www.bilibili.com' + href
                yield Request(href, callback=self.parse_page)

        # 爬取视频主要信息
        item = BilibiliVideo()
        raw_av = response.url.split("/")
        if raw_av[-1] is "":
            av_num = raw_av[-2]
        else:
            av_num = raw_av[-1]
        item['av'] = av_num.lstrip("av")
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
        response = urllib.request.urlopen(raw_url, timeout=10)
        raw_data = json.loads(response.read().decode("utf8"))
        item['plays'] = raw_data['data']['view']
        item['barrages'] = raw_data['data']['danmaku']
        item['coins'] = raw_data['data']['coin']
        item['replys'] = raw_data['data']['reply']
        item['favorites'] = raw_data['data']['favorite']
        yield item

