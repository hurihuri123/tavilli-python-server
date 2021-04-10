

import functools
import json

from config.config import DATABASE_NAME, OFFERS_IMAGES_FOLDER, REQUESTS_IMAGES_FOLDER
# Tables
OFFERS_TABLE = "offers"
REQUESTS_TABLE = "requests"

# Fields
OWNER_ID_FIELD = "ownerId"
DESCRIPTION_FIELD = "description"
IMAGES_FIELD = "images"
TITLE_FIELD = "title"
PRICE_FIELD = "price"
ID_FIELD = "id"
CATEGORY_FIELD = "category"
SUBCATEGORY_FIELD = "subCategory"
AUTO_SUBMIT_FIELD = "autoSubmit"
STATUS_FIELD = "status"
LOCKED_FIELDS = "lockedFields"
EXTRA_FIELDS = "extraFields"

# Static values
OPEN_STATUS = 1
REQUEST_OBJECT_NAME = "request"
OFFER_OBJECT_NAME = "offer"

MATCH_FIELDS = "{},{},{},{},{},{},{},{},{},{}".format(
    DESCRIPTION_FIELD, OWNER_ID_FIELD, IMAGES_FIELD, TITLE_FIELD, PRICE_FIELD, ID_FIELD, CATEGORY_FIELD, SUBCATEGORY_FIELD, EXTRA_FIELDS)
REQUEST_EXTRA_FIELDS = ",{}".format(LOCKED_FIELDS)


class Queries():
    @staticmethod
    def getOffers(start_id=None, category_id=None, subcategory_id=None, required_images=False, auto_submit=True, status=OPEN_STATUS):
        query_orderby = ""
        query_extra_filters = ""

        # Set optional query filter fields
        if start_id is not None:
            query_extra_filters += "AND id > {}".format(start_id)
            query_orderby = "ORDER BY id"
        if category_id is not None and subcategory_id is not None:
            query_extra_filters += "AND {category} = {categoryValue} AND {subcategory} = {subcategoryValue}".format(
                category=CATEGORY_FIELD,
                categoryValue=category_id, subcategory=SUBCATEGORY_FIELD, subcategoryValue=subcategory_id)
        if required_images:
            query_extra_filters += "AND {images} != ''".format(
                images=IMAGES_FIELD)

        return "SELECT {matchFields} FROM {table} WHERE {statusField} = {statusValue} AND {autoSubmit} = {autoSubmitValue} {extraFilters} {orderBy}".format(
            matchFields=MATCH_FIELDS, table=OFFERS_TABLE, statusField=STATUS_FIELD, statusValue=status, autoSubmit=AUTO_SUBMIT_FIELD,
            autoSubmitValue=auto_submit, extraFilters=query_extra_filters, orderBy=query_orderby)

    @staticmethod
    def getRequests(start_id=None, category_id=None, subcategory_id=None, status=OPEN_STATUS):
        query_orderby = ""
        query_extra_filters = ""

        # Set optional query filter fields
        if start_id is not None:
            query_extra_filters += "AND id > {}".format(start_id)
            query_orderby = "ORDER BY id"
        if category_id is not None and subcategory_id is not None:
            query_extra_filters += "AND {category} = {categoryValue} AND {subcategory} = {subcategoryValue}".format(
                category=CATEGORY_FIELD,
                categoryValue=category_id, subcategory=SUBCATEGORY_FIELD, subcategoryValue=subcategory_id)

        return "SELECT {matchFields}{requestExtraFields} FROM {table} WHERE  {statusField} = {statusValue} {extraFilters} {orderBy}".format(
            matchFields=MATCH_FIELDS, requestExtraFields=REQUEST_EXTRA_FIELDS, table=REQUESTS_TABLE, extraFilters=query_extra_filters, orderBy=query_orderby,
            statusField=STATUS_FIELD, statusValue=status)

    @staticmethod
    def getRequestById(request_id):
        return "SELECT {matchFields} FROM {table} WHERE {idField} = {idValue}".format(matchFields=MATCH_FIELDS,
                                                                                      table=REQUESTS_TABLE, idField=ID_FIELD, idValue=request_id)

    @staticmethod
    def getOfferById(offer_id):
        return "SELECT {matchFields} FROM {table} WHERE {idField} = {idValue}".format(matchFields=MATCH_FIELDS,
                                                                                      table=OFFERS_TABLE, idField=ID_FIELD, idValue=offer_id)


class Offer(object):
    def __init__(self, offer):
        super().__init__()
        self.offer = offer

    @property
    def id(self):
        return int(self.offer[ID_FIELD])

    @property
    def ownerId(self):
        return int(self.offer[OWNER_ID_FIELD])

    @property
    @functools.lru_cache()
    def images(self):
        result = []
        if(self.offer[IMAGES_FIELD] != ""):
            images = self.offer[IMAGES_FIELD].split(",")
            # Append full path to each image name
            for image in images:
                result.append(OFFERS_IMAGES_FOLDER + "/" + image)

        return result

    @property
    def category(self):
        return int(self.offer[CATEGORY_FIELD])

    @property
    def subcategory(self):
        return int(self.offer[SUBCATEGORY_FIELD])

    @property
    def price(self):
        return int(self.offer[PRICE_FIELD])

    @property
    def description(self):
        return self.offer[DESCRIPTION_FIELD] if self.offer[DESCRIPTION_FIELD] is not None else ""

    @property
    def title(self):
        return self.offer[TITLE_FIELD]

    @property
    def extraFields(self):
        extra_fields = {}
        if self.offer[EXTRA_FIELDS] is not None:
            extra_fields = json.loads(self.offer[EXTRA_FIELDS])
        return extra_fields

    def __str__(self):
        return OFFER_OBJECT_NAME


class Request(object):
    def __init__(self, request):
        super().__init__()
        self.request = request

    @property
    def id(self):
        return int(self.request[ID_FIELD])

    @property
    def ownerId(self):
        return int(self.request[OWNER_ID_FIELD])

    @property
    def category(self):
        return int(self.request[CATEGORY_FIELD])

    @property
    def subcategory(self):
        return int(self.request[SUBCATEGORY_FIELD])

    @property
    @functools.lru_cache()
    def images(self):
        result = []
        if(self.request[IMAGES_FIELD] != ""):
            images = self.request[IMAGES_FIELD].split(",")
            # Append full path to each image name
            for image in images:
                result.append(REQUESTS_IMAGES_FOLDER + "/" + image)

        return result

    @property
    def price(self):
        if self.request[PRICE_FIELD]:
            return int(self.request[PRICE_FIELD])
        return None

    @property
    def locked_fields(self):
        return self.request[LOCKED_FIELDS]

    @property
    def description(self):
        return self.request[DESCRIPTION_FIELD] if self.request[DESCRIPTION_FIELD] is not None else ""

    @property
    def title(self):
        return self.request[TITLE_FIELD]

    @property
    def extraFields(self):
        extra_fields = {}
        if self.request[EXTRA_FIELDS] is not None:
            extra_fields = json.loads(self.request[EXTRA_FIELDS])
        return extra_fields

    def __str__(self):
        return REQUEST_OBJECT_NAME
