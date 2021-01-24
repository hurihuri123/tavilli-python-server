import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

MIN_MATCH_COUNT = 4


dirname = os.path.dirname(__file__)
dirPath = os.path.join(dirname, "testImages")
queryImagePath = os.path.join(
    dirPath, "ashkan-forouzani-zAEZ2MOeJ9M-unsplash.jpg")
templateImagePath = os.path.join(
    dirPath, "arno-senoner-ZT16YkAYueo-unsplash.jpg")


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
bf = cv2.BFMatcher(cv2.NORM_L1)
matches = bf.knnMatch(des1,des2, k=2)

# Apply ratio test
good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])

# cv2.drawMatchesKnn expects list of lists as matches.
img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,flags=2)

plt.imshow(img3),plt.show()
print(good)