from collections import UserDict
from datetime import datetime, date
 
 
class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value
 
    @property
    def value(self):         
        return self.__value
 
    @value.setter
    def value(self, value):
        self.__value = value
 
    def __str__(self):
        return str(self.__value)
 
class Name(Field):
    pass
 
 
class Birthday(Field):
    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self, birthday):
        try:
            datetime.strptime(birthday, '%d.%m.%Y').date() # якщо переданий рядок перетворюється у формат дати без помилок то передаємо його далі (валідація пройшла)
            self.__value = birthday
        except ValueError:
            raise ValueError('Формат дати повинен бути ДД.ММ.РРРР')
 
 
class Phone(Field):
    @property
    def value(self):
        return self.__value
    @value.setter
    #@Field.value.setter не працює
    def value(self, new_phone):
        if new_phone.isdigit() and len(new_phone) == 10:
            self.__value = new_phone
        else:
            raise ValueError('Невірний формат номеру телефону')
 
 
class Record:
 
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday) if birthday else birthday # якщо др було пепедано, то в клас Birthday передається рядок для перевірки, якщо не було передачі , то self.birthday = None
        self.phones = []
 
    def add_phone(self, phone_str):  # додавання телефону
        self.phones.append(Phone(phone_str))
        return self.phones
 
    def find_phone(self, phone_for_find_str):  # пошук телефону
        for phone_obj in self.phones:
            if phone_obj.value == phone_for_find_str:
                return phone_obj.value
 
    def edit_phone(self, phone_for_edit_str_old, phone_for_edit_str_new):
        self.remove_phone(phone_for_edit_str_old)
        self.phones.append(Phone(phone_for_edit_str_new))
 
    def remove_phone(self, phone_for_remove_str):  # видалення телефону
        phone_obj = self.find_phone(phone_for_remove_str)
 
        for phone in self.phones:
            if phone.value == phone_obj:
                self.phones.remove(phone)  # видалення телефону
 
    def day_to_birthday(self):
        today = date.today()
        if not self.birthday:
            return 'День народження не вказано'
        else:
            birthday = datetime.strptime(self.birthday.value, '%d.%m.%Y').date()
 
            if birthday.month > today.month:
                birthday = date(today.year, birthday.month, birthday.day)
            elif birthday.month == today.month:
                if birthday.day < today.day:
                    birthday = date(today.year+1, birthday.month, birthday.day)
                else:
                    birthday = date(today.year, birthday.month, birthday.day)
            else:
                birthday = date(today.year+1, birthday.month, birthday.day)
 
            day = birthday - today
 
            if day.days == 0:
                result = 'День народження сьогодні'
            elif day.days == 1:
               result = 'День народження завтра'
            else:
                result = f'Днів до дня народження: {day.days}'
            return result
 
    def __repr__(self):        
        if self.birthday == None:
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
            yield records[i:i + n]
 
    def __str__(self):
        return '\n'.join(f"{value}" for value in self.data.values())
 