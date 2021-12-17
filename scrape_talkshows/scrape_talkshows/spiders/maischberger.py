from itemloaders.processors import TakeFirst, MapCompose
import scrapy
from scrapy.loader import ItemLoader
from datetime import datetime

from scrape_talkshows.items import TalkshowItem


class MaischbergerSpider(scrapy.Spider):
    name = 'maischberger'    
    start_urls=['https://www.daserste.de/information/talk/maischberger/sendung/index.html']

    def parse(self, response):        
        for href in response.css('.sectionZ .headline a::attr("href")').getall():                
                yield response.follow(href, callback=self.parse_show)

        # next_page = response.css('.sectionZ .right a::attr("href")').get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

    def parse_show(self, response):
        loader = ItemLoader(item=TalkshowItem(), response=response)
        loader.default_output_processor = TakeFirst()                

        loader.date_in = MapCompose(lambda date: datetime.strptime(date, '%d.%m.%y | %H:%M'))
        loader.guests_in = MapCompose(str.strip)
        loader.guests_out = lambda gts: gts[[gts.index(g) for g in gts if 'Gäste' in g][0] + 1:]

        loader.add_value('host', 'Sandra Maischberger')
        loader.add_value('channel', 'ARD')        
        loader.add_css('title', 'h1.headline::text')        
        loader.add_css('date', '.infoBroadcastDateBox p::text',  re=r'(\d+.\d+.\d+ \| \d+:\d+)')        
        loader.add_css('guests', '.modParagraph p > strong:only-child::text, .modParagraph h2::text', re=r'^.*?(?=[,(])|^.+')
        loader.add_value('url', response.url)        
        
        yield loader.load_item()