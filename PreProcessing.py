import cv2 as cv
import numpy as np
from copy import copy
from PIL import Image
import Directories
import math


detector = cv.SimpleBlobDetector_create()

def grayScale(src, letter):
    print("grayScaling...")
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

    result_pillow = img_grayscaled
    result_cv = np.array(img_grayscaled)
    Directories.save(result_cv, letter, "grayscaled")
    print("grayscaling has finished")
    # cv.imshow("grayscaled", result_cv)
    return result_cv

def blur_gaussian(_src, letter, _kernel):
    print("initiating gaussian blur...")
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
        print("converted from ", noOfChannels, " to ", len(singleChannel.split()), " channels before applying gaussian blur")

    kernelSum = np.sum(kernel)

    for y in range(2, imageArray.shape[0] - 2):
        for x in range(2, imageArray.shape[1] - 2):
            for c in range(imageArray.shape[2]):
                sum = 0
                for kernel_x in range(5):
                    for kernel_y in range(5):
                        sum += imageArray[y + kernel_x - 2, x + kernel_y - 2, c] * kernel[kernel_x, kernel_y]
                imageArray[y, x, c] = sum / kernelSum
    print("finished gausian blur!")
    Directories.save(imageArray, letter, "Blurred")
    return imageArray

def binarize(src):
    print("binarizing image using otsu method...")
    grayScaleImg = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    th, otsuThresh = cv.threshold(grayScaleImg, 128, 192, cv.THRESH_OTSU)
    # otsuThreshInverted = cv.bitwise_not(otsuThresh)
    # keypoints = detector.detect(otsuThresh)

    # im_with_keypoints = cv.drawKeypoints(otsuThresh, keypoints, np.array([]), (0, 0, 255),
    # cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    print("finished binarizing")
    return otsuThresh

def threshold_otsu(image, nbins = 0.1):
    # validate grayscale
    if len(image.shape) == 1:
        print("threshold algorithm received a one-channel image")
        return

    if np.min(image) == np.max(image):
        print("threshold algorithm received a multi-colored image")
        return

    allColors = image.flatten()
    total_weight = len(allColors)
    leastVariance = -1
    leastVarianceTreshold = -1

    # create an array of all possible threshold values which we want to loop through
    color_thresholds = np.arange(np.min(image) + nbins, np.max(image) - nbins, nbins)

    # loop through the thresholds to find the one with the least within class variance
    for color_threshold in color_thresholds:
        bg_pixels = allColors[allColors < color_threshold]
        weight_bg = len(bg_pixels) / total_weight
        variance_bg = np.var(bg_pixels)

        fg_pixels = allColors[allColors >= color_threshold]
        weight_fg = len(fg_pixels) / total_weight
        variance_fg = np.var(fg_pixels)

        within_class_variance = weight_fg * variance_fg + weight_bg * variance_bg
        if least_variance == -1 or least_variance > within_class_variance:
            least_variance = within_class_variance
            least_variance_threshold = color_threshold
        print("trace:", within_class_variance, color_threshold)

    return least_variance_threshold

def removeOtherStuff(src):
    # TODO check format of image
    print("removing stuff that is not hand from the image...")
    img = Image.fromarray(src)
    pxls = img.load()  # load the pixel data from the image
    height, width = img.size  # get the size of the image

    img_isolated = Image.new(img.mode, img.size)  # make a canvas to hold the new picture
    print(img_isolated.size)

    for row in range(0, height):
        for column in range(0, width):
            if (pxls[row, column]) == 255:
                img_isolated.putpixel((row, column), 100)

    result = np.array(img_isolated)
    print("removed stuff")
    return result

def detectShapes(src):
    print("detecting shapes...")
    img = copy(src)
    # Finding Contours
    # Use a copy of the image e.g. edged.copy()
    # since findContours alters the image
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    cv.imshow('Canny Edges After Contouring', img)
    cv.waitKey(0)

    print("Number of Contours found = " + str(len(contours)))

    # Draw all contours
    # -1 signifies drawing all contours
    # cv.drawContours(img, contours, -1, (0, 255, 0), 3)
    cv.drawContours(img, contours, -1, 255, 6)
    print("detected shapes!")
    return img
    # cv.imshow('shapes', img)
