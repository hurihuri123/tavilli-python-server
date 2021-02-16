from algorithms.textMatch import calculateTextMatch
from algorithms.imageMatch import ImageMatch
from utilities.queries import *
from utilities.utilities import round_float_number


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
        match_percentage = None
        if self.images_distance:
            # If negative then zero
            match_percentage = max(0, 1 - self.images_distance) * 100

        return match_percentage

    @property
    def matchPercantage(self):
        sum = 0
        if(self.images):
            sum = sum + self.images
        return round_float_number(sum)

    def __str__(self):
        return {"requestId": self.request.id, "offerId": self.offer.id, "percentage": self.matchPercantage}
