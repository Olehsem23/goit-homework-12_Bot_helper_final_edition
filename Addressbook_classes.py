from collections import UserDict
from datetime import datetime
import pickle
import re


class Field:
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value
       
    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)
        

class Name(Field):
    ...


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not re.match(r'^\+380\d{9}$', value):
            print('Wrong format. Phone number should be in the format +380XXXXXXXXX.')
            raise ValueError
        self.__value = value


class Birthday(Field):
    @property
    def value(self):
        return self.__value
        
    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, '%d.%m.%Y').date()
        except ValueError:
            print('Wrong format. Enter birthday in format dd.mm.YYYY')
            raise ValueError
        
    def __str__(self):
        return self.value.strftime('%d-%m-%Y')


class Email(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if '@' not in value and '.' not in value:
            print("Wrong format. E-mail should have '@' and '.' in its string")
            raise ValueError
        self.__value = value


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None, email: Email = None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday
        self.email = email
    
    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} add to contact {self.name}"
        return f"phone: {phone} is already registered for user {self.name}"
    
    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday
        return f'Birthday for user {self.name} was added successfully'
    
    def days_to_birthday(self):  # Функція повертає кількість днів до дня народження користувача.
        if not self.birthday:
            return f'No data for birthday of user {self.name}'
        today = datetime.now().date()
        bd_current_year = self.birthday.value.replace(year=today.year)
        bd_next_year = self.birthday.value.replace(year=today.year + 1)
        diff_years = today.year - self.birthday.value.year
        if (bd_current_year - today).days == 0:
            return f"Today {self.name} celebrate {diff_years} birthday. Don't forget to buy a gift."
        elif (bd_current_year - today).days > 0:
            diff_days = (bd_current_year - today).days
            return f"There are {diff_days} days left until the {self.name}'s {diff_years} birthday"
        diff_days = (bd_next_year - today).days
        return f"There are {diff_days} days left until the {self.name}'s {diff_years + 1} birthday"
    
    def add_email(self, email: Email):
        self.email = email
        return f'E-mail for user {self.name} was added successfully'
    
    def change_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
                return f"old phone {old_phone} was changed to new: {new_phone}"
        return f"{old_phone} not present in phones of contact {self.name}"
    
    def __str__(self) -> str:
        return f"User: {self.name} | phones: {', '.join(str(p) for p in self.phones)} | birthday: {self.birthday} " \
               f"| email: {self.email}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record.name} was added successfully"
    
    def iterator(self, n=10):
        print(n)
        result = ""
        count = 0
        for rec in self.data.values():
            result += str(rec) + "\n"
            count += 1
            if count >= n:
                yield result
                count = 0
                result = ""
        if result:
            yield result
    
    def save_to_file(self, filename):
        with open(filename, mode="wb") as file:
            pickle.dump(self.data, file)
            print("Address book save.")

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.data = pickle.load(f)
                print("Address book loaded.")
        except (FileNotFoundError, pickle.UnpicklingError):
            with open(filename, 'wb') as f:
                self.data = {}
                pickle.dump(self.data, f)

    def search_match(self, match):
        found_match = []
        for item in self.data.values():
            if match in str(item):
                found_match.append(str(item))
        if len(found_match) == 0:
            return f"No matches found for '{match}' in whole addressbook"
        else:
            for el in found_match:
                print(el)
            return f"We found matches for '{match}' in {len(found_match)} contacts in whole addressbook" 
    
    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())
