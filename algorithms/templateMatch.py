import cv2
import os
import ntpath
from imutils.paths import list_images


def getFeature(imagePath):
    return {}


def compareFeatures(feature1, feature2):
    return 100


if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    dirPath = os.path.join(dirname, "testImages")
    queryImagePath = os.path.join(dirPath, "ball.jpg")

    resultIndexes = {}
    for imagePath in list_images(dirPath):
        imageName = ntpath.basename(imagePath)
        resultIndexes[imageName] = getFeature(imagePath)

    queryFeatures = getFeature(queryImagePath)
    results = {}
    for(k, features) in resultIndexes.items():
        results[k] = compareFeatures(features, queryFeatures)

    results = sorted([(v, k) for (k, v) in results.items()])
    print(results)
