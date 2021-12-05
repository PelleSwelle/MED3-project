from typing import no_type_check_decorator
import cv2 as cv
import numpy as np
from numpy.lib.index_tricks import nd_grid

def extract_contours(image: np.array):
    # returns contours:list, hierarchy: np.ndarray
    contours, hierarchy = cv.findContours(
    image=image, 
    mode=cv.RETR_TREE, 
    method=cv.CHAIN_APPROX_SIMPLE)
    print("contours type: ", type(contours), "hierarchy type: ", type(hierarchy))
    return contours, hierarchy

# Load the image
img1 = cv.imread('reference/Wsign2.jpg')

# Convert it to greyscale
img = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
cv.imshow("grayscaled", img)

blurred = cv.GaussianBlur(img, (7, 7), 1)

# Threshold the image
# ret -> float, thresh -> np.ndarray
ret, thresh = cv.threshold(
    src=blurred,
    thresh=240,
    maxval=255,
    type=cv.THRESH_BINARY_INV
)

# cv.imshow("thresh", thresh[0])
# print("ret:\n", ret, "is of type: ", type(ret))
# print("thresh\n", thresh, "is of type: ", type(thresh))

cv.imshow("thresh", thresh)

# returns a tuple
contours = extract_contours(thresh)
print("extract_contours: contours is of type: ", type(contours))

# returns a list
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
print("cv.findContours: contours is of type: ", type(contours))


contoured_image = cv.drawContours(thresh, contours, -1, (100, 100, 100), 4)

cv.imshow("contours", contoured_image)

# print("contours: ", contours, "is of type: ", type(contours))

# cv.drawContours(
#     image=thresh, 
#     contours=contours, 
#     contourIdx=-1, 
#     color=(0, 0, 255), 
#     thickness=1)
# cv.imshow("contours", thresh)

# For each contour, find the convex hull and draw it
# on the image.
canvas = np.zeros((img.shape[0], img.shape[1]))

for i in range(len(contours)):
    hull = cv.convexHull(points=contours[i])

cv.drawContours(
        image=img1, 
        contours=[hull], 
        contourIdx=-1, 
        color=(255, 0, 0), 
        thickness=2
    )

# Display the final convex hull image
# cv.imshow('ConvexHull', img1)
cv.imshow("data", img1)
cv.waitKey(0)