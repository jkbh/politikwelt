from itemloaders.processors import Identity, MapCompose, TakeFirst
import scrapy
from scrapy.loader import ItemLoader
from datetime import datetime
import re
from scrape_talkshows.items import TalkshowItem


class AnneWillSpider(scrapy.Spider):
    name = 'will'    
    start_urls=['https://daserste.ndr.de/annewill/archiv/index.html']

    def parse(self, response):        
        for href in response.css('.sectionZ .headline a::attr("href")').getall():                
                yield response.follow(href, callback=self.parse_show)

        # next_page = response.css('.paging .next a::attr("href")').get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

    def parse_show(self, response):
        loader = ItemLoader(item=TalkshowItem(), response=response)        
        
        loader.date_in = MapCompose(lambda d: datetime.strptime(d, '%d.%m.%Y | %H:%M'))

        loader.add_value('host', 'Anne Will')
        loader.add_value('channel', 'ARD')        
        loader.add_css('title', 'h1.headline::text')        
        loader.add_css('date', '.infokasten h2::text',  re=r'(\d+.\d+.\d+ \| \d+:\d+)')        
        loader.add_value('url', response.url)

        guests_href = response.css('h4.headline a::attr("href")').getall()[0]

        yield response.follow(guests_href, callback=self.parse_guests, meta={'item': loader.load_item()})


    def parse_guests(self, response):       
        loader = ItemLoader(item=response.meta['item'], response=response) 
        loader.default_output_processor = TakeFirst()      
        
        loader.guests_in = MapCompose(lambda g: re.sub(r' \(.+', '', g))
        loader.guests_out = Identity()

        loader.add_css('guests', 'h3.subtitle::text')

        yield loader.load_item()