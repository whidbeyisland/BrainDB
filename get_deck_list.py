import sys
from query_executor import QueryExecutor

try:
    userid = sys.argv[2]
    if userid == '':
        print('Not logged in. Cannot query list of decks')
    else:
        q = QueryExecutor()
        query_string = '''
        SELECT * FROM Decks
        WHERE UserId = \'%s\'
        ''' % userid
        q.execute_select_query(query_string)
except:
    print('Not logged in. Cannot query list of decks')