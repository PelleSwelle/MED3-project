import cv2 as cv
import numpy as np
from copy import copy
from PIL import Image
from PIL import ImageDraw
import pandas as pd
import math

img_cv = cv.imread('thresholded.jpg')
originalImg = Image.fromarray(img_cv)
coloredImg_cv = cv.imread('reference/A1008.jpg')
coloredImage = Image.fromarray(coloredImg_cv)
white = '\033[0m'  # white (normal)
red = '\033[31m'  # red
green = '\033[32m'  # green
orange = '\033[33m'  # orange
blue = '\033[34m'  # blue
purple = '\033[35m'  # purple


# cv.imshow("original", img_cv)


# returns the row of pixels containing the most white pixels
def findCenterRow(_img):
    height, width = _img.size  # get the size of the image
    biggestRow = 0
    maximum = 0
    for _row in range(2, height - 2):
        noOfPlackPixels = 0  # zero out the number of white pixels, because we only count per row
        for _column in range(0, width):
            if _img.getpixel((_row, _column)) == 255:
                noOfPlackPixels += 1
                if noOfPlackPixels > maximum:
                    biggestRow = _row
                    maximum = noOfPlackPixels

        # print("line: " + str(y), ": ", blackPixels)
    print(orange + "row with most white: ", biggestRow, "with ", maximum)
    # return int value of the row containing the most white pixels
    return biggestRow


# returns the column of pixels containing the most white pixels
def findCenterColumn(_img):
    height, width = _img.size  # get the size of the image
    biggestColumn = 0
    maximum = 0
    for _column in range(2, width - 2):
        noOfWhitePixels = 0
        for _row in range(2, height - 2):
            if _img.getpixel((_row, _column)) == 255:
                noOfWhitePixels += 1
                if noOfWhitePixels > maximum:
                    biggestColumn = _column
                    maximum = noOfWhitePixels

    print("column with most white: ", biggestColumn, "with ", maximum)
    return biggestColumn


def invertColor(_img):
    _img = convertToSingleChannel(_img)
    threshold: int = 100
    height, width = _img.size  # get the size of the image
    for x in range(0, height):
        for y in range(0, height):
            if _img.getpixel((x, y)) <= threshold:
                _img.putpixel((x, y), 255)
            elif _img.getpixel((x, y)) >= threshold:
                _img.putpixel((x, y), 0)
    return _img


def getCenterPixel(_img):
    # draw = ImageDraw.Draw(_img)
    centerX = findCenterRow(_img)
    centerY = findCenterColumn(_img)
    rad = 2
    # draw.ellipse((centerX - rad, centerY - rad, centerX + rad, centerY + rad), fill=100, outline=100)
    print("center coordinate: ", centerX, " ", centerY)
    # cv.imshow("center: ", np.array(_img))
    return centerX, centerY


def drawPoint(_img, _x, _y):
    rad = 2
    draw = ImageDraw.Draw(_img)
    draw.ellipse((_x - rad, _y - rad,
                  _x + rad, _y + rad), fill=100, outline=100, width=1)


def convertToSingleChannel(img):
    if len(img.split()) == 3:
        singleChannel = img.convert('L')  # convert to single channel
    return singleChannel


# TODO
def detectRotation(_img):
    pass


def getHighestPoint(_img):
    width, height = _img.size
    # find the first row that contains a white pixel
    for _row in range(1, height - 1):
        for _column in range(1, width - 1):
            if _img.getpixel((_column, _row)) == 255:
                print("white pixel found at row: ", _row, ", ", _column)
                return _column, _row


# takes in an edged image
def getAllWhitePixels(_img):
    width, height = _img.size
    coords = []
    for x in range(0, width):
        # coordinatePair = []
        for y in range(0, height):
            if _img.getpixel((x, y)) == 255:
                coordinatePair = [x, y]
                coords.append(coordinatePair)

    print(coords)

    return coords


def getHighestPointsWithContours(_img):
    _draw = ImageDraw.Draw(_img)
    _img = np.array(_img)
    # Find Canny edges
    edged = cv.Canny(_img, 30, 200)

    contours, hierarchy = cv.findContours(edged, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    cv.imshow('Canny Edges After Contouring', edged)

    print("Number of Contours found = " + str(len(contours)))

    # for every point on the contour, find the normal,
    # if the normal points upward, add it to the list.
    # Draw all contours
    # -1 signifies drawing all contours
    cv.drawContours(_img, contours, -1, (0, 255, 0), 3)

    cv.imshow('Contours', _img)


def getHighestPoints(_img):
    # run through image horizontally.
    # if white pixel has a black after it, mark that pixel as tip.
    width, height = _img.size[0], _img.size[1] - getCenterPixel(_img)[1]  # get from center point up
    for _column in range(2, width - 2):
        for _row in range(2, height - 2):
            # find white pixel
            if _img.getpixel((_column, _row)) == 255:
                # is there a black pixel after it?
                if _img.getpixel((_column + 1, _row)) == 0:
                    drawPoint(_img, _column, _row)

    cv.imshow("points", np.array(_img))
    # return coordinates for each finger


# invert colors
whiteHand = invertColor(originalImg)
cv.imshow("inverted colors", np.array(whiteHand))

edged = Image.fromarray(cv.Canny(np.array(whiteHand), 30, 200))


contours, hierarchy = cv.findContours(np.array(whiteHand), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
contours = max(contours, key=lambda x: cv.contourArea(x))
cv.drawContours(np.array(originalImg), [contours], -1, 100, 2)
cv.imshow("contours", np.array(originalImg))

cv.imshow("edged", np.array(edged))
hull = cv.convexHull(np.array(edged))

whitePixels = getAllWhitePixels(edged)
# get the coordinates of the center of the hand and draw them on the image.
centerCoordinates = getCenterPixel(whiteHand)
drawPoint(whiteHand, centerCoordinates[0], centerCoordinates[1])
# cv.imshow("center point: ", np.array(whiteHand))

dataframe = pd.DataFrame(whitePixels)
dataframe.to_csv("./whitePixels.csv")

highestPoint = getHighestPoint(whiteHand)
drawPoint(whiteHand, highestPoint[0], highestPoint[1])
# cv.imshow("highest point: ", np.array(whiteHand))


draw = ImageDraw.Draw(whiteHand)
draw.line((centerCoordinates, highestPoint), fill=100, width=2)
# cv.imshow("line from center to top point", np.array(whiteHand))

cv.waitKey(0)
cv.destroyAllWindows()
