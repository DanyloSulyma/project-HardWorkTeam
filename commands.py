from colorama import Fore, Style

from address_book import AddressBook
from notes import NoteBook


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


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return Fore.RED + f"Error: {error}"
        except IndexError:
            return Fore.RED + "Error: Missing arguments for the command."
        except KeyError:
            return Fore.RED + "Error: Contact or note not found."
        except TypeError as error:
            return Fore.RED + f"Error: {error}"

    return inner


@input_error
def show_help() -> str:
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
        "Спробуйте ввести: 'Слава Україні', 'Слава Нації' або 'Україна'.",
    ]
    return "\n".join(help_text)


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
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
def change_contact(args: list[str], book: AddressBook) -> str:
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)
    if not record:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return Fore.GREEN + f"Phone for {name} changed from {old_phone} to {new_phone}."


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError
    if not record.phones:
        return Fore.YELLOW + f"Contact {name} has no phones."
    phones = ", ".join(phone.value for phone in record.phones)
    return Fore.CYAN + f"{name}: {phones}"


@input_error
def delete_contact(args: list[str], book: AddressBook) -> str:
    name = args[0]
    if book.delete(name):
        return Fore.GREEN + f"Contact {name} deleted."
    raise KeyError


@input_error
def search_contacts(args: list[str], book: AddressBook) -> str:
    query = " ".join(args)
    results = book.search(query)
    if not results:
        return Fore.YELLOW + "No contacts found matching your query."
    return "\n".join(str(record) for record in results)


@input_error
def add_email(args: list[str], book: AddressBook) -> str:
    name, email = args[0], args[1]
    record = book.find(name)
    if not record:
        raise KeyError
    record.add_email(email)
    return Fore.GREEN + f"Email added to {name}."


@input_error
def add_address(args: list[str], book: AddressBook) -> str:
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)
    if not record:
        raise KeyError
    record.add_address(address)
    return Fore.GREEN + f"Address added to {name}."


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    from models import Birthday

    name, birthday_str = args[0], args[1]
    record = book.find(name)
    if not record:
        raise KeyError
    record.birthday = Birthday(birthday_str)
    return Fore.GREEN + f"Birthday for {name} set to {birthday_str}."


@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError
    if not record.birthday:
        return Fore.YELLOW + f"Birthday for {name} is not set."
    return Fore.CYAN + f"{name}: {record.birthday}"


@input_error
def show_birthdays(args: list[str], book: AddressBook) -> str:
    days = int(args[0]) if args else 7
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return Fore.YELLOW + f"No birthdays in the next {days} days."
    result = Fore.CYAN + f"Upcoming birthdays ({days} days):\n"
    for item in upcoming:
        result += f" {item['name']}: {item['congratulation_date']}\n"
    return result.strip()


@input_error
def add_note(args: list[str], notebook: NoteBook) -> str:
    title = args[0]
    text = " ".join(args[1:])
    notebook.add_note(title, text)
    return Fore.GREEN + f"Note '{title}' added successfully."


@input_error
def edit_note(args: list[str], notebook: NoteBook) -> str:
    title = args[0]
    new_text = " ".join(args[1:])
    note = notebook.find_by_title(title)
    if not note:
        raise KeyError
    note.edit_text(new_text)
    return Fore.GREEN + f"Note '{title}' updated successfully."


@input_error
def delete_note(args: list[str], notebook: NoteBook) -> str:
    title = args[0]
    if notebook.delete_note(title):
        return Fore.GREEN + f"Note '{title}' deleted successfully."
    raise KeyError


@input_error
def add_tag(args: list[str], notebook: NoteBook) -> str:
    title, tag = args[0], args[1]
    note = notebook.find_by_title(title)
    if not note:
        raise KeyError
    if note.add_tag(tag):
        return Fore.GREEN + f"Tag '{tag}' added to note '{title}'."
    return Fore.YELLOW + f"Tag '{tag}' already exists in note '{title}'."


@input_error
def remove_tag(args: list[str], notebook: NoteBook) -> str:
    title, tag = args[0], args[1]
    note = notebook.find_by_title(title)
    if not note:
        raise KeyError
    if note.remove_tag(tag):
        return Fore.GREEN + f"Tag '{tag}' removed from note '{title}'."
    return Fore.YELLOW + f"Tag '{tag}' not found in note '{title}'."


@input_error
def search_notes(args: list[str], notebook: NoteBook) -> str:
    query = args[0]
    results = notebook.search_by_text(query)
    if not results:
        return Fore.YELLOW + "No notes found matching your query."
    return "\n---\n".join(str(note) for note in results)


@input_error
def search_notes_tag(args: list[str], notebook: NoteBook) -> str:
    tag = args[0]
    results = notebook.search_by_tag(tag)
    if not results:
        return Fore.YELLOW + f"No notes found for tag '{tag}'."
    return "\n---\n".join(str(note) for note in results)


@input_error
def sort_notes(notebook: NoteBook) -> str:
    sorted_items = notebook.sort_by_tags()
    if not sorted_items:
        return Fore.YELLOW + "No notes to sort."
    return "\n---\n".join(str(note) for note in sorted_items)


def execute_command(command: str, args: list[str], book: AddressBook, notebook: NoteBook) -> str | None:
    if command == "hello":
        return "How can I help you?"
    if command == "help":
        return show_help()
    if command == "add-contact":
        return add_contact(args, book)
    if command == "change-contact":
        return change_contact(args, book)
    if command == "phone":
        return show_phone(args, book)
    if command == "delete-contact":
        return delete_contact(args, book)
    if command == "search-contacts":
        return search_contacts(args, book)
    if command == "add-email":
        return add_email(args, book)
    if command == "add-address":
        return add_address(args, book)
    if command == "add-birthday":
        return add_birthday(args, book)
    if command == "show-birthday":
        return show_birthday(args, book)
    if command == "birthdays":
        return show_birthdays(args, book)
    if command == "add-note":
        return add_note(args, notebook)
    if command == "edit-note":
        return edit_note(args, notebook)
    if command == "delete-note":
        return delete_note(args, notebook)
    if command == "add-tag":
        return add_tag(args, notebook)
    if command == "remove-tag":
        return remove_tag(args, notebook)
    if command == "search-notes":
        return search_notes(args, notebook)
    if command == "search-notes-tag":
        return search_notes_tag(args, notebook)
    if command == "sort-notes":
        return sort_notes(notebook)
    if command == "all-contacts":
        if not book.values():
            return Fore.YELLOW + "No contacts saved yet."
        return "\n".join(str(record) for record in book.values())
    if command == "all-notes":
        if not notebook:
            return Fore.YELLOW + "No notes saved yet."
        return "\n---\n".join(str(note) for note in notebook)
    return None