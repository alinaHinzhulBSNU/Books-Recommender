import re
import os
import json


BASE_DIR = "../raw_json_data/"
RESULT_PATH = "../clean_json_data/books.json"


def split_tags(input_string):
    result = []

    pattern = re.compile(r"([А-ЩЬЮЯҐЄIЇІ])")

    # Split by symbol
    if '.' in input_string:
        parts = input_string.split('.')
    else:
        parts = input_string.split(';')

    # Split by capital letter
    for i in range(0, len(parts)):
        parts[i] = parts[i].strip()
        matches = pattern.finditer(parts[i])
        indexes = [match.start() for match in matches]

        if len(indexes) > 1:
            splitted = []

            for j in range(0, len(indexes) - 1):
                splitted.append(parts[i][indexes[j]:indexes[j + 1]].strip())
            # from last index
            splitted.append(parts[i][indexes[-1]:].strip())
            
            result = result + splitted
        else:
            result.append(parts[i])

    return result


if __name__ == "__main__":
    
    # Шляхи до JSON-файлів з даними про книги у директррії BASE_DIR
    file_paths = [e.path for e in os.scandir(BASE_DIR) if e.is_file() and e.name.endswith(".json")]

    # ОЧИЩЕННІ ДАНІ
    unified_books = []

    for file_path in file_paths:

        with open(file_path, "r") as file:

            books = json.load(file)

            for book in books:
                unified_book = dict()

                # ISBN
                isbn_keys = ["ISBN", "ISBN:", "Виробник"]
                for isbn_key in isbn_keys:
                    if isbn_key in book.keys():
                        isbn = book[isbn_key]
                unified_book["ISBN"] = isbn

                # Tags
                tag_keys = ["meta", "Категорія", "Тематика", '"Серія"', "Теми", "Категорії"]
                for tag_key in tag_keys:
                    if tag_key in book.keys():
                        tags = book[tag_key]
                        tags = split_tags(tags)
                unified_book["Теги"] = tags

                # Author
                author_keys = ["Автор", "author", "Авторки:", "Авторка:"]
                for author_key in author_keys:
                    if author_key in book.keys():
                        authors = book[author_key]
                        authors = [author.strip() for author in authors.split(',')]
                unified_book["Автори"] = authors

                # Pages
                pages_keys = ["Кількість сторінок", "К-сть сторінок"]
                for pages_key in pages_keys:
                    if pages_key in book.keys():
                        pages = book[pages_key]
                unified_book["Сторінки"] = pages

                # Size
                size_keys = ["Розміри", "Розмір", "Розміри в палітурці (твердій обкладинці)",  "Розміри в м'якій обкладинці"]
                for size_key in size_keys:
                    if size_key in book.keys():
                        size = book[size_key]

                unified_book["Розмір"] = size

                # Publisher
                publisher_keys = ["publisher", "Видавництво"]
                for publisher_key in publisher_keys:
                    if publisher_key in book.keys():
                        publisher = book[publisher_key]

                unified_book["Видавництво"] = publisher

                # Merge with the rest of the data
                used_keys = isbn_keys + tag_keys + author_keys + pages_keys + size_keys + publisher_keys
                filtered_book_dict = {key: value for key, value in book.items() if key not in used_keys}

                unified_book = {**unified_book, **filtered_book_dict}
                unified_books.append(unified_book)

    # Збереження результатів очищення даних
    with open(RESULT_PATH, "w") as f:
        json.dump(unified_books, f, ensure_ascii = False)
        print(f"JSON-файл успішно збережено. Файл містить дані про таку кількість книг: {len(unified_books)}")
