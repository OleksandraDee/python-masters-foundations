from collections import UserDict

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
        if not new_value.isdigit() or len(new_value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        self._value = new_value

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone_value):
        for phone in self.phones:
            if phone.value == phone_value:
                self.phones.remove(phone)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        return False

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"

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


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command."
    return inner

@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)
    if record:
        record.add_phone(phone)
        return "Phone added to existing contact."
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."

@input_error
def change_contact(args, book):
    name, new_phone = args
    record = book.find(name)
    if not record:
        raise KeyError
    if record.phones:
        record.phones[0] = Phone(new_phone)
        return "Phone updated."
    else:
        return "No phones to update. Use 'add' to add a phone first."

@input_error
def show_phone(args, book):
    name, = args
    record = book.find(name)
    if not record:
        raise KeyError
    return record

@input_error
def show_all(book):
    if not book.data:
        return "No contacts available."
    return "\n".join(str(record) for record in book.data.values())

def main():
    book = AddressBook()
    print("Hello! This is your assistant bot.")
    while True:
        command = input("Enter a command: ").strip().lower()
        if command in ["exit", "close", "quit"]:
            print("Good bye!")
            break

        if command == "add":
            args = input("Enter name and phone: ").split()
            print(add_contact(args, book))

        elif command == "change":
            args = input("Enter name and new phone: ").split()
            print(change_contact(args, book))

        elif command == "phone":
            args = input("Enter name: ").split()
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
