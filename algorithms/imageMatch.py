from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
import numpy as np
from PIL import Image
import ntpath
from pathlib import Path

from services.loggerService import LoggerService
# from imutils.paths import list_images


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
        # features = {}
        # for img_path in list_images(source_dir):
        #     # Extract Features
        #     feature = self.extract(Image.open(img_path))
        #     # Extract image name
        #     image_name = os.path.basename(img_path)  # Extract name from path
        #     # image_name = os.path.splitext(image_name)[0]  # Extract extention from name
        #     # Save the Numpy array (.npy) on designated path
        #     features[image_name] = feature
        # return features


class ImageMatch(FeatureExtractor):
    def __init__(self):
        super().__init__()

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

        """
        
        Args:
            dataset: loaded dataset with (features, img_paths) tuple
            query features: result extracted image features 
        Returns:
            Matches results as dict with "image_path" as a key and "match score" as value
        """

    def calculate_matches(self, dataset, query_features):
        scores = {}
        features, img_paths = dataset
        features = np.array(features)
        # L2 distances to features
        dists = np.linalg.norm(features-query_features, axis=1)
        for index, score in enumerate(dists):
            scores[img_paths[index]] = score

        return scores

        """        
        Args:
            images: array of image_paths stings
            match_scores: result object from "calculate_matches"
        Returns:
            Best match score existing in the images array
        """

    def find_images_best_match(self, images, match_scores):
        lowest_distance = None
        for image in images:
            try:
                score = match_scores[image]
                if lowest_distance is None:
                    lowest_distance = score
                elif score < lowest_distance:
                    lowest_distance = score
            except:
                LoggerService.error(
                    "Critical Error - image {} doesn't exists in dataset".format(image))
                pass
        return lowest_distance

        """        
        Args:
            images: array of image_paths stings
            matches_scores_list: list of result object from "calculate_matches"
        Returns:
            Best match score existing in the images array
        """

    def find_images_best_matches(self, images, matches_scores_list):
        best_match = None
        for scores in matches_scores_list:
            score = self.find_images_best_match(images, scores)
            if score is not None:
                if best_match is None:
                    best_match = score
                elif score < best_match:
                    best_match = score

        return best_match
