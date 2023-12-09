import json
import ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod


class WebScraper(ABC):

    def __init__(self, initial_url, book_basic_url, result_file_path, page_base_url = None):
        self.INITIAL_URL = initial_url
        self.BASIC_URL = book_basic_url
        self.result_file_path = result_file_path
        self.page_base_url = page_base_url
        
        self.soup = self.__parse_web_data(self.INITIAL_URL)


    # PARSING
    def __parse_web_data(self, url):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        html = urlopen(url, context=ctx).read()

        return BeautifulSoup(html, "html.parser")


    # PAGE LINKS
    @abstractmethod
    def generate_page_links(self, soup):
        pass


    # BOOK LINKS
    @abstractmethod
    def generate_book_links(self, soup):
        pass


    # BOOK DATA
    @abstractmethod
    def parse_book_data(self, book_link):
        pass


    # PARSE
    def parse(self):
        print(f"\nЗбір даних з сайту: {self.INITIAL_URL}\n")

        page_links = self.generate_page_links(self.soup)

        # ЗБІР ПОСИЛАНЬ НА КНИГИ
        book_links = []
        
        i = 1
        pages_count = len(page_links)

        for page_link in page_links:
            print(f"\rПошук посилань на книги на сторінці {i} з {pages_count} ({page_link})\t\t\t", end = "\t")
            
            soup = self.__parse_web_data(page_link)
            
            page_book_links = self.generate_book_links(soup)
            book_links.extend(page_book_links)
            
            i = i + 1

        print()
        
        # СКАНУВАННЯ СТОРІНОК ПРО ОКРЕМІ КНИГИ
        books = []

        i = 1
        books_count = len(book_links)
        self.books_count = books_count


        for book_link in book_links:
            print(f"\rПроскановано {i / books_count * 100:.0f}% сторінок про окремі книги", end = "\t")
            
            book = self.parse_book_data(book_link)
            books.append(book)

            i = i + 1

        # Збереження результатів парсингу
        with open(self.result_file_path, "w") as f:
            json.dump(books, f, ensure_ascii = False)
            print(f"\nJSON-файл успішно збережено. Кількість книг: {books_count}")