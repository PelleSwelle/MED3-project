import cv2 as cv
import numpy as np

detector = cv.SimpleBlobDetector_create()

def removeBackground(src):
    grayScaleImg = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    th, otsuThresh = cv.threshold(grayScaleImg, 128, 192, cv.THRESH_OTSU)

    otsuThreshInverted = cv.bitwise_not(otsuThresh)
    keypoints = detector.detect(otsuThreshInverted)

    im_with_keypoints = cv.drawKeypoints(otsuThreshInverted, keypoints, np.array([]), (0, 0, 255),
                                         cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # m = cv.moments(im_gray_th_otsu)
    # # Calculate area
    # area = m['m00']
    # # Calculate centroid
    # cx = int(m['m10'] / m['m00'])
    # cy = int(m['m01'] / m['m00'])
    # cv.circle(output, (cx, cy), 20, (255, 0, 0), 3)
    return im_with_keypoints