from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
    pass
    

class Phone(Field):
    
    def __init__(self, phone):        
        if phone.isdigit() and len(phone) == 10:
            self.value = phone
        else:
            raise ValueError
   

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self):
        pass

    def remove_phone(self):
        pass

    def edit_phone(self):
        pass

    def find_phone(self):
        pass


    # реалізація класу

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    # реалізація класу
    def add_record(self, name):
        self.data['name'] = name
        # додає запис до self.data
        pass

    def find(self):
        # шукає за ім'ям 
        pass

    def delete(self):
        # видаляє за ім'ям
        pass

