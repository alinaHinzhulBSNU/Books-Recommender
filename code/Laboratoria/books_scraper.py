import json
from datetime import datetime
from links_scraper import parse_web_data


def parse_book_data(book_link):
    soup = parse_web_data(book_link)

    book = dict()

    # Назва книги
    book["title"] = soup.select(".product-title")[0].text.strip()

    # Характеристики
    keys = [tag.text.strip() for tag in soup.select(".product-features__name")]
    values = [tag.text.strip() for tag in soup.select(".product-features__values")]

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
    with open("../raw/laboratoria_books.json", "w") as f:
        json.dump(books, f, ensure_ascii = False)
        print(f"\nJSON-файл успішно збережено. Кількість книг: {i - 1}")

    current_time = datetime.now()
    print(current_time.strftime("(%d, %b %Y, %H:%M:%S)"))