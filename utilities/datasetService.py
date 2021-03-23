import hickle as hkl
import os

from services.loggerService import LoggerService

DATASET_FEATURES_INDEX = 0
DATASET_IMAGE_NAME_INDEX = 1


class DatasetService(object):
    # Appending isn't an open becuase we uses a dict in order to load all objects at once
    @staticmethod
    def save_dataset(dataset, dataset_path, command_mode='w'):
        dataset_dict = DatasetService.convert_dataset_to_dict(dataset)

        dir_path = os.path.dirname(dataset_path)
        if os.path.exists(dir_path) == False:
            os.makedirs(dir_path)

        hkl.dump(dataset_dict, dataset_path, command_mode)

    @staticmethod
    def load_dataset(dataset_path):
        if os.path.exists(dataset_path):
            dataset_dict = hkl.load(dataset_path)
        else:
            dataset_dict = {}
        dataset = DatasetService.convert_dict_to_dataset(dataset_dict)
        return dataset

    @staticmethod
    def new_dataset():
        return ([], [])

    @staticmethod
    def add_item_to_dataset(dataset, feature, img_path):
        dataset[DATASET_FEATURES_INDEX].append(feature)
        dataset[DATASET_IMAGE_NAME_INDEX].append(img_path)

    @staticmethod
    def delete_item_from_dataset(dataset, img_path):
        try:
            index = dataset[DATASET_IMAGE_NAME_INDEX].index(img_path)
            del dataset[DATASET_FEATURES_INDEX][index]
            del dataset[DATASET_IMAGE_NAME_INDEX][index]
        except ValueError:  # image not found
            LoggerService.error(
                "Error at delete image from dataset image: {} not found".format(img_path))

    @staticmethod
    def merge_datasets(dataset1, dataset2):
        (features1, img_paths1) = dataset1
        (features2, img_paths2) = dataset2

        new_features = features1 + features2
        new_img_paths = img_paths1 + img_paths2

        return (new_features, new_img_paths)

    @staticmethod
    def print_dataset(dataset):
        (features, img_paths) = dataset
        for img_path in img_paths:
            LoggerService.debug(img_path)

    @staticmethod
    def is_dataset_empty(dataset):
        if not dataset:
            return True
        (features, img_paths) = dataset
        return len(img_paths) == 0 or len(features) == 0

    @staticmethod
    def convert_dataset_to_dict(dataset):
        (features, img_paths) = dataset
        result = {}
        for index, img_path in enumerate(img_paths):
            result[img_path] = features[index]
        return result

    @staticmethod
    def convert_dict_to_dataset(dataset_dict):
        features = []
        img_paths = []

        for key, value in dataset_dict.items():
            features.append(value)
            img_paths.append(key)
        return (features, img_paths)
