import json
from datetime import datetime
from links_scraper import parse_web_data


def parse_book_data(soup):
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
    else:
        book["price"] = None

    # Тип
    type_tag = product_info.select(".active")
    if type_tag:
        book["type"] = type_tag[0].text.split()[0]
    else:
        book["type"] = None

    # Статус
    status_tag = product_info.select('div[class*="status-"]')
    if status_tag:
        book["status"] = status_tag[0].text.strip()
    else:
        book["status"] = None
    
    # Інші подробиці
    keys = [row.find_all("td")[0].text.strip() for row in product_info.find_all("tr")]
    values = [row.find_all("td")[1].text.strip() for row in product_info.find_all("tr")]
    book.update(zip(keys, values))
    
    # Опис книги
    book["description"] = ''.join([p.text for p in 
                           product_info.select(".product-page__description")[0].find_all("p")])

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
        
        soup = parse_web_data(book_link)

        book = parse_book_data(soup)
        books.append(book)

        i = i + 1

    # Збереження результатів парсингу
    with open("../raw/olph_books.json", "w") as f:
        json.dump(books, f, ensure_ascii = False)
        print("\nJSON-файл успішно збережено.")

    current_time = datetime.now()
    print(current_time.strftime("\n(%d, %b %Y, %H:%M:%S)"))
