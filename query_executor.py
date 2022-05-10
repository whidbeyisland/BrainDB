import pyodbc
from config import myuser, mypassword, mydatabase, myhost

class QueryExecutor:
    def __init__(self):
        self.cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+myhost+';DATABASE='+mydatabase+';UID='+myuser+';PWD='+ mypassword)

    def execute_select_query(self, query):
        cursor = self.cnxn.cursor()
        cursor.execute(query)

        row = cursor.fetchone()
        while row:
            print(row)
            row = cursor.fetchone()

    def execute_insert_query(self, query):
        cursor = self.cnxn.cursor()
        cursor.execute(query)

        self.cnxn.commit()



# import adodbapi
# from config import myuser, mypassword, mydatabase, myhost

# connStr = 'Provider=SQLOLEDB.1; User ID=%s; Password=%s; Initial Catalog=%s; Data Source= %s'
# myConnStr = connStr % (myuser, mypassword, mydatabase, myhost)
# myConn = adodbapi.connect(myConnStr)
# curs = myConn.cursor()

# def execute_query(query):
#     curs.execute(query)
#     # curs.fetchall()
#     # results = curs.fetchall()
#     # for row in results:
#     #    return(row)
#     # return results