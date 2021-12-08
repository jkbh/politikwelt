from genericpath import exists
import os
from tqdm import tqdm
from playwright.sync_api import sync_playwright
import json

def _get_lanz_urls():
    with sync_playwright() as p:   
        browser = p.firefox.launch()    
        page = browser.new_page()    
        page_path = 'https://www.zdf.de/gesellschaft/markus-lanz'        
        page.goto(page_path)        

        page.click('//*[@id="onetrust-accept-btn-handler"]')

        scroll_button = page.locator('button.js-scrollbox-next').first
        while scroll_button.is_enabled():
            scroll_button.click()

        div = page.locator('div.js-scrollbox-list').first
        links = [element.get_attribute('href') for element in div.locator('a:has-text("Der Talk vom")').element_handles()]            
        
        browser.close()

    return links

def _get_lanz_show(href):
    with sync_playwright() as p:   
        browser = p.firefox.launch()    
        page = browser.new_page()                    
        page.goto(f'https://www.zdf.de{href}')
        
        title = page.text_content('h1.big-headline').strip(' \n')
        date = page.locator('div.other-infos').locator('dd.teaser-info').nth(1).text_content()

        lines = page.inner_text('div.b-post-content').splitlines()       
        lines = [line for line in lines if line != '']

        browser.close()

    guests = lines[::2]
    comments = lines[1::2]

    guests = [{'name': guest.split(',')[0].strip(), 'job': guest.split(',')[1].strip(), 'comment': comment} for (guest, comment) in zip(guests, comments)]

    details = {
        'url': href,
        'channel': 'ZDF',
        'title': title,     
        'date': date,
        'guests': guests
        }

    return details

def update_lanz(path):    
    if exists(path):
        known_shows = json.load(open(path, 'r'))
        known_urls = [show['url'] for show in known_shows]
    else:
        known_shows = []
        known_urls = []

    urls = [url for url in  _get_lanz_urls() if url not in known_urls]
    shows = [_get_lanz_show(url) for url in tqdm(urls)]
    known_shows.extend(shows)

    json.dump(known_shows, open(path, 'w'), indent=4)
    