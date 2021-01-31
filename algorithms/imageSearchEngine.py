from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
import numpy as np
import os
from PIL import Image
from imutils.paths import list_images
import ntpath


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


dirname = os.path.dirname(__file__)
dataset_dir = os.path.join(dirname, "dataset")
features_dir = os.path.join(dirname, "features")


fe = FeatureExtractor()
# Iterate through images (Change the path based on your image location)
for img_path in list_images(dataset_dir):
    # Extract Features
    feature = fe.extract(img=Image.open(img_path))
    # Extract image name
    image_name = os.path.basename(img_path)  # Extract name from path
    image_name = os.path.splitext(image_name)[0]  # Extract extention from name
    # Save the Numpy array (.npy) on designated path
    feature_path = os.path.join(features_dir, "{}.npy".format(image_name))
    np.save(feature_path, feature)
    print("formated {}".format(feature_path))
