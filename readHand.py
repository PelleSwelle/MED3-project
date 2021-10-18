import cv2 as cv
import argparse
import PreProcessing
import Directories
from PIL import Image
import os
import math
import numpy as np
from copy import copy

# read in images using pillow
# SIGN_A = Image.open(referenceDir + "A.jpg")
# SIGN_F = Image.open(referenceDir + "F.jpg")
# SIGN_P = Image.open(referenceDir + "P.jpg")

directory = "./out"

parser = argparse.ArgumentParser()  # argument parser

# parser.add_argument("square", help="display a square of a given number", type=int)
# parser.add_argument("handpose", help="set input image as A, F or P")
args = parser.parse_args()

# image = SIGN_A

# if args.handpose == "a":
#     print("processing sign for A")
#     image = SIGN_A
# elif args.handpose == "f":
#     print("processing sign for F")
#     image = SIGN_F
# elif args.handpose == "p":
#     print("processing sign for P")
#     image = SIGN_P


print("\nin: ")
for file in os.listdir(Directories.inFolder):
    print("    ", file)
print("\nout: ")
for file in os.listdir(Directories.outFolder):
    print("    ", file)

title = input("\nwhich image?\n")
fileName = title + ".jpg"

for file in Directories.allFiles():
    if fileName == file:
        image = file
        print("working on ", image)






image_cv = cv.imread(dir + title + ".jpg")
image_pillow = Image.open(dir + title + ".jpg")


print("[g]rayscale?")
print("[b]lur?")
print("[t]reshold?")
print("[c]ountours?")
print("[r]emove other stuff?")

toDo = input("\nwhat do?\n")
if toDo == "g":
    img_grayscaled = PreProcessing.grayScale(image_pillow, title)
elif toDo == "b":
    img_blurred = PreProcessing.blur_gaussian(np.array(image_cv), title, 5)
elif toDo == "t":
    th, img_thresholded = cv.threshold(image, 120, 255, cv.THRESH_BINARY)  # TODO make own thresholder
elif toDo == "c":
    pass
    # contours
elif toDo == "r":
    pass
    # remove stuff





# th = threshold value, img_thresholded is the image as an array

# img_canny = cv.Canny(img_thresholded, 100, 200)  # TODO make our own edge detection algorithm


# FIND OUT WHICH SHAPE IS HAND AND REMOVE ANYTHING ELSE
# img_isolated = PreProcessing.removeOtherStuff(img_canny)

# cv.imshow("isolated", img_isolated)

# img_contoured = PreProcessing.detectShapes(img_canny)
# cv.imshow("contoured", img_contoured)

# if shape not hand, remove
# find center of hand
# detect upper tips
#

# ************************************** DISPLAYING OUTPUT FILES **************************************
# for file in os.listdir(outDir):
    # cv.imshow("file", file)


cv.waitKey(0)
cv.destroyAllWindows()
