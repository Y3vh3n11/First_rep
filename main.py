from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
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
        print(self.name)      


    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        # print(self.phones)
        return self.phones
        

    def remove_phone(self):
        pass

    def edit_phone(self):
        pass

    def find_phone(self):
        pass


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record_obj):        
        self.data[record_obj.name.value] = record_obj
        # додає запис до self.data
        

    def find(self):
        # шукає за ім'ям 
        pass

    def delete(self):
        # видаляє за ім'ям
        pass

    def __str__(self):
        return f"Contact name: "

book = AddressBook()
print(book)
john_record = Record('John')
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
# print(john_record.__str__())
book.add_record(john_record)
print(book.__str__())