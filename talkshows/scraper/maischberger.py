import datetime
from playwright._impl._api_types import TimeoutError
from playwright._impl._page import Page
import re

def scrape_hrefs(page: Page):    
    hrefs = []
    hasNextButton = True

    while hasNextButton:           
        for handle in page.query_selector_all('div.sectionZ >> h4.headline >> a'):
            hrefs.append(handle.get_attribute('href'))

        button_next = page.locator('div.sectionZ >> div.right >> a')
        button_next.click()        

        try:
            button_next.wait_for(timeout=5000)            
        except TimeoutError as e:
            hasNextButton = False        
        
    return hrefs


def scrape_show(page: Page):
    title = page.text_content('h1.headline')      

    date = page.text_content('div.infoBroadcastDateBox >> p')
    date = re.search(r'(\d+.\d+.\d+ \| \d+:\d+)', date).group(1)
    
    date = datetime.datetime.strptime(date, '%d.%m.%y | %H:%M').isoformat()
    
    guests = page.locator('css=p:below(:text("Gäste")) >> strong').all_text_contents()    
    guests = [re.sub(r'\(.*', '', guest).split(',')[0].strip() for guest in guests]
    guests = [guest for guest in guests if guest != 'mehr' and guest != 'Gäste:' and guest != '']
    guests = list({guest.strip(): guest.strip() for guest in guests}.keys())

    show = {        
        'channel': 'Das Erste',
        'host': 'Sandra Maischberger',
        'title': title,     
        'date': date,
        'guests': guests
    }

    return show