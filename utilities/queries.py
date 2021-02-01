

from config.config import DATABASE_NAME
OFFERS_TABLE = "offers"
REQUESTS_TABLE = "requests"

DESCRIPTION_FIELD = "description"
IMAGES_FIELD = "images"
TITLE_FIELD = "title"
PRICE_FIELD = "price"
ID_FIELD = "id"
CATEGORY_FIELD = "category"
SUBCATEGORY_FIELD = "subCategory"
AUTO_SUBMIT_FIELD = "autoSubmit"

MATCH_FIELDS = "{},ownerId,{},{},{},{}".format(
    DESCRIPTION_FIELD, IMAGES_FIELD, TITLE_FIELD, PRICE_FIELD, ID_FIELD)


class Queries():
    # TODO: filter by category
    @staticmethod
    def getOffers(category_id, subcategory_id, auto_submit=True):
        where_query = "WHERE {autoSubmit} = {autoSubmitValue} AND {category} = {categoryValue} AND {subcategory} = {subcategoryValue}".format(
            autoSubmit=AUTO_SUBMIT_FIELD, autoSubmitValue=auto_submit, category=CATEGORY_FIELD,
            categoryValue=category_id, subcategory=SUBCATEGORY_FIELD, subcategoryValue=subcategory_id)
        return "SELECT {matchFields} FROM {table} {whereQuery}".format(matchFields=MATCH_FIELDS, table=OFFERS_TABLE, whereQuery=where_query)

    @staticmethod
    def getRequests():
        return "SELECT {} FROM {}".format(MATCH_FIELDS, REQUESTS_TABLE)
