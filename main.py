import difflib
import shlex
import re
from colorama import Fore, Style, init
from address_book import AddressBook
from config import CONTACTS_FILE, NOTES_FILE
from notes import NoteBook
from storage import load_from_file, save_to_file

# Ініціалізація Colorama для Windows
init(autoreset=True)

# Список команд для інтелектуального аналізу
COMMANDS = [
    "hello",
    "help",
    "add-contact",
    "change-contact",
    "phone",
    "delete-contact",
    "search-contacts",
    "all-contacts",
    "add-email",
    "add-address",
    "add-birthday",
    "show-birthday",
    "birthdays",
    "add-note",
    "edit-note",
    "delete-note",
    "add-tag",
    "remove-tag",
    "search-notes",
    "search-notes-tag",
    "sort-notes",
    "all-notes",
    "exit",
    "close",
]

# Простий словник намірів: фрази, які можуть описувати команду природною мовою.
INTENT_PHRASES = {
    "all-contacts": [
        "all contacts",
        "show contacts",
        "покажи контакти",
        "всі контакти",
        "список контактів",
    ],
    "search-contacts": [
        "find contact",
        "search contact",
        "знайди контакт",
        "пошук контакту",
    ],
    "add-contact": [
        "add contact",
        "new contact",
        "додай контакт",
        "створити контакт",
    ],
    "change-contact": [
        "change phone",
        "edit contact",
        "змінити номер",
        "редагувати контакт",
    ],
    "delete-contact": [
        "delete contact",
        "remove contact",
        "видали контакт",
    ],
    "phone": [
        "show phone",
        "contact phone",
        "номер телефону",
        "покажи номер",
    ],
    "add-email": [
        "add email",
        "додай email",
        "додай пошту",
    ],
    "add-address": [
        "add address",
        "додай адресу",
        "address for contact",
    ],
    "add-birthday": [
        "add birthday",
        "додай день народження",
    ],
    "show-birthday": [
        "show birthday",
        "покажи день народження",
    ],
    "birthdays": [
        "upcoming birthdays",
        "nearest birthdays",
        "іменинники",
        "дні народження",
    ],
    "all-notes": [
        "all notes",
        "show notes",
        "всі нотатки",
        "покажи нотатки",
    ],
    "search-notes": [
        "search notes",
        "find note",
        "пошук нотаток",
        "знайди нотатку",
    ],
    "add-note": [
        "add note",
        "new note",
        "додай нотатку",
        "створити нотатку",
    ],
    "edit-note": [
        "edit note",
        "change note",
        "редагувати нотатку",
    ],
    "delete-note": [
        "delete note",
        "remove note",
        "видали нотатку",
    ],
    "add-tag": [
        "add tag",
        "додай тег",
    ],
    "remove-tag": [
        "remove tag",
        "видали тег",
    ],
    "search-notes-tag": [
        "search by tag",
        "find by tag",
        "пошук за тегом",
    ],
    "sort-notes": [
        "sort notes",
        "сортуй нотатки",
        "відсортуй нотатки",
    ],
    "help": [
        "help",
        "допомога",
        "список команд",
    ],
    "hello": [
        "hello",
        "привіт",
    ],
    "exit": [
        "exit",
        "quit",
        "вийти",
        "завершити",
    ],
}

# --- Декоратор для обробки помилок ---
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return Fore.RED + f"Error: {e}"
        except IndexError:
            return Fore.RED + "Error: Missing arguments for the command."
        except KeyError:
            return Fore.RED + "Error: Contact or note not found."
        except TypeError as e:
            return Fore.RED + f"Error: {e}"
        except Exception as e:
            return Fore.RED + f"An unexpected error occurred: {e}"
    return inner

