import cv2 as cv
import numpy as np
from copy import copy
from PIL import Image
import math

detector = cv.SimpleBlobDetector_create()


def binarize(src):
    grayScaleImg = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    th, otsuThresh = cv.threshold(grayScaleImg, 128, 192, cv.THRESH_OTSU)
    # otsuThreshInverted = cv.bitwise_not(otsuThresh)
    # keypoints = detector.detect(otsuThresh)

    # im_with_keypoints = cv.drawKeypoints(otsuThresh, keypoints, np.array([]), (0, 0, 255),
    # cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    return otsuThresh

def grayScale(src):
    pxls = src.load() # load the pixel data from the image
    height, width = src.size  # get the size of the image

    img_grayscaled = Image.new(src.mode, src.size)  # make a canvas to hold the new picture

    for row in range(0, height):
        for column in range(0, width):
            red, blue, green = pxls[row, column] # capture the color channels
            avg = math.floor((red + blue + green) / 3)  # grayscale image is when all three color values are the same
            # fill the canvas with the new values
            img_grayscaled.putpixel((row, column), (avg, avg, avg))

    result = np.array(img_grayscaled)
    return result


def blur_gaussian(src):
    kernel = np.array([[1,  4,  6,  4, 1],
                       [4, 16, 26, 16, 4],
                       [6, 26, 43, 26, 6],
                       [4, 16, 26, 16, 4],
                       [1,  4,  6,  4, 1]])
    gaussian3x3 = copy(src)
    kernelSum = np.sum(kernel)

    for y in range(2, src.shape[0] - 2):
        for x in range(2, src.shape[1] - 2):
            for c in range(src.shape[2]):
                sum = 0
                for ky in range(3):
                    for kx in range(3):
                        sum += src[y + ky - 1, x + kx - 1, c] * kernel[ky, kx]
                gaussian3x3[y, x, c] = sum / kernelSum

    return gaussian3x3
