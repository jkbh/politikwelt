from itemloaders.processors import Identity, MapCompose, TakeFirst
import scrapy
from scrapy.loader import ItemLoader
from datetime import datetime
import re
from scrape_talkshows.items import TalkshowItem


class HartAberFairSpider(scrapy.Spider):
    name = 'hartaberfair'    
    start_urls=['https://www1.wdr.de/daserste/hartaberfair/sendungen/index.html']

    def parse(self, response):        
        for href in response.css('.teaser a::attr("href")').getall()[5]:                
                yield response.follow(href, callback=self.parse_show)
       

    def parse_show(self, response):
        loader = ItemLoader(item=TalkshowItem(), response=response)        

        loader.default_output_processor = TakeFirst()
        loader.date_in = MapCompose(lambda d: datetime.strptime(d, '%d.%m.%Y'))
        loader.title_in = MapCompose(lambda t: t.strip("\n "))
        loader.guests_in = MapCompose(
            lambda g: g.strip("\n "),
            lambda g: re.sub(r', .+', '', g),
            lambda g: re.sub(r'.*: ', '', g)
        )
        loader.guests_out = Identity()

        loader.add_value('host', 'Frank Plasberg')
        loader.add_value('channel', 'ARD')        
        loader.add_css('title', '.sectionA h4.headline[data-pre-headline="Hart aber fair"]::text')        
        loader.add_css('date', '.sectionA h2.conHeadline::text',  re=r'(\d+.\d+.\d+)')        
        loader.add_value('url', response.url)
        loader.add_css('guests', 'div.modD:nth-child(2) h4::text')

        yield loader.load_item()
        

    