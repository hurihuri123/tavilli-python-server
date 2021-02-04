from utilities.mySql import MySqlConnector
from utilities.multiKeysDict import MultiKeysDict
from utilities.queries import Queries, OFFERS_TABLE, REQUESTS_TABLE, MATCH_FIELDS, CATEGORY_FIELD, SUBCATEGORY_FIELD, Offer, Request
from utilities.utilities import get_image_from_url
from utilities.configParser import ConfigParser

from config.config import DATABASE_HOST, DATABASE_USERNAME, DATEBASE_PASSWORD, DATABASE_NAME


from algorithms.match import Match
from algorithms.imageMatch import ImageMatch

from config.config import *
from imutils.paths import list_images

from PIL import Image
import os
from pathlib import Path

# TODO: doc and change name
DATASET_FILE_EXTENTION = "hkl"

CONFIG_LAST_REQUEST_ID_KEY = "lastRequestId"


class someClass():
    def __init__(self):
        super().__init__()
        self.database = MySqlConnector(
            DATABASE_HOST, DATABASE_USERNAME, DATEBASE_PASSWORD, DATABASE_NAME)
        self.image_matcher = ImageMatch()
        self.config_parser = ConfigParser()

        current_directory = os.path.dirname(__file__)
        dataset_directory = os.path.join(current_directory, "dataset")
        self.offers_directory = os.path.join(dataset_directory, "offers")
        self.requests_directory = os.path.join(dataset_directory, "requests")

        # self.init_datasets()

    def init_datasets(self):
        new_offers = self.init_dataset_offers()
        new_requests = self.init_dataset_requests()
        for request in new_requests:
            matches = self.search_match_for_request(request)

    def init_dataset_requests(self):
        new_requests = []
        categories_dataset = MultiKeysDict()
        categories_with_images_ids = MultiKeysDict()

        last_handled_request_id = self.config_parser.read_config_value(
            CONFIG_LAST_REQUEST_ID_KEY)
        # Get new requests
        requests = self.database.executeQuery(
            Queries.getRequests(start_id=last_handled_request_id))
        # Map each json to request object
        requests = map(lambda item: Request(item), requests)
        # Map each new request to dataset object
        for request in requests:
            # Find dataset by category
            category_dataset = self.find_or_create_category_dataset(
                categories_dataset, request.category, request.subcategory)

            for image in request.images:
                # Download image and extract it's features
                image_features = self.image_matcher.extract(
                    img=Image.open(get_image_from_url(image)))
                # Append features to dataset array
                category_dataset[0].append(image_features)
                # Append Image to images array
                category_dataset[1].append(image)
                # Mark that category has image
                categories_with_images_ids.newItem(
                    True, request.category, request.subcategory)

            new_requests.append(request)

        # Save new request's features to dataset files
        for category, subcategories in categories_with_images_ids.items():
            for subcategory in subcategories:
                category_dataset = categories_dataset.readItem(
                    category, subcategory)
                filename = self.get_filename_from_category(
                    category, subcategory)
                # Write/Append new feature to dataset flie
                self.image_matcher.save_dataset(
                    category_dataset, os.path.join(self.requests_directory, filename), 'a')

        if len(new_requests) > 0:
            # Get highest request id (requests are ordered by ascending ID)
            last_request = new_requests[-1]
            self.config_parser.write_config_value(
                CONFIG_LAST_REQUEST_ID_KEY, last_request.id)

        return new_requests

    def init_dataset_offers(self):
        new_offers = []
        # Get all offers
        offers = self.database.executeQuery(
            Queries.getOffers())
        # Map each json to offer object
        offers = map(lambda item: Offer(item), offers)

        # Read all existing offers datasets features
        categories_dataset = MultiKeysDict()
        for dataset_file in Path(self.offers_directory).glob("*.{}".format(DATASET_FILE_EXTENTION)):
            (features, imgs_path) = self.image_matcher.load_dataset(dataset_file)
            category, subcategory = self.get_category_from_filename(
                dataset_file.stem)

            categories_dataset.newItem(
                (features, imgs_path), category, subcategory)

        # Iterate on offers and append missing features
        modified_categories_ids = MultiKeysDict()
        for offer in offers:
            # Find dataset by category
            category_dataset = self.find_or_create_category_dataset(
                categories_dataset, offer.category, offer.subcategory)

            # Search for new images that aren't in dataset
            for image in offer.images:
                found = self.image_matcher.find_feature_by_image_path(
                    category_dataset, image)
                if found is None:
                    # Download image and extract it's features
                    image_features = self.image_matcher.extract(
                        img=Image.open(get_image_from_url(image)))
                    # Append features to dataset
                    category_dataset[0].append(image_features)
                    # Append Image to images array
                    category_dataset[1].append(image)
                    # Mark dataset as modified
                    modified_categories_ids.newItem(
                        True, offer.category, offer.subcategory)
            new_offers.append(offer)

        # Save updated datasets to file
        for category, subcategories in modified_categories_ids.items():
            for subcategory in subcategories:
                category_dataset = categories_dataset.readItem(
                    category, subcategory)

                filename = self.get_filename_from_category(
                    category, subcategory)
                self.image_matcher.save_dataset(
                    category_dataset, os.path.join(self.offers_directory, filename))

        return new_offers

    def search_match_for_request(self, request):
        matches = []
        # TODO: select filter by request price as well
        # Select offers according to request info
        offers = self.database.executeQuery(Queries.getOffers(
            request.category, request.subcategory))
        request_images = request.images
        if(len(list(request_images)) > 0):  # Convert map object to list and check length
            # Load offers images dataset according to request category
            dataset_path = os.path.join(self.offers_directory, self.get_filename_from_category(
                request.category, request.subcategory))
            dataset = self.image_matcher.load_dataset(dataset_path)
            for image in request_images:
                # Download and open image
                img = Image.open(get_image_from_url(image))
                # Calculate image match percatage
                image_matches = self.image_matcher.calculate_matches(
                    dataset, img)
                # TODO: set highest match for each offer

        # Compare dataset with query features
        for offer in offers:
            # Find related offer matches results
            # Pass list of images matches results to match object (might be more than one image)
            match = Match(request, offer)
            if(match.matchPercantage > 70):
                matches.append(match)
        return matches

    def find_or_create_category_dataset(self,  categories_dataset, category, subcategory):
        category_dataset = categories_dataset.readItem(
            category, subcategory)
        if category_dataset is None:
            category_dataset = ([], [])  # New empty category dataset
            categories_dataset.newItem(
                category_dataset, category, subcategory)
        return category_dataset

    def search_match_for_offer(self, offer):
        pass

    def new_request(self):
        pass
        # TODO: update "lastRequestId field"

    def new_offer(self):
        pass

    @staticmethod
    def get_filename_from_category(category_id, subcategory_id):
        return "{}_{}.{}".format(category_id, subcategory_id, DATASET_FILE_EXTENTION)

    @staticmethod
    def get_category_from_filename(filename):
        splited = filename.split("_")
        if len(splited) >= 2:
            category = int(splited[0])
            splited = splited[1].split(".")
            subcategory = int(splited[0])
        else:
            category = -1
            subcategory = -1

        return (category, subcategory)


if __name__ == "__main__":
    some_class_object = someClass()
    requests = some_class_object.database.executeQuery(Queries.getRequests())
    requests = map(lambda item: Request(item), requests)
    for request in requests:
        matches = some_class_object.search_match_for_request(request)
