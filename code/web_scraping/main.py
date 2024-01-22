from datetime import datetime
from routes import ROUTES
from komora_web_scraper import KomoraWebScraper
from nash_format_web_scraper import NashFormatWebScraper

if __name__ == "__main__":
    print("\n----------WEB SCRAPING----------\n")

    current_time = datetime.now()
    print(current_time.strftime("(%d, %b %Y)"))

    web_scrapers = []

    # Komora
    routes = ROUTES["komora"]
    komora_ws = KomoraWebScraper(routes["initial"], routes["book"], routes["file"])
    web_scrapers.append(komora_ws)

    # Publishers: Laboratoria, Old Lion Publishing House, Nash Format, Fabula, Vivat
    publishers = ["laboratoria", "olph", "nf", "fabula", "vivat"]
    for publisher in publishers:
        routes = ROUTES[publisher]
        ws = NashFormatWebScraper(routes["initial"], routes["book"], routes["file"], routes["base"])
        web_scrapers.append(ws)

    # PARSING
    total = 0
    for web_scraper in web_scrapers:
        web_scraper.parse()
        total = total + web_scraper.books_count
    
    # ВИСНОВКИ
    print(f"Отже, загальна кількість книг: {total}")
