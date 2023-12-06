from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re


INITIAL_URL = "https://laboratoria.pro/catalog/books"
BASIC_URL = "https://laboratoria.pro/"


# PARSING
def parse_web_data(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    html = urlopen(url, context=ctx).read()

    return BeautifulSoup(html, "html.parser")

# GENERATE PAGE LINKS
def generate_page_links(soup):
    all_links = [a_tag["href"] for a_tag in soup.find_all("a")]

    # Get total number of pages
    page_basic_url = "https://laboratoria.pro/catalog/books/page-"

    page_numbers = []
    for link in all_links:
        is_page = re.search(r"^" + page_basic_url + r"\S+$", link)
        if is_page:
            num = re.findall(r"^" + page_basic_url + r"(\S+)$", link)
            page_numbers.append(int(num[0]))

    total_number = max(page_numbers)

    # Generate links for all pages
    page_links = []
    for page_num in range(1, total_number + 1):
        link = page_basic_url + str(page_num)
        page_links.append(link)

    return page_links


# GET LINKS TO BOOKS
def get_book_links(soup):
    book_links = set()

    for tag in soup.find_all("a"):
        rel_link = tag["href"]

        is_book = re.search(r"products/\S+", rel_link)
        if is_book: 
            link = BASIC_URL + rel_link
            book_links.add(link)

    return book_links


if __name__ == "__main__":
    soup = parse_web_data(INITIAL_URL)
    page_links = generate_page_links(soup)

    # ЗБІР ПОСИЛАНЬ НА КНИГИ З САЙТУ
    book_links = []
    
    i = 1
    pages_count = len(page_links)

    for page_link in page_links:
        print(f"\rПроскановано {i} сторінку з {pages_count} ({page_link})", end = "\t")
        
        soup = parse_web_data(page_link)
        page_book_links = get_book_links(soup)
        book_links.extend(page_book_links)
        
        i = i + 1
    
    # ЗБЕРЕЖЕННЯ РЕЗУЛЬТАТІВ
    print(f"\nКількість посилань на книги: {len(book_links)}.")
    
    with open("book_links.txt", "w") as f:
        f.writelines(book_link + '\n' for book_link in book_links)