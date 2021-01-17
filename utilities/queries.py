

from config.config import DATABASE_NAME
OFFERS_TABLE = "offers"
REQUESTS_TABLE = "requests"

DESCRIPTION_FIELD = "description"
IMAGES_FIELD = "images"
TITLE_FIELD = "title"
PRICE_FIELD = "price"
ID_FIELD = "id"

MATCH_FIELDS = "{},ownerId,{},{},{},{}".format(
    DESCRIPTION_FIELD, IMAGES_FIELD, TITLE_FIELD, PRICE_FIELD, ID_FIELD)


class Queries():
    @staticmethod
    def getOffers(autoSubmit=True):
        return "SELECT {} FROM {} WHERE autoSubmit = {}".format(MATCH_FIELDS, OFFERS_TABLE, autoSubmit)

    @staticmethod
    def getRequests():
        return "SELECT {} FROM {}".format(MATCH_FIELDS, REQUESTS_TABLE)
