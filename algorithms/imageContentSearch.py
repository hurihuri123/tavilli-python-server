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


# Create a thresholded image
def getImageMask(imagePath):
    image = cv2.imread(imagePath)
    # convert it to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # pad the image with extra white pixels to ensure the
    # edges of the image are not up against the borders
    # of the image
    image = cv2.copyMakeBorder(image, 15, 15, 15, 15,
                               cv2.BORDER_CONSTANT, value=255)

    return image


def getImageOutline(maskedImage):
    # invert the image and threshold it
    thresh = cv2.bitwise_not(maskedImage)
    thresh[thresh > 0] = 255

    # Create a blanck image to store our outline
    outline = np.zeros(maskedImage.shape, dtype="uint8")
    # Find the outermost contours
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    # handles parsing the contours for various versions of OpenCV.
    cnts = imutils.grab_contours(cnts)
    # sort contours descending order and keep the largest
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
    cv2.drawContours(outline, [cnts], -1, 255, -1)

    return outline


def indexDataset(dirPath):
    # Variable Definition
    resultIndexes = {}

    # Initialize a descriptor
    descriptor = ImageDescriptor(21)

    for imagePath in list_images(dirPath):
        imageName = ntpath.basename(imagePath)
        image = getImageMask(imagePath)
        height, width = image.shape
        outlilne = getImageOutline(image)
        try:
            resultIndexes[imageName] = descriptor.describeByShape(outlilne)
        except Exception as err:
            # Probably too large image for our system (under linux we can set a flag to prevent this issue)
            print("Error indexing image {} , err: {}".format(imageName, err))

    return resultIndexes


dirname = os.path.dirname(__file__)
dirPath = os.path.join(dirname, "testImages")
resultFolder = os.path.join(dirname, "indexedImages")

imagesVectors = indexDataset(dirPath)

# TODO: generic create/open folder and write bytes function
if not os.path.exists(resultFolder):
    os.makedirs(resultFolder)
f = open(resultFolder, "wb")
f.write(pickle.dumps(imagesVectors))
f.close()


print("done")
