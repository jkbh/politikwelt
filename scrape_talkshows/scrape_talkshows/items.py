# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Compose, Identity, MapCompose, TakeFirst, Join
from datetime import datetime


class LanzShow(scrapy.Item):
    title =  scrapy.Field(
        input_processor=MapCompose(lambda t: t.strip('\n '))
    )
    host = scrapy.Field()
    guests = scrapy.Field(
        input_processor=MapCompose(lambda g: g.split(',')[0]),
        output_processor=Identity()
    )
    channel = scrapy.Field()
    date = scrapy.Field(
        input_processor=MapCompose(lambda date: datetime.strptime(date, '%d.%m.%Y'))
    )
    url = scrapy.Field()

class MaischbergerShow(scrapy.Item): 
    title =  scrapy.Field()
    host = scrapy.Field()
    guests = scrapy.Field(  
        input_processor=MapCompose(str.strip),      
        output_processor=lambda gts: gts[[gts.index(g) for g in gts if 'Gäste' in g][0] + 1:]
    )
    channel = scrapy.Field()
    date = scrapy.Field(
        input_processor=MapCompose(lambda date: datetime.strptime(date, '%d.%m.%y | %H:%M'))        
    )
    url = scrapy.Field()    