# --- Функції-обробники (Handlers) ---
@input_error
def show_help():
    """Повертає список усіх доступних команд з описом."""
    help_text = [
        Fore.YELLOW + "\nДоступні команди:" + Style.RESET_ALL,
        f"{Fore.CYAN}hello{Style.RESET_ALL} - Привітання від помічника.",
        f"{Fore.CYAN}help{Style.RESET_ALL} - Показати цей список команд.",
        f"{Fore.CYAN}add-contact [ім'я] [телефон]{Style.RESET_ALL} - Додати новий контакт.",
        f"{Fore.CYAN}change-contact [ім'я] [старий] [новий]{Style.RESET_ALL} - Змінити номер телефону.",
        f"{Fore.CYAN}delete-contact [ім'я]{Style.RESET_ALL} - Видалити контакт.",
        f"{Fore.CYAN}phone [ім'я]{Style.RESET_ALL} - Показати телефони контакту.",
        f"{Fore.CYAN}all-contacts{Style.RESET_ALL} - Показати всі контакти в адресній книзі.",
        f"{Fore.CYAN}search-contacts [запит]{Style.RESET_ALL} - Пошук контактів за ім'ям або номером.",
        f"{Fore.CYAN}add-email [ім'я] [email]{Style.RESET_ALL} - Додати email до контакту.",
        f"{Fore.CYAN}add-address [ім'я] [адреса]{Style.RESET_ALL} - Додати адресу до контакту.",
        f"{Fore.CYAN}add-birthday [ім'я] [DD.MM.YYYY]{Style.RESET_ALL} - Додати день народження.",
        f"{Fore.CYAN}show-birthday [ім'я]{Style.RESET_ALL} - Показати день народження контакту.",
        f"{Fore.CYAN}birthdays [дні]{Style.RESET_ALL} - Помічник покаже іменинників на найближчі N днів.",
        f"{Fore.CYAN}add-note [заголовок] [текст]{Style.RESET_ALL} - Створити нову нотатку.",
        f"{Fore.CYAN}edit-note [заголовок] [новий_текст]{Style.RESET_ALL} - Редагувати текст нотатки.",
        f"{Fore.CYAN}delete-note [заголовок]{Style.RESET_ALL} - Видалити нотатку.",
        f"{Fore.CYAN}add-tag [заголовок] [тег]{Style.RESET_ALL} - Додати тег до нотатки.",
        f"{Fore.CYAN}remove-tag [заголовок] [тег]{Style.RESET_ALL} - Видалити тег із нотатки.",
        f"{Fore.CYAN}all-notes{Style.RESET_ALL} - Показати всі збережені нотатки.",
        f"{Fore.CYAN}search-notes [запит]{Style.RESET_ALL} - Пошук нотаток за заголовком, текстом або тегами.",
        f"{Fore.CYAN}search-notes-tag [тег]{Style.RESET_ALL} - Пошук нотаток за тегом.",
        f"{Fore.CYAN}sort-notes{Style.RESET_ALL} - Відсортувати нотатки за тегами.",
        f"{Fore.CYAN}Порада:{Style.RESET_ALL} якщо у параметрі є пробіли, використовуйте лапки.",
        f"{Fore.CYAN}Приклад:{Style.RESET_ALL} add-address Ivan \"Kyiv, Khreshchatyk 1\"",
        f"{Fore.CYAN}exit / close{Style.RESET_ALL} - Зберегти дані та вийти з програми.",
        Fore.YELLOW + "\nПатріотичні пасхалки:" + Style.RESET_ALL,
        "Спробуйте ввести: 'Слава Україні', 'Слава Нації' або 'Україна'."
    ]
    return "\n".join(help_text)

@input_error
def add_contact(args, book: AddressBook):
    from models import Record
    name, phone = args[0], args[1]
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    if record.find_phone(phone):
        return Fore.YELLOW + f"Phone {phone} already exists for {name}."
    record.add_phone(phone)
    return Fore.GREEN + f"Contact {name} updated with phone {phone}."


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)
    if not record:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return Fore.GREEN + f"Phone for {name} changed from {old_phone} to {new_phone}."


@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError
    if not record.phones:
        return Fore.YELLOW + f"Contact {name} has no phones."
    phones = ", ".join(phone.value for phone in record.phones)
    return Fore.CYAN + f"{name}: {phones}"


@input_error
def delete_contact(args, book: AddressBook):
    name = args[0]
    if book.delete(name):
        return Fore.GREEN + f"Contact {name} deleted."
    raise KeyError


