import os
import time
import sqlite3
import random
import query_params
import time
# from generate_cards import temp_card_list, temp_deck_name
temp_card_list, temp_deck_name = [], ''

path_cwd = os.getcwd()
path_anki = os.path.join(path_cwd, 'files', 'anki-pkgs')
path_anki_db = os.path.join(path_anki, 'user-deck-card-info-02.db')

# temp variables, should be grabbed from generate_cards.py
if len(temp_card_list) == 0:
    print('No card list provided, inserting default cards into SQLite DB')
    temp_card_list = [['Front 1', 'Back 1'], ['Front 2', 'Back 2']]
if temp_deck_name == '':
    temp_deck_name = 'New Deck ' + str(random.randint(0, 1e6 - 1))

try:
    print('Connecting to SQLite...')
    con = sqlite3.connect(path_anki_db)
    cur = con.cursor()

    # collect all query segments that will be used --- SQLite only allows executing
    # one ";" statement at a time
    query_segments = []
    for i in range(1, 22):
        _query_path = 'sql_queries/create-deck-%s.sql' % str(i).zfill(2)
        with open(_query_path, 'r') as file:
            _query_string_lines = file.readlines()
            _query_string = '\n'.join(_query_string_lines)
            query_segments.append(_query_string)
    
    # generate random id params that will be used throughout the main query
    print('Preparing to insert into SQLite, hang tight...')
    sql_did = random.randint(1.6e12, 1.7e12 - 1)
    sql_deckName = temp_deck_name
    sql_curModel = random.randint(1.3e12, 1.4e12 - 1)
    sql_mod = query_params.sql_mod
    sql_crt = random.randint(1.4e9, 1.5e9 - 1)

    # add query segment for "col"
    query_segments_3 = query_segments[3]
    query_segments_3 = query_segments_3.replace('$sql_did', str(sql_did))
    query_segments_3 = query_segments_3.replace('$sql_deckName', sql_deckName)
    query_segments_3 = query_segments_3.replace('$sql_curModel', str(sql_curModel))
    query_segments_3 = query_segments_3.replace('$sql_mod', str(sql_mod))
    query_segments_3 = query_segments_3.replace('$sql_crt', str(sql_crt))
    query_segments[3] = query_segments_3

    # create a list containing individual query segments for each card and each note
    query_segments_5 = [] # card
    query_segments_7 = [] # note

    for i in range(0, len(temp_card_list)):
        print('Inserting card #%s into SQLite...' % str(i + 1))
        _query_segments_5 = query_segments[5]

        _sql_id = random.randint(1.6e12, 1.7e12 - 1) # card id
        _sql_nid = random.randint(1.6e12, 1.7e12 - 1)
        _sql_colid = random.randint(1.6e12, 1.7e12 - 1)
        _sql_guid = random.randint(1e9, 1e10 - 1)
        _sql_front = temp_card_list[i][0]
        _sql_back = temp_card_list[i][1]
        _sql_csum = random.randint(4.2e9, 4.3e9 - 1)

        _query_segments_5 = _query_segments_5.replace('$sql_did', str(sql_did))
        _query_segments_5 = _query_segments_5.replace('$sql_deckName', str(sql_deckName))
        _query_segments_5 = _query_segments_5.replace('$sql_curModel', str(sql_curModel))
        _query_segments_5 = _query_segments_5.replace('$sql_id', str(_sql_id))
        _query_segments_5 = _query_segments_5.replace('$sql_nid', str(_sql_nid))
        _query_segments_5 = _query_segments_5.replace('$sql_mod', str(sql_mod))
        _query_segments_5 = _query_segments_5.replace('$sql_crt', str(sql_crt))
        _query_segments_5 = _query_segments_5.replace('$sql_colid', str(_sql_colid))
        _query_segments_5 = _query_segments_5.replace('$sql_guid', str(_sql_guid))
        _query_segments_5 = _query_segments_5.replace('$sql_front', _sql_front)
        _query_segments_5 = _query_segments_5.replace('$sql_back', _sql_back)
        _query_segments_5 = _query_segments_5.replace('$sql_csum', str(_sql_csum))

        query_segments_5.append(_query_segments_5)

        _query_segments_7 = query_segments[7]

        _query_segments_7 = _query_segments_7.replace('$sql_did', str(sql_did))
        _query_segments_7 = _query_segments_7.replace('$sql_deckName', str(sql_deckName))
        _query_segments_7 = _query_segments_7.replace('$sql_curModel', str(sql_curModel))
        _query_segments_7 = _query_segments_7.replace('$sql_id', str(_sql_id))
        _query_segments_7 = _query_segments_7.replace('$sql_nid', str(_sql_nid))
        _query_segments_7 = _query_segments_7.replace('$sql_mod', str(sql_mod))
        _query_segments_7 = _query_segments_7.replace('$sql_crt', str(sql_crt))
        _query_segments_7 = _query_segments_7.replace('$sql_colid', str(_sql_colid))
        _query_segments_7 = _query_segments_7.replace('$sql_guid', str(_sql_guid))
        _query_segments_7 = _query_segments_7.replace('$sql_front', _sql_front)
        _query_segments_7 = _query_segments_7.replace('$sql_back', _sql_back)
        _query_segments_7 = _query_segments_7.replace('$sql_csum', str(_sql_csum))

        query_segments_7.append(_query_segments_7)

    # execute all queries in order
    for i in range(0, len(query_segments)):
        print('Executing query #%s...' % str(i + 1))
        # SQLite can only execute one ";" transaction at a time, so the query segments
        # for adding *each* card and *each* note must be executed individually
        print(query_segments[i])
        if i == 5: # cards
            for j in range(0, len(query_segments_5)):
                cur.execute(query_segments_5[j])
        elif i == 7: # notes
            for j in range(0, len(query_segments_7)):
                cur.execute(query_segments_7[j])
        else:
            cur.execute(query_segments[i])
    print('Successfully stored deck!')
except Exception as e:
    print(e)