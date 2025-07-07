from collections import UserDict
from datetime import datetime, timedelta, date
import re


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value  # викличе setter

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, new_value):
        normalized = normalize_phone(new_value)
        if not re.fullmatch(r'\+380\d{9}', normalized):
            raise ValueError("Номер телефону має бути у форматі +380XXXXXXXXX — український мобільний номер.")
        self._value = normalized


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте формат: ДД.ММ.РРРР")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                try:
                    self.phones[i] = Phone(new_phone)
                    return "Номер оновлено."
                except ValueError as e:
                    return f"Помилка при зміні номера: {e}"
        return "Старий номер не знайдено."

    def find_phone(self, phone_value):
        for phone in self.phones:
            if phone.value == phone_value:
                return phone
        return None

    def add_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday)
            return "День народження додано."
        except ValueError as e:
            return f"Помилка: {e}"

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", день народження: {self.birthday}" if self.birthday else ""
        return f"Контакт: {self.name}, телефони: {phones_str}{birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False

    def get_upcoming_birthdays(self):
        today = date.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.value
                this_year_birthday = bday.replace(year=today.year)

                if this_year_birthday < today:
                    this_year_birthday = this_year_birthday.replace(year=today.year + 1)

                days_until_birthday = (this_year_birthday - today).days

                if 0 <= days_until_birthday <= 7:
                    if this_year_birthday.weekday() >= 5:
                        delta = 7 - this_year_birthday.weekday()
                        congrats_day = this_year_birthday + timedelta(days=delta)
                    else:
                        congrats_day = this_year_birthday

                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congrats_date": congrats_day.strftime("%A, %d.%m.%Y")
                    })

        return upcoming_birthdays


# ----------------------- Допоміжні функції -----------------------
def normalize_phone(phone_number):
    cleaned = re.sub(r'[^\d+]', '', phone_number.strip())
    if cleaned.startswith('+380'):
        return cleaned
    if cleaned.startswith('380'):
        return '+' + cleaned
    if cleaned.startswith('0'):
        return '+38' + cleaned
    return '+38' + cleaned


# ----------------------- Обробка команд -----------------------
def parse_input(user_input):
    parts = user_input.strip().split()
    return parts[0].lower(), parts[1:]


def handle_hello():
    return "Чим я можу вам допомогти?"


def handle_add(args, book):
    if len(args) < 2:
        return "Команда 'add' вимагає два аргументи: Ім’я і Телефон. Наприклад: add Anna +380951234567"
    name, phone = args[0], args[1]
    if book.find(name):
        return "Контакт з таким ім’ям вже існує."
    try:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return f"Контакт {name} додано."
    except ValueError as e:
        return f"Помилка: {e}"


def handle_change(args, book):
    if len(args) < 2:
        return "Команда 'change' вимагає два аргументи: Ім’я і НовийТелефон. Наприклад: change Anna +380951234567"
    name, new_phone = args[0], args[1]
    record = book.find(name)
    if not record:
        return "Контакт не знайдено."
    return record.edit_phone(record.phones[0].value, new_phone)


def handle_phone(args, book):
    if len(args) < 1:
        return "Команда 'phone' вимагає ім’я. Наприклад: phone Anna"
    name = args[0]
    record = book.find(name)
    if record and record.phones:
        return f"{name}: {record.phones[0]}"
    else:
        return "Контакт або номер не знайдено."


def handle_all(book):
    if not book.data:
        return "Книга контактів порожня."
    result = ["Усі контакти:"]
    for rec in book.data.values():
        result.append(str(rec))
    return "\n".join(result)


def handle_birthdays(book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "Немає іменинників найближчим часом."
    result = ["Іменинники цього тижня:"]
    for b in upcoming:
        result.append(f"{b['name']} — привітати {b['congrats_date']}")
    return "\n".join(result)

def handle_add_birthday(args, book):
    if len(args) < 2:
        return "Команда 'add-birthday' вимагає два аргументи: Ім’я і дату народження. Наприклад: add-birthday Anna 12.12.1990"
    name, bday = args[0], args[1]
    record = book.find(name)
    if not record:
        return "Контакт не знайдено."
    return record.add_birthday(bday)

def handle_show_birthday(args, book):
    if len(args) < 1:
        return "Команда 'show-birthday' вимагає ім’я. Наприклад: show-birthday Anna"
    name = args[0]
    record = book.find(name)
    if not record:
        return "Контакт не знайдено."
    if not record.birthday:
        return "Для цього контакту не вказано день народження."
    return f"День народження {name}: {record.birthday.value.strftime('%d.%m.%Y')}"

# ----------------------- Основна функція -----------------------
def main():
    book = AddressBook()

    print("Вітаю! Це ваш контакт-бот.")
    while True:
        user_input = input("Введіть команду: ").strip()
        if not user_input:
            continue

        command, args = parse_input(user_input)

        if command in ["exit", "close"]:
            print("До побачення!")
            break
        elif command == "hello":
            print(handle_hello())
        elif command == "add":
            print(handle_add(args, book))
        elif command == "change":
            print(handle_change(args, book))
        elif command == "phone":
            print(handle_phone(args, book))
        elif command == "all":
            print(handle_all(book))
        elif command == "add-birthday":
            print(handle_add_birthday(args, book))
        elif command == "show-birthday":
            print(handle_show_birthday(args, book))
        elif command == "birthdays":
            print(handle_birthdays(book))
        else:
            print("Невідома команда. Спробуйте знову.")


if __name__ == "__main__":
    main()
