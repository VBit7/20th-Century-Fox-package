from datetime import datetime, timedelta
from collections import UserDict

import random
import json


class Field:
    """
    Base class for record fields.
    Will be the parent for all fields.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """
    Class for storing the contact name.
    A mandatory field.
    """
    def __init__(self, name):
        self._name = None
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name


class Phone(Field):
    """
    Class for storing a phone number.
    Has format validation (10 digits).
    An optional field for phone numbers. One Record can contain multiple phone numbers.
    """
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_phone):
        if self.check_number(new_phone):
            self._value = new_phone
        else:
            raise ValueError("Invalid phone: phone should consist of 10 digits only")

    @staticmethod
    def check_number(phone_number):
        return len(phone_number) == 10 and phone_number.isdigit()


class Email(Field):
    """
    Class for storing an email address.
    Has format validation for email.
    An optional field.
    """
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_email):
        if self.check_email(new_email):
            self._value = new_email
        else:
            raise ValueError("Invalid email format")

    @staticmethod
    def check_email(email):
        # Simple check for the email format (more complex checks can be used as needed).
        return "@" in email and "." in email.split("@")[-1]

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    """
    Class representing the "Birthday" field.
    """
    def __init__(self, birthday):
        self._birthday = None
        self.birthday = birthday
        
    form = '%d.%m.%Y'

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, new_bd):
        self._birthday = datetime.strptime(new_bd, self.form)

    def __str__(self):
        if self._birthday:
            return self._birthday.strftime(self.form)
        else:
            return "Birthday not set!"


class Record:
    """
    Class for storing information about a contact, including the name and a list of phones.
    Also contains a list of email addresses and an address.
    Responsible for the logic of adding/removing/editing optional fields and storing the mandatory Name field.
    """
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.address = None
        self.notes = None
        self.birthday = Birthday(birthday) if birthday else birthday

    # Adding phone numbers
    def add_phone(self, phone_number):
        phone = phone_number
        self.phones.append(Phone(phone))

    # Adding email addresses
    def add_email(self, email):
        self.emails.append(Email(email))
        return self.emails[-1]

    # Adding birthday
    def add_birthday(self, bd):
        self.birthday = Birthday(bd)
        return self.birthday

    # Returns the number of days until the next birthday
    def days_to_bd(self):
        if not self.birthday:
            return "Birthday not set"

        now = datetime.now()
        bd = self.birthday.birthday
        certain_year = now.year
        bd = bd.replace(year=certain_year)
        if bd < now:
            bd = bd.replace(year=certain_year + 1)
        days_to_bdd = (bd.date() - now.date()).days

        return f"{days_to_bdd} days before the birthday"

    # Removes phone numbers
    def remove_phone(self, phone):
        for el in self.phones:
            if el.value == phone:
                self.phones.remove(el)
                return f"Phone {phone} has been deleted"
        return f"Phone {phone} is not found"

    # Edits phone numbers
    def edit_phone(self, old_phone, new_phone):
        for ind, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[ind] = Phone(new_phone)
                return f"Phone number has been updated for {self.name.name}"
        raise ValueError

    # Removes email addresses
    def remove_email(self, email):
        for el in self.emails:
            if el.value == email:
                self.emails.remove(el)
                return f"Email {email} has been deleted"
        return f"Email {email} is not found"

    # Edits email addresses
    def edit_email(self, old_email, new_email):
        for ind, email in enumerate(self.emails):
            if email.value == old_email:
                self.emails[ind] = Email(new_email)
                return f"Email address has been updated for {self.name.name}"
        raise ValueError

    # Finds phone number
    def find_phone(self, phone_to_find):
        for phone in self.phones:
            if phone.value == phone_to_find:
                return phone
        return None

    # Converts object data to dictionary format
    def to_dict(self):
        return {
            "name": self.name.name,
            "phones": [str(phone) for phone in self.phones],
            "emails": [str(email) for email in self.emails],
            "address": str(self.address) if self.address else "not set",
            "birthday": str(self.birthday) if self.birthday else "not set",
            "notes": str(self.notes) if self.notes else "",
        }

    def __str__(self):
        phone_numbers = ', '.join(str(phone) for phone in self.phones)
        email_addresses = ', '.join(str(email) for email in self.emails)
        address = self.address if self.address else "not set"
        birthday = self.birthday if self.birthday else "not set"
        notes = self.notes if self.notes else ""

        return f'{self.name.name} - Phones: {phone_numbers}, Emails: {email_addresses}, Address: {address}, Birthday: {birthday}, Note: {notes}'


class AddressBookIterator:
    """
    Generator for records in AddressBook, returning representations for N records in one iteration
    """
    def __init__(self, address_book, per_page=10):
        self.address_book = address_book
        self.keys = list(address_book.data.keys())
        self.per_page = per_page
        self.current_page = 0

    def __iter__(self):
        return self

    def __next__(self):
        start_idx = self.current_page * self.per_page
        end_idx = (self.current_page + 1) * self.per_page

        if start_idx >= len(self.keys):
            raise StopIteration

        page_keys = self.keys[start_idx:end_idx]
        page_records = [self.address_book.data[key] for key in page_keys]

        self.current_page += 1

        return page_records


class AddressBook(UserDict):
    """
    Class for storing and managing records.
    Inherits from UserDict and contains logic for searching records within this class
    """
    def __init__(self):
        super().__init__()
        self.load_from_json("address_book.json")

    # Adding records
    def add_record(self, record: Record):
        self.data[record.name.name] = record

    # Search for records by name
    def find(self, name):
        return self.data.get(name, None)

    # Delete records by name
    def delete(self, name):
        if name in self.data:
            self.data.pop(name)
            return f"{name} has been deleted from the AddressBook"
        return f"{name} is not in the AddressBook"

    # Restore the address book from disk
    def load_from_json(self, filename):
        try:
            with open(filename, "r") as file:
                records_data = json.load(file)

                for name, data in records_data.items():
                    record = Record(data["name"])

                    for phone_number in data["phones"]:
                        record.add_phone(phone_number)

                    for email_address in data["emails"]:
                        record.add_email(email_address)

                    if "address" in data:
                        record.address = data["address"]

                    if data["birthday"] != "not set":
                        record.add_birthday(data["birthday"])

                    if "notes" in data:
                        record.notes = data["notes"]

                    self.data[name] = record

        except FileNotFoundError:
            pass

    def filter_contacts_by_birthday(self, days):
        now = datetime.now()

        def is_birthday_soon(contact):
            if not contact.birthday:
                return False

            bd = contact.birthday.birthday.replace(year=now.year)
            if bd < now:
                bd = bd.replace(year=now.year + 1)

            days_to_bdd = (bd.date() - now.date()).days
            return 0 <= days_to_bdd <= days

        return list(filter(is_birthday_soon, self.data.values()))

    # Save the address book to disk
    def save_to_json(self, filename):
        records_data = {name: record.to_dict() for name, record in self.data.items()}
        with open(filename, "w") as file:
            json.dump(records_data, file, indent=3)

    # Performs a search in the address book by the username or phone number.
    # Supports partial search by name or phone number.
    def find_data_in_book(self, search_string):
        found_users = set()

        for record in self.data.values():
            if search_string.lower() in record.name.name.lower():
                found_users.add(record)

            for phone in record.phones:
                if search_string.lower() in phone.value.lower():
                    found_users.add(record)

            for email in record.emails:
                if search_string.lower() in email.value.lower():
                    found_users.add(record)

            if record.address and search_string.lower() in record.address.lower():
                found_users.add(record)

            if record.birthday and search_string.lower() in str(record.birthday).lower():
                found_users.add(record)

        return list(found_users)

# Generation of a random birthdate
def generate_random_birthdate(start_date='1970-01-01', end_date='2000-12-31', date_format='%Y-%m-%d'):
    start_date = datetime.strptime(start_date, date_format)
    end_date = datetime.strptime(end_date, date_format)

    random_days = random.randint(0, (end_date - start_date).days)
    random_birthdate = start_date + timedelta(days=random_days)

    return random_birthdate.strftime(date_format)


if __name__ == "__main__":
    # Creating a new address book
    # If the address_book.json file exists, it will be automatically loaded
    book = AddressBook()

    # Adding a record to the address book with random name, phone number, and birthdate
    user_number = random.randint(100, 999)
    data_record = Record(f'User-{user_number}')
    phone_number = ''.join(map(str, [random.randint(0, 9) for _ in range(10)]))
    data_record.add_phone(phone_number)
    data_record.add_birthday(generate_random_birthdate())
    book.add_record(data_record)

    # Searching in the address book by a partial username
    print("Search by partial username")
    book.find_data_in_book("Jo")
    # Searching in the address book by a partial phone number
    print("Search by partial phone number")
    book.find_data_in_book("098765")

    # Save the address book to a file
    book.save_to_json("address_book.json")

    print("Good bye!")
