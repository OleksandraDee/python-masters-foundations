import pickle
import os
import re
from collections import UserDict
from datetime import datetime, timedelta, date


def normalize_phone(phone):
    return re.sub(r"\D", "", phone).replace("380", "+380", 1) if phone.startswith("380") else phone


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

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
        return self.data.pop(name, None)

    def get_upcoming_birthdays(self):
        today = date.today()
        result = []

        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.value.replace(year=today.year)
                if bday < today:
                    bday = bday.replace(year=today.year + 1)

                days_diff = (bday - today).days
                if 0 <= days_diff <= 7:
                    if bday.weekday() >= 5:  # вихідні
                        bday += timedelta(days=(7 - bday.weekday()))
                    result.append({
                        "name": record.name.value,
                        "congrats_date": bday.strftime("%A, %d.%m.%Y")
                    })
        return result


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return AddressBook()


def main():
    book = load_data()

    while True:
        command = input(">>> ").strip().lower()

        if command == "add":
            name = input("Ім'я: ")
            phone = input("Телефон: ")
            rec = Record(name)
            try:
                rec.add_phone(phone)
                book.add_record(rec)
                print("Контакт додано.")
            except ValueError as e:
                print(f"Помилка: {e}")

        elif command == "show":
            for record in book.values():
                print(record)

        elif command == "exit":
            save_data(book)
            print("Дані збережено. До побачення!")
            break

        else:
            print("Невідома команда.")


if __name__ == "__main__":
    main()
