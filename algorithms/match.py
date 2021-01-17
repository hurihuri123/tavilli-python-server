from algorithms.textMatch import calculateTextMatch
from utilities.queries import *


class Match(object):
    def __init__(self, request, offer):
        self.request = request
        self.offer = offer
        self.matchPercantage = 0

    def calculate(self):
        description_match = calculateTextMatch(
            self.request[DESCRIPTION_FIELD], self.offer[DESCRIPTION_FIELD])

        self.matchPercantage = description_match
        return self.matchPercantage

    def __str__(self):
        return "requestId {}, offerId {} has {}% match".format(self.request[ID_FIELD], self.offer[ID_FIELD], self.matchPercantage)
