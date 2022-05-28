import os
import time
import sqlite3
import query_params
from generate_cards import temp_card_list

path_cwd = os.getcwd()
path_anki = os.path.join(path_cwd, 'files', 'anki-pkgs')
path_anki_db = os.path.join(path_anki, 'user-deck-card-info.db')

# data structure, should be grabbed from generate_cards.py
cards_to_add = temp_card_list
if len(cards_to_add) == 0:
    print('No card list provided, inserting default cards into SQLite DB')
    cards_to_add = [['Front 1', 'Back 1'], ['Front 2', 'Back 2']]

try:
    con = sqlite3.connect(path_anki_db)
    cur = con.cursor()

    # grab main query file, and secondary scripts for query segments
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
    
    # generate missing parameters in query segments
    # sql_id = 1653683561709
    # sql_nid = 1653683561708
    # sql_did = 1653683537446
    # sql_mod = 1653683561
    # sql_due = 29355
    # sql_crt = 1442476800
    # sql_scm = 1653683608163
    # sql_colid = 1653683608163
    # sql_curModel = 1376926904739
    # sql_deckName = 'BrainDB Deck'
    # sql_guid = 'eB[BHB5POk'
    # sql_front = '$front'
    # sql_back = '$back'
    # sql_csum = 4251924563

    # put all query segments back into the main query
    query_full = query_full.replace('$cards.sql', query_cards)
    query_full = query_full.replace('$col.sql', query_col)
    query_full = query_full.replace('$notes.sql', query_notes)

    # cur.execute(query_full)
    print('Successfully generated deck!')
except Exception as e:
    print(e)
    print('One or more SQL query file(s) could not be loaded')