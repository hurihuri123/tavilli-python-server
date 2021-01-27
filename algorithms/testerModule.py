import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

MIN_MATCH_COUNT = 10
orb = cv2.ORB_create()
orbMatcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

sift = cv2.xfeatures2d.SIFT_create()
# siftMathcer = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
siftMathcer = cv2.BFMatcher()


class TesterModule(object):
    def __init__(self, readCallBack, detectCallBack, searchMatchCallback, handleMatchesCB):
        super().__init__()
        self.readCallBack = readCallBack
        self.detectCallBack = detectCallBack
        self.searchMatchCallback = searchMatchCallback
        self.handleMatchesCB = handleMatchesCB

    def test(self, path1, path2):
        img1 = self.readCallBack(path1)
        img2 = self.readCallBack(path2)
        index1 = self.detectCallBack(img1)
        index2 = self.detectCallBack(img2)
        matches = self.searchMatchCallback(index1, index2)
        print(self.handleMatchesCB(matches))


def getImageMask(imagePath):
    image = cv2.imread(imagePath)
    image = cv2.resize(image, (64, 64))
    # # convert it to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # # pad the image with extra white pixels to ensure the
    # # edges of the image are not up against the borders
    # # of the image
    image = cv2.copyMakeBorder(image, 15, 15, 15, 15,
                               cv2.BORDER_CONSTANT, value=255)

    return image


def ORB_read_callback(path):
    return getImageMask(path)


def ORB_detect_callback(image):
    return orb.detectAndCompute(image, None)


def ORB_match_callback(index1, index2):
    something, des1 = index1
    something, des2 = index2
    return orbMatcher.match(des1, des2)


def ORBhandleResult(matches):
    matches = sorted(matches, key=lambda x: x.distance)
    distanceSum = 0
    for item in matches:
        distanceSum += item.distance

    return ("ORB ->>>>>>>>> sum is {} length is {}".format(
        distanceSum, len(matches)))

# --------------------------


def SIFT_detect_callback(image):
    return sift.detectAndCompute(image, None)


def SIFT_match_callback(index1, index2):
    something, des1 = index1
    something, des2 = index2
    # return siftMathcer.match(des1, des2)
    return siftMathcer.knnMatch(des1, des2, k=2)


def SIF_handle_result(matches):
    # matches = sorted(matches, key=lambda x: x.distance)

    totalDistance = 0
    # Apply ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.75*n.distance:
            good.append(m)

    totalDistance = 0
    for g in good:
        totalDistance += g.distance

    print("SIFT->>>>> distance total {}".format(totalDistance))


dirname = os.path.dirname(__file__)
dirPath = os.path.join(dirname, "testImages")
queryImagePath = os.path.join(
    dirPath, "linda-xu-fUEP0djb1hA-unsplash.jpg")
templateImagePath = os.path.join(
    dirPath, "jeremy-alford-EfLwt5Xz5Ek-unsplash.jpg")


testORB = TesterModule(readCallBack=ORB_read_callback,
                       detectCallBack=ORB_detect_callback, searchMatchCallback=ORB_match_callback,
                       handleMatchesCB=ORBhandleResult)
testORB.test(queryImagePath, templateImagePath)

testSIFT = TesterModule(readCallBack=ORB_read_callback,
                        detectCallBack=SIFT_detect_callback, searchMatchCallback=SIFT_match_callback,
                        handleMatchesCB=SIF_handle_result)
testSIFT.test(queryImagePath, templateImagePath)
