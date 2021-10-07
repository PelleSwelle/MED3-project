import cv2 as cv
import PreProcessing

import numpy as np

imgPath = "./reference1.jpg"
scaleFactor = 500
initImg = cv.imread(imgPath)
img = cv.resize(initImg, (initImg.shape[1] - scaleFactor, initImg.shape[0] - scaleFactor))
cv.imshow("reference photo", img)

img_Grayscale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # TODO make our own grayscaler

img_canny = cv.Canny(img_Grayscale, 100, 200)

th, img_thresholded = cv.threshold(img_Grayscale, 128, 129, cv.THRESH_BINARY) # TODO make own thresholder

cv.imshow("img_Grayscale", img_Grayscale)
cv.imshow("img_thresholded", img_canny)

cv.waitKey(0)

cv.destroyAllWindows()
