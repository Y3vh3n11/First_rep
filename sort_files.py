import sys
from pathlib import Path
import re
import shutil
import os


dict_of_file = dict()       # словник категорій. Ключі категорії, значення списки файлів по категоріям
folders = ['Images', 'Documents', 'Audio', 'Video', 'Archives'] # папки для файлів
list_of_bad_folders = list()                                    # список папок для видалення 
def main():
    try:
        folder = Path(sys.argv[1])
        if len(sys.argv) > 2:                                   # Перевірка кількості аргументів
            raise IndexError
        elif not folder.exists():                               # Перевірка чи існує папка           
            raise FileNotFoundError        
    
    except FileNotFoundError:
        print('\nПомилка: папка не знайдена\n')
        exit(1)
    except IndexError:
        print('\nПомилка: необхідно вказати шлях до папки в якості одного аргументу\n')
        exit(1)
    else:
        print(f"\nПривіт сортуємо файли у папці {sys.argv[1]}\n")
        
    folder_absolute = folder.absolute()
    a = 0
    for i in folders:                       # Створення абсолютних шляхів для папок категорій
        folders[a] = str(folder_absolute.joinpath(i))
        a += 1
    
    for i in folders:                       # Перевірка на наявність папок категорій та створення якщо відсутні
        if not os.path.exists(i):
            os.mkdir(i)
            print(f'{i} папку створено')
                

    find_files(folder)                      # пошук файлів у заданій папці
    
    print('\n|{:-^50}|'.format('АРХІВИ'), '\n', '*'*50)                 #
    for i in dict_of_file['archives']:                                  #
        print('|{:-^50}|'.format(i))                                    #
    print('\n|{:-^50}|'.format('ЗОБРАЖЕННЯ'), '\n', '*'*50)             #
    for i in dict_of_file['images']:                                    #   
        print('|{:-^50}|'.format(i))                                    #
    print('\n|{:-^50}|'.format('ЗВУК'), '\n', '*'*50)                   #   
    for i in dict_of_file['audio']:                                     #   
        print('|{:-^50}|'.format(i))                                    #
    print('\n|{:-^50}|'.format('ДОКУМЕНТИ'), '\n', '*'*50)              # відображення інформації 
    for i in dict_of_file['documents']:                                 #
        print('|{:-^50}|'.format(i))                                    #
    print('\n|{:-^50}|'.format('ВІДОМІ РОЗШИРЕННЯ'), '\n', '*'*50)      #
    for i in dict_of_file['set_of_suffix']:                             #
        print('|{:-^50}|'.format(i))                                    #
    print('\n|{:-^50}|'.format('НЕВІДОМІ РОЗШИРЕННЯ'), '\n', '*'*50)    #
    for i in dict_of_file['set_of_unk_suffix']:                         #
        print('|{:-^50}|'.format(i))                                    #
        
    list_of_bad_folders.reverse()                   
    for i in list_of_bad_folders:                                       # Видалення пустих папок
        print(f'Видаляємо пусту папку {i}')
        os.rmdir(i)


def find_files(path):
    global dict_of_file
    global folders
    global list_of_bad_folders
    set_of_suffix = set()
    set_of_unk_suffix = set()
    list_of_img = list()
    list_of_doc = list()
    list_of_audio = list()
    list_of_vid = list()
    list_of_achives = list()
    list_of_unknown = list()   

    for files in path.iterdir():
        
        if files.is_file():            
            if files.suffix.upper() in ('.JPEG', '.PNG', '.JPG', '.SVG'):
                norm_name = normalize(files.name)       # перейменування файлу
                list_of_img.append(norm_name)           # додавання в список категорії
                set_of_suffix.add(files.suffix)         # додавання в список розширень
                shutil.move(files.absolute(), '\\'.join([folders[0], norm_name]))     # переміщення файлу           
            elif files.suffix.upper() in  ('.AVI', '.MP4', '.MOV', '.MKV'):
                norm_name = normalize(files.name)
                list_of_vid.append(norm_name)
                set_of_suffix.add(files.suffix)
                shutil.move(files.absolute(), '\\'.join([folders[3], norm_name]))
            elif files.suffix.upper() in ('.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'):
                norm_name = normalize(files.name)
                list_of_doc.append(norm_name)
                set_of_suffix.add(files.suffix)
                shutil.move(files.absolute(), '\\'.join([folders[1], norm_name]))
            elif files.suffix.upper() in ('.MP3', '.OGG', '.WAV', '.AMR'):
                norm_name = normalize(files.name)
                list_of_audio.append(norm_name)
                set_of_suffix.add(files.suffix)
                shutil.move(files.absolute(), '\\'.join([folders[2], norm_name]))
            elif files.suffix.upper() in  ('.ZIP', '.GZ', '.TAR'):
                norm_name = normalize(files.name)
                list_of_achives.append(norm_name)
                set_of_suffix.add(files.suffix)
                shutil.unpack_archive(files.name, '\\'.join([folders[4], re.sub('\.\w+$', '', norm_name)]))
                os.remove(files.absolute())   
            else:                
                list_of_unknown.append(files.name)
                set_of_unk_suffix.add(files.suffix)                
             
        elif files.is_dir():            
            if files.name in ['Images', 'Documents', 'Audio', 'Video', 'Archives',]:
                continue                       
            else:
                list_of_bad_folders.append(files.absolute())
                find_files(files)

     
    dict_of_file['images'] = list_of_img
    dict_of_file['archives'] = list_of_achives
    dict_of_file['audio'] = list_of_audio
    dict_of_file['documents'] = list_of_doc
    dict_of_file['set_of_suffix'] = list(set_of_suffix)
    dict_of_file['set_of_unk_suffix'] = list(set_of_unk_suffix)
    dict_of_file['unknown'] = list_of_unknown
    dict_of_file['video'] = list_of_vid
    
    return dict_of_file


def normalize(not_normal_name): # функція перейменування 
    map = {1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G', 1076: 'd', 1044: 'D', 1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I', 1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M', 1085: 'n', 1053: 'N', 1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T', 1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS', 1095: 'ch', 1063: 'CH', 1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH', 1098: '', 1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '', 1101: 'e', 1069: 'E', 1102: 'yu', 1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je', 1028: 'JE', 1110: 'i', 1030: 'I', 1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G', 33: '_', 64: '_', 35: '_', 36: '_', 37: '_', 94: '_', 38: '_', 40: '_', 41: '_', 45: '_', 43: '_', 59: '_', 46: '_', 44: '_', 32: '_'}    
    suffix = re.search('\.\w+$', not_normal_name)                   # визначення розширення файлу
    name_without_suf = re.sub(suffix.group(), '', not_normal_name)  # видалення розширення 
    name_without_suf2 = name_without_suf.translate(map)             # перейменування файлу
    norm_name = name_without_suf2 + suffix.group()                  # повернення розширення

    return norm_name


if __name__ == '__main__':
    main()