from scraper.update_lanz import update_lanz

def update_all(path):
    print('Updating Lanz Shows')
    update_lanz(path)

if __name__ == '__main__':    
    update_all('talkshows.json')