# Imports for image describe
from imutils.paths import list_images

import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
import pickle

# Imports for comparing algorithm

# Global imports
import sys
# from utilities.helper import Helper

INDEX_IMAGE_RADIUS = 21
isOrb = False


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
        # Initiate SIFT detector
        self.descriptor = cv2.ORB_create() if isOrb else cv2.xfeatures2d.SIFT_create()

    def describeByColor(self, image):
        return None  # Not implemeneted

    def describeByShape(self, image):
        kp, des = self.descriptor.detectAndCompute(image, None)
        return des


def getShapeIndex(imagePath, descriptorCallback):
    resultIndex = None
    image = cv2.imread(imagePath, 0)
    try:
        resultIndex = descriptorCallback(image)
    except Exception as err:
        # Probably too large image for our system (under linux we can set a flag to prevent this issue)
        print("Error indexing image {} , err: {}".format(imagePath, err))
    finally:
        return resultIndex


def indexDataset(dirPath, radius):
    # Variable Definition
    resultIndexes = {}

    descriptor = ImageDescriptor(radius)
    for imagePath in list_images(dirPath):
        imageName = os.path.basename(imagePath)
        index = getShapeIndex(
            imagePath, descriptor.describeByShape)
        if index is not None:
            resultIndexes[imageName] = index

    return resultIndexes


class Searcher:
    def __init__(self, index):
        super().__init__()
        # store the pre-computed features index that we will be searching over
        self.index = index
        self.bf = cv2.BFMatcher(
            cv2.NORM_HAMMING, crossCheck=True) if isOrb else cv2.BFMatcher()

    def knnMatch(self, features1, features2):
        # compute the distance between the query features
        # and features in our index, then update the results
        matches = self.bf.knnMatch(features1, features2, k=2)
        # Apply ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.75*n.distance:
                good.append(m)
        matchPercentage = len(good) / len(matches) * 100
        return matchPercentage

    def bfMatch(self, features1, features2):
        # compute the distance between the query features
        # and features in our index, then update the results
        matches = self.bf.match(features1, features2)
        # Apply ratio test
        distance = 0
        for g in matches:
            distance += g.distance
        return distance

    def search(self, queryFeatures):
        results = {}
        # loop over the images in our index
        for(k, features) in self.index.items():
            results[k] = self.bfMatch(queryFeatures, features) if isOrb else self.knnMatch(
                queryFeatures, features)

        # sort our results, where a smaller distance indicates higher similarity
        results = sorted([(v, k) for (k, v) in results.items()])
        if not isOrb:
            results = reversed(results)  # Sort ascending (top->down)
        return results


def showImage(imPath, name="result-image"):
    image = cv2.imread(os.path.join(dirPath, imPath))
    image = cv2.resize(image, (600, 600))
    cv2.imshow(name, image)


# TODO - think about the right modules organization for maximum abstraction and future easy uses
dirname = os.path.dirname(__file__)
dirPath = os.path.join(dirname, "testImages")
queryImagePath = os.path.join(
    dirPath, "images (63).jpg")
resultIndex = os.path.join(dirname, "imagesIndexes")

imagesVectors = indexDataset(dirPath, INDEX_IMAGE_RADIUS)
writeBinaryToFile(resultIndex, pickle.dumps(imagesVectors))

loadedIndex = readBinaryFromFile(resultIndex)
loadedIndex = pickle.loads(loadedIndex)

descriptor = ImageDescriptor(INDEX_IMAGE_RADIUS)
queryFeatures = getShapeIndex(queryImagePath, descriptor.describeByShape)

searchInstance = Searcher(loadedIndex)
results = searchInstance.search(queryFeatures)


showImage(queryImagePath, "queryImage")
cv2.waitKey(0)
for result in results:
    print("Match with {} perecentage {}".format(result[1], result[0]))
    showImage(result[1])
    cv2.waitKey(0)
