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
    sql_due = query_params.sql_due
    sql_crt = random.randint(1.4e9, 1.5e9 - 1)
    sql_scm = random.randint(1.6e12, 1.7e12 - 1)

    # add query segment for "col"
    query_segments_3 = query_segments[3]
    query_segments_3 = query_segments_3.replace('$sql_did', str(sql_did))
    query_segments_3 = query_segments_3.replace('$sql_scm', str(sql_scm))
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
        _query_segments_5 = _query_segments_5.replace('$sql_due', str(sql_due))
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
        _query_segments_7 = _query_segments_7.replace('$sql_due', str(sql_due))
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
        # if i == 3:
        #     cur.execute(
        #         'INSERT INTO col VALUES();',
        #         ('''1,1442476800,1653683608168,1653683608163,11,0,0,0,'{"schedVer":1,"sortBackwards":false,"nextPos":1,"newSpread":0,"addToCur":true,"estTimes":true,"collapseTime":1200,"sortType":"noteFld","timeLim":0,"dueCounts":true,"curDeck":1,"dayLearnFirst":false,"curModel":1376926904739,"activeDecks":[1]}','{"1376926904739":{"id":1376926904739,"name":"Basic-669e0","type":0,"mod":1653683567,"usn":-1,"sortf":0,"did":1653683537446,"tmpls":[{"name":"Card 1","ord":0,"qfmt":"{{Front}}","afmt":"{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}","bqfmt":"","bafmt":"","did":null,"bfont":"","bsize":0}],"flds":[{"name":"Front","ord":0,"sticky":false,"rtl":false,"font":"Arial","size":20,"media":[],"description":""},{"name":"Back","ord":1,"sticky":false,"rtl":false,"font":"Arial","size":20,"media":[],"description":""}],"css":".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n","latexPre":"\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n","latexPost":"\\end{document}","latexsvg":false,"req":[[0,"any",[0]]],"tags":["created-with-braindb"],"vers":[]},"1653683608163":{"id":1653683608163,"name":"Basic","type":0,"mod":0,"usn":0,"sortf":0,"did":1,"tmpls":[{"name":"Card 1","ord":0,"qfmt":"{{Front}}","afmt":"{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}","bqfmt":"","bafmt":"","did":null,"bfont":"","bsize":0}],"flds":[{"name":"Front","ord":0,"sticky":false,"rtl":false,"font":"Arial","size":20},{"name":"Back","ord":1,"sticky":false,"rtl":false,"font":"Arial","size":20}],"css":".card {\n  font-family: arial;\n  font-size: 20px;\n  text-align: center;\n  color: black;\n  background-color: white;\n}\n","latexPre":"\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n","latexPost":"\\end{document}","latexsvg":false,"req":[[0,"any",[0]]]}}','{"1653683537446":{"id":1653683537446,"mod":1653683537,"name":"BrainDB Deck","usn":-1,"lrnToday":[0,0],"revToday":[0,0],"newToday":[0,0],"timeToday":[0,0],"collapsed":false,"browserCollapsed":false,"desc":"","dyn":0,"conf":1,"extendNew":0,"extendRev":0},"1":{"id":1,"mod":0,"name":"Default","usn":0,"lrnToday":[0,0],"revToday":[0,0],"newToday":[0,0],"timeToday":[0,0],"collapsed":false,"browserCollapsed":false,"desc":"","dyn":0,"conf":1,"extendNew":0,"extendRev":0}}','{"1":{"id":1,"mod":0,"name":"Default","usn":0,"maxTaken":60,"autoplay":true,"timer":0,"replayq":true,"new":{"bury":false,"delays":[1.0,10.0],"initialFactor":2500,"ints":[1,4,0],"order":1,"perDay":20},"rev":{"bury":false,"ease4":1.3,"ivlFct":1.0,"maxIvl":36500,"perDay":200,"hardFactor":1.2},"lapse":{"delays":[10.0],"leechAction":1,"leechFails":8,"minInt":1,"mult":0.0},"dyn":false}}','{}' ''')
        #     )
        if i == 5: # cards
            for j in range(0, len(query_segments_5)):
                print(query_segments_5[j])
                cur.execute(query_segments_5[j])
        elif i == 7: # notes
            for j in range(0, len(query_segments_7)):
                print(query_segments_7[j])
                cur.execute(query_segments_7[j])
        else:
            print(query_segments[i])
            cur.execute(query_segments[i])
    print('Successfully stored deck!')
except Exception as e:
    print(e)