

OFFERS_TABLE = "offers"
REQUESTS_TABLE = "requests"


class Queries():
    @staticmethod
    def getOffers():
        return "SELECT * FROM {}".format(OFFERS_TABLE)

    @staticmethod
    def getRequests():
        return "SELECT * FROM {}".format(REQUESTS_TABLE)

    @staticmethod
    def showTableColumns(tableName):
        return "SHOW COLUMNS FROM {}".format(tableName)
