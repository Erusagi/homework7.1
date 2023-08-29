import os
import shutil
import sys
import zipfile
import tarfile
import gzip
import re

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")


TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()


def translit(name):
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', "_", new_name)
    return f"{new_name}.{'.'.join(extension)}"

def sort_files(folder_path):
    extensions = {
        "images": ("JPEG", "PNG", "JPG", "SVG"),
        "video" : ('AVI', 'MP4', 'MOV', 'MKV' ),
        "documents" : ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
        "music" : ('MP3', 'OGG', 'WAV', 'AMR'),
        "archives": ('ZIP', 'GZ', 'TAR')

    }

    unknown_extensions = set()

    for root, _, files in os.walk(folder_path):
        for file in files:
            try:
                split_tup = os.path.splitext(file)
                filename = split_tup[0]
                file_extension = split_tup[1]
                normalized_name = translit(filename)
                target_folder = None

                for folder, ext_list in extensions.items():
                    if file_extension[1:].upper()  in ext_list:
                        target_folder = folder
                        break

                if target_folder is None :
                    print(file_extension)
                    unknown_extensions.add(file_extension);
                    continue;

                source_file_path = os.path.join(root, file)
                target_folder_path = os.path.join(folder_path, target_folder)
                if not os.path.exists(target_folder_path):
                    os.makedirs(target_folder_path)

                if file_extension[1:].upper() in extensions["archives"]:
                    archive_path = os.path.join(root, file)
                    extract_path = os.path.join(target_folder_path,normalized_name)
                    if file_extension == ".zip":
                        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                            zip_ref.extractall(extract_path)
                    elif file_extension == ".tar":
                        with tarfile.open(archive_path, 'r') as tar_ref:
                            tar_ref.extractall(extract_path)
                    elif file_extension == ".gz":
                        with gzip.open(archive_path, 'rb') as gz_ref:
                            with open(extract_path, 'wb') as extract_file:
                                extract_file.write(gz_ref.read())

                else:
                    target_file_path = os.path.join(target_folder_path, normalized_name + file_extension[1:])
                    shutil.move(source_file_path, target_file_path)
            except Exception as e:
                print("Error", e)


def main():
    sort_files(sys.argv[1])

