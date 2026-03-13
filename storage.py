"""
storage.py
Модуль для збереження та завантаження даних.
Використовує pickle для серіалізації та pathlib для шляху до файлу.
Дані зберігаються в домашній директорії користувача.
"""

import pickle
from pathlib import Path
from typing import Callable, TypeVar


# Домашня директорія користувача (~/)
HOME_DIR = Path.home()
T = TypeVar("T")


def save_to_file(data: object, filename: str) -> None:
    """
    Зберігає будь-який об'єкт у бінарний файл у домашній директорії.

    Args:
        data: Будь-який об'єкт для збереження (AddressBook, NoteBook тощо)
        filename: Ім'я файлу (наприклад 'contacts.pkl')
    """
    file_path = HOME_DIR / filename
    with open(file_path, "wb") as f:
        pickle.dump(data, f)
    print(f"Data saved to '{file_path}'.")


def load_from_file(filename: str, default_factory: Callable[[], T]) -> T:
    """
    Завантажує об'єкт з бінарного файлу у домашній директорії.
    Якщо файл не знайдено — повертає новий порожній об'єкт.

    Args:
        filename: Ім'я файлу (наприклад 'contacts.pkl')
        default_factory: Клас або функція для створення порожнього об'єкта
                        (наприклад AddressBook або NoteBook)

    Returns:
        Завантажений об'єкт або новий порожній об'єкт
    """
    file_path = HOME_DIR / filename
    try:
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        print(f"Data loaded from '{file_path}'.")
        return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found. Starting fresh.")
        return default_factory()
    except Exception as e:
        print(f"Error loading file: {e}. Starting fresh.")
        return default_factory()
