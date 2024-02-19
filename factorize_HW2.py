import logging
import time
from multiprocessing import Pool, cpu_count

def decor(func):
    def wrapper(*args, **kwargs):
        start = time.time()        
        res = func(*args, **kwargs)
        end = time.time()
        result_time = end - start
        logging.debug(f'Time = {result_time}\n')
        return res
    return wrapper


def find_factorize(number):
    factorize_list = []    

    for i in range(1, number+1):
        if not number % i:
            factorize_list.append(i)

    return factorize_list
    
@decor
def factorize_synchronous(*num):    
    logging.debug('factorize_synchronous:')
    return map(find_factorize, num)


@decor
def factorize_multiprocessing(*num):
    logging.debug('factorize_multiprocessing:')
    with Pool(processes=cpu_count()) as pool:            
        return pool.map(find_factorize, num)



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    a, b, c, d  = factorize_multiprocessing(128, 255, 99999, 10651060)
    a, b, c, d  = factorize_synchronous(128, 255, 99999, 10651060)
    
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
