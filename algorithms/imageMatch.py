from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
import numpy as np
import os
from PIL import Image
from imutils.paths import list_images
import ntpath
from pathlib import Path
import hickle as hkl

import cv2  # Temporary import (just for show)


class FeatureExtractor:
    def __init__(self):
        # Use VGG-16 as the architecture and ImageNet (pre-tranined model) for the weight
        base_model = VGG16(weights='imagenet')
        # Customize the model to return features from fully-connected layer
        self.model = Model(inputs=base_model.input,
                           outputs=base_model.get_layer('fc1').output)

    def extract(self, img):
        """
        Extract a deep feature from an input image
        Args:
            img: from PIL.Image.open(path) or tensorflow.keras.preprocessing.image.load_img(path)
        Returns:
            feature (np.ndarray): deep feature with the shape=(4096, )
        """
        img = img.resize((224, 224))  # VGG must take a 224x224 img as an input
        img = img.convert('RGB')  # Make sure img is color
        # To np.array. Height x Width x Channel. dtype=float32
        x = image.img_to_array(img)
        # (H, W, C)->(1, H, W, C), where the first elem is the number of img
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)  # Subtracting avg values for each pixel
        feature = self.model.predict(x)[0]  # (1, 4096) -> (4096, )
        return feature / np.linalg.norm(feature)  # Normalize

    def extractDirectory(self, source_dir):
        """
        Iterate threw directory and extract feature for each image
        Args:
            sourcePath: directory path            
        Returns:
            features dictonary
        """
        features = {}
        for img_path in list_images(source_dir):
            # Extract Features
            feature = self.extract(Image.open(img_path))
            # Extract image name
            image_name = os.path.basename(img_path)  # Extract name from path
            # image_name = os.path.splitext(image_name)[0]  # Extract extention from name
            # Save the Numpy array (.npy) on designated path
            features[image_name] = feature
        return features


class ImageMatch(FeatureExtractor):
    def __init__(self):
        super().__init__()

    def save_dataset(self, dataset, result_file, command_mode='w'):
        dataset_dict = self.convert_dataset_to_dict(dataset)
        hkl.dump(dataset_dict, result_file, command_mode)

    def load_dataset(self, dataset_path):
        if os.path.exists(dataset_path):
            dataset_dict = hkl.load(dataset_path)
        else:
            dataset_dict = {}
        return self.convert_dict_to_dataset(dataset_dict)

    def convert_dataset_to_dict(self, dataset):
        (features, img_paths) = dataset
        result = {}
        for index, img_path in enumerate(img_paths):
            result[img_path] = features[index]
        return result

    def convert_dict_to_dataset(self, dataset_dict):
        features = []
        img_paths = []

        for key, value in dataset_dict.items():
            features.append(value)
            img_paths.append(key)
        features = np.array(features)
        return (features, img_paths)

    def find_feature_by_image_path(self, dataset_tuple, image_path, start_index=0):
        (features, img_paths) = dataset_tuple
        feature = None
        try:
            index = img_paths.index(image_path, start_index)
            feature = features[index]
        except ValueError:
            pass
        finally:
            return feature

    # TODO pass Image opened object instand of path
    #
        """
        Iterate threw directory and extract feature for each image
        Args:
            dataset: loaded dataset with (features, img_paths) tuple
            img: from PIL.Image.open(path) or tensorflow.keras.preprocessing.image.load_img(path)
        Returns:
            list with match perectage for each feature
        """

    def calculate_matches(self, dataset, img):
        features, img_paths = dataset
        # Calculate new image features
        query_features = self.extract(img)

        # L2 distances to features
        dists = np.linalg.norm(features-query_features, axis=1)
        ids = np.argsort(dists)  # Ascending sort
        scores = [(dists[id], img_paths[id]) for id in ids]
        return scores


DATASET_FILE_NAME = "dataset.hkl"

dirname = os.path.dirname(__file__)
images_dir = os.path.join(dirname, "testImages")
TEMPORARY_IMAGE_DIR = images_dir


def showImage(image_path, name="result-image"):
    image = cv2.imread(os.path.join(images_dir, image_path))
    image = cv2.resize(image, (600, 600))
    cv2.imshow(name, image)


if __name__ == "__main__":
    image_matcher = ImageMatch()
    if not os.path.isfile(DATASET_FILE_NAME):
        image_matcher.save_dataset(images_dir, DATASET_FILE_NAME)
    scores = image_matcher.search(
        DATASET_FILE_NAME, os.path.join(images_dir, "images (61).jpg"))

    print(scores)
    for score in scores:
        print("Match with {} perecentage {}".format(score[1], score[0]))
        showImage(score[1])
        cv2.waitKey(0)
