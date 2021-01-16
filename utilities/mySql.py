import mysql.connector


class MySqlConnector:
    def __init__(self, host, user, password, database):
        self.db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database)
        self.manager = self.db_connection.cursor(
            buffered=True)  # manager with access to the DB

    def createConnection(self, dbFilePath):
        try:
            # NOTE -  SQLite creates a new database if db file doesn't exsists
            conn = sqlite3.connect(dbFilePath)
            print("Connected successfully to DB")
            return conn
        except Error as e:
            print(e)
            return e

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
        self.manager.execute(query)

    def insertRowToTable(self, tableName, rowData, columns):
        # Build query
        query = "insert into " + tableName + " values (?,?)"
        try:
            self.manager.execute(query, rowData)    # Execute query
            self.db_connection.commit()                        # Save changes
        except sqlite3.Error as err:
            raise ValueError(err)

    def executeQuery(self, query):
        return self.manager.execute(query).fetchall()

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
