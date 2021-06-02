from algorithms.textMatch import calculateTextMatch
from algorithms.imageMatch import ImageMatch
from utilities.queries import *
from utilities.utilities import round_float_number, distance_percentage
from services.loggerService import LoggerService

import functools

MAX_PRICE_DISTANCE_PERCENTAGE = 50
MIN_MATCH_RATE = 75
NO_MATCH_PERCENTAGE = 0
MAX_DIMENSIONS_PERCENTAGE_DISTANCE = 30


class Match(object):
    def __init__(self, request, offer, images_distance=None):
        self.request = request
        self.offer = offer
        self.images_distance = images_distance

    @property
    @functools.lru_cache()
    def textFields(self):
        request_extra_fields_values = ""
        for key, value in self.request.extraFields.items():
            request_extra_fields_values += "{} ".format(value)

        offer_extra_fields_values = ""
        for key, value in self.offer.extraFields.items():
            offer_extra_fields_values += "{} ".format(value)

        text_match = calculateTextMatch(
            "{} {} {}".format(self.request.description,
                              self.request.title, request_extra_fields_values),
            "{} {} {}".format(self.offer.description, self.offer.title, offer_extra_fields_values))
        return text_match

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
            if self.images_distance > 1.15:  # Distance above 1 result with 0% match
                match_percentage = 0
            elif self.images_distance >= 0.90:  # Distance 0.90 - 1.15 result with 80-85% match
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
                self.request.model, self.offer.model) >= 100 else False
        return is_model_match

    @property
    def dimensions(self):
        is_dimensions_match = True
        if self.offer.height is not None and self.request.height is not None and distance_percentage(self.offer.height, self.request.height) > MAX_DIMENSIONS_PERCENTAGE_DISTANCE:
            is_dimensions_match = False
        elif self.offer.width is not None and self.request.width is not None and distance_percentage(self.offer.width, self.request.width) > MAX_DIMENSIONS_PERCENTAGE_DISTANCE:
            is_dimensions_match = False
        elif self.offer.length is not None and self.request.length is not None and distance_percentage(self.offer.length, self.request.length) > MAX_DIMENSIONS_PERCENTAGE_DISTANCE:
            is_dimensions_match = False
        return is_dimensions_match

    @property
    def has_dealbreaker_fields(self):
        # Variable Definition
        result = True

        # Code Section
        if self.price is None or self.price > MAX_PRICE_DISTANCE_PERCENTAGE:
            pass  # Price mismatch
        elif self.dimensions == False:
            pass  # Dimensions mismatch
        else:
            result = False
        return result

    @property
    @functools.lru_cache()
    def matchPercantage(self):
        if self.has_dealbreaker_fields:
            return NO_MATCH_PERCENTAGE

        # Set up match range according to fields priority
        (min_match_rate, max_match_rate) = self.getMatchRanges()

        # Calculate match fields priority
        if self.images is None:
            match_result = self.textFields
        elif self.model is None:
            match_result = 0.6 * self.images + 0.4 * self.textFields
        else:
            match_result = 0.2 * self.images + 0.8 * self.textFields

        if min_match_rate is not None and match_result < min_match_rate:
            # Calculate relative match result starting from min_match_rate
            match_result = min_match_rate + \
                (match_result / 100) * (100 - min_match_rate)
        elif max_match_rate is not None and match_result > max_match_rate:
            match_result = max_match_rate

        return round_float_number(match_result)

    def getMatchRanges(self):
        min_match_rate = None
        max_match_rate = None

        if self.model is None:
            pass
        elif self.model == False:
            max_match_rate = 90
        else:
            min_match_rate = 90

        if self.images is not None and self.images >= 85:
            min_match_rate = MIN_MATCH_RATE
        elif self.images is not None:
            LoggerService.info("Request '{}' offer '{}' image match '{}' distance '{}'".format(
                self.request.id, self.offer.id, self.images, self.images_distance))
        return (min_match_rate, max_match_rate)

    def __str__(self):
        return {"requestId": self.request.id, "offerId": self.offer.id, "percentage": self.matchPercantage, "priceDistance": self.price}
