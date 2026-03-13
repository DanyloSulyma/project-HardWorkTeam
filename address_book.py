"""
address_book.py
Модуль для управління адресною книгою.
Містить клас AddressBook для зберігання та пошуку контактів.
"""

from collections import UserDict
from datetime import date, timedelta
from models import Record 




class AddressBook(UserDict):
    """
    Клас для зберігання та управління контактами.
    Спадкоємець UserDict — зберігає записи у словнику self.data.
    Ключ: ім'я контакту (str), Значення: об'єкт Record.
    """

    def add_record(self, record: Record) -> None:
        """
        Додає запис до адресної книги.

        Args:
            record: Об'єкт Record з атрибутом name.value
        """
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        """
        Знаходить запис за іменем.

        Args:
            name: Ім'я контакту для пошуку

        Returns:
            Об'єкт Record якщо знайдено, None якщо ні
        """
        return self.data.get(name, None)

    def delete(self, name: str) -> bool:
        """
        Видаляє запис за іменем.

        Args:
            name: Ім'я контакту для видалення

        Returns:
            True якщо видалено, False якщо не знайдено
        """
        if name in self.data:
            del self.data[name]
            return True
        return False

    def search(self, query: str) -> list:
        """
        Шукає контакти за частиною імені або номера телефону.

        Args:
            query: Рядок для пошуку

        Returns:
            Список знайдених об'єктів Record
        """
        q = query.lower()
        results = []
        for record in self.data.values():
            if q in record.name.value.lower():
                results.append(record)
                continue
            if hasattr(record, "phones"):
                if any(q in p.value for p in record.phones):
                    results.append(record)
        return results

    def get_upcoming_birthdays(self, days: int = 7) -> list:
        """
        Повертає список контактів, у яких день народження
        протягом наступних N днів від сьогодні.
        Якщо день народження випадає на вихідний —
        привітання переноситься на понеділок.
        Якщо контакт народився 29 лютого —
        у не високосний рік використовується 1 березня.

        Args:
            days: Кількість днів для перевірки (за замовчуванням 7)

        Returns:
            Список словників з ключами 'name' та 'congratulation_date'
        """
        today = date.today()
        deadline = today + timedelta(days=days)
        upcoming = []

        for record in self.data.values():
            # Пропускаємо контакти без дня народження
            if record.birthday is None:
                continue

            birthday = record.birthday.value

            # Замінюємо рік на поточний
            # Обробка 29 лютого у не високосний рік
            try:
                birthday_this_year = birthday.replace(year=today.year)
            except ValueError:
                birthday_this_year = birthday.replace(
                    year=today.year, month=3, day=1
                )

            # Якщо день народження вже минув цього року — беремо наступний рік
            if birthday_this_year < today:
                try:
                    birthday_this_year = birthday_this_year.replace(
                        year=today.year + 1
                    )
                except ValueError:
                    birthday_this_year = birthday_this_year.replace(
                        year=today.year + 1, month=3, day=1
                    )

            # Перевіряємо чи потрапляє у діапазон
            if today <= birthday_this_year <= deadline:

                # Переносимо з вихідних на понеділок
                if birthday_this_year.weekday() == 5:   # Субота
                    birthday_this_year += timedelta(days=2)
                elif birthday_this_year.weekday() == 6:  # Неділя
                    birthday_this_year += timedelta(days=1)

                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": birthday_this_year.strftime("%d.%m.%Y")
                })

        return upcoming
