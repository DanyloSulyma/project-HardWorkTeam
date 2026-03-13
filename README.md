# project-HardWorkTeam

Personal Assistant CLI

## Notes Module

The `notes.py` module provides two classes — `Note` and `NoteBook` — for creating, editing, searching, and organising text notes.

### Note

| Method | Description |
|--------|-------------|
| `Note(title, text, tags=None)` | Create a note with a title, text, and optional list of tags |
| `edit_title(new_title)` | Change the note's title |
| `edit_text(new_text)` | Change the note's text |
| `add_tag(tag)` | Add a tag (returns `False` if it already exists) |
| `remove_tag(tag)` | Remove a tag (returns `False` if not found) |

- Title and text cannot be empty.
- Tags are stored in lowercase and stripped of whitespace.
- Each note records a `created_at` timestamp automatically.

### NoteBook

`NoteBook` extends `UserList` and manages a collection of `Note` objects.

| Method | Description |
|--------|-------------|
| `add_note(title, text, tags=None)` | Create and store a note (title must be unique) |
| `find_by_title(title)` | Find a note by title (case-insensitive) |
| `delete_note(title)` | Delete a note by title |
| `search_by_text(query)` | Search notes whose title or text contains the query |
| `search_by_tag(tag)` | Search notes by tag |
| `sort_by_tags()` | Return notes sorted by first tag (untagged last) |
| `save(filename=None)` | Save notes to file (uses `config.NOTES_FILE` by default) |
| `load(filename=None)` | Load notes from file |

### Quick Example

```python
from notes import NoteBook

book = NoteBook()
book.add_note("Shopping", "Buy milk and eggs", ["grocery", "home"])
book.add_note("Meeting", "Team sync at 10 AM", ["work"])

print(book.search_by_tag("work"))   # [Note(title='Meeting', tags=['work'])]
print(book.sort_by_tags())          # sorted by first tag alphabetically
```
