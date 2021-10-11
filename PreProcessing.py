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
    pxls = src.load()  # load the pixel data from the image
    height, width = src.size  # get the size of the image

    img_grayscaled = Image.new(src.mode, src.size)  # make a canvas to hold the new picture

    for row in range(0, height):
        for column in range(0, width):
            red, blue, green = pxls[row, column]  # capture the color channels
            avg = math.floor((red + blue + green) / 3)  # grayscale image is when all three color values are the same
            # fill the canvas with the new values
            img_grayscaled.putpixel((row, column), (avg, avg, avg))
    #       TODO this should convert to a single channel (from black to white)

    result = np.array(img_grayscaled)
    return result


def blur_gaussian(_src, _kernel):
    if _kernel == 3:
        kernel = np.array([[1, 2, 1],
                              [2, 4, 2],
                              [1, 2, 1]])
    elif _kernel == 5:
        kernel = np.array([[1,  4,  6,  4, 1],
                           [4, 16, 26, 16, 4],
                           [6, 26, 43, 26, 6],
                           [4, 16, 26, 16, 4],
                           [1,  4,  6,  4, 1]])
    # check color channels
    imageArray = copy(_src)
    image = Image.fromarray(_src)
    noOfChannels = len(image.split())

    if noOfChannels == 3:
        singleChannel = image.convert('L')  # convert to single channel
        image = singleChannel

        print("converted from ", noOfChannels, " to ", len(singleChannel.split()), " channels")
    elif noOfChannels == 1:
        print("the image has 1 color channel")

    # blurred_output = copy(_src)
    kernelSum = np.sum(kernel)

    for y in range(2, imageArray.shape[0] - 2):
        for x in range(2, imageArray.shape[1] - 2):
            for c in range(imageArray.shape[2]):
                sum = 0
                for kernel_x in range(5):
                    for kernel_y in range(5):
                        sum += imageArray[y + kernel_x - 2, x + kernel_y - 2, c] * kernel[kernel_x, kernel_y]
                imageArray[y, x, c] = sum / kernelSum

    return imageArray
