from web_scraper import WebScraper
import re

class NashFormatWebScraper(WebScraper):


    # PAGE LINKS
    def generate_page_links(self, soup):
        page_links = set()

        # Всі сторінки
        pages = [page.text for page in soup.select(".page-link")]

        # Остання сторінка - максимальна за номером
        last = int(pages[-1])

        # Генерація посилань за шаблоном
        for page_number in range(1, last + 1):
            url = self.page_base_url + str(page_number)
            page_links.add(url)

        return page_links


    # BOOK LINKS
    def generate_book_links(self, soup):
        products = soup.select(".product-list")

        return set([self.BASIC_URL + product.find_all("a")[0].get("href") for product in products])


    # BOOK DATA
    def parse_book_data(self, book_link):
        soup = self._WebScraper__parse_web_data(book_link)

        book = dict()

        # Назва
        book["title"] = soup.find("h1").text

        # Характеристики
        keys = [key.text.strip() for key in soup.select(".attr")]
        values = [" ".join(value.text.strip().split()).strip() for value in soup.select(".value")]
        
        book.update(zip(keys, values))

        # Ціна
        book["price"] = dict()

        sources = [".tabs-btn_paper", ".tabs-btn_electronic", ".tabs-btn_audio"]

        for source in sources:
            data = soup.select(source)
            if data:
                data = data[0].text.split()
                book["price"][data[0]] = "".join(data[1:])

        # Тема
        tags = soup.select(".product_shelve")

        if tags:
            raw_meta = [elem.text for elem in tags[0].find_all("a")]
            meta = [re.findall(r"(.+)\([0-9]+\)", tag)[0].strip() for tag in raw_meta]
            book["meta"] = ";".join(meta)


        book["description"] = soup.select("#annotation")[0].text.strip()

        # Посилання
        book["url"] = book_link

        # Обкладинка
        book["cover_img"] = soup.select(".fn-img")[0]["data-src"]

        return book