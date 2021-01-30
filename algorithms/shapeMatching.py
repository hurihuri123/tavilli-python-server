import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
import pickle
from imutils.paths import list_images
import ntpath


def showImage(imPath, name="result-image"):
    image = cv2.imread(os.path.join(dirPath, imPath))
    image = cv2.resize(image, (600, 600))
    cv2.imshow(name, image)


def showResults(queryPath, results):
    showImage(queryPath, "queryImage")
    cv2.waitKey(0)
    for result in results:
        print("Match with {} perecentage {}".format(result[1], result[0]))
        showImage(result[1])
        cv2.waitKey(0)


def drawCon(contours, image, name="name"):
    cv2.drawContours(image, contours, -1, (0, 255, 0), -1)
    cv2.imshow(name, image)


def match(contours, contours2):
    distanceHausdor = cv2.createHausdorffDistanceExtractor(
    ).computeDistance(contours[0], contours2[0])

    distance = cv2.matchShapes(
        contours[0], contours2[0], cv2.CONTOURS_MATCH_I1, 0)

    return distanceHausdor


def getImageContur(imagePath):
    im1 = cv2.imread(imagePath)

    queryImage = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)

    # apply erosion
    kernel = np.ones((2, 2), np.uint8)
    originalErosion = cv2.erode(queryImage, kernel, iterations=1)

    # retrieve edges with Canny
    thresh = 175
    originalEdges = cv2.Canny(originalErosion, thresh, thresh*2)
    contours, hierarchy = cv2.findContours(
        originalEdges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


dirname = os.path.dirname(__file__)
dirPath = os.path.join(dirname, "testImages")
queryImagePath = os.path.join(
    dirPath, "identical1.jpg")


queryConturs = getImageContur(queryImagePath)
queryImage = cv2.imread(queryImagePath)
drawCon(queryConturs, queryImage, name="image1")
cv2.waitKey()


results = {}
for imagePath in list_images(dirPath):
    imageName = ntpath.basename(imagePath)
    currentConturs = getImageContur(imagePath)

    # currentImage = cv2.imread(imagePath)
    # drawCon(currentConturs, currentImage, name="image2")

    distance = match(currentConturs, queryConturs)
    # print("distance is {}".format(distance))
    # cv2.waitKey()
    results[imageName] = distance


results = sorted([(v, k) for (k, v) in results.items()])
showResults(queryImagePath, reversed(results))
