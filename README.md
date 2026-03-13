# project-HardWorkTeam
Personal Assistant CLI 
Персональний помічник з інтерфейсом командного рядка для керування контактами та нотатками.
Встановлення
Вимоги

Python 3.10+
Не потребує сторонніх бібліотек

Крок 1 — Клонування репозиторію
git clone https://github.com/your-repo/personal-assistant.git
cd personal-assistant
Крок 2 — Запуск напряму
python main.py
Крок 3 — Або встановити як пакет
pip install .
assistant

Команди для контактів
add-contact [ім'я] [телефон] — Додати новий контакт
add-phone [ім'я] [телефон] — Додати телефон до контакту
change-phone [ім'я] [старий] [новий] — Змінити номер телефону
add-email [ім'я] [email] — Додати email до контакту
add-address [ім'я] [адреса] — Додати адресу до контакту
add-birthday [ім'я] [ДД.ММ.РРРР] — Додати день народження
show-birthday [ім'я] — Показати день народження
show-phone [ім'я] — Показати телефони контакту
show-contact [ім'я] — Показати повну інформацію
delete-contact [ім'я] — Видалити контакт
search-contacts [запит] — Пошук контактів
all-contacts — Показати всі контакти
birthdays [днів] — Найближчі дні народження
Команди для нотаток
add-note [заголовок] [текст] — Додати нову нотатку
show-note [id] — Показати нотатку за ID
edit-note [id] [title/content] [значення] — Редагувати нотатку
delete-note [id] — Видалити нотатку
search-notes [запит] — Пошук нотаток за текстом
all-notes — Показати всі нотатки
add-tag [id] [тег] — Додати тег до нотатки
remove-tag [id] [тег] — Видалити тег з нотатки
search-tag [тег] — Пошук нотаток за тегом
notes-by-tag — Показати нотатки відсортовані за тегом

Загальні команди
hello — Привітання
help — Показати всі команди
close / exit — Зберегти та вийти

Приклади використання
add-contact John 1234567890
add-email John john@example.com
add-birthday John 15.03.1990
birthdays 30
add-note Зустріч Обговорити проєкт
add-tag 1 робота
search-tag робота

Збереження даних
Контакти зберігаються у файл contacts.pkl
Нотатки зберігаються у файл notes.pkl
Дані автоматично зберігаються при введенні exit або close
При наступному запуску всі дані автоматично завантажуються

Структура проєкту
main.py — Головний файл, CLI інтерфейс
address_book.py — Клас AddressBook, управління контактами
storage.py — Серіалізація даних через pickle
records.py — Класи Record, Field, Phone, Email тощо
notes.py — Класи Note та NoteBook
setup.py — Встановлення як пакету
README.md — Документація
contacts.pkl — Автоматично створюється при запуску
notes.pkl — Автоматично створюється при запуску

Автори
Danylo  — Тімлід: CLI інтерфейс, інтеграція 
Dmytro — Контакти: Класи Record, Field, Phone, Email, Birthday
Masha — База даних: AddressBook, storage.py, README
Anton — Нотатки: Note, NoteBook, теги