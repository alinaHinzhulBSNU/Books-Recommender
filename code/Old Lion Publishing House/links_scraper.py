# Даний скрипт призначено для збору посилань на окремі книги на сайті "Видавництво Старого Лева"

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re


INITIAL_URL = "https://starylev.com.ua/bookstore/category--paperovi-knyzhky"
BASIC_URL = "https://starylev.com.ua"


# PARSING
def parse_web_data(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    html = urlopen(url, context=ctx).read()

    return BeautifulSoup(html, "html.parser")


# ЧИТАННЯ ВСІХ ПОСИЛАНЬ
def get_all_links(soup):
    raw_links = [tag.get("href") for tag in soup("a")]
    clean_links = list(filter(lambda item: item is not None, raw_links)) # drop None

    return clean_links


# ВИБІР ПОИСЛАНЬ ЗА РЕГУЛЯРНИМ ВИРАЗОМ
def get_links_by_pattern(links, link_regex):
    book_links = set()

    for link in links:
        url = BASIC_URL + link
        is_book = re.search(link_regex, link)
        if is_book: book_links.add(url)

    return book_links


if __name__ == "__main__":
    soup = parse_web_data(INITIAL_URL)
    links = get_all_links(soup)
    page_links = get_links_by_pattern(links, r"/bookstore/page--\S+")

    # ЗБІР ПОСИЛАНЬ НА КНИГИ З САЙТУ
    book_links = []
    
    i = 1
    pages_count = len(page_links)

    for page_link in page_links:
        print(f"\rПроскановано {i} сторінку з {pages_count} ({page_link})", end = "\t")
        
        soup = parse_web_data(page_link)
        links = get_all_links(soup)

        page_book_links = get_links_by_pattern(links, r"\S+knyga\S+")
        book_links.extend(page_book_links)
        
        i = i + 1
    
    # ЗБЕРЕЖЕННЯ РЕЗУЛЬТАТІВ
    print(f"\nКількість посилань на книги: {len(book_links)}.")
    
    with open("book_links.txt", "w") as f:
        f.writelines(book_link + '\n' for book_link in book_links)
