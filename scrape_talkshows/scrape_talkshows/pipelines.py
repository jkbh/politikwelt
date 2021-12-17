# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter
import json
from os.path import exists

from scrapy.exceptions import DropItem
            

class DuplicatePipeline:
    def __init__(self) -> None:
        self.known_urls = []
    
    def open_spider(self, spider):
        if exists('items.json'):
            self.known_urls.extend([json.loads(item)['url'] for item in open('items.json', 'r')])        
    
    def process_item(self, item, spider):        
        if item['url'] in self.known_urls:
            raise DropItem('Item already exists')
        else:
            return item
    

class TalkshowPipeline:
    def __init__(self) -> None:
        self.exporter = None

    def open_spider(self, spider):
        if exists('items.json'):
            self.exporter = JsonLinesItemExporter(open('items.json', 'ab'))
        else:
            self.exporter = JsonLinesItemExporter(open('items.json', 'xb'))

    def process_item(self, item, spider):       
        self.exporter.export_item(item)
        return item