@input_error
def search_contacts(args, book: AddressBook):
    query = " ".join(args)
    results = book.search(query)
    if not results:
        return Fore.YELLOW + "No contacts found matching your query."
    return "\n".join(str(record) for record in results)


@input_error
def add_email(args, book: AddressBook):
    name, email = args[0], args[1]
    record = book.find(name)
    if not record:
        raise KeyError
    record.add_email(email)
    return Fore.GREEN + f"Email added to {name}."


@input_error
def add_address(args, book: AddressBook):
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)
    if not record:
        raise KeyError
    record.add_address(address)
    return Fore.GREEN + f"Address added to {name}."


@input_error
def add_birthday(args, book: AddressBook):
    from models import Birthday
    name, birthday_str = args[0], args[1]
    record = book.find(name)
    if not record:
        raise KeyError
    record.birthday = Birthday(birthday_str)
    return Fore.GREEN + f"Birthday for {name} set to {birthday_str}."


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError
    if not record.birthday:
        return Fore.YELLOW + f"Birthday for {name} is not set."
    return Fore.CYAN + f"{name}: {record.birthday}"

@input_error
def show_birthdays(args, book: AddressBook):
    days = int(args[0]) if args else 7
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return Fore.YELLOW + f"No birthdays in the next {days} days."
    res = Fore.CYAN + f"Upcoming birthdays ({days} days):\n"
    for item in upcoming:
        res += f" {item['name']}: {item['congratulation_date']}\n"
    return res.strip()

@input_error
def add_note(args, notebook: NoteBook):
    title = args[0]
    text = " ".join(args[1:])
    notebook.add_note(title, text)
    return Fore.GREEN + f"Note '{title}' added successfully."


@input_error
def edit_note(args, notebook: NoteBook):
    title = args[0]
    new_text = " ".join(args[1:])
    note = notebook.find_by_title(title)
    if not note:
        raise KeyError
    note.edit_text(new_text)
    return Fore.GREEN + f"Note '{title}' updated successfully."


@input_error
def delete_note(args, notebook: NoteBook):
    title = args[0]
    if notebook.delete_note(title):
        return Fore.GREEN + f"Note '{title}' deleted successfully."
    raise KeyError


@input_error
def add_tag(args, notebook: NoteBook):
    title, tag = args[0], args[1]
    note = notebook.find_by_title(title)
    if not note:
        raise KeyError
    if note.add_tag(tag):
        return Fore.GREEN + f"Tag '{tag}' added to note '{title}'."
    return Fore.YELLOW + f"Tag '{tag}' already exists in note '{title}'."


@input_error
def remove_tag(args, notebook: NoteBook):
    title, tag = args[0], args[1]
    note = notebook.find_by_title(title)
    if not note:
        raise KeyError
    if note.remove_tag(tag):
        return Fore.GREEN + f"Tag '{tag}' removed from note '{title}'."
    return Fore.YELLOW + f"Tag '{tag}' not found in note '{title}'."

@input_error
def search_notes(args, notebook: NoteBook):
    query = args[0]
    results = notebook.search_by_text(query)
    if not results:
        return Fore.YELLOW + "No notes found matching your query."
    return "\n---\n".join(str(n) for n in results)


@input_error
def search_notes_tag(args, notebook: NoteBook):
    tag = args[0]
    results = notebook.search_by_tag(tag)
    if not results:
        return Fore.YELLOW + f"No notes found for tag '{tag}'."
    return "\n---\n".join(str(n) for n in results)


@input_error
def sort_notes(notebook: NoteBook):
    sorted_items = notebook.sort_by_tags()
    if not sorted_items:
        return Fore.YELLOW + "No notes to sort."
    return "\n---\n".join(str(note) for note in sorted_items)

# --- Допоміжні функції ---

