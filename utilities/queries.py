

from config.config import DATABASE_NAME, OFFERS_IMAGES_FOLDER
# Tables
OFFERS_TABLE = "offers"
REQUESTS_TABLE = "requests"

# Fields
DESCRIPTION_FIELD = "description"
IMAGES_FIELD = "images"
TITLE_FIELD = "title"
PRICE_FIELD = "price"
ID_FIELD = "id"
CATEGORY_FIELD = "category"
SUBCATEGORY_FIELD = "subCategory"
AUTO_SUBMIT_FIELD = "autoSubmit"


MATCH_FIELDS = "{},ownerId,{},{},{},{},{},{}".format(
    DESCRIPTION_FIELD, IMAGES_FIELD, TITLE_FIELD, PRICE_FIELD, ID_FIELD, CATEGORY_FIELD, SUBCATEGORY_FIELD)


class Queries():
    # TODO: filter by category
    @staticmethod
    def getOffers(category_id=None, subcategory_id=None, required_images=False, auto_submit=True):
        query_extra_filters = ""

        # Set optional query filter fields
        if category_id is not None and subcategory_id is not None:
            query_extra_filters += "AND {category} = {categoryValue} AND {subcategory} = {subcategoryValue}".format(
                category=CATEGORY_FIELD,
                categoryValue=category_id, subcategory=SUBCATEGORY_FIELD, subcategoryValue=subcategory_id)
        if required_images:
            query_extra_filters += "AND {images} != ''".format(
                images=IMAGES_FIELD)

        return "SELECT {matchFields} FROM {table} WHERE {autoSubmit} = {autoSubmitValue} {extraFilters}".format(
            matchFields=MATCH_FIELDS, table=OFFERS_TABLE, autoSubmit=AUTO_SUBMIT_FIELD,
            autoSubmitValue=auto_submit, extraFilters=query_extra_filters)

    @staticmethod
    def getRequests():
        return "SELECT {} FROM {}".format(MATCH_FIELDS, REQUESTS_TABLE)


class Offer(object):
    def __init__(self, offer):
        super().__init__()
        self.offer = offer

    @property
    def images(self):
        result = []
        if(self.offer[IMAGES_FIELD] != ""):
            images = self.offer[IMAGES_FIELD].split(",")
            # Append full path to each image name
            return map(lambda image_name: OFFERS_IMAGES_FOLDER + image_name, images)

        return result

    @property
    def category(self):
        return self.offer[CATEGORY_FIELD]

    @property
    def subcategory(self):
        return self.offer[SUBCATEGORY_FIELD]
