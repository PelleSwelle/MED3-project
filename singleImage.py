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

parser = argparse.ArgumentParser()  # argument parser

# parser.add_argument("square", help="display a square of a given number", type=int)
parser.add_argument("handpose", help="set input image as A, F or P")
args = parser.parse_args()

image = SIGN_A

if args.handpose == "a":
    print("processing sign for A")
    image = SIGN_A
elif args.handpose == "f":
    print("processing sign for F")
    image = SIGN_F
elif args.handpose == "p":
    print("processing sign for P")
    image = SIGN_P

img_grayscaled = PreProcessing.grayScale(image)

img_blurred = PreProcessing.blur_gaussian(np.array(img_grayscaled), 5)

# th = threshold value, img_thresholded is the image as an array
th, img_thresholded = cv.threshold(img_grayscaled, 120, 255, cv.THRESH_BINARY)  # TODO make own thresholder
img_canny = cv.Canny(img_thresholded, 100, 200)  # TODO make our own edge detection algorithm

# img_isolated = PreProcessing.removeOtherStuff(img_canny)
#
# cv.imshow("isolated", img_isolated)

# find out which shape is hand
# if shape not hand, remove

# ************************************** DISPLAYING WINDOWS **************************************
step_one = image
step_two = img_blurred
step_three = img_thresholded
step_four = img_canny
# *******************         STEP ONE         *******************
stepOneTitle = str(step_one)
cv.namedWindow(stepOneTitle)
cv.imshow(stepOneTitle, np.array(step_one))

# *******************         STEP TWO        *******************
stepTwoTitle = str(step_two)
cv.namedWindow(stepTwoTitle)
cv.imshow(stepTwoTitle, np.array(step_two))

# *******************      STEP THREE     *******************
stepThreeTitle = str(step_three)
cv.namedWindow(stepThreeTitle)
cv.imshow(stepThreeTitle, np.array((step_three)))

# *******************      STEP FOUR     *******************
stepFourTitle = str(step_four)
cv.namedWindow(stepFourTitle)
cv.imshow(stepFourTitle, np.array((step_four)))

# cv.imshow("default gaus", cv.GaussianBlur(np.array(input_grayscaled), (5, 5), 0))


cv.waitKey(0)
cv.destroyAllWindows()
