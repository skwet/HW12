from class_bot import Field,AddressBook,Record,Name,Phone,Birthday

def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError:
            return 'Not enough data'
        except KeyError:
            return 'Are you sure that you added this contact?.Try again'
        except ValueError:
            return 'Impossible to add or change this number'
    return wrapper

address_book = AddressBook()

def hello(*args):
    return 'What`s up?How can I help you?'

@input_error
def add(*args):
    input_split = args[0].split()
    name = Name(input_split[0])
    phone = Phone(input_split[1])
    birthday = Birthday(input_split[2])
    if not birthday:
        rec = Record(name,phone)
    rec = Record(name,phone,birthday)
    address_book.add_record(rec)
    return f'U added {name} with phone {phone} and birthday {birthday}'

@input_error
def change(*args):
    input_split = args[0].split()
    name = Name(input_split[0])
    old_phone = Phone(input_split[1])
    new_phone= Phone(input_split[2])
    rec = Record(name,old_phone)
    rec.edit_phone(old_phone,new_phone)
    address_book.add_record(rec)
    if new_phone in rec.phones:
        return 'Phone has been changed'
    raise ValueError

@input_error
def search_contact(*args):
    input_split = args[0].split()
    spec = input_split[0]

    find_spec = address_book.search_record(spec)
    return find_spec
@input_error
def delete_phone(*args):
    input_split = args[0].split()
    name = input_split[0]
    phone = input_split[1]
    rec = Record(name,phone)
    rec.delete_phone(phone)
    if phone not in rec.phones:
        return 'Phone has been removed'   
    raise ValueError
    
@input_error
def phones(*args):
    input_split = args[0].split()
    name = input_split[0]
    phone_number = address_book[name]
    if not name:
        raise KeyError
    return f'{phone_number}'

def show_all(*args):
    input_split = args[0].split()
    page = int(input_split[0])
    gen_obj = address_book.iterator(page)
    for i in gen_obj:
        return i.copy()

    
def bb(*args):
    return 'Good bye'

commands = {hello:'hello',
            add:'add',
            change:'change',  
            phones:'phone',
            show_all:'show all',
            delete_phone:'delete',
            search_contact:'search',
            bb:'bye'}

def handler(text):
    for command,kword in commands.items():
        if text.startswith(kword):
            return command,text.replace(kword,'').strip()
    return None

def main():
    while True:
        user_input = input('>>>')
        command,data =handler(user_input)
        print(command(data))
        if command == bb:
            break

if __name__ == '__main__':
    main()