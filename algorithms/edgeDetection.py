import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
from sklearn.decomposition import PCA

dirname = os.path.dirname(__file__)
dirPath = os.path.join(dirname, "testImages")
queryImagePath = os.path.join(
    dirPath, "images (15).jpg")

img = cv2.imread(queryImagePath, 0)
edges = cv2.Canny(img, 100, 200)
print(edges)

plt.subplot(121), plt.imshow(img, cmap='gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(edges, cmap='gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()
