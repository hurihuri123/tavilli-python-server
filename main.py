from utilities.mySql import MySqlConnector
from utilities.multiKeysDict import MultiKeysDict
from utilities.queries import Queries, OFFERS_TABLE, REQUESTS_TABLE, MATCH_FIELDS, CATEGORY_FIELD, SUBCATEGORY_FIELD, Offer

from algorithms.match import Match
from algorithms.imageMatch import ImageMatch

from config.config import *
from imutils.paths import list_images
import os

# TODO: doc


class someClass():
    def __init__(self):
        super().__init__()
        self.database = MySqlConnector(
            DATABASE_HOST, DATABASE_USERNAME, DATEBASE_PASSWORD, DATABASE_NAME)
        self.image_matcher = ImageMatch()

        current_directory = os.path.dirname(__file__)
        dataset_directory = os.path.join(current_directory, "dataset")
        self.offers_directory = os.path.join(dataset_directory, "offers")
        self.requests_directory = os.path.join(dataset_directory, "requests")

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
        self.init_dataset_offers()
        # dataset_filename = self.get_filename_from_category(2, 2)
        # if not os.path.isfile(dataset_filename):  # Check if dataset file exists
        #     self.init_category_dataset(2, 2)

    def init_dataset_offers(self):
        # Get all offers
        offers = self.database.executeQuery(
            Queries.getOffers(required_images=True))

        # Read all existing offers datasets features
        categories_dataset = MultiKeysDict()
        for dataset_file in list_images(self.offers_directory):
            (features, imgs_path) = self.image_matcher.load_dataset(dataset_file)
            category, subcategory = self.get_category_from_filename(
                dataset_file)

            categories_dataset.newItem(
                (features, imgs_path), category, subcategory)

        # Iterate on offers and append missing features
        modified_categories_ids = MultiKeysDict()
        for item in offers:
            offer = Offer(item)
            # Find dataset by category
            category_dataset = categories_dataset.readItem(
                offer.category, offer.subcategory)
            if category_dataset is None:
                category_dataset = ([], [])  # New empty category dataset
                categories_dataset.newItem(
                    category_dataset, offer.category, offer.subcategory)

            # Search for new images that aren't in dataset
            for image in offer.images:
                found = self.image_matcher.find_feature_by_image_path(
                    category_dataset, image)
                if found is None:
                    # TODO: download new image and append to dataset / create dataset
                    modified_categories_ids.newItem(
                        True, offer.category, offer.subcategory)  # Mark dataset as modified
            # Save updated datasets to file
            for category, subcategory in modified_categories_ids.items():
                pass

    def init_category_dataset(self, category_id, subcategory_id):
        # TODO: select all images
        imagesDir = None
        image_matcher.init_dataset(
            imagesDir, self.get_filename_from_category(category_id, subcategory_id))

    @staticmethod
    def get_filename_from_category(category_id, subcategory_id):
        return "{}/{}.hkl".format(category_id, subcategory_id)

    @staticmethod
    def get_category_from_filename(filename):
        splited = filename.split("/")
        category = splited[0]
        splited = filename.split(".")
        subcategory = splited[0]
        return (category, subcategory)


if __name__ == "__main__":
    some_class_object = someClass()

    requests = some_class_object.database.executeQuery(Queries.getRequests())
    matches = some_class_object.search_match_for_request(requests[0])
