import pickle
from collections import UserDict
from datetime import datetime,date

class Field:
    def __init__(self, value):
        self._value = value
    
    def __str__(self) -> str:
        return str(self._value)
    
    @property
    def value_getter(self):
        return self._value
    
    @value_getter.setter
    def value_setter(self,value):
        self._value = value

class Name(Field):
    pass

class Phone(Field):
  
    def __init__(self,_value):
        super().__init__(_value)
        if not self._value.startswith('+'):
            raise ValueError('Phone must begin with "+"')
        if len(self._value) < 13:
            raise ValueError('Phone must have 13 characters')
        

class Birthday(Field):
    def __init__(self, _value):
        super().__init__(_value)
        if not isinstance(_value,str):
            raise ValueError('Must be a string')
        try:
            datetime.strptime(self._value,'%d-%m-%Y')
        except:
            raise ValueError('Incorrect format of birthday')
        
    
class Record:
    def __init__(self, name: Name, phone: Phone,birthday: Birthday = None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        if phone:
            self.phones.append(phone)
    
    def add(self, phone: Phone):
        self.phones.append(phone)
    
    def delete_phone(self, phone: Phone):
        for i in range(len(self.phones)):
            if self.phones[i] == phone:
                self.phones[i] = ''

    def edit_phone(self,old_phone: Phone, new_phone:Phone):
        for i, p in enumerate(self.phones):
            if old_phone._value == p._value:
                self.phones[i] = new_phone
                return f'Phone {old_phone} change on {new_phone}'
        return f'Record dont have phone {old_phone}'
    
    def days_to_birthday(self):
        today = datetime.now().date()
        birthday_in_year =datetime.strptime(self.birthday._value,'%d-%m-%Y').date() 
        birthday_in_year = birthday_in_year.replace(year=today.year)
        if birthday_in_year < today:
            birthday_in_year = birthday_in_year.replace(year=today.year + 1)
        days_left = (birthday_in_year - today).days
        return days_left
    
    def __str__(self) -> str:
        return str(f'{self.name}: {", ".join(str(p) for p in self.phones)}, {self.birthday}')
 
class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name._value] = record
    
    def __str__(self) -> str:
        return '\n'.join([str(rec) for rec in self.data.values()])

    def find_phone(self, name:Name):
        if name in self.data:
            return self.data[name]
        else:
            return f'There is no contact with name {name}'
    
    def iterator(self,page = 3):
        start = 0
        while start < len(self.data):
            res = list(self.data.values())[start:start+page]
            yield res
            start+=page
    
    def save_record_to_file(self,file_name):
        with open(file_name,'wb') as f:
            pickle.dump(self.data,f)
    
    @staticmethod
    def load_record_from_file(file_name):
        with open(file_name,'rb') as f:
           rec_copy = pickle.load(f)
           return rec_copy
        
    def search_record(self,specifications:str):
        records_with_specs = []
        for rec in self.data.values():
            if specifications in rec.name._value or specifications in rec.phones:
                records_with_specs.append(rec)
        return records_with_specs


