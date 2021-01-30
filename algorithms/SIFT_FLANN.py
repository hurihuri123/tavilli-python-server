import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
from imutils.paths import list_images
import ntpath

dirname = os.path.dirname(__file__)
dirPath = os.path.join(dirname, "testImages")
queryImagePath = os.path.join(
    dirPath, "images (45).jpg")


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


# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()


img1 = cv2.imread(queryImagePath, 0)          # queryImage
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1, None)

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)   # or pass empty dictionary

flann = cv2.FlannBasedMatcher(index_params, search_params)

results = {}
for imagePath in list_images(dirPath):
    imageName = ntpath.basename(imagePath)
    img2 = cv2.imread(imagePath, 0)  # trainImage
    kp2, des2 = sift.detectAndCompute(img2, None)

    matches = flann.knnMatch(des1, des2, k=2)

    # Need to draw only good matches, so create a mask
    matchesMask = [[0, 0] for i in range(len(matches))]

    # ratio test as per Lowe's paper
    goodLength = 0
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            matchesMask[i] = [1, 0]
            goodLength = goodLength + 1

    results[imageName] = goodLength
    # draw_params = dict(matchColor=(0, 255, 0),
    #                    singlePointColor=(255, 0, 0),
    #                    matchesMask=matchesMask,
    #                    flags=0)

    # img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2,
    #                           matches, None, **draw_params)

    # plt.imshow(img3,), plt.show()
results = sorted([(v, k) for (k, v) in results.items()])
showResults(queryImagePath, reversed(results))
