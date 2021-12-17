# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Compose, Identity, MapCompose, TakeFirst, Join
from datetime import datetime


class TalkshowItem(scrapy.Item):
    title =  scrapy.Field()
    host = scrapy.Field()
    guests = scrapy.Field()
    channel = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
