

from config.config import DATABASE_NAME
OFFERS_TABLE = "offers"
REQUESTS_TABLE = "requests"

MATCH_FIELDS = "id,ownerId,title,images,price"


class Queries():
    @staticmethod
    def getOffers(autoSubmit=True):
        return "SELECT {} FROM {} WHERE autoSubmit = {}".format(MATCH_FIELDS, OFFERS_TABLE, autoSubmit)

    @staticmethod
    def getRequests():
        return "SELECT {} FROM {}".format(MATCH_FIELDS, REQUESTS_TABLE)
