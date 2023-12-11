phone_book = {}
def input_error(func):
    def wrapper():
        while True:        
            try:
                res = func()
                if res == 'Бувай!':
                    print(res)                    
                    break
            except KeyError:
                print( 'Команда не знайдена')
            except TypeError:
                print( 'Невірні параметри команди')
            except IndexError:
                print( 'Введено невірні дані')
            else:
                print(res)            
    return wrapper

def add_func(name, num):
    if name not in phone_book.keys():
        phone_book[name] = num
        return f'Створено контакт {name} із номером {num}'
    else:
        return 'Такий контакт вже створено '  
    

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
        
def good_bye_func():
    return 'Бувай!'
def hello_func():
    return 'Привіт, чим можу допомогти?'    

@input_error
def main():
    cmd_with_args = {'add': add_func,
              'change': change_func,
              'show': show_func,
              'phone': show_func}
    cmd_without_args = {'exit': good_bye_func, 'close': good_bye_func, 'good bye': good_bye_func,              
              'hello': hello_func}

    while True:
        user_input = input('Чекаю команду: ').lower()
        split_input = user_input.split()
        if len(split_input) > 1 and split_input[1] in ['bye']:
            handler_name = ' '.join(split_input[:2])
        else:
            handler_name = split_input[0]
            args = split_input[1:]            
        
        if handler_name in cmd_without_args:            
            res = cmd_without_args[handler_name]()
            if res == 'Бувай!':
                return res
            else:
                print(res)
            
        elif handler_name in cmd_with_args:
            res = cmd_with_args[handler_name](*args)
            print(res)
        else:
            raise KeyError
        
        
            
    
    
if __name__ == '__main__':
    main()