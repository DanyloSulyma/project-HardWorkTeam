"""
Модуль нотаток
Класи Note та NoteBook для створення, редагування, пошуку та збереження нотаток.
"""

from storage import save_to_file, load_from_file
from datetime import datetime
from collections import UserList
from config import NOTES_FILE


class Note:
    """Окрема нотатка з текстом, тегами та міткою часу."""

    def __init__(self, title: str, text: str, tags: list[str] | None = None):
        if not title or not title.strip():
            raise ValueError("Note title cannot be empty.")
        if not text or not text.strip():
            raise ValueError("Note text cannot be empty.")
        self.title = title.strip()
        self.text = text.strip()
        self.tags = [t.strip().lower() for t in tags if t.strip()] if tags else []
        self.created_at = datetime.now()

    def edit_text(self, new_text: str):
        """Редагувати текст нотатки."""
        if not new_text or not new_text.strip():
            raise ValueError("Note text cannot be empty.")
        self.text = new_text.strip()

    def edit_title(self, new_title: str):
        """Редагувати заголовок нотатки."""
        if not new_title or not new_title.strip():
            raise ValueError("Note title cannot be empty.")
        self.title = new_title.strip()

    def add_tag(self, tag: str) -> bool:
        """Додати тег до нотатки. Повертає True якщо додано, False якщо вже існує."""
        tag = tag.strip().lower()
        if not tag:
            raise ValueError("Tag cannot be empty.")
        if tag in self.tags:
            return False
        self.tags.append(tag)
        return True

    def remove_tag(self, tag: str) -> bool:
        """Видалити тег з нотатки. Повертає True якщо видалено, False якщо не знайдено."""
        tag = tag.strip().lower()
        if tag in self.tags:
            self.tags.remove(tag)
            return True
        return False

    def __repr__(self):
        return f"Note(title={self.title!r}, tags={self.tags!r})"

    def __str__(self):
        tags_str = ", ".join(self.tags) if self.tags else "none"
        return (
            f"Title: {self.title}\n"
            f"   {self.text}\n"
            f"   Tags: {tags_str}\n"
            f"   Created: {self.created_at:%Y-%m-%d %H:%M}"
        )


class NoteBook(UserList):
    """Колекція нотаток з можливостями пошуку, сортування та збереження."""

    FILENAME = NOTES_FILE

    # ── Операції CRUD ─────────────────────────────────────

    def add_note(self, title: str, text: str, tags: list[str] | None = None) -> Note:
        """Створити та додати нову нотатку. Піднімає ValueError якщо заголовок вже існує."""
        if self.find_by_title(title):
            raise ValueError(f"Note with title '{title}' already exists.")
        note = Note(title, text, tags)
        self.data.append(note)
        return note

    def find_by_title(self, title: str) -> Note | None:
        """Знайти першу нотатку за заголовком (без урахування регістру)."""
        title_lower = title.strip().lower()
        for note in self.data:
            if note.title.lower() == title_lower:
                return note
        return None

    def delete_note(self, title: str) -> bool:
        """Видалити нотатку за заголовком. Повертає True якщо видалено."""
        note = self.find_by_title(title)
        if note:
            self.data.remove(note)
            return True
        return False

    # ── Пошук ─────────────────────────────────────────────

    def search_by_text(self, query: str) -> list[Note]:
        """Пошук нотаток, що містять запит у заголовку або тексті."""
        q = query.strip().lower()
        return [n for n in self.data if q in n.title.lower() or q in n.text.lower()]

    def search_by_tag(self, tag: str) -> list[Note]:
        """Пошук нотаток за тегом."""
        tag = tag.strip().lower()
        return [n for n in self.data if tag in n.tags]

    # ── Сортування ────────────────────────────────────────

    def sort_by_tags(self) -> list[Note]:
        """Повертає нотатки, відсортовані за першим тегом (без тегів — в кінці)."""
        return sorted(
            self.data,
            key=lambda n: n.tags[0] if n.tags else "\uffff",
        )

    # ── Збереження / Завантаження ──────────────────────────

    def save(self):
        # Використовуємо ваш універсальний storage
        save_to_file(self.data, self.FILENAME)

    def load(self):
        # default_factory=list, бо ми наслідуємося від UserList (self.data має бути списком)
        self.data = list(load_from_file(self.FILENAME, list))