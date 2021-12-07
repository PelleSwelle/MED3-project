import cv2 as cv
import numpy as np
from copy import copy
from PIL import Image
import math


def binarize(src: np.ndarray):
    grayScaleImg = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    th, otsuThresh = cv.threshold(grayScaleImg, 128, 192, cv.THRESH_OTSU)

    return otsuThresh


def convertToSingleChannel(img: Image):
    singleChannel = img
    if len(img.split()) == 3:
        singleChannel = img.convert('L')  # convert to single channel
        print("converted to single channel")
    return singleChannel


def grayScale(img: Image):
    pxls = img.load()  # load the pixel data from the image
    height, width = img.size  # get the size of the image

    img_grayscaled = Image.new(img.mode, img.size)  # make a canvas to hold the new picture

    for row in range(0, height):
        for column in range(0, width):
            red, blue, green = pxls[row, column]  # capture the color channels
            avg = math.floor((red + blue + green) / 3)  # grayscale image is when all three color values are the same
            # fill the canvas with the new values
            img_grayscaled.putpixel((row, column), (avg, avg, avg))
    #       TODO this should convert to a single channel (from black to white)

    result = np.array(img_grayscaled)
    return result
    # this should add to the list of versions in the hand


def invertColor(img: Image):
    threshold: int = 100
    width, height = img.size  # get the size of the image
    for x in range(0, width):
        for y in range(0, height):
            if img.getpixel((x, y)) <= threshold:
                img.putpixel((x, y), 255)
            elif img.getpixel((x, y)) >= threshold:
                img.putpixel((x, y), 0)
    return img


def downSize(array: np.ndarray, scale: float):
    array = np.array(array)
    scaled_f_down = cv.resize(array, None, fx=scale, fy=scale, interpolation=cv.INTER_LINEAR)
    return Image.fromarray(scaled_f_down)


def old_blur_gaussian(array: np.ndarray):

    kernel = np.array([[1, 4, 6, 4, 1],
                       [4, 16, 26, 16, 4],
                       [6, 26, 43, 26, 6],
                       [4, 16, 26, 16, 4],
                       [1, 4, 6, 4, 1]])

    kernelSum = np.sum(kernel)

    for y in range(2, array.shape[0] - 2):
        for x in range(2, array.shape[1] - 2):
            for c in range(array.shape[2]):
                sum = 0
                for kernel_x in range(5):
                    for kernel_y in range(5):
                        sum += array[y + kernel_x - 2, x + kernel_y - 2, c] * kernel[kernel_x, kernel_y]
                array[y, x, c] = sum / kernelSum

    return array


# TODO this is the homemade thresholding function currently not implemented
def threshold_otsu(image, nbins=0.1):
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
    img = Image.fromarray(src)
    pxls = img.load()  # load the pixel data from the image
    height, width = img.size  # get the size of the image

    img_isolated = Image.new(img.mode, img.size)  # make a canvas to hold the new picture

    for row in range(0, height):
        for column in range(0, width):
            if img.getPixel((row, column) == 255):
                print("demo")
                # img_isolated.putpixel((row, column), 0)

    result = np.array(img_isolated)
    return result


# def detectCenter(src):
#     # img = Image.fromarray(src)
#     findBroadestX(src)
#     centerX = 50
#     centerY = 50
#     imageCircled = cv.circle(src, (centerX, centerY), 1, (0, 0, 255), 2)
#     return imageCircled
