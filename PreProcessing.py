import cv2 as cv
import numpy as np

detector = cv.SimpleBlobDetector_create()

def removeBackground(src):
    grayScaleImg = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    th, otsuThresh = cv.threshold(grayScaleImg, 128, 192, cv.THRESH_OTSU)
    # otsuThreshInverted = cv.bitwise_not(otsuThresh)
    keypoints = detector.detect(otsuThresh)

    im_with_keypoints = cv.drawKeypoints(otsuThresh, keypoints, np.array([]), (0, 0, 255),
                                         cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    return im_with_keypoints