# Imports for image describe
import mahotas
from imutils.paths import list_images
import numpy as np
import argparse
import pickle
import imutils
import cv2
import os
import ntpath


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

    # Initialize a descriptor
    descriptor = ImageDescriptor(21)

    for imagePath in list_images(sourcePath):
        image = cv2.imread(imagePath)
        # convert it to grayscale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # pad the image with extra white pixels to ensure the
        # edges of the image are not up against the borders
        # of the image
        image = cv2.copyMakeBorder(image, 15, 15, 15, 15,
                                   cv2.BORDER_CONSTANT, value=255)
        # invert the image and threshold it
        thresh = cv2.bitwise_not(image)
        thresh[thresh > 0] = 255


dirname = os.path.dirname(__file__)
sourceDir = os.path.join(dirname, "testImages")
destDir = os.path.join(dirname, "result")
indexDataset(sourceDir, destDir)
print("done")
