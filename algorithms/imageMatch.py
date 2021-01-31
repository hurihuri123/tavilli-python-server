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


def showImage(image_path, name="result-image"):
    image = cv2.imread(os.path.join(images_dir, image_path))
    image = cv2.resize(image, (600, 600))
    cv2.imshow(name, image)


class FeatureExtractor:
    def __init__(self):
        # Use VGG-16 as the architecture and ImageNet (pre-tranined model) for the weight
        base_model = VGG16(weights='imagenet')
        # Customize the model to return features from fully-connected layer
        self.model = Model(inputs=base_model.input,
                           outputs=base_model.get_layer('fc1').output)

    def extract(self, img_path):
        """
        Extract a deep feature from an input image
        Args:
            img: 
        Returns:
            feature (np.ndarray): deep feature with the shape=(4096, )
        """
        # open image with PIL.Image.open(path) or tensorflow.keras.preprocessing.image.load_img(path)
        img = Image.open(img_path)
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
            feature = self.extract(img_path)
            # Extract image name
            image_name = os.path.basename(img_path)  # Extract name from path
            # image_name = os.path.splitext(image_name)[0]  # Extract extention from name
            # Save the Numpy array (.npy) on designated path
            features[image_name] = feature
        return features


dirname = os.path.dirname(__file__)
images_dir = os.path.join(dirname, "testImages")
dataset_path = "dataset.hkl"

queryPath = os.path.join(images_dir, "images (61).jpg")

fe = FeatureExtractor()
# features = fe.extractDirectory(images_dir)
# hkl.dump(features, dataset_path)
# np.save(dataset_path, features)

dataset = hkl.load(dataset_path)

features = []
img_paths = []
for key, value in dataset.items():
    features.append(value)
    img_paths.append(key)
features = np.array(features)

# TODO: download query image

# Calculate query features
query_features = fe.extract(queryPath)

# Perform search
# L2 distances to features
dists = np.linalg.norm(features-query_features, axis=1)
ids = np.argsort(dists)[:30]  # Top 30 results
scores = [(dists[id], img_paths[id]) for id in ids]

print(scores)
for score in scores:
    print("Match with {} perecentage {}".format(score[1], score[0]))
    showImage(score[1])
    cv2.waitKey(0)