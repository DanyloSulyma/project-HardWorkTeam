from colorama import Fore, Style, init

from address_book import AddressBook
from cli_parser import get_intent_suggestion, get_special_response, get_suggestion, parse_input
from commands import COMMANDS, INTENT_PHRASES, execute_command
from config import CONTACTS_FILE, NOTES_FILE
from notes import NoteBook
from storage import load_from_file, save_to_file

# Ініціалізація Colorama для Windows
init(autoreset=True)

# --- Головний цикл ---

def main():
    book = load_from_file(CONTACTS_FILE, AddressBook)
    notebook = load_from_file(NOTES_FILE, NoteBook)
    
    print(Fore.BLUE + Style.BRIGHT + "========================================")
    print(Fore.YELLOW + Style.BRIGHT + "   Welcome to HardWorkTeam Assistant!   ")
    print(Fore.BLUE + Style.BRIGHT + "========================================")

    while True:
        user_input = input(Fore.CYAN + "Enter a command: " + Style.RESET_ALL).strip()
        
        if not user_input:
            continue

        special = get_special_response(user_input)
        if special:
            print(special)
            continue

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

        result = execute_command(command, args, book, notebook)
        if result is not None:
            print(result)
        else:
            suggestion = get_intent_suggestion(user_input, COMMANDS, INTENT_PHRASES)
            if not suggestion:
                suggestion = get_suggestion(command, COMMANDS)
            if suggestion:
                print(Fore.YELLOW + f"Unknown command. Did you mean '{suggestion}'?")
            else:
                print(Fore.RED + "Unknown command. Try again.")

if __name__ == "__main__":
    main()
