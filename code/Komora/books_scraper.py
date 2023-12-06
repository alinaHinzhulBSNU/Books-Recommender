import json
from datetime import datetime
from links_scraper import parse_web_data


def parse_book_data(book_link):
    # Parsing
    soup = parse_web_data(book_link)
    
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

    return book


if __name__ == "__main__":
   
   # Завантаження посилань на книги
    book_links = []
    with open("book_links.txt", "r") as f:
        book_links = [book_link.strip() for book_link in f.readlines()]

    # Парсинг даних про книги
    books = []

    i = 1
    books_count = len(book_links)

    for book_link in book_links:
        print(f"\rПроскановано {i / books_count * 100:.0f}%", end = "\t")
        
        book = parse_book_data(book_link)
        books.append(book)

        i = i + 1

    # Збереження результатів парсингу
    with open("../raw/komora_books.json", "w") as f:
        json.dump(books, f, ensure_ascii = False)
        print(f"\nJSON-файл успішно збережено. Кількість книг: {i - 1}")

    current_time = datetime.now()
    print(current_time.strftime("(%d, %b %Y, %H:%M:%S)"))