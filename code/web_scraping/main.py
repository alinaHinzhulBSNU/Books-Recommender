from datetime import datetime
from routes import ROUTES
from komora_web_scraper import KomoraWebScraper
from laboratoria_web_scraper import LaboratoriaWebScraper
from old_lion_web_scraper import OldLionWebScraper
from nash_format_web_scraper import NashFormatWebScraper

if __name__ == "__main__":
    print("\n----------WEB SCRAPING----------\n")

    current_time = datetime.now()
    print(current_time.strftime("(%d, %b %Y, %H:%M:%S)"))

    web_scrapers = []

    # Komora
    routes = ROUTES["komora"]
    komora_ws = KomoraWebScraper(routes["initial"], routes["book"], routes["file"])
    web_scrapers.append(komora_ws)

    # Laboratoria
    routes = ROUTES["laboratoria"]
    l_ws = LaboratoriaWebScraper(routes["initial"], routes["book"], routes["file"], routes["base"])
    web_scrapers.append(l_ws)

    # Old Lion Publishing House
    routes = ROUTES["olph"]
    olph_ws = OldLionWebScraper(routes["initial"], routes["book"], routes["file"])
    web_scrapers.append(olph_ws)

    # Nash Format (Publisher: Nash Format)
    routes = ROUTES["nf"]
    nf_ws = NashFormatWebScraper(routes["initial"], routes["book"], routes["file"], routes["base"])
    web_scrapers.append(nf_ws)

    # Nash Format (Publisher: Fabula)
    routes = ROUTES["fabula"]
    fabula_ws = NashFormatWebScraper(routes["initial"], routes["book"], routes["file"], routes["base"])
    web_scrapers.append(fabula_ws)

    # Nash Format (Publisher: Vivat)
    routes = ROUTES["vivat"]
    vivat_ws = NashFormatWebScraper(routes["initial"], routes["book"], routes["file"], routes["base"])
    web_scrapers.append(vivat_ws)

    # PARSING
    total = 0
    for web_scraper in web_scrapers:
        web_scraper.parse()
        total = total + web_scraper.books_count

    # ВИСНОВКИ
    print(f"Отже, загальна кількість книг: {total}")

    current_time = datetime.now()
    print(current_time.strftime("(%d, %b %Y, %H:%M:%S)"))