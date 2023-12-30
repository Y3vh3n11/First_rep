from collections import UserDict
from datetime import datetime, date
import json
 
 
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
    def __repr__(self):
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
    def __str__(self):
        return str(self.__value)
 
 
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
    def __str__(self):
        return str(self.__value)
 
 
class Record:
 
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday) if birthday != None else birthday # якщо др було пепедано, то в клас Birthday передається рядок для перевірки, якщо не було передачі , то self.birthday = None
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
    
    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str) if birthday_str != None else None

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
        
    def find_new(self, find_str: str):
        result = []
        for i in self.data.values():
            str_correction = str(i).split()
            str_correction.remove('Contact')
            str_correction.remove('name:')
            str_correction.remove('phones:')
            if 'birthday:' in str(i):
                str_correction.remove('birthday:')
            str_correction = ' '.join(str_correction)
            if find_str.lower() in str_correction.lower():
                result.append(i)
        return result
 
    def delete(self, record_for_del_obj):
        if record_for_del_obj.name.value in self.data.keys():
            del self.data[record_for_del_obj.name.value]
 
    def iterator(self, n):
        records = list(self.data.values())
        for i in range(0, len(self.data), n):
            yield records[i:i + n]

    def write_to_file(self): # збереження даних у файл
        val = {}
        for key, values in self.data.items():
            val[key] = {
                'name' : str(values.name),
                'phones': [str(phone) for phone in values.phones],
                'birthday': str(values.birthday if values.birthday else '')
            }               
        
        with open('AddressBook.json', 'w') as file:
            json.dump(val, file)

    def load_from_file(self): # завантаження даних із файлу
        with open('AddressBook.json', 'r') as file:
            load_book = json.load(file)                       
            for key, values in load_book.items():                
                record = Record(name=str(values['name'].lower()), birthday=values['birthday'] if values['birthday'] else None)
                if values['phones']:
                    for phone in values['phones']:
                        record.add_phone(phone)
                phone_book.add_record(record)

    def __str__(self):
        return '\n'.join(f"{value}" for value in self.data.values())



def input_error(func):                                                  # докоратор обробки помилок
    def wrapper(*args, **kwargs):        
        while True:        
            try:
                res = func(*args, **kwargs)          
            except KeyError:
                return 'Команда не знайдена'                 
            except TypeError:
                return 'Невірні параметри команди'                
            except IndexError:
                return 'Введено невірні дані'                
            else:
                return res           
    return wrapper

@input_error
def add_func(name, num, birthday=None):                                                # функція додавання контактів
    if name not in str(phone_book.keys()):
        record = Record(name, birthday)
        record.add_phone(num)
        phone_book.add_record(record)
        return f'Створено контакт {name} із номером {num}'
    else:
        return 'Такий контакт вже створено'  
    
@input_error
def change_func(name, num1, num2):                                             # функція зміни контактів
        if name in str(phone_book.keys()):
            phone_book[name].edit_phone(num1, num2)
            return f'Номер {name} змінено з {num1} на {num2}'
        else:
            return 'Такого контакту не існує'
        
@input_error
def show_all_func():                                                    # функція відображення всієї книги
    # phone_book.__str__()
    return phone_book
    
@input_error
def phone_func(name: str):                                                   # функція відображення одного контакту
    if name not in str(phone_book.keys()):
        return 'Такого контакту не існує'
    else:
        return f'{phone_book[name]}'
    
    
@input_error
def bye_func(): 
    phone_book.write_to_file()
    return 'Бувай!'

@input_error
def hello_func():
    return 'Привіт, чим можу допомогти?'

@input_error
def day_to_birthday_func(name):                                         # днів до дня народження
    return phone_book[name].day_to_birthday()

@input_error
def add_phone_func(name, phone):
    phone_book[name].add_phone(phone)
    return f'Користувачу {name} додано телефон {phone}'

@input_error
def add_birthday_func(name, birthday):
    phone_book[name].add_birthday(birthday)
    return f'Користувачеві {name} додано день народження {birthday}'


@input_error
def find_func(find_str):
    return phone_book.find_new(find_str)


@input_error        
def pars_input(strng):                                                  # розбиття введених даних на команду та аргументи
    if strng == 'show all':
        handler_name = 'show all'
        args = tuple()        
    elif strng == 'good bye':
        handler_name = 'good bye'
        args = tuple()
    else:
        split_input = strng.split()
        handler_name = split_input[0]
        args = split_input[1:]    
    return  handler_name, args  

# словник команд 
cmd_with_args = {'add': add_func,               # додати користувача
              'change': change_func,            # змінити номер телефону
              'show all': show_all_func,        # відобразити всю книгу
              'phone': phone_func,              # відобразити конкретного користувача
              'exit': bye_func, 'close': bye_func, 'good bye': bye_func,    # завершити роботу та зберегти дані
              'hello': hello_func,              # привітатися
              'day_to_birthday': day_to_birthday_func,  # днів до дня народження
              'add_phone': add_phone_func,              # додати користувачу телефон
              'add_birthday': add_birthday_func,        # додати користувачу день народження 
              'find': find_func                         # пошук інформації по рядку
              }  

@input_error
def start_cmd(handler_name, args):                                      # виклик команди із списку
    if args:
        res = cmd_with_args[handler_name](*args)
    else:
        res = cmd_with_args[handler_name]()
    return res

@input_error
def main():    
    try:
        phone_book.load_from_file()
    except FileNotFoundError:
        pass
    while True:        
            
        user_input = input('Чекаю команду: ').lower()
        result_of_pars = pars_input(user_input)                  # результат обробки введених даних
        
        if type(result_of_pars) == str and result_of_pars not in ['show all', 'good bye']:                                 # друк помилки якщо вона виникла
            print(result_of_pars)
            continue
        res = start_cmd(*result_of_pars)    
        print(res)                                                      # друк результату виконання команди із списку
        if res == 'Бувай!':
            break          
        

if __name__ == '__main__':    
    phone_book = AddressBook()    
    main()
   