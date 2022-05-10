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