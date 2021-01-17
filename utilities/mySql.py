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

    def createTable(self, tableName, columns):
        # Build query
        query = "create table " + tableName + " ("  # Define table name
        for column in columns:                      # Set table columns
            query += column + ","
        query = query[:-1]                          # Substring the last ,
        query += ")"

        # Execute query
        self.cursor.execute(query)

    def insertRowToTable(self, tableName, rowData, columns):
        # Build query
        query = "insert into " + tableName + " values (?,?)"
        try:
            self.cursor.execute(query, rowData)    # Execute query
            self.db_connection.commit()                        # Save changes
        except mysql.connector.Error as err:
            raise ValueError(err)

    def executeQuery(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def testTableExistence(self, tableName):
        query = "SELECT 1 FROM " + tableName + " LIMIT 1;"
        try:
            self.executeQuery(query)
            return True
        except:
            return False

    def testRowExistence(self, tableName, idColumnName, rowID):
        query = "SELECT COUNT(*) FROM " + tableName + \
            " WHERE " + idColumnName + " = '" + rowID + "'"
        result = self.executeQuery(query)
        return not not result[0][0]

    def testLogin(self, tableName, tableColumns, loginInfo):
        query = "SELECT COUNT(*) FROM " + tableName + " WHERE " + \
                tableColumns[0] + " = '" + loginInfo[tableColumns[0]] + "'" + \
            " AND " + tableColumns[1] + " = '" + \
                loginInfo[tableColumns[1]] + "'"

        result = self.executeQuery(query)
        return not not result[0][0]

    def updateRow(self, tableName, updatedValues, condition):
        query = "UPDATE " + tableName + " SET " + updatedValues + " WHERE " + condition
        print(query)
        result = self.executeQuery(query)
        print("update results ", result)

    def deleteRow(self, tableName, condition):
        query = "DELETE FROM " + tableName + " WHERE " + condition
        self.executeQuery(query)
