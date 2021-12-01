import cv2 as cv
import numpy as np
# Load the image
img1 = cv.imread('reference/Wsign2.jpg')
# Convert it to greyscale
img = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
cv.imshow("grayscaled", img)

blurred = cv.GaussianBlur(img, (7, 7), 1)

# Threshold the image
ret, thresh = cv.threshold(
    src=blurred,
    thresh=250,
    maxval=255,
    type=cv.THRESH_BINARY_INV
)
cv.imshow("thresholded", thresh)
# Find the contours
contours, hierarchy = cv.findContours(
    image=thresh, 
    mode=cv.RETR_TREE, 
    method=cv.CHAIN_APPROX_SIMPLE)

cv.drawContours(
    image=thresh, 
    contours=contours, 
    contourIdx=-1, 
    color=(0, 0, 255), 
    thickness=1)
cv.imshow("contours", thresh)

# For each contour, find the convex hull and draw it
# on the original image.
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
cv.imshow('ConvexHull', img1)
cv.imshow("data", img1)
cv.waitKey(0)