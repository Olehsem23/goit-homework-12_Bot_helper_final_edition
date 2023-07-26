from Addressbook_classes import AddressBook, Name, Phone, Birthday, Email, Record


address_book = AddressBook()
filename = 'addressbook.bin'  # Шлях до файлу з адресною книгою.


def input_error(func):  # Декоратор. Обробляє помилки при вводі.
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return f"No user with name {args[0]}"
        except ValueError as e:
            return e
        except IndexError:
            return 'Enter user name and phone'
        except AttributeError:
            return f"User {args[0]} doesn't exist. First create a record about this user."
    return wrapper


@input_error
def hello_user():  # Відповідь на команду 'Hello'
    return "Hello! How can I help you?"


@input_error
def add_user_command(*args):  # Додаємо користувача і номер телефону.
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)
    rec = Record(name, phone)
    return address_book.add_record(rec)


@input_error
def add_birthday_command(*args):  # додаємо дату народження для користувача
    name = Name(args[0])
    birthday = Birthday(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_birthday(birthday)
    rec = Record(name)
    return address_book.add_record(rec)


@input_error
def days_to_birthday(*args):  # Повертає кількість днів до дня народження користувача.
    name = Name(args[0])
    rec: Record = address_book.get(str(name))
    return rec.days_to_birthday()


@input_error
def add_email_command(*args):  # додаємо e-mail для користувача
    name = Name(args[0])
    email = Email(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_email(email)
    rec = Record(name)
    return address_book.add_record(rec)


@input_error
def change_command(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"No contact {name} in address book"


@input_error
def show_all_command():  # Видрукувати весь список імен і телефонів зі словника address_book.
    if len(address_book) == 0:  # Якщо словник порожній.
        return 'Address book is now empty. Please add some users'
    else:
        print(f'There are {len(address_book)} users in address book')
        return address_book


@input_error
def show_pages_command():  # Видрукувати весь список імен і телефонів зі словника address_book.
    if len(address_book) == 0:  # Якщо словник порожній.
        return 'Address book is now empty. Please add some users'
    else:
        print(f'There are {len(address_book)} users in address book')
        n = int(input('Enter integer number of contacts shown per page: '))
        for rec in address_book.iterator(n):
            print(rec)
        return 'Addressbook was printed.'


@input_error
def phone_command(*args):  # Пошук телефона вибраного користувача.
    return address_book[args[0]]


@input_error
def delete_user_command(*args):  # Видаляє запис про користувача з addressbook.
    name = Name(args[0])
    rec: Record = address_book.get(str(name))
    if rec:
        confirm = input(f'Do you really want to delete user {args[0]}? Type Y/N: ')
        if confirm.lower() != 'y':
            return 'Continue work with addressbook.'
        address_book.pop(args[0])
        return f'User {args[0]} was deleted from addressbook.'
    else:
        return f'No user with name {name}'


@input_error
def search_command(*args):  # Шукає задану послідовність символів у addressbook.
    match = args[0]
    if len(match) <= 2:
        return 'Search is too short. Enter at least 2 symbols.'
    return address_book.search_match(match)


def helper():
    res = ''
    for value in COMMANDS.values():
        res += f'{value[0]}\n'
    return 'Bot has such commands: \n' + res


def exit_command():  # Вихід з програми.
    address_book.save_to_file(filename)
    return 'Bye. Have a nice day. See you next time.'


def unknown_command():  # Коли вводимо невідому команду.
    return 'Unknown command. Try again'


# COMMANDS - словник, де ключі - це функції, які викликаються при наборі відповідної команди з кортежу можливих команд.
COMMANDS = {
    hello_user: ('hello', 'hi', 'aloha', 'привіт'),
    show_all_command: ('show all', 'all phones', 'addressbook', 'phonebook'),
    show_pages_command: ('show pages', 'show by pages'),
    add_birthday_command: ('add birthday', 'birthday'),
    days_to_birthday: ('days to birthday', 'days to bd'),
    add_email_command: ('add email',),
    add_user_command: ('new user', 'add', '+'),
    delete_user_command: ('delete user', 'remove', 'delete'),
    change_command: ('change phone for', 'change', 'зміни', 'замінити'),
    phone_command: ('show number', 'phone', 'number', 'show'),
    search_command: ('search', 'find', 'match'),
    exit_command: ('exit', 'bye', 'end', 'close', 'goodbye', 'учше'),
    helper: ('help', 'рудз')
}


def parser(text: str):  # Парсер команд
    for cmd, keywords in COMMANDS.items():
        for kwd in keywords:
            if text.lower().startswith(kwd):
                # print(cmd)
                data = text[len(kwd):].strip().split()
                # print(data)
                return cmd, data 
    return unknown_command, []


def main():
    address_book.load_from_file(filename)
    while True:
        user_input = input('Enter your command and args: ')
        
        cmd, data = parser(user_input)
        
        result = cmd(*data)
        
        print(result)
        
        if cmd == exit_command:  # Вихід з бота
            break


if __name__ == "__main__":  # Точка входження
    main()
