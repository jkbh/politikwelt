from itemloaders.processors import MapCompose, TakeFirst, Identity
import scrapy
from datetime import datetime

from scrapy.loader import ItemLoader

from scrape_talkshows.items import TalkshowItem
from playwright.sync_api import sync_playwright


class LanzSpider(scrapy.Spider):
    name = 'lanz'

    def start_requests(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()    
            page = browser.new_page()
            page.goto('https://www.zdf.de/gesellschaft/markus-lanz')
            page.click('//*[@id="onetrust-accept-btn-handler"]')

            # scroll_button = page.locator('button.js-scrollbox-next').first        
            # while scroll_button.is_enabled():                
            #     scroll_button.click()
            #     page.wait_for_timeout(1000)                
            
            for href_handle in page.locator('a.teaser-title-link:has-text("Der Talk vom")').element_handles():
                href = 'https://www.zdf.de' + href_handle.get_attribute('href')                
                yield scrapy.Request(href)

            browser.close()

        

    def parse(self, response):        
        loader = ItemLoader(item=TalkshowItem(), response=response)
        loader.default_output_processor = TakeFirst()

        loader.title_in = MapCompose(lambda t: t.strip('\n '))
        loader.date_in = MapCompose(lambda d: datetime.strptime(d, '%d.%m.%Y'))
        loader.guests_in = MapCompose(lambda g: g.split(',')[0])
        loader.guests_out = Identity()

        loader.add_value('host', 'Markus Lanz')
        loader.add_value('channel' ,'ZDF')
        loader.add_css('title', 'h1.big-headline::text') 
        loader.add_css('date', 'div.other-infos dd.teaser-info::text', re=r'(\d+.\d+.\d+)')         
        loader.add_css('guests', 'p b::text, strong::text')
        loader.add_value('url', response.url)

        yield loader.load_item()
