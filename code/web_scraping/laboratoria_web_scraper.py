from web_scraper import WebScraper
import re


class LaboratoriaWebScraper(WebScraper):


    # PAGE LINKS
    def generate_page_links(self, soup):
        all_links = [a_tag["href"] for a_tag in soup.find_all("a")]

        # Get total number of pages
        page_basic_url = self.page_base_url

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
            link = self.page_base_url + str(page_num)
            page_links.append(link)

        return page_links


    # BOOK LINKS
    def generate_book_links(self, soup): 
        book_links = set()

        for tag in soup.find_all("a"):
            rel_link = tag["href"]

            is_book = re.search(r"products/\S+", rel_link)
            if is_book: 
                link = self.BASIC_URL + rel_link
                book_links.add(link)

        return book_links


    # BOOK DATA
    def parse_book_data(self, book_link):
        soup = self._WebScraper__parse_web_data(book_link)

        book = dict()

        # Назва книги
        book["title"] = soup.select(".product-title")[0].text.strip()

        # Характеристики
        keys = [tag.text.strip() for tag in soup.select(".product-features__name")]
        values = [" ".join(tag.text.strip().split()).strip() for tag in soup.select(".product-features__values")]

        book.update(zip(keys, values))

        # Ціна    
        prices_values = [tag.text for tag in soup.select(".fn_price")]
        versions = [tag.text for tag in soup.select(".fn_variant_name")]

        book["price"] = dict(zip(versions, prices_values))

        # Опис
        descrption_tags = soup.select(".product__description")
        if descrption_tags:
            book["description"] = '\n'.join([text.text for text in descrption_tags[0].find_all("p")])

        # Теми
        meta_data_tags = soup.select(".product-features-special__values")
        if meta_data_tags:
            book["meta"] = ";".join([tag.text for tag in meta_data_tags[0] if tag.text != ' '])

        # Посилання
        book["url"] = book_link

        return book