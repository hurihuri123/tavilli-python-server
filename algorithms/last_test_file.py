import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

MIN_MATCH_COUNT = 10


dirname = os.path.dirname(__file__)
dirPath = os.path.join(dirname, "testImages")
queryImagePath = os.path.join(
    dirPath, "ball.jpg")
templateImagePath = os.path.join(
    dirPath, "nicolas-lobos-MJIIEUlQH60-unsplash.jpg")


img1 = cv2.imread(queryImagePath, 0)          # queryImage
img2 = cv2.imread(templateImagePath, 0)  # trainImage

if img1 is None or img2 is None:
    print("NONE IMAGE")

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()


# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)


# BFMatcher with default params
bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
matches = bf.knnMatch(des1, des2, k=2)

# Apply ratio test
goodPointMatches = []
for m, n in matches:
    if m.distance < 0.75*n.distance:
        goodPointMatches.append([m])

print(len(goodPointMatches))
img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2,
                          goodPointMatches, None, flags=2)

plt.imshow(img3), plt.show()
