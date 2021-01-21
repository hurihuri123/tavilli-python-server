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

# Imports for comparing algorithm
from scipy.spatial import distance as dist

# Global imports
import sys
# from utilities.helper import Helper

INDEX_IMAGE_RADIUS = 21


# TODO - use this function from 'utilities' (will work when starting module from main)
def writeBinaryToFile(filePath, data):
    f = open(filePath, "wb")
    f.write(data)
    f.close()


def readBinaryFromFile(filePath):
    f = open(filePath, "rb")
    data = f.read()
    f.close()
    return data
# -----------


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
    image = cv2.resize(image, (64, 64))
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


def getShapeIndex(imagePath, descriptorCallback):
    resultIndex = None
    image = getImageMask(imagePath)
    outlilne = getImageOutline(image)

    try:
        resultIndex = descriptorCallback(outlilne)
    except Exception as err:
        # Probably too large image for our system (under linux we can set a flag to prevent this issue)
        print("Error indexing image {} , err: {}".format(imagePath, err))
    finally:
        return resultIndex


def indexDataset(dirPath, radius):
    # Variable Definition
    resultIndexes = {}

    # Initialize a descriptor
    descriptor = ImageDescriptor(radius)

    for imagePath in list_images(dirPath):
        imageName = ntpath.basename(imagePath)
        index = getShapeIndex(
            imagePath, descriptor.describeByShape)

        if index is not None:
            print(index)
            resultIndexes[imageName] = index

    return resultIndexes


class Searcher:
    def __init__(self, index):
        super().__init__()
        # store the pre-computed features index that we will be searching over
        self.index = index

    def search(self, queryFeatures):
        results = {}

        # loop over the images in our index
        for(k, features) in self.index.items():
            # compute the distance between the query features
            # and features in our index, then update the results
            d = dist.euclidean(queryFeatures, features)
            results[k] = d

            # sort our results, where a smaller distance indicates higher similarity
        results = sorted([(v, k) for (k, v) in results.items()])

        return results


def showImage(imPath, name="result-image"):
    image = cv2.imread(os.path.join(dirPath, imPath))
    image = cv2.resize(image, (600, 600))
    cv2.imshow(name, image)


# TODO - think about the right modules organization for maximum abstraction and future easy uses
dirname = os.path.dirname(__file__)
dirPath = os.path.join(dirname, "testImages")
queryImagePath = os.path.join(
    dirPath, "revolt-164_6wVEHfI-unsplash.jpg")
resultIndex = os.path.join(dirname, "imagesIndexes")

imagesVectors = indexDataset(dirPath, INDEX_IMAGE_RADIUS)
writeBinaryToFile(resultIndex, pickle.dumps(imagesVectors))

loadedIndex = readBinaryFromFile(resultIndex)
loadedIndex = pickle.loads(loadedIndex)

descriptor = ImageDescriptor(INDEX_IMAGE_RADIUS)
queryFeatures = getShapeIndex(queryImagePath, descriptor.describeByShape)

searchInstance = Searcher(loadedIndex)
results = searchInstance.search(queryFeatures)

results = results[:5]  # Temporary take only top 5 matches
showImage(queryImagePath, "queryImage")
cv2.waitKey(0)
for result in results:
    print("match of {}% for image {}".format(
        result[0], result[1].upper()))
    showImage(result[1])
    cv2.waitKey(0)
