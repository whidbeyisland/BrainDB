import os
import time
from zipfile import ZipFile

path_cwd = os.getcwd()
path_anki = os.path.join(path_cwd, 'files', 'anki-pkgs2')
path_deck_input = os.path.join(path_anki, '(CORE) Python.apkg')
path_deck_collection = os.path.join(path_anki, 'collection.anki2')
path_deck_media = os.path.join(path_anki, 'media')
path_deck_output = os.path.join(path_anki, '(CORE) Python 2.apkg')
path_anki_deck_output = os.path.join(path_anki, 'Saratoga Hotel.apkg')

# with ZipFile(path_deck_input, 'r') as zip:
#     zip.printdir()
#     zip.extractall()

# time.sleep(2)

myzip = ZipFile(path_anki_deck_output, 'w')
myzip.write(os.path.join(path_anki, 'collection.anki2'), 'collection.anki2')
myzip.write(os.path.join(path_anki, 'media'), 'media')
print('got here!')
myzip.close()

# with ZipFile(path_anki_deck_output, 'w') as myzip:
#     myzip.write('collection.anki2')
#     myzip.write('media')
#     print('got here!')
#     myzip.close()