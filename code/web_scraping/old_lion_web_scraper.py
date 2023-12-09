from web_scraper import WebScraper
import re


class OldLionWebScraper(WebScraper):
    
    # PAGE LINKS
    def generate_page_links(self, soup):
        page_links = set()

        links = [tag.get("href") for tag in soup("a") if tag.get("href") is not None]

        for link in links:
            is_page = re.search(r"/bookstore/page--\S+", link)
            if is_page: 
                url = self.BASIC_URL + link
                page_links.add(url)

        return page_links


    # BOOK LINKS
    def generate_book_links(self, soup):
        product_cards = soup.select(".ant-card-body")
        a_tags = [elem.find_all("a") for elem in product_cards]

        return set([self.BASIC_URL + (a[0]["href"]) for a in a_tags])


    # BOOK DATA
    def parse_book_data(self, book_link):
        # Parsing
        soup = self._WebScraper__parse_web_data(book_link)
        product_info = soup.find("div").find("section").find("main").find_all("div")[5]
        
        book = dict()

        # Назва книги
        book["title"] = product_info.find("h1").text.strip()

        # Автор книги
        book["author"] = product_info.find("a").text.strip()

        # Ціна
        price_tag = product_info.select(".product-price")
        if price_tag:
            book["price"] = price_tag[0].text.split()[0]

        # Тип
        type_tag = product_info.select(".active")
        if type_tag:
            book["type"] = type_tag[0].text.split()[0]

        # Статус
        status_tag = product_info.select('div[class*="status-"]')
        if status_tag:
            book["status"] = status_tag[0].text.strip()
        
        # Інші подробиці
        keys = [row.find_all("td")[0].text.strip() for row in product_info.find_all("tr")]
        values = [row.find_all("td")[1].text.strip() for row in product_info.find_all("tr")]
        book.update(zip(keys, values))
        
        # Опис книги
        book["description"] = ''.join([p.text for p in 
                            product_info.select(".product-page__description")[0].find_all("p")])
        
        # Посилання на книгу
        book["url"] = book_link

        return book
