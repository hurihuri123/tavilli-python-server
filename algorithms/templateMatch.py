import cv2
import os
import ntpath
from imutils.paths import list_images
import numpy as np
# from skimage.measure import structural_similarity as ssim


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    height, width = imageA.shape
    imageB = cv2.resize(imageB, (width, height))
    diff = cv2.absdiff(imageA, imageB)

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return diff.sum()


class Features():
    def __init__(self):
        super().__init__()

    def getFeature(self, imagePath):
        image = cv2.imread(imagePath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    def compareFeatures(self, feature1, feature2):
        return mse(feature1, feature2)


class Search():
    def __init__(self, getFeature, compareFeatures):
        super().__init__()
        self.getFeature = getFeature
        self.compareFeatures = compareFeatures

    def match(self, queryPath):
        resultIndexes = {}
        for imagePath in list_images(dirPath):
            imageName = ntpath.basename(imagePath)
            resultIndexes[imageName] = self.getFeature(imagePath)

        queryFeatures = self.getFeature(queryPath)
        results = {}
        for(k, features) in resultIndexes.items():
            results[k] = self.compareFeatures(features, queryFeatures)

        results = sorted([(v, k) for (k, v) in results.items()])
        return results


if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    dirPath = os.path.join(dirname, "testImages")
    queryImagePath = os.path.join(dirPath, "identical1.jpg")

    features = Features()
    searcher = Search(features.getFeature, features.compareFeatures)
    print(searcher.match(queryImagePath))
