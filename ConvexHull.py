import numpy as np
import cv2
from PIL import Image
from matplotlib import pyplot as plt


def show(img):
    plt.imshow(img, cmap='gray')
    plt.xticks([])
    plt.yticks([])

img_original = cv2.imread('hand.jpg', 0)
h, w = img_original.shape
img = np.zeros((h+160,w), np.uint8)
img[80:-80,:] = img_original
plt.figure(figsize=(15,5))
plt.subplot(131)
show(img)
blur = cv2.GaussianBlur(img,(5,5),0)
plt.subplot(132)
show(blur)
_, threshold = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
plt.subplot(133)
show(threshold)
plt.tight_layout()
plt.show()

image = cv2.imread("hand.jpg", 0)


#Predefining a constant k as the centroid point for the palm
#k = 1

#Resize image
# width, height = 300, 300
# hand = cv2.resize(image, (width, height))
#
# ret, threshold = cv2.threshold(hand, 10, 255, cv2.THRESH_BINARY)
#
# contours, hierachy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
# hull = [cv2.convexHull(c) for c in contours]
# final = cv2.drawContours(hand, hull, -1, (255, 255, 255))

#Finding centroid point of palm
M = cv2.moments(threshold)
h, w = img.shape
x_c = M['m10'] // M['m00']
y_c = M['m01'] // M['m00']
plt.figure(figsize=(15,5))
plt.subplot(121)
show(threshold)
plt.plot(x_c, y_c, 'bx', markersize=10)
kernel = np.array([[0, 1, 0],
                   [1, 1, 1],
                   [0, 1, 0]]).astype(np.uint8)
erosion = cv2.erode(threshold,kernel,iterations=1)
boundary = threshold - erosion

centroidPoint, _ = cv2.findContours(boundary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
img_c = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
centroidPoint = centroidPoint[0]
img_cnt = cv2.drawContours(img_c, [centroidPoint], 0, (255,0,0), 2)
plt.subplot(122)
plt.plot(x_c, y_c, 'bx', markersize=10)
show(img_cnt)
plt.tight_layout()
plt.show()

centroidPoint = centroidPoint.reshape(-1,2)
left_id = np.argmin(centroidPoint.sum(-1))
centroidPoint = np.concatenate([centroidPoint[left_id:,:], centroidPoint[:left_id,:]])




#cv2.imshow('Original', hand)
#cv2.imshow('Thresh', threshold)
#cv2.imshow('Convey Hull', hand)

cv2.waitKey(0)