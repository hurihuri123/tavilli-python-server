from algorithms.textMatch import calculateTextMatch
from algorithms.imageMatch import ImageMatch
from utilities.queries import *


class Match(object):
    def __init__(self, request, offer):
        self.request = request
        self.offer = offer

    @property
    def description(self):
        return calculateTextMatch(
            self.request[DESCRIPTION_FIELD], self.offer[DESCRIPTION_FIELD])

    @property
    def price(self):
        return 100

    @property
    def title(self):
        return 100

    @property
    def images(self):
        self.request[IMAGES_FIELD] = "https://www.ace.co.il/media/catalog/product/cache/1/small_image/250x/9df78eab33525d08d6e5fb8d27136e95/5/7/5777943_4__1.jpg"
        self.offer[IMAGES_FIELD] = "https://www.ace.co.il/media/catalog/product/cache/1/small_image/250x/9df78eab33525d08d6e5fb8d27136e95/5/7/5778186_3__1.jpg"

        if(self.request[IMAGES_FIELD] == "" or self.offer[IMAGES_FIELD] == ""):
            return None  # One of the object has no images
        return templateMatch(
            self.request[IMAGES_FIELD], self.offer[IMAGES_FIELD])

    @property
    def matchPercantage(self):
        sum = 0
        if(self.images):
            sum = sum + self.images
        return sum

    def __str__(self):
        return "requestId {}, offerId {} has {}% match".format(self.request[ID_FIELD], self.offer[ID_FIELD], self.matchPercantage)
