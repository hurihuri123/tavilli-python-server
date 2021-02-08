from utilities.mySql import MySqlConnector
from utilities.multiKeysDict import MultiKeysDict
from utilities.queries import Queries, OFFERS_TABLE, REQUESTS_TABLE, MATCH_FIELDS, CATEGORY_FIELD, SUBCATEGORY_FIELD, Offer, Request, REQUEST_OBJECT_NAME, OFFER_OBJECT_NAME
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
import numpy as np


# TODO: doc and change name
DATASET_FILE_EXTENTION = "hkl"

CONFIG_LAST_REQUEST_ID_KEY = "lastRequestId"
CONFIG_LAST_OFFER_ID_KEY = "lastOfferId"
MIN_MATCH_RATE = 0


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

        self.init_datasets()

    def init_datasets(self):
        new_offers = self.init_dataset_offers()
        new_requests = self.init_dataset_requests()
        matches = []
        for request in new_requests:
            matches = matches + self.search_matches(item=request, other_item_type=Offer,
                                                    select_other_items_callback=Queries.getOffers, other_items_dir=self.offers_directory)
        for offer in new_offers:
            matches = matches + self.search_matches(item=offer, other_item_type=Request,
                                                    select_other_items_callback=Queries.getRequests, other_items_dir=self.requests_directory)
        # TODO: search for duplications
        for match in matches:
            print(match)

    def init_dataset_requests(self):
        return self.init_dataset(config_last_item_key=CONFIG_LAST_REQUEST_ID_KEY,
                                 select_items_callback=Queries.getRequests,
                                 item_type=Request, items_directory_path=self.requests_directory)

    def init_dataset_offers(self):
        return self.init_dataset(config_last_item_key=CONFIG_LAST_OFFER_ID_KEY,
                                 select_items_callback=Queries.getOffers,
                                 item_type=Offer, items_directory_path=self.offers_directory)

        """
        1.Select new requests (that probably posted while service was off)
        2.Extract new requests features and save to dataset
        Args:
        Returns:
            List with new requests objects
        """

    def init_dataset(self, config_last_item_key, select_items_callback, item_type, items_directory_path):
        new_items = []
        categories_dataset = MultiKeysDict()
        categories_with_images_ids = MultiKeysDict()

        last_handled_item_id = self.config_parser.read_config_value(
            config_last_item_key)
        # Select new items
        items = self.database.executeQuery(
            select_items_callback(start_id=last_handled_item_id))
        # Map each json to request object
        items = map(lambda item: item_type(item), items)
        # Map each new request to dataset object
        for item in items:
            # Find dataset by category
            category_dataset = self.find_or_create_category_dataset(
                categories_dataset, item.category, item.subcategory)

            for image in item.images:
                # Download image and extract it's features
                image_features = self.image_matcher.extract(
                    img=Image.open(get_image_from_url(image)))
                # Append new item to dataset
                category_dataset = self.image_matcher.merge_datasets(
                    category_dataset, (image_features, image))
                # Mark that category has image
                categories_with_images_ids.newItem(
                    True, item.category, item.subcategory)

            new_items.append(item)

        # Save new request's features to dataset files
        for category, subcategories in categories_with_images_ids.items():
            for subcategory in subcategories:
                category_dataset = categories_dataset.readItem(
                    category, subcategory)
                filename = self.get_filename_from_category(
                    category, subcategory)
                # Load existing stored dataset
                dataset = self.image_matcher.load_dataset(filename)
                # Append new features to dataset dict
                dataset = self.image_matcher.merge_datasets(
                    dataset1=dataset, dataset2=category_dataset)
                # Save changes to file
                self.image_matcher.save_dataset(
                    dataset, os.path.join(items_directory_path, filename))

        if len(new_items) > 0:
            # Get highest request id (requests are ordered by ascending ID)
            last_item = new_items[-1]
            self.config_parser.write_config_value(
                config_last_item_key, last_item.id)

        return new_items

    def search_matches(self, item, other_item_type, select_other_items_callback, other_items_dir):
        # TODO: select filter by item price as well
        other_items = self.database.executeQuery(select_other_items_callback(
            item.category, item.subcategory))
        other_items = map(lambda other_item: other_item_type(
            other_item), other_items)

        match_images_results = []
        item_images = item.images
        if(len(item_images) > 0):
            # Load  images dataset according to item category
            dataset_path = os.path.join(other_items_dir, self.get_filename_from_category(
                item.category, item.subcategory))
            dataset = self.image_matcher.load_dataset(dataset_path)
            is_dataset_empty = self.image_matcher.is_dataset_empty(dataset)
            new_features_dataset = self.image_matcher.new_dataset()

            for image in item_images:
                image_features = self.image_matcher.find_feature_by_image_path(
                    dataset, image)
                if image_features is None:
                    # Download image and extract it's features
                    image_features = self.image_matcher.extract(
                        img=Image.open(get_image_from_url(image)))
                    new_features_dataset = self.image_matcher.merge_datasets(
                        new_features_dataset, (image_features, image))

                if is_dataset_empty == False:
                    # Calculate image match percatage
                    image_matches = self.image_matcher.calculate_matches(
                        dataset, image_features)
                    match_images_results.append(image_matches)

            # Append new features to dataset dict
            dataset = self.image_matcher.merge_datasets(
                dataset1=dataset, dataset2=new_features_dataset)
            # Save changes to file
            self.image_matcher.save_dataset(
                dataset, dataset_path)

        matches = []
        for other_item in other_items:
            # Find best 2 images matches
            images_match_score = self.image_matcher.find_images_best_matches(
                other_item.images, match_images_results)

            if item.__str__() == REQUEST_OBJECT_NAME:
                match = Match(request=item, offer=other_item,
                              images_distance=images_match_score)
            else:
                match = Match(
                    request=other_item, offer=item, images_distance=images_match_score)

            if(match.matchPercantage >= MIN_MATCH_RATE):
                matches.append(match)
                # TODO: see if passing request + offer id would be enough instand of all object
        return matches

    def find_or_create_category_dataset(self,  categories_dataset, category, subcategory):
        category_dataset = categories_dataset.readItem(
            category, subcategory)
        if category_dataset is None:
            # New empty category dataset
            category_dataset = self.image_matcher.new_dataset()
            categories_dataset.newItem(
                category_dataset, category, subcategory)
        return category_dataset

    @ staticmethod
    def get_filename_from_category(category_id, subcategory_id):
        return "{}_{}.{}".format(category_id, subcategory_id, DATASET_FILE_EXTENTION)

    @ staticmethod
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
