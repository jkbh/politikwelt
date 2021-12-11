from typing import Any, Callable, List
from playwright.sync_api import sync_playwright
from playwright._impl._page import Page


class ShowScraper:
    def __init__(self, root_url: str, index_href: str, scrape_hrefs_func: Callable[[Page], List[str]], scrape_show_func: Callable[[Page], dict[str, Any]]) -> None:
        self.root_url = root_url
        self.index_href = index_href        
        self.scrape_hrefs_func = scrape_hrefs_func
        self.scrape_show_func = scrape_show_func

    def fetch_hrefs(self) -> List[str]:
        with sync_playwright() as p:   
            browser = p.chromium.launch()    
            page = browser.new_page()        
            page.goto(self.root_url + self.index_href)  

            hrefs = self.scrape_hrefs_func(page)

            browser.close()

        return hrefs

    def fetch_show(self, href: str) -> dict[str: Any]:
        with sync_playwright() as p:   
            browser = p.chromium.launch()    
            page = browser.new_page()           
            page.goto(self.root_url + href) 

            show = self.scrape_show_func(page)        

            browser.close()

        show['href'] = href
        return show

    def fetch_new_shows(self, known_hrefs: list[str]) -> dict[str: Any]:        
        new_hrefs = [href for href in self.fetch_hrefs() if href not in known_hrefs]        
        new_shows = [self.fetch_show(href=href) for href in new_hrefs]
        return new_shows
    