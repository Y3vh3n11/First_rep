from collections import UserDict

class Field: # батьківський клас
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field): # 
    pass
    

class Phone(Field): # 
    
    def __init__(self, phone):       # валідація номера, 10 цифр
        if phone.isdigit() and len(phone) == 10:
            self.value = phone
        else:
            raise ValueError
    
   

class Record:
    
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        # print(self.name)      


    def add_phone(self, phone_str): # додавання телефону
        self.phones.append(Phone(phone_str)) 
        return self.phones           

    def find_phone(self, phone_for_find_str): # пошук телефону
        for phone_obj in self.phones:            
            if str(phone_obj) == phone_for_find_str:
                return phone_obj
    
    def edit_phone(self, phone_for_edit_str_old, phone_for_edit_str_new):
        self.remove_phone(phone_for_edit_str_old)
        self.phones.append(Phone(phone_for_edit_str_new))
            
    def remove_phone(self, phone_for_remove_str): # видалення телефону          
        phone_obj = self.find_phone(phone_for_remove_str)        
        self.phones.remove(phone_obj)  # видалення телефону     


    def __str__(self): 
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
   
    def add_record(self, record_obj):        
        self.data[record_obj.name.value] = record_obj
        

    def find(self, record_for_find_str): 
        if record_for_find_str in self.data.keys():
            return self.data[record_for_find_str]
        else:
            return None 
        

    def delete(self, record_for_del_str):         
        if record_for_del_str in self.data.keys():
            del self.data[record_for_del_str]
                    
    def __str__(self):
        return '\n'.join(f"{value}" for value in self.data.values())
