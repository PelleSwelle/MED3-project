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

input_grayscaled = PreProcessing.grayScale(image)

input_blurred = PreProcessing.blur_gaussian(np.array(input_grayscaled), 5)

input_canny = cv.Canny(input_grayscaled, 100, 200)  # TODO make our own edge detection algorithm

th, img_thresholded = cv.threshold(input_grayscaled, 128, 129, cv.THRESH_BINARY)  # TODO make own thresholder

# ******************* displaying windows *******************
inputWindow_name = "in"
outputWindow_name = "out"
referenceWindow_name = "reference"
cv.namedWindow(inputWindow_name)
cv.namedWindow(outputWindow_name)
cv.namedWindow(referenceWindow_name)

cv.imshow(inputWindow_name, np.array(input_grayscaled))
cv.imshow(outputWindow_name, np.array(input_blurred))
cv.imshow(referenceWindow_name, np.array((img_thresholded)))

cv.imshow("default gaus", cv.GaussianBlur(np.array(input_grayscaled), (5, 5), 0))


cv.waitKey(0)
cv.destroyAllWindows()
