import datetime
from playwright._impl._api_types import TimeoutError

def scrape_hrefs(page):
    page.click('//*[@id="onetrust-accept-btn-handler"]')

    scroll_button = page.locator('button.js-scrollbox-next').first        
    while scroll_button.is_enabled():
        try:
            scroll_button.click()            
        except TimeoutError as e:
            print('Received TimeoutError. Probably caused by delayed disabling of the button.')            

    div = page.locator('div.js-scrollbox-list').first
    hrefs = [element.get_attribute('href') for element in div.locator('a:has-text("Der Talk vom")').element_handles()]

    return hrefs


def scrape_show(page):
    title = page.text_content('h1.big-headline').strip(' \n')
    date = page.locator('div.other-infos').locator('dd.teaser-info').nth(1).text_content()
    date = datetime.datetime.strptime(date, '%d.%m.%Y').isoformat()

    lines = page.inner_text('div.b-post-content').splitlines()       
    lines = [line for line in lines if line != '']
    guests = lines[::2]    

    guests = [guest.split(',')[0].strip() for guest in guests]

    show = {        
        'channel': 'ZDF',
        'host': 'Markus Lanz',
        'title': title,     
        'date': date,
        'guests': guests
    }

    return show