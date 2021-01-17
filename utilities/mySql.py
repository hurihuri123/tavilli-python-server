import mysql.connector
from mysql.connector import errorcode


class MySqlConnector:
    def __init__(self, host, user, password, database):
        self.db_connection = self.createConnection(
            host, user, password, database)
        if self.db_connection:
            self.cursor = self.db_connection.cursor(
                buffered=True)  # cursor with access to the DB

    def createConnection(self, host, user, password, database):
        try:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database)
            print("Connected successfully to DB")
            return conn
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            return None

    def closeConnection(self):
        self.db_connection.close()

    def executeQuery(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
