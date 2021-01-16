import cv2
import numpy as np
from matplotlib import pyplot as plt


def templateMatch(sourceImagePath, templateImagePath):
    img_rgb = cv2.imread(sourceImagePath)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(templateImagePath, 0)

    return
