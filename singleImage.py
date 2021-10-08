import cv2 as cv
import PreProcessing
from PIL import Image
import math
import numpy as np
from copy import copy

imgPath = "./reference1.jpg"
scaleFactor = 500

initImg = cv.imread(imgPath)
pilImg = Image.open(imgPath)

img = cv.resize(initImg, (initImg.shape[1] - scaleFactor, initImg.shape[0] - scaleFactor))
cv.imshow("reference photo", img)

img_Grayscale = PreProcessing.grayScale(pilImg)
# img_gaussianBlur = PreProcessing.blur_gaussian(img_Grayscale)

img_canny = cv.Canny(img_Grayscale, 100, 200)  # TODO make our own edge detection algorithm

th, img_thresholded = cv.threshold(img_Grayscale, 128, 129, cv.THRESH_BINARY)  # TODO make own thresholder



cv.imshow("img_Grayscale", img_Grayscale)
# cv.imshow("img_thresholded", img_canny)
# cv.imshow("gaussian blur", img_gaussianBlur)
cv.waitKey(0)

cv.destroyAllWindows()
