import cv2 as cv
import argparse
import PreProcessing
from PIL import Image
import math
import numpy as np
from copy import copy

referenceDir = "./reference/"

# read reference images using pillow
SIGN_A = Image.open(referenceDir + "A1008.jpg")
SIGN_F = Image.open(referenceDir + "F1001.jpg")
SIGN_P = Image.open(referenceDir + "P1014.jpg")

parser = argparse.ArgumentParser()
parser.add_argument("echo")

args = parser.parse_args()
print(args.echo)

# cv.imshow("reference A", np.array(a_sign))

sign_A_grayscale = PreProcessing.grayScale(SIGN_A)

sign_A_blurred = PreProcessing.blur_gaussian(np.array(sign_A_grayscale), 5)


img_canny = cv.Canny(sign_A_grayscale, 100, 200)  # TODO make our own edge detection algorithm

th, img_thresholded = cv.threshold(sign_A_grayscale, 128, 129, cv.THRESH_BINARY)  # TODO make own thresholder

# ******************* displaying windows *******************
inputWindow_name = "in_A"
outputWindow_name = "out_A"
cv.namedWindow(inputWindow_name)
cv.namedWindow(outputWindow_name)

cv.imshow(inputWindow_name, np.array(sign_A_grayscale))
# cv.imshow(outputWindow_name, np.array(sign_A_grayscale))
cv.imshow(outputWindow_name, np.array(sign_A_blurred))

cv.imshow("default gaus", cv.GaussianBlur(np.array(sign_A_grayscale), (5,5), 0))

cv.waitKey(0)
cv.destroyAllWindows()
