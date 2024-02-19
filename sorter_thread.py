import argparse
import logging
from pathlib import Path
import shutil
from threading import Thread


parser = argparse.ArgumentParser(description="sorting folder")
parser.add_argument("--source", "-s", help="source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="Output")  # за замовчуванням переміщаємо файли в папку dist  


args = vars(parser.parse_args())  # парсер аргументів
print(f"\nПочинаємо сортування в каталозі {args['source']}")


source = Path(args.get("source"))  # де знаходяться вихідні файли
output = Path(args.get("output"))  # куди складувати файли

folders = []


def grabs_folder(path: Path):  # рекурсивно знаходимо всі папки та додаємо їх у список folders
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)

a = 0
def normalize(not_normal_name, path: Path): # функція перейменування path папка куда складувати
    global a
    map = {1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G', 1076: 'd', 1044: 'D', 1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I', 1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M', 1085: 'n', 1053: 'N', 1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T', 1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS', 1095: 'ch', 1063: 'CH', 1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH', 1098: '', 1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '', 1101: 'e', 1069: 'E', 1102: 'yu', 1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je', 1028: 'JE', 1110: 'i', 1030: 'I', 1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G', 33: '_', 64: '_', 35: '_', 36: '_', 37: '_', 94: '_', 38: '_', 40: '_', 41: '_', 45: '_', 43: '_', 59: '_', 46: '_', 44: '_', 32: '_'}    
    suffix = Path(not_normal_name).suffix                  # визначення розширення файлу
    name_without_suf = str(not_normal_name).replace(str(suffix), '') # видалення розширення 
    name_without_suf2 = name_without_suf.translate(map)             # перейменування файлу
    norm_name = name_without_suf2 + suffix.lower()                  # повернення розширення
    if path.joinpath(norm_name).exists():
        name_without_suf2 += f'({str(a)})'
        a += 1
        norm_name = name_without_suf2 + suffix.lower()
    return norm_name

def copy_file(path: Path):
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix[1:]  # визначення суфіксу файлу
            ext_folder = output.joinpath(ext)  # створення папки по назві суфікса
            try:
                ext_folder.mkdir(exist_ok=True, parents=True)  # створення директорії (exist_ok якщо папка існує, то нічого не рожбимо, parents - створення декількох рекурсивних папок)
                norm_name = normalize(el.name, ext_folder)               
                shutil.copyfile(el, ext_folder.joinpath(norm_name))  # копіювання файлу
            except OSError as err:
                logging.error(err)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format=f"%(threadName)s [%(message)s]")

    folders.append(source)
    grabs_folder(source)

    threads = []
    for folder in folders:
        th = Thread(target=copy_file, args=(folder,))  # Створення потоків
        th.start()
        threads.append(th)

        [th.join() for th in threads]  # чекаємо завершення роботи всіх потоків
    print(f"Файли переміщено у папку {output}.\nМожна видаляти {source}\n")
