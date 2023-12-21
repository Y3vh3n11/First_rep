from collections import UserDict
from datetime import datetime, date

class Field: # батьківський клас
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self._value)

class Name(Field): 
    pass
    

class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, birthday):
        try:
            birthday = datetime.strptime(birthday, '%d.%m.%Y').date()
            self.__value = birthday            
        except ValueError:
            raise ValueError('Формат дати повинен бути ДД.ММ.РРРР')
        except TypeError:
            self.__value = None

class Phone(Field): 
    @property
    def value(self):
        return self.__value

    @value.setter
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
        if self.birthday.value.month >= today.month:
            birthday = date(today.year, self.birthday.value.month, self.birthday.value.day)
        else:
            birthday = date(today.year+1, self.birthday.value.month, self.birthday.value.day)
            
        day = birthday - today   
        
        if day.days == -1:
            result = 'День народження сьогодні'
        elif day.days == 0:
            result = 'День народження завтра'
        else:
            result = f'Днів до дня народження: {day.days}' 
        return result        

    def __str__(self): 
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
        try:
            step = 0
            full_len = 0
            result = ''
            for val in self.data.values():
                result += f'{val}\n'
                step += 1
                full_len +=1
                if full_len >= len(self.data):
                    yield result
                    result = ''
                elif step >= n:
                    yield result
                    result = ''                    
                    step = 0
            raise StopIteration           
        
        except StopIteration:
            return 'Книга закінчилася'        

    def __str__(self):
        return '\n'.join(f"{value}" for value in self.data.values())
