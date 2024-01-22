from web_scraper import WebScraper
import re

class KomoraWebScraper(WebScraper):
    
    # SAFE CAST
    def safe_cast(self, val, to_type, default=None):
        try:
            return to_type(val)
        except (ValueError, TypeError):
            return default   
    
    
    # PAGE LINKS
    def generate_page_links(self, soup):
        links = []

        pagination_tags = soup.select(".page-numbers")[0].find_all("li")
        pages = [self.safe_cast(tag.text, int, 0) for tag in pagination_tags]
        
        all_pages = range(1, max(pages) + 1)
        for page in all_pages:
            link = self.BASIC_URL + str(page)
            links.append(link)

        return links


    # BOOK LINKS
    def generate_book_links(self, soup):
        all_links = [tag.get("href") for tag in soup.find_all("a")]
    
        book_links = set()

        for link in all_links:
            is_book = re.search(r"\S+product/(?![^/]*komplekt)[^/]+", link)
            if is_book: book_links.add(link)
        
        return book_links


    # BOOK DATA
    def parse_book_data(self, book_link):
        # Parsing
        soup = self._WebScraper__parse_web_data(book_link)
        
        book = dict()

        # Назва книги
        book["title"] = soup.select(".single-product-page-title")[0].text.strip()
        
        # Детальна інформація
        keys_tags = soup.select(".single-page-info-item-key")
        keys = [tag.text.strip() for tag in keys_tags if tag.text.strip() != '']

        values_tags = soup.select(".single-page-info-item-value")
        values = [tag.text.strip() for tag in values_tags if tag.text.strip() != '']

        book.update(zip(keys, values))

        # Ціна
        book["price"] = soup.select(".price")[0].text.strip()
        
        # Опис книги
        book["description"] = soup.select(".single-product-description-text")[0].text

        # Meta
        meta = ';'.join([tag.text for tag in soup.select(".product_meta")[0].find_all("a")])
        if meta != '': book["meta"] = meta

        # Посилання на книгу
        book["url"] = book_link

        # Обкладинка
        book["cover_img"] = soup.select(".woocommerce-product-gallery__image")[0].find_all("a")[0]["href"]

        return book