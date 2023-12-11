phone_book = {}
error = ''
def input_error(func):
    def wrapper():
        global error
        while True:        
            try:
                res = func()                
            except KeyError:
                error = 'Команда не знайдена'                 
            except TypeError:
                error = 'Невірні параметри команди'                
            except IndexError:
                error = 'Введено невірні дані'                
            else:
                return res           
    return wrapper

def add_func(name, num):
    if name not in phone_book.keys():
        phone_book[name] = num
        return f'Створено контакт {name} із номером {num}'
    else:
        return 'такий контакт вже створено '  
    

def change_func(name, num):
        if name in phone_book.keys():
            phone_book[name] = num
            return f'Номер {name} змінено на {num}'
        else:
            return 'Такого контакту не існує'
        

def show_func(name):
    if name == 'all':
        return phone_book
    elif name not in phone_book.keys():
        return 'Такого контакту не існує'
    else:
        return f'{name} номер = {phone_book[name]}'
        

@input_error
def main():
    global error
    cmd_with_args = {'add': add_func,
              'change': change_func,
              'show': show_func,
              'phone': show_func}
    
    while True:
        if error :
            print(error)
            error = ''        
        user_input = input('Чекаю команду: ').lower()
        split_input = user_input.split()
        
        if len(split_input) > 1 and split_input[1] in ['bye']:
            handler_name = ' '.join(split_input[:2])
        else:
            handler_name = split_input[0]
            args = split_input[1:]            
        
        if handler_name in ['exit', 'close', 'good bye']:            
            return print('Бувай!')          
        elif handler_name == 'hello':
            print('Привіт, чим можу допомогти?')
            
        elif handler_name in cmd_with_args:
            res = cmd_with_args[handler_name](*args)
            print(res)
        else:
            raise KeyError
        
        
            
    
    
if __name__ == '__main__':
    main()