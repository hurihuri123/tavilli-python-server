from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
import numpy as np
import os
from PIL import Image
from imutils.paths import list_images
import ntpath
from pathlib import Path


class FeatureExtractor:
    def __init__(self):
        base_model = VGG16(weights='imagenet')
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


# Build features dataset
# Iterate through images (Change the path based on your image location)

    def extractDirectory(self, sourcePath, destPath):
        for img_path in list_images(dataset_dir):
            # Extract Features
            feature = self.extract(img=Image.open(img_path))
            # Extract image name
            image_name = os.path.basename(img_path)  # Extract name from path
            # image_name = os.path.splitext(image_name)[0]  # Extract extention from name
            # Save the Numpy array (.npy) on designated path
            feature_path = os.path.join(
                features_dir, "{}.npy".format(image_name))
            np.save(feature_path, feature)
            print("formated {}".format(feature_path))


dirname = os.path.dirname(__file__)
dataset_dir = os.path.join(dirname, "testImages")
features_dir = os.path.join(dirname, "features")

queryPath = os.path.join(dataset_dir, "identical1.jpg")

fe = FeatureExtractor()
# fe.extractDirectory(dataset_dir, features_dir)


# Read features from dataset to memory
features = []
img_paths = []
for feature_path in Path(features_dir).glob("*.npy"):
    features.append(np.load(feature_path))
    img_paths.append(os.path.join(dataset_dir, feature_path.stem))
features = np.array(features)

# TODO: download query image

# Calculate query features
query_features = fe.extract(img=Image.open(queryPath))

# Perform search
# L2 distances to features
dists = np.linalg.norm(features-query_features, axis=1)
ids = np.argsort(dists)[:30]  # Top 30 results
scores = [(dists[id], img_paths[id]) for id in ids]
print(scores)
