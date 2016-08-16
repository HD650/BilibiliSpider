# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

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
