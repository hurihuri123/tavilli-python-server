# Imports for image describe
import mahotas
from imutils.paths import list_images
import numpy as np
import argparse
import pickle
import imutils
import cv2


class ImageDescriptor:
    def __init__(self, radius):
        super().__init__()
        # The radius of the polynomial in pixels
        # The larger the radius the more pixels will be included in the computation
        self.radius = radius  # Used when computing moments

    def describeByColor(self, image):
        return None  # Not implemeneted

    def describeByShape(self, image):
        # return the Zernike moments for the image
        return mahotas.features.zernike_moments(image, self.radius)


def indexDataset(sourcePath, resultPath):
    # Variable Definition
    resultIndexes = {}

    # Initialization - construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", sourcePath, required=True,
                    help="Path where the sprites will be stored")
    ap.add_argument("-i", resultPath, required=True,
                    help="Path to where the index file will be stored")
    args = vars(ap.parse_args())

    # Initialize a descriptor
    descriptor = ImageDescriptor(21)

    # Loop over the sprite images
    for spritePath in list_images(args["sprites"]):
        # parse out the image name, then load the image and
        # convert it to grayscale
        pokemon = spritePath[spritePath.rfind("/") + 1:].replace(".png", "")
        image = cv2.imread(spritePath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # pad the image with extra white pixels to ensure the
        # edges of the image are not up against the borders
        # of the image
        image = cv2.copyMakeBorder(image, 15, 15, 15, 15,
                                   cv2.BORDER_CONSTANT, value=255)
        # invert the image and threshold it
        thresh = cv2.bitwise_not(image)
        thresh[thresh > 0] = 255
