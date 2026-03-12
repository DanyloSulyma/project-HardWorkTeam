"""
storage.py
Модуль для збереження та завантаження даних адресної книги.
Використовує модуль pickle для серіалізації/десеріалізації.
"""

import pickle
from address_book import AddressBook

# Файл за замовчуванням для зберігання даних
DEFAULT_FILE = "contacts.pkl"


def save_to_file(data: AddressBook, filename: str = DEFAULT_FILE) -> None:
    """
    Зберігає об'єкт AddressBook у бінарний файл за допомогою pickle.

    Args:
        data: Об'єкт AddressBook для збереження
        filename: Ім'я файлу (за замовчуванням 'contacts.pkl')
    """
    with open(filename, "wb") as f:
        pickle.dump(data, f)
    print(f"Data saved to '{filename}'.")


def load_from_file(filename: str = DEFAULT_FILE) -> AddressBook:
    """
    Завантажує об'єкт AddressBook з бінарного файлу.
    Якщо файл не знайдено — повертає порожню AddressBook.

    Args:
        filename: Ім'я файлу (за замовчуванням 'contacts.pkl')

    Returns:
        Завантажений об'єкт AddressBook або новий порожній
    """
    try:
        with open(filename, "rb") as f:
            data = pickle.load(f)
        print(f"Data loaded from '{filename}'.")
        return data
    except FileNotFoundError:
        print(f"File '{filename}' not found. Starting with empty address book.")
        return AddressBook()
    except Exception as e:
        print(f"Error loading file: {e}. Starting with empty address book.")
        return AddressBook()
