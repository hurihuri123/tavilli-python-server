from algorithms.textMatch import calculateTextMatch
from utilities.queries import *


class Match(object):
    def __init__(self, request, offer):
        self.request = request
        self.offer = offer

    @property
    def descriptionMatch(self):
        return calculateTextMatch(
            self.request[DESCRIPTION_FIELD], self.offer[DESCRIPTION_FIELD])

    @property
    def matchPercantage(self):
        return self.descriptionMatch

    def __str__(self):
        return "requestId {}, offerId {} has {}% match".format(self.request[ID_FIELD], self.offer[ID_FIELD], self.matchPercantage)
