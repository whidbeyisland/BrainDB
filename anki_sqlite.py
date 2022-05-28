import os
import time
import sqlite3
import random
import query_params
from generate_cards import temp_card_list, temp_deck_name

path_cwd = os.getcwd()
path_anki = os.path.join(path_cwd, 'files', 'anki-pkgs')
path_anki_db = os.path.join(path_anki, 'user-deck-card-info.db')

# temp variables, should be grabbed from generate_cards.py
if len(temp_card_list) == 0:
    print('No card list provided, inserting default cards into SQLite DB')
    temp_card_list = [['Front 1', 'Back 1'], ['Front 2', 'Back 2']]
if temp_deck_name == '':
    temp_deck_name = 'New Deck ' + str(random.randint(0, 1e6 - 1))

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
    
    # generate random id params that will be used throughout the main query
    sql_did = random.randint(1.6e12, 1.7e12 - 1)
    sql_deckName = temp_deck_name
    sql_curModel = random.randint(1.3e12, 1.4e12 - 1)
    sql_mod = query_params.sql_mod
    sql_crt = random.randint(1.4e9, 1.5e9 - 1)

    # add query segment for "col"
    query_col = query_col.replace('$sql_did', sql_did)
    query_col = query_col.replace('$sql_deckName', sql_deckName)
    query_col = query_col.replace('$sql_curModel', sql_curModel)
    query_col = query_col.replace('$sql_mod', sql_mod)
    query_col = query_col.replace('$sql_crt', sql_crt)

    # add query segments for each card and each note
    queries_cards = []
    queries_notes = []
    for i in range(0, len(temp_card_list)):
        _query_cards = query_cards

        _sql_id = random.randint(1.6e12, 1.7e12 - 1) # card id
        _sql_nid = random.randint(1.6e12, 1.7e12 - 1)
        _sql_colid = random.randint(1.6e12, 1.7e12 - 1)
        _sql_guid = random.randint(1e9, 1e10 - 1)
        _sql_front = temp_card_list[i][0]
        _sql_back = temp_card_list[i][1]
        _sql_csum = random.randint(4.2e9, 4.3e9 - 1)

        _query_cards = _query_cards.replace('$sql_did', str(sql_did))
        _query_cards = _query_cards.replace('$sql_deckName', str(sql_deckName))
        _query_cards = _query_cards.replace('$sql_curModel', str(sql_curModel))
        _query_cards = _query_cards.replace('$sql_id', str(_sql_id))
        _query_cards = _query_cards.replace('$sql_nid', str(_sql_nid))
        _query_cards = _query_cards.replace('$sql_mod', str(sql_mod))
        _query_cards = _query_cards.replace('$sql_crt', str(sql_crt))
        _query_cards = _query_cards.replace('$sql_colid', str(_sql_colid))
        _query_cards = _query_cards.replace('$sql_guid', str(_sql_guid))
        _query_cards = _query_cards.replace('$sql_front', _sql_front)
        _query_cards = _query_cards.replace('$sql_back', _sql_back)
        _query_cards = _query_cards.replace('$sql_csum', str(_sql_csum))

        queries_cards.append(_query_cards)

        _query_notes = _query_notes.replace('$sql_did', str(sql_did))
        _query_notes = _query_notes.replace('$sql_deckName', str(sql_deckName))
        _query_notes = _query_notes.replace('$sql_curModel', str(sql_curModel))
        _query_notes = _query_notes.replace('$sql_id', str(_sql_id))
        _query_notes = _query_notes.replace('$sql_nid', str(_sql_nid))
        _query_notes = _query_notes.replace('$sql_mod', str(sql_mod))
        _query_notes = _query_notes.replace('$sql_crt', str(sql_crt))
        _query_notes = _query_notes.replace('$sql_colid', str(_sql_colid))
        _query_notes = _query_notes.replace('$sql_guid', str(_sql_guid))
        _query_notes = _query_notes.replace('$sql_front', _sql_front)
        _query_notes = _query_notes.replace('$sql_back', _sql_back)
        _query_notes = _query_notes.replace('$sql_csum', str(_sql_csum))

        queries_notes.append(_query_notes)
    queries_cards_str = '\n'.join(queries_cards)
    queries_notes_str = '\n'.join(queries_notes)

    # put all query segments back into the main query
    query_full = query_full.replace('$cards.sql', queries_cards_str)
    query_full = query_full.replace('$col.sql', query_col)
    query_full = query_full.replace('$notes.sql', queries_notes_str)

    cur.execute(query_full)
    print('Successfully generated deck!')
except Exception as e:
    print(e)
    print('One or more SQL query file(s) could not be loaded')