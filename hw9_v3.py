phone_book = {} # записна книга (словнк)

def input_error(func):
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
def add_func(name, num):
    if name not in phone_book.keys():
        phone_book[name] = num
        return f'Створено контакт {name} із номером {num}'
    else:
        return 'Такий контакт вже створено'  
    
@input_error
def change_func(name, num):
        if name in phone_book.keys():
            phone_book[name] = num
            return f'Номер {name} змінено на {num}'
        else:
            return 'Такого контакту не існує'
        
@input_error
def show_func(name):
    if name == 'all':
        return phone_book
    elif name not in phone_book.keys():
        return 'Такого контакту не існує'
    else:
        return f'{name} номер = {phone_book[name]}'

@input_error
def bye_func(a=None):
    return 'Бувай!'

@input_error
def hello_func():
    return 'Привіт, чим можу допомогти?'
 
@input_error        
def pars_input(strng):    
    split_input = strng.split()
    handler_name = split_input[0]
    args = split_input[1:]    
    return  handler_name, args  


cmd_with_args = {'add': add_func,
              'change': change_func,
              'show': show_func,
              'phone': show_func,
              'exit': bye_func, 'close': bye_func, 'good': bye_func,
              'hello': hello_func}  

@input_error
def start_cmd(handler_name, args):
    res = cmd_with_args[handler_name](*args)
    return res

@input_error
def main():    
    
    while True:        
            
        user_input = input('Чекаю команду: ').lower()
        result_of_pars = pars_input(user_input)                  
        
        if type(result_of_pars) == str:
            print(result_of_pars)
            continue
        res = start_cmd(*result_of_pars)
        print(res)
        if res == 'Бувай!':
            break          
        

if __name__ == '__main__':    
    main()