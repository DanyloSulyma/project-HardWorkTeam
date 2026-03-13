# project-HardWorkTeam

Personal Assistant CLI for:
- contact management (name, phones, email, address, birthday)
- notes management (text notes with tags)
- persistence between restarts

## Requirements

- Python 3.10+
- Dependencies from `requirements.txt`

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Data Storage

The app saves data in your home directory (`Path.home()`):
- contacts: `contacts.bin`
- notes: `notes.bin`

Files are configured in `config.py`:
- `CONTACTS_FILE`
- `NOTES_FILE`

## Command Reference

### General

- `hello` - greeting
- `help` - show available commands
- `exit` / `close` - save data and quit

### Contacts

- `add-contact [name] [phone]`
- `change-contact [name] [old_phone] [new_phone]`
- `delete-contact [name]`
- `phone [name]`
- `all-contacts`
- `search-contacts [query]`
- `add-email [name] [email]`
- `add-address [name] [address]`
- `add-birthday [name] [DD.MM.YYYY]`
- `show-birthday [name]`
- `birthdays [days]`

### Notes

- `add-note [title] [text]`
- `edit-note [title] [new_text]`
- `delete-note [title]`
- `all-notes`
- `search-notes [query]`
- `add-tag [title] [tag]`
- `remove-tag [title] [tag]`
- `search-notes-tag [tag]`
- `sort-notes`

## Validation Rules

- Phone must be exactly 10 digits.
- Email format is validated.
- Birthday format: `DD.MM.YYYY`.
- Note title and note text cannot be empty.

## Smart Suggestions

If a command is unknown, assistant suggests the closest command.

It supports:
- typo-based suggestions (for example, `serch-notes` -> `search-notes`)
- intent-based suggestions from free text (for example, `покажи всі контакти` -> `all-contacts`)

## Quotes For Multi-word Arguments

Use quotes when argument contains spaces.

Example:

```text
add-address Ivan "Kyiv, Khreshchatyk 1"
edit-note Work "finish project today"
```

## Patriotic Easter Eggs

The assistant includes custom reactions for phrases like:
- `Слава`
- `Слава Нації`
- `Україна`

## Notes Module (API)

### `Note`

| Method | Description |
|--------|-------------|
| `Note(title, text, tags=None)` | Create a note with a title, text, and optional tags |
| `edit_title(new_title)` | Change note title |
| `edit_text(new_text)` | Change note text |
| `add_tag(tag)` | Add tag (`False` if exists) |
| `remove_tag(tag)` | Remove tag (`False` if missing) |

### `NoteBook`

| Method | Description |
|--------|-------------|
| `add_note(title, text, tags=None)` | Create and store a note |
| `find_by_title(title)` | Find note by title (case-insensitive) |
| `delete_note(title)` | Delete note by title |
| `search_by_text(query)` | Search by title/text |
| `search_by_tag(tag)` | Search by tag |
| `sort_by_tags()` | Sort notes by first tag |
| `save()` | Save to `NOTES_FILE` |
| `load()` | Load from `NOTES_FILE` |
