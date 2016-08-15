# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class BilibiliVideo(Item):
    name = Field()
    av = Field()
    plays = Field()
    barrages = Field()
    coins = Field()
    date = Field()
    author = Field()
    category = Field()
