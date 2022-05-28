import os
import time
import sqlite3
import query_params

path_cwd = os.getcwd()
path_anki = os.path.join(path_cwd, 'files', 'anki-pkgs')
path_anki_db = os.path.join(path_anki, 'test2.db')

con = sqlite3.connect(path_anki_db)
cur = con.cursor()

try:
    query_full = ''
    query_cards = ''
    query_col = ''
    query_notes = ''

    with open('sql_queries/create-deck.sql', 'r') as file:
        query_full = file.read()
    with open('sql_queries/cards.sql', 'r') as file:
        query_cards = file.read()
    with open('sql_queries/col.sql', 'r') as file:
        query_col = file.read()
    with open('sql_queries/notes.sql', 'r') as file:
        query_notes = file.read()
    query_full = query_full.replace('$cards.sql', query_cards)
    query_full = query_full.replace('$col.sql', query_col)
    query_full = query_full.replace('$notes.sql', query_notes)
    print(query_full[:2000])

    # cur.execute(query_full)
    print('Successfully generated deck!')
except Exception as e:
    print(e)
    print('One or more SQL query file(s) could not be loaded')