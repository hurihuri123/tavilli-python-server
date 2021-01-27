import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
import pickle


def useBruteForce(img1, img2, kp1, kp2, des1, des2, setDraw, ORB):
    # create BFMatcher object
    bf = cv2.BFMatcher(
        cv2.NORM_HAMMING, crossCheck=True) if ORB else cv2.BFMatcher()

    # Match descriptors.
    matches = bf.match(des1, des2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key=lambda x: x.distance)

    totalDistance = 0
    for g in matches:
        totalDistance += g.distance

    if setDraw == True:
        # Draw matches.
        img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches, None, flags=2)
        plt.imshow(img3), plt.show()

    return totalDistance


def useBruteForceWithRatioTest(img1, img2, kp1, kp2, des1, des2, setDraw, ORB):
    # BFMatcher with default params
    if ORB:
        bf = cv2.BFMatcher(
            cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
    else:
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

    # Apply ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.75*n.distance:
            good.append(m)

    totalDistance = 0
    for g in good:
        totalDistance += g.distance

    if setDraw == True:
        # cv2.drawMatchesKnn expects list of lists as matches.
        img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, [good], None, flags=2)
        plt.imshow(img3), plt.show()

    return totalDistance


def useFLANN(img1, img2, kp1, kp2, des1, des2, setDraw, type):
    # Fast Library for Approximate Nearest Neighbors
    MIN_MATCH_COUNT = 1
    FLANN_INDEX_KDTREE = 0
    FLANN_INDEX_LSH = 6

    if type == True:
        # Detect with ORB
        index_params = dict(algorithm=FLANN_INDEX_LSH,
                            table_number=6,  # 12
                            key_size=12,     # 20
                            multi_probe_level=1)  # 2
    else:
        # Detect with Others such as SURF, SIFT
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)

    # It specifies the number of times the trees in the index should be recursively traversed. Higher values gives better precision, but also takes more time
    search_params = dict(checks=90)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)

    totalDistance = 0
    for g in good:
        totalDistance += g.distance

    if setDraw == True:
        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32(
                [kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32(
                [kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()

            h, w = img1.shape
            pts = np.float32([[0, 0], [0, h-1], [w-1, h-1],
                              [w-1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            img2 = cv2.polylines(
                img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

        else:
            print("Not enough matches are found {}".format(len(good)))
            matchesMask = None

        draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                           singlePointColor=None,
                           matchesMask=matchesMask,  # draw only inliers
                           flags=2)

        img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
        plt.imshow(img3, 'gray'), plt.show()

    return totalDistance

# -----------------------------------------


def check(img1, img2, kp1, kp2, des1, des2, matcherType, setDraw, ORB):
    if matcherType == 1:
        return useBruteForce(img1, img2, kp1, kp2, des1, des2, setDraw, ORB)
    elif matcherType == 2:
        return useBruteForceWithRatioTest(img1, img2, kp1, kp2, des1, des2, setDraw, ORB)
    elif matcherType == 3:
        return useFLANN(img1, img2, kp1, kp2, des1, des2, setDraw, ORB)
    else:
        print("Matcher not chosen correctly, use Brute Force matcher as default")
        return useBruteForce(img1, img2, kp1, kp2, des1, des2, matcherType, setDraw)


def useORB(filename1, filename2, matcherType, setDraw):
    img1 = cv2.imread(filename1, 0)  # queryImage
    img2 = cv2.imread(filename2, 0)  # trainImage

    # Initiate ORB detector
    orb = cv2.ORB_create()

    # find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    ORB = True
    distance = check(img1, img2, kp1, kp2, des1,
                     des2, matcherType, setDraw, ORB)
    print("ORB with matcher type {} result total distance :{}".format(
        matcherType, distance))
    return distance


def useSIFT(filename1, filename2, matcherType, setDraw):
    img1 = cv2.imread(filename1, 0)  # queryImage
    img2 = cv2.imread(filename2, 0)  # trainImage

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    ORB = False
    distance = check(img1, img2, kp1, kp2, des1,
                     des2, matcherType, setDraw, ORB)
    print("SIFT with matcher type {} result total distance :{}".format(
        matcherType, distance))
    return distance


def useSURF(filename1, filename2, matcherType, setDraw):
    img1 = cv2.imread(filename1, 0)
    img2 = cv2.imread(filename2, 0)

    # Here I set Hessian Threshold to 400
    surf = cv2.xfeatures2d.SURF_create()

    # Find keypoints and descriptors directly
    kp1, des1 = surf.detectAndCompute(img1, None)
    kp2, des2 = surf.detectAndCompute(img2, None)
    ORB = False
    distance = check(img1, img2, kp1, kp2, des1,
                     des2, matcherType, setDraw, ORB)
    print("SURF with matcher type {} result total distance :{}".format(
        matcherType, distance))
    return distance


def useBRISK(filename1, filename2, matcherType, setDraw):
    img1 = cv2.imread(filename1, 0)  # queryImage
    img2 = cv2.imread(filename2, 0)  # trainImage

    # Initiate BRISK detector
    brisk = cv2.BRISK_create()

    # find the keypoints and descriptors with BRISK
    kp1, des1 = brisk.detectAndCompute(img1, None)
    kp2, des2 = brisk.detectAndCompute(img2, None)
    ORB = True
    distance = check(img1, img2, kp1, kp2, des1,
                     des2, matcherType, setDraw, ORB)
    print("BRISK with matcher type {} result total distance :{}".format(
        matcherType, distance))
    return distance


dirname = os.path.dirname(__file__)
dirPath = os.path.join(dirname, "testImages")
ball = os.path.join(
    dirPath, "ball.jpg")
bug = os.path.join(
    dirPath, "creative-headline-APNnyM36puU-unsplash.jpg")
ball2 = os.path.join(
    dirPath, "joshua-hoehne-kl6VSadl5mA-unsplash.jpg")


print("Comparing ball with ball:")
useBRISK(ball, bug, 1, False)
useORB(ball, bug, 1, False)
print("Comparing ball with bug:")
useBRISK(ball, ball2, 1, False)
useORB(ball, ball2, 1, False)
