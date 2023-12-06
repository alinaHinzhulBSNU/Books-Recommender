from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re


INITIAL_URL = "https://komorabooks.com/shop/"
BASIC_URL = "https://komorabooks.com/shop/?product-page="


# SAFE CAST
def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


# PARSING
def parse_web_data(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    html = urlopen(url, context=ctx).read()

    return BeautifulSoup(html, "html.parser")


# GENERATE PAGE LINKS
def generate_page_links(soup):
    links = []

    pagination_tags = soup.select(".page-numbers")[0].find_all("li")
    pages = [safe_cast(tag.text, int, 0) for tag in pagination_tags]
    
    all_pages = range(1, max(pages) + 1)
    for page in all_pages:
        link = BASIC_URL + str(page)
        links.append(link)

    return links


# BOOK LINKS
def get_book_links(soup):
    all_links = [tag.get("href") for tag in soup.find_all("a")]
    
    book_links = set()

    for link in all_links:
        is_book = re.search(r"\S+product/(?![^/]*komplekt)[^/]+", link)
        if is_book: book_links.add(link)
    
    return book_links


if __name__ == "__main__":
    soup = parse_web_data(INITIAL_URL)
    page_links = generate_page_links(soup)

    # ЗБІР ПОСИЛАНЬ НА КНИГИ
    book_links = []
    
    i = 1
    pages_count = len(page_links)

    for page_link in page_links:
        print(f"\rПроскановано {i} сторінку з {pages_count} ({page_link})\t\t\t", end = "\t")
        
        soup = parse_web_data(page_link)
        
        page_book_links = get_book_links(soup)
        book_links.extend(page_book_links)
        
        i = i + 1
    
    # ЗБЕРЕЖЕННЯ РЕЗУЛЬТАТІВ
    print(f"\nКількість посилань на книги: {len(book_links)}.")
    
    with open("book_links.txt", "w") as f:
        f.writelines(book_link + '\n' for book_link in book_links)