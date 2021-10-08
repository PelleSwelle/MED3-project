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
    # load the pixel data from the image
    pxls = src.load()
    height, width = src.size

    # make a canvas to hold the new picture
    img_grayscaled = Image.new(src.mode, src.size)

    for row in range(0, height):
        for column in range(0, width):
            # capture the color channels
            red, blue, green = pxls[row, column]
            avg = math.floor((red + blue + green) / 3)
            # fill the canvas with the new values
            img_grayscaled.putpixel((row, column), (avg, avg, avg))

    result = np.array(img_grayscaled)
    return result


def blur_gaussian(src):
    kernel = np.array([[1, 2, 1],
                       [2, 4, 2],
                       [1, 2, 1]])
    output = copy(src)
    # get pixel data
    # pxls = src.load()

    # Creating coordinates of the pixel (x,y)
    # coordinates = x, y = 40, 60

    # getting pixel value using getpixel() method
    # print(pxls.getpixel(coordinates))

    kernelSum = np.sum(kernel)
    matrix = np.zeros(src.shape)
    mat = np.matrix(matrix)

    normalized = 0
    print("kernelSum: ", kernelSum)

    for _y in range(1, src.shape[0] - 1):
        for _x in range(1, src.shape[1] - 1):  # for every pixel
            inputSum = 0
            # for value in range(1):
            # inputSum += src[_y + color_y - 1, _x + color_x - 1] * kernel[color_y, color_x]

            mat[_y, _x] = inputSum/kernelSum
            print(mat[_y, _x])


                # for color_x in range(1):
                #     # normalized += inputSum / kernelSum
            output[_y, _x] = inputSum / kernelSum

    # write matrix to file
    with open('matrix.txt') as file:
        for line in mat:
            # np.savetxt(file, line, fmt='%.2f')
            pass
    return output
