import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
import pickle

dirname = os.path.dirname(__file__)
dirPath = os.path.join(dirname, "testImages")
queryImagePath = os.path.join(
    dirPath, "images (61).jpg")
queryImagePath2 = os.path.join(
    dirPath, "images (62).jpg")

im1 = cv2.imread(queryImagePath, cv2.IMREAD_GRAYSCALE)
im2 = cv2.imread(queryImagePath2, cv2.IMREAD_GRAYSCALE)


distance = cv2.matchShapes(im1, im2, cv2.CONTOURS_MATCH_I1, 0)
print(distance)
