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
        self.sift = cv2.xfeatures2d.SIFT_create()

    def describeByColor(self, image):
        return None  # Not implemeneted

    def describeByShape(self, image):
        # return the Zernike moments for the image
        kp, des = self.sift.detectAndCompute(image, None)
        return des

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
    # image = getImageMask(imagePath)
    # outlilne = getImageOutline(image)
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

    # Initialize a descriptor
    descriptor = ImageDescriptor(radius)
    # Temporary convert to list and iterate on 5
    # in list(list_images(dirPath))[:2]
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
        self.bf = cv2.BFMatcher()

    def search(self, queryFeatures):
        results = {}

        # loop over the images in our index
        for(k, features) in self.index.items():
            # compute the distance between the query features
            # and features in our index, then update the results
            matches = self.bf.knnMatch(queryFeatures, features, k=2)
            totalDistance = 0
            # Apply ratio test
            good = []
            for m, n in matches:
                if m.distance < 0.75*n.distance:
                    good.append(m)

            totalDistance = 0
            for g in good:
                totalDistance += g.distance

            results[k] = totalDistance
            print("searching match for query image with {} , distance: {}".format(
                k, results[k]))

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
    dirPath, "jeremy-alford-EfLwt5Xz5Ek-unsplash.jpg")
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
    print("match of {}% for image {}".format(
        result[0], result[1].upper()))
    showImage(result[1])
    cv2.waitKey(0)
