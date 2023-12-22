from collections import UserDict
from datetime import datetime, date

class Field: 
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if not self.is_valid(value):
            raise ValueError
        self.__value = value
    
    def is_valid(self, value):
        return True

    def __str__(self):
        return str(self.__value)

class Name(Field): 
    pass
    
class Birthday(Field):
    @Field.value.setter    
    def value(self, birthday):
        try:
            birthday = datetime.strptime(birthday, '%d.%m.%Y').date()
            self.__value = str(birthday)      
        except ValueError:
            raise ValueError('Формат дати повинен бути ДД.ММ.РРРР')
        except TypeError:
            self.__value = None

class Phone(Field):    
    @Field.value.setter
    def value(self, new_phone):
        if new_phone.isdigit() and len(new_phone) == 10:
            self.__value = new_phone
        else:
            raise ValueError('Невірний формат номеру телефону')
        
class Record:
    
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday)
        self.phones = []
        
    def add_phone(self, phone_str): # додавання телефону
        self.phones.append(Phone(phone_str)) 
        return self.phones           

    def find_phone(self, phone_for_find_str): # пошук телефону        
        for phone_obj in self.phones:                        
            if phone_obj.value == phone_for_find_str:
                return phone_obj.value
    
    def edit_phone(self, phone_for_edit_str_old, phone_for_edit_str_new):
        self.remove_phone(phone_for_edit_str_old)
        self.phones.append(Phone(phone_for_edit_str_new))
            
    def remove_phone(self, phone_for_remove_str): # видалення телефону          
        phone_obj = self.find_phone(phone_for_remove_str)       
        
        for phone in self.phones:            
            if phone.value == phone_obj:
                self.phones.remove(phone)  # видалення телефону     

    def day_to_birthday(self):
        today = date.today()       
        if self.birthday.value == None:
            return 'День народження не вказано'
        else:
            birthday = datetime.strptime(self.birthday.value, '%d.%m.%Y').date()
        
        if birthday.month >= today.month:
            birthday = date(today.year, self.birthday.
                            value.month, birthday.day)
        else:
            birthday = date(today.year+1, birthday.month, birthday.day)
            
        day = birthday - today   
        
        if day.days == -1:
            result = 'День народження сьогодні'
        elif day.days == 0:
            result = 'День народження завтра'
        else:
            result = f'Днів до дня народження: {day.days}' 
        return result        

    def __repr__(self): 
        if self.birthday.value == None:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"    
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value}"
        
class AddressBook(UserDict):   
    
    def add_record(self, record_obj):        
        self.data[record_obj.name.value] = record_obj        

    def find(self, record_for_find_str): 
        if record_for_find_str in self.data.keys():
            return self.data[record_for_find_str]
        else:
            return None         

    def delete(self, record_for_del_obj):
        if record_for_del_obj.name.value in self.data.keys():            
            del self.data[record_for_del_obj.name.value]
    
    def iterator(self, n):        
        records = list(self.data.values())       
        for i in range(0, len(self.data), n):
            yield records[i:i+n]        
        
    def __str__(self):
        return '\n'.join(f"{value}" for value in self.data.values())


book = AddressBook()

john_record = Record('John', '21.11.2002')
john_record.add_phone("12345ff67890")
john_record.add_phone("5555555555")
book.add_record(john_record)
olesya_record = Record('Olesya')
olesya_record.add_phone('0961336547')
olesya_record.add_phone('0000000000')
olesya_record.add_phone('2222222222')
book.add_record(olesya_record)
jane_rec = Record('Jane')
jane_rec.add_phone('0931256987')
book.add_record(jane_rec)
a = Record('A')
book.add_record(a)
b = Record('B')
book.add_record(b)
c = Record('C')
book.add_record(c)
d = Record('D')
book.add_record(d)
print(john_record.day_to_birthday())
print(olesya_record.day_to_birthday())
print(book)

book.delete(jane_rec)
print(book.find('John'))
print(olesya_record)
print(olesya_record)
olesya_record.remove_phone('2222222222')
print(olesya_record.find_phone('0000000000'))
olesya_record.edit_phone('0000000000', '1111111111')
print(olesya_record)
a = book.iterator(2)
print(next(a))
print(next(a))
print(next(a))
print(next(a))
print(next(a))