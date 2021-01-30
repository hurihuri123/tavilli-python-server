import cv2
import os
import ntpath
from imutils.paths import list_images
import numpy as np
# from skimage.measure import structural_similarity as ssim


def showImage(imPath, name="result-image"):
    image = cv2.imread(os.path.join(dirPath, imPath))
    image = cv2.resize(image, (600, 600))
    cv2.imshow(name, image)


class BRISK():
    def __init__(self):
        super().__init__()
        self.brisk = cv2.BRISK_create()
        self.matcher = cv2.BFMatcher(normType=cv2.NORM_HAMMING,
                                     crossCheck=True)

    def getFeature(self, imagePath):
        image = cv2.imread(imagePath, flags=cv2.IMREAD_GRAYSCALE)
        keypoints1, descriptors1 = self.brisk.detectAndCompute(image, None)
        return (keypoints1, descriptors1)

    def compareFeatures(self, feature1, feature2):
        keypoints1, descriptors1 = feature1
        keypoints2, descriptors2 = feature2
        matches = self.matcher.match(descriptors1,
                                     descriptors2)
        return 100


class Search():
    def __init__(self, getFeature, compareFeatures):
        super().__init__()
        self.getFeature = getFeature
        self.compareFeatures = compareFeatures

    def match(self, queryPath):
        resultIndexes = {}
        for imagePath in list_images(dirPath):
            imageName = ntpath.basename(imagePath)
            resultIndexes[imageName] = self.getFeature(imagePath)

        queryFeatures = self.getFeature(queryPath)
        results = {}
        for(k, features) in resultIndexes.items():
            results[k] = self.compareFeatures(features, queryFeatures)

        results = sorted([(v, k) for (k, v) in results.items()])
        return results

    def showResults(self, queryPath, results):
        showImage(queryPath, "queryImage")
        cv2.waitKey(0)
        for result in results:
            print("Match with {} perecentage {}".format(result[1], result[0]))
            showImage(result[1])
            cv2.waitKey(0)


if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    dirPath = os.path.join(dirname, "testImages")
    queryImagePath = os.path.join(dirPath, "identical1.jpg")

    brisk = BRISK()
    searchBRISK = Search(brisk.getFeature, brisk.compareFeatures)
    searchBRISK.showResults(queryImagePath, searchBRISK.match(queryImagePath))
