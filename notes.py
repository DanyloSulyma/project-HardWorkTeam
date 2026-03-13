"""
Notes Module
Classes Note and NoteBook for creating, editing, searching, and saving notes.
"""

from datetime import datetime
from collections import UserList
# from storage import save_to_file, load_from_file # Uncomment when storage module is implemented
from config import NOTES_FILE


class Note:
    """A single note with text, tags, and a timestamp."""

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
        """Edit the note's text."""
        if not new_text or not new_text.strip():
            raise ValueError("Note text cannot be empty.")
        self.text = new_text.strip()

    def edit_title(self, new_title: str):
        """Edit the note's title."""
        if not new_title or not new_title.strip():
            raise ValueError("Note title cannot be empty.")
        self.title = new_title.strip()

    def add_tag(self, tag: str) -> bool:
        """Add a tag to the note. Returns True if added, False if already exists."""
        tag = tag.strip().lower()
        if not tag:
            raise ValueError("Tag cannot be empty.")
        if tag in self.tags:
            return False
        self.tags.append(tag)
        return True

    def remove_tag(self, tag: str) -> bool:
        """Remove a tag from the note. Returns True if removed, False if not found."""
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
    """A collection of notes with search, sort, and persistence capabilities."""

    FILENAME = NOTES_FILE

    # ── CRUD ──────────────────────────────────────────────

    def add_note(self, title: str, text: str, tags: list[str] | None = None) -> Note:
        """Create and add a new note. Raises ValueError if title already exists."""
        if self.find_by_title(title):
            raise ValueError(f"Note with title '{title}' already exists.")
        note = Note(title, text, tags)
        self.data.append(note)
        return note

    def find_by_title(self, title: str) -> Note | None:
        """Find the first note matching the given title (case-insensitive)."""
        title_lower = title.strip().lower()
        for note in self.data:
            if note.title.lower() == title_lower:
                return note
        return None

    def delete_note(self, title: str) -> bool:
        """Delete a note by title. Returns True if deleted."""
        note = self.find_by_title(title)
        if note:
            self.data.remove(note)
            return True
        return False

    # ── Search ────────────────────────────────────────────

    def search_by_text(self, query: str) -> list[Note]:
        """Search notes containing the query in their title or text."""
        q = query.strip().lower()
        return [n for n in self.data if q in n.title.lower() or q in n.text.lower()]

    def search_by_tag(self, tag: str) -> list[Note]:
        """Search notes by tag."""
        tag = tag.strip().lower()
        return [n for n in self.data if tag in n.tags]

    # ── Sorting ───────────────────────────────────────────

    def sort_by_tags(self) -> list[Note]:
        """Return notes sorted by their first tag (untagged notes go last)."""
        return sorted(
            self.data,
            key=lambda n: n.tags[0] if n.tags else "\uffff",
        )

    # ── Save / Load ───────────────────────────────────────

    def save(self, filename: str | None = None):
        """Save notes to a file via the storage module."""
        # save_to_file(self.data, filename or self.FILENAME) # Uncomment when storage module is implemented

    def load(self, filename: str | None = None):
        """Load notes from a file via the storage module."""
        # self.data = load_from_file(filename or self.FILENAME, list) # Uncomment when storage module is implemented

