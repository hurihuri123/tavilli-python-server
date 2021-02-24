import mysql.connector
from mysql.connector import errorcode


def convertQueryResultToDict(queryResult, description):
    column_names = [col[0] for col in description]
    return [dict(zip(column_names, row))
            for row in queryResult]


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
                database=database,
                autocommit=True  # Ensures that DB stay updated according to different source changes
            )
            print("Connected successfully to DB")
            return conn
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise Exception(
                    "Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise Exception("Database does not exist")
            else:
                raise Exception(err)
            return None

    def closeConnection(self):
        self.db_connection.close()

    def executeQuery(self, query, toDict=True):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return convertQueryResultToDict(result, self.cursor.description) if toDict else result
