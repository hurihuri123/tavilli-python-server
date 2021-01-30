import cv2
import os
import ntpath
from imutils.paths import list_images


def getFeature(imagePath):
    return {}


dirname = os.path.dirname(__file__)
dirPath = os.path.join(dirname, "testImages")
queryImagePath = os.path.join(dirPath, "ball.jpg")
resultIndex = os.path.join(dirname, "imagesIndexes")

resultIndexes = {}
for imagePath in list_images(dirPath):
    imageName = ntpath.basename(imagePath)
    resultIndexes[imageName] = getFeature(imagePath)


results = {}
for(k, features) in resultIndex.items():
    results[k] = -1

results = sorted([(v, k) for (k, v) in results.items()])
print(results)
