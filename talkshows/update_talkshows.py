import json
from genericpath import exists
import scraper.maischberger as maischberger
import scraper.lanz as lanz
from scraper.show_scraper import ShowScraper

def main():
    path = 'talkshows.json'
    if exists(path):
        known_shows = json.load(open(path, 'r'))
        known_hrefs = [show['href'] for show in known_shows]
    else:
        known_shows = []
        known_hrefs = []

    scrapers: list[ShowScraper] = [
        ShowScraper('https://www.zdf.de', '/gesellschaft/markus-lanz', lanz.scrape_hrefs, lanz.scrape_show),
        ShowScraper('https://www.daserste.de', '/information/talk/maischberger/sendung/index.html', maischberger.scrape_hrefs, maischberger.scrape_show)
    ]

    for scraper in scrapers:
        new_shows = scraper.fetch_new_shows(known_hrefs)
        known_shows.extend(new_shows)

    json.dump(known_shows, open(path, 'w'), indent=4) 
    

if __name__ == '__main__':    
    main()