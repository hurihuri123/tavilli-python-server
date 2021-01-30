import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
import pickle


def drawCon(contours, image, name="name"):
    cv2.drawContours(image, contours, -1, (0, 255, 0), -1)
    cv2.imshow(name, image)


dirname = os.path.dirname(__file__)
dirPath = os.path.join(dirname, "testImages")
queryImagePath = os.path.join(
    dirPath, "identical1.jpg")
queryImagePath2 = os.path.join(
    dirPath, "identical2.jpg")

im1 = cv2.imread(queryImagePath)
im2 = cv2.imread(queryImagePath2)

# make them gray
originalGray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
drawnGray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

# apply erosion
kernel = np.ones((2, 2), np.uint8)
originalErosion = cv2.erode(originalGray, kernel, iterations=1)
drawnErosion = cv2.erode(drawnGray, kernel, iterations=1)

# retrieve edges with Canny
thresh = 175
originalEdges = cv2.Canny(originalErosion, thresh, thresh*2)
drawnEdges = cv2.Canny(drawnErosion, thresh, thresh*2)

# extract contours
contours, hierarchy = cv2.findContours(
    originalEdges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contours2, hierarchy2 = cv2.findContours(
    drawnEdges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

drawCon(contours, im1, name="image1")
drawCon(contours2, im2, name="image2")
cv2.waitKey()

distance = cv2.matchShapes(
    contours[0], contours2[0], cv2.CONTOURS_MATCH_I1, 0)
print(distance)
