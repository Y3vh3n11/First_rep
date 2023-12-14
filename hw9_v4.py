phone_book = {}                                                         # записна книга (словнк)

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
def add_func(name, num):                                                # функція додавання контактів
    if name not in phone_book.keys():
        phone_book[name] = num
        return f'Створено контакт {name} із номером {num}'
    else:
        return 'Такий контакт вже створено'  
    
@input_error
def change_func(name, num):                                             # функція зміни контактів
        if name in phone_book.keys():
            phone_book[name] = num
            return f'Номер {name} змінено на {num}'
        else:
            return 'Такого контакту не існує'
        
@input_error
def show_all_func():                                                    # функція відображення всієї книги
    return phone_book
    
@input_error
def phone_func(name):                                                   # функція відображення одного контакту
    if name not in phone_book.keys():
        return 'Такого контакту не існує'
    else:
        return f'{name} номер = {phone_book[name]}'
    
@input_error
def bye_func(): 
    return 'Бувай!'

@input_error
def hello_func():
    return 'Привіт, чим можу допомогти?'
 
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
cmd_with_args = {'add': add_func,  
              'change': change_func,
              'show all': show_all_func,
              'phone': phone_func,
              'exit': bye_func, 'close': bye_func, 'good bye': bye_func,
              'hello': hello_func}  

@input_error
def start_cmd(handler_name, args):                                      # виклик команди із списку
    if args:
        res = cmd_with_args[handler_name](*args)
    else:
        res = cmd_with_args[handler_name]()
    return res

@input_error
def main():    
    
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
    main()