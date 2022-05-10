import adodbapi
from config import myuser, mypassword, mydatabase, myhost

connStr = 'Provider=SQLOLEDB.1; User ID=%s; Password=%s; Initial Catalog=%s; Data Source= %s'
myConnStr = connStr % (myuser, mypassword, mydatabase, myhost)
myConn = adodbapi.connect(myConnStr)
curs = myConn.cursor()

def execute_query(query):
    curs.execute(query)
    # curs.fetchall()
    # results = curs.fetchall()
    # for row in results:
    #    return(row)
    # return results