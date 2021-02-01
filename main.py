from utilities.mySql import MySqlConnector
from utilities.queries import Queries, OFFERS_TABLE, REQUESTS_TABLE, MATCH_FIELDS, CATEGORY_FIELD, SUBCATEGORY_FIELD
from algorithms.match import Match
from algorithms.imageMatch import ImageMatch
from config.config import *
import os

#TODO: doc


class someClass():
    def __init__(self):
        super().__init__()
        self.database = MySqlConnector(
            DATABASE_HOST, DATABASE_USERNAME, DATEBASE_PASSWORD, DATABASE_NAME)
        self.image_matcher = ImageMatch()
        self.init_datasets()

    def search_match_for_request(self, request):
        matches = []
        # TODO: select filter by request price as well
        # Select offers according to request info
        offers = self.database.executeQuery(Queries.getOffers(
            request[CATEGORY_FIELD], request[SUBCATEGORY_FIELD]))
        # Init images dataset according to request category

        # Get request's image features
        # Compare dataset with query features
        for offer in offers:
            # Find related offer matches results
            # Pass list of images matches results to match object (might be more than one image)
            match = Match(request, offer)
            if(match.matchPercantage > 70):
                matches.append(match)
        return matches

    def search_match_for_offer(self, offer):
        pass

    def init_datasets(self):
        # TODO: select all offers and check that i have a dataset file for each existing cateogry, otherwise, create one
        dataset_filename = self.get_dataset_filename(2, 2)
        if not os.path.isfile(dataset_filename):  # Check if dataset file exists
            self.init_category_dataset(2, 2)

    def init_category_dataset(self, category_id, subcategory_id):
        # TODO: read all images
        imagesDir = None
        image_matcher.init_dataset(
            imagesDir, self.get_dataset_filename(category_id, subcategory_id))

    def get_dataset_filename(self, category_id, subcategory_id):
        return "{}/{}.hkl".format(category_id, subcategory_id)


if __name__ == "__main__":
    some_class_object = someClass()

    requests = some_class_object.database.executeQuery(Queries.getRequests())
    matches = some_class_object.search_match_for_request(requests[0])
