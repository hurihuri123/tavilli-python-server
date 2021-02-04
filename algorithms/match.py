from algorithms.textMatch import calculateTextMatch
from algorithms.imageMatch import ImageMatch
from utilities.queries import *


class Match(object):
    def __init__(self, request, offer, images_distance=None):
        self.request = request
        self.offer = offer
        self.images_distance = images_distance

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
        # self.request[IMAGES_FIELD] = "https://www.ace.co.il/media/catalog/product/cache/1/small_image/250x/9df78eab33525d08d6e5fb8d27136e95/5/7/5777943_4__1.jpg"
        # self.offer[IMAGES_FIELD] = "https://www.ace.co.il/media/catalog/product/cache/1/small_image/250x/9df78eab33525d08d6e5fb8d27136e95/5/7/5778186_3__1.jpg"

        # if(self.request[IMAGES_FIELD] == "" or self.offer[IMAGES_FIELD] == ""):
        # return None  # One of the object has no images
        match_percentage = None
        if self.images_distance:
            # If negative then zero
            match_percentage = max(0, 1 - self.images_distance)

        return match_percentage

    @property
    def matchPercantage(self):
        sum = 0
        if(self.images):
            sum = sum + self.images
        return sum

    def __str__(self):
        return "requestId {}, offerId {} has {}% match".format(self.request[ID_FIELD], self.offer[ID_FIELD], self.matchPercantage)
