import sys
import re
from shutil import unpack_archive, copyfile
from pathlib import Path


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}

structure = {'Images': ['JPEG', 'PNG', 'JPG', 'SVG', 'TIFF', 'TIF', 'GIF'],
             'Video': ['AVI', 'MP4', 'MOV', 'MKV'],
             'Documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'CSV', 'LOG', 'JSON', 'XML', 'YAML'],
             'Audio': ['MP3', 'OGG', 'WAV', 'AMR', 'FLAC', 'AAC'],
             'Presentations': ['PPT', 'PPTX'],
             'Computer graphics': ['PSD', 'AI', 'SVG', 'EPS'],
             'Databases': ['DB', 'SQLITE', 'DBF', 'MDB'],
             'Executable scripts': ['PY', 'JS', 'SH', 'BAT'],
             'Archives': ['ZIP', 'GZ', 'TAR'],
             'Books' : ['FB2', 'EPUB', 'MOBI'],
             '3D models': ['3DS', 'STEP', 'STP', 'OBJ', 'FBX', 'IGS', 'MB', 'MAX', 'C4D']
             }

list_name = []


def copy_file(root, file_path):  # File copying to new directory
    
    if (file_path.suffix[1:]).upper() in structure['Archives']:
        print(file_path, file_path.name, root)
        unpack_archive(file_path, create_folder(root, file_path) / normalize(file_path)[:str(file_path.name).rfind('.')])  # Archives without suffix
    else:
        copyfile(file_path, create_folder(root, file_path) / normalize(file_path))


def create_folder(root, file_path):  # Create folder using file-format as folder name
    
    new_directory = Path(fr'{root}/Sorted/{create_volume(file_path) or "Other"}/{(file_path.suffix[1:]).upper()}')
    new_directory.mkdir(parents=True, exist_ok=True)
    return new_directory


def create_volume(file_path): # Find file-format in Dictionary and return Key as a folder name
    
    for key, value in structure.items():
        for suffix in value:
            if (file_path.suffix[1:]).upper() == suffix:
                return key


def normalize(file_path): # Normalize filename
    
    name = file_path.name[:str(file_path.name).rfind('.')] # Filename without suffix
    new_name = re.sub(r'\W', '_', name.translate(TRANS))  # New filename - transliterated
    file_name = f'{new_name}{file_path.suffix}'  # New filename with suffix
    new_name = is_duplicate(file_name, new_name) or new_name # New filename or New filename with extra number if more than one exists
    return f'{new_name}{file_path.suffix}'


def is_duplicate(file_name, new_name):
    
    list_name.append(file_name)  # Add to global list with filenames
    if list_name.count(file_name) > 1:
        # Add NUMBER to filename if filename already exist
        new_name = f'{new_name}({list_name.count(file_name) - 1})'
        return new_name


def parse_folder(root, path):  # Iter in the directory
    
    for element in path.iterdir():
        if element.name.lower() == 'sorted':
            raise FileExistsError
    for element in path.iterdir():
        if element.is_dir():
            parse_folder(root, element)  # Recursion
            if element.name in structure.keys():
                continue
            else:
                try:
                    element.rmdir()  # Delete empty folder
                except:
                    pass
        else:
            copy_file(root, element)


for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def main(input_text):
    path = Path(input_text.split()[1].lower())
    root = path
    try:
        parse_folder(root, path)
    except FileNotFoundError:
        print("\nDirectory does not exist. Try again\n")
    except FileExistsError:
        print("\nFolder 'Sorted' already exist. Sorting was not complete\n")
    else:
        print(f"\nFolder 'Sorted' was created\nSorting in the directory {root} has been completed successfully.\n")


if __name__ == '__main__':
    path = Path(sys.argv[1])
    root = path
    parse_folder(root, path)
    print(path, '  Done')