def get_suggestion(command):
    matches = difflib.get_close_matches(command, COMMANDS, n=1, cutoff=0.6)
    return matches[0] if matches else None


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def get_intent_suggestion(user_input: str):
    normalized = normalize_text(user_input)
    if not normalized:
        return None

    best_command = None
    best_score = 0.0

    # 1) Порівняння зі списком явних фраз намірів.
    for command, phrases in INTENT_PHRASES.items():
        for phrase in phrases:
            ratio = difflib.SequenceMatcher(None, normalized, phrase).ratio()
            if phrase in normalized:
                ratio = max(ratio, 0.95)
            if ratio > best_score:
                best_score = ratio
                best_command = command

    # 2) Порівняння з назвами команд як fallback.
    command_guess = difflib.get_close_matches(normalized, COMMANDS, n=1, cutoff=0.55)
    if command_guess and best_score < 0.72:
        return command_guess[0]

    return best_command if best_score >= 0.5 else None


def parse_input(user_input):
    parts = shlex.split(user_input)
    if not parts:
        return "", []
    cmd, *args = parts
    cmd = cmd.strip().lower()
    return cmd, args

# --- Головний цикл ---

def main():
    # Завантаження даних
    book = load_from_file(CONTACTS_FILE, AddressBook)
    notebook = load_from_file(NOTES_FILE, NoteBook)
    
    print(Fore.BLUE + Style.BRIGHT + "========================================")
    print(Fore.YELLOW + Style.BRIGHT + "   Welcome to HardWorkTeam Assistant!   ")
    print(Fore.BLUE + Style.BRIGHT + "========================================")

    while True:
        user_input = input(Fore.CYAN + "Enter a command: " + Style.RESET_ALL).strip()
        
        if not user_input:
            continue

        # Патріотичні пасхалки
        input_lower = user_input.lower()

        if "слава україні" in input_lower or input_lower == "слава":
            print(Fore.YELLOW + Style.BRIGHT + "Героям Слава! 🇺🇦")
            continue
            
        elif "слава нації" in input_lower:
            print(Fore.RED + Style.BRIGHT + "Смерть ворогам! 💀")
            continue
            
        elif "україна" in input_lower:
            # Якщо це не "Слава Україні", а просто згадка України
            if "понад усе" not in input_lower:
                print(Fore.BLUE + Style.BRIGHT + "Понад усе! 💙" + Fore.YELLOW + Style.BRIGHT + "💛")
                continue

        elif "путін" in input_lower:
            print(Fore.RED + Style.BRIGHT + "Хуйло! ❌")
            continue
        # ---------------------------------

        try:
            command, args = parse_input(user_input)
        except ValueError:
            print(Fore.RED + "Invalid input format. Check quotes and try again.")
            continue

        if command in ["close", "exit"]:
            save_to_file(book, CONTACTS_FILE)
            save_to_file(notebook, NOTES_FILE)
            print(Fore.YELLOW + "Data saved. Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "help":
            print(show_help())

        elif command == "add-contact":
            print(add_contact(args, book))

        elif command == "change-contact":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "delete-contact":
            print(delete_contact(args, book))

        elif command == "search-contacts":
            print(search_contacts(args, book))

        elif command == "add-email":
            print(add_email(args, book))

        elif command == "add-address":
            print(add_address(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(show_birthdays(args, book))

        elif command == "add-note":
            print(add_note(args, notebook))

        elif command == "edit-note":
            print(edit_note(args, notebook))

        elif command == "delete-note":
            print(delete_note(args, notebook))

        elif command == "add-tag":
            print(add_tag(args, notebook))

        elif command == "remove-tag":
            print(remove_tag(args, notebook))

        elif command == "search-notes":
            print(search_notes(args, notebook))

        elif command == "search-notes-tag":
            print(search_notes_tag(args, notebook))

        elif command == "sort-notes":
            print(sort_notes(notebook))

        elif command == "all-contacts":
            if not book.values():
                print(Fore.YELLOW + "No contacts saved yet.")
            for record in book.values():
                print(record)

        elif command == "all-notes":
            if not notebook:
                print(Fore.YELLOW + "No notes saved yet.")
            for note in notebook:
                print(f"{note}\n---")

        else:
            suggestion = get_intent_suggestion(user_input)
            if not suggestion:
                suggestion = get_suggestion(command)
            if suggestion:
                print(Fore.YELLOW + f"Unknown command. Did you mean '{suggestion}'?")
            else:
                print(Fore.RED + "Unknown command. Try again.")

if __name__ == "__main__":
    main()
