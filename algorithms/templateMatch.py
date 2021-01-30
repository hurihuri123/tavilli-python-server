import cv2
import os
import ntpath
from imutils.paths import list_images


# TODO - wrap this 2 with class that can store objects
class Features():
    def __init__(self):
        super().__init__()

    def getFeature(self, imagePath):
        return {}

    def compareFeatures(self, feature1, feature2):
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


if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    dirPath = os.path.join(dirname, "testImages")
    queryImagePath = os.path.join(dirPath, "ball.jpg")

    features = Features()
    searcher = Search(features.getFeature, features.compareFeatures)
    print(searcher.match(queryImagePath))
