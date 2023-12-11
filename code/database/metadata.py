import os
import re
import json


BASE_DIR = "../raw_json_data/"


if __name__ == "__main__":

    # Шляхи до JSON-файлів з даними про книги у директррії BASE_DIR
    file_paths = [e.path for e in os.scandir(BASE_DIR) if e.is_file() and e.name.endswith(".json")]

    # Визначення переліку всіх можливих унікальних атрибутів
    # (вказано яке саме видавництво використовує атрибут для характеристики книги)
    unique_attributes = list()

    for file_path in file_paths:
        publisher = re.findall(r"^\S+/(\S+)_books.json", file_path)[0]

        publisher_unique_attributes = set()

        with open(file_path, "r") as file:
            books = json.load(file)

            for book in books:
                book_attributes = set(book.keys())
                publisher_unique_attributes.update(book_attributes)

        unique_attributes.extend([{attribute: publisher} for attribute in publisher_unique_attributes])

    # Метадані
    print("\nУнікальні атрибути для опису книг у ріхних видавців:\n")
    for attribute in unique_attributes:
        print(attribute)