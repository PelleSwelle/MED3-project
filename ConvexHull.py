import numpy as np
import cv2
from PIL import Image
import matplotlib


image = cv2.imread("hand.jpg", 0)


#Predefining a constant k as the centroid point for the palm

k = 1

#Resize image
width, height = 300, 300
hand = cv2.resize(image, (width, height))

ret, threshold = cv2.threshold(hand, 10, 255, cv2.THRESH_BINARY)

contours, hierachy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

hull = [cv2.convexHull(c) for c in contours]
final = cv2.drawContours(hand, hull, -1, (255, 255, 255))

#Finding centroid point of palm





#cv2.imshow('Original', hand)
cv2.imshow('Thresh', threshold)
cv2.imshow('Convey Hull', hand)

cv2.waitKey(0)