from algorithms.textMatch import calculateTextMatch
from algorithms.imageMatch import ImageMatch
from utilities.queries import *
from utilities.utilities import round_float_number, distance_percentage

import functools

MAX_PRICE_DISTANCE_PERCENTAGE = 50
MIN_MATCH_RATE = 75
NO_MATCH_PERCENTAGE = 0


class Match(object):
    def __init__(self, request, offer, images_distance=None):
        self.request = request
        self.offer = offer
        self.images_distance = images_distance

    @property
    @functools.lru_cache()
    def textFields(self):
        return calculateTextMatch(
            self.request[DESCRIPTION_FIELD], self.offer[DESCRIPTION_FIELD])

    @property
    @functools.lru_cache()
    def price(self):
        """  
        Calculate distance between request and offer price      
        Args:
        Returns:
            price_distance: lower distance means better match
        """
        prices_distance = None

        if self.offer.price is None:
            pass
        elif self.request.price is None or self.offer.price <= self.request.price:
            prices_distance = 0
        elif self.request.locked_fields is not None and PRICE_FIELD in self.request.locked_fields:
            # Request price is locked which means price is final
            pass
        else:  # Request has an open price
            prices_distance = distance_percentage(
                self.offer.price, self.request.price)

        return prices_distance

    """        
        Args:
            distance: images distance value (lower distance means better match percentage)
            start_range: start value of distance's percentage group
            end_range: end value of distance's percentage group
            min_percentage: minimum percentage for distance's percentage group
            max_percentage: maximum percentage for distance's percentage group
        Returns:
            Match percentage in range 0 to 100
    """
    @staticmethod
    def convertImageDistanceToPercentage(distance, start_range, end_range, min_percentage, max_percentage):
        all_way = end_range - start_range
        traveled = distance - start_range
        way_passed_percentage = traveled / all_way
        return min_percentage + way_passed_percentage * (max_percentage - min_percentage)

    @property
    @functools.lru_cache()
    def images(self):
        match_percentage = None
        if self.images_distance is not None:
            if self.images_distance > 1:  # Distance above 1 result with 0% match
                match_percentage = 0
            elif self.images_distance >= 0.90:  # Distance 0.90 - 1 result with 80-85% match
                match_percentage = self.convertImageDistanceToPercentage(
                    self.images_distance, 0.90, 1, 80, 85)
            elif self.images_distance >= 0.70:  # Distance 0.70 - 0.90 result with 85-90% match
                match_percentage = self.convertImageDistanceToPercentage(
                    self.images_distance, 0.70, 0.90, 85, 90)
            elif self.images_distance >= 0.50:  # Distance 0.50 - 0.70 result with 90-95% match
                match_percentage = self.convertImageDistanceToPercentage(
                    self.images_distance, 0.50, 0.70, 90, 95)
            elif self.images_distance >= 0.20:  # Distance 0.20 - 0.50 result with 90-95% match
                match_percentage = self.convertImageDistanceToPercentage(
                    self.images_distance, 0.20, 0.50, 95, 100)
            else:
                match_percentage = 100  # Distance 0-0.20 result with 100% match

        return match_percentage

    @property
    @functools.lru_cache()
    def model(self):
        is_model_match = None
        if self.offer.model is None or self.request.model is None:
            pass
        else:
            is_model_match = True if calculateTextMatch(
                self.request.model, self.offer.model) >= 70 else False
        return is_model_match

    @property
    @functools.lru_cache()
    def matchPercantage(self):
        if self.price is None or self.price > MAX_PRICE_DISTANCE_PERCENTAGE:
            return NO_MATCH_PERCENTAGE  # Price mistmatch

        # Set up match range according to fields priority
        (min_match_rate, max_match_rate) = self.getMatchRanges()
        return round_float_number(sum)

    def getMatchRanges(self):
        min_match_rate = None
        max_match_rate = None

        if self.model is None:
            pass
        elif self.model == False:
            max_match_rate = 90
        else:
            min_match_rate = 90

        if self.images is not None and self.images >= 90:
            min_match_rate = MIN_MATCH_RATE
        return (min_match_rate, max_match_rate)

    def __str__(self):
        return {"requestId": self.request.id, "offerId": self.offer.id, "percentage": self.matchPercantage, "priceDistance": self.price}
