import os
import time
import sqlite3

path_cwd = os.getcwd()
path_anki = os.path.join(path_cwd, 'files', 'anki-pkgs')
path_anki_db = os.path.join(path_anki, 'test.db')

con = sqlite3.connect(path_anki_db)
cur = con.cursor()
for row in cur.execute('SELECT * FROM test_table;'):
    print(row)