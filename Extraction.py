import cv2 as cv
import numpy as np
from copy import copy
from PIL import Image
from PIL import ImageDraw
import pandas as pd
import math
import Colors
import matplotlib.pyplot as plt

# helper function to draw on the image.
def draw_point(_img: Image, _x: int, _y: int, color):
    rad = 2
    draw = ImageDraw.Draw(_img)
    draw.ellipse((_x - rad, _y - rad,
                  _x + rad, _y + rad), color, outline=100, width=1)


def get_defects(contours):
    hull = cv.convexHull(contours, returnPoints=False)
    return cv.convexityDefects(contours, hull)

def get_number_of_fingers(defects, contours, analyze_image, draw_image: np.ndarray):
    """Uses hull defects to count the nmber of fingers outside of the palm."""

    if defects is not None:
        cnt = 0

    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(contours[s][0])
        end = tuple(contours[e][0])
        far = tuple(contours[f][0])
        # cv.line(draw_image, start, end, Colors.hull_color, 2)

        # TODO put center of hand in this function
        cv.line(draw_image, get_palm_center(analyze_image), end, Colors.hull_color, 1)
        cv.circle(draw_image, far, 5, Colors.defect_color, -1)

    # THIS PART CALCULATES THE ANGLES BETWEEN THE DEFECTS
    # for i in range(defects.shape[0]):  # calculate the angle
    #     s, e, f, d = defects[i][0]
    #     start = tuple(contours[s][0])
    #     end = tuple(contours[e][0])
    #     far = tuple(contours[f][0])
    #     print(Colors.blue+"start: ", start, " end: ", end, " far ", far, "" + Colors.white)
    #     cv.circle(draw_image, start, 4, [0, 255, 0], -1)

    #     a = np.sqrt(
    #         (end[0] - start[0]) ** 2 
    #         + (end[1] - start[1]) ** 2)
    #     b = np.sqrt(
    #         (far[0] - start[0]) ** 2 
    #         + (far[1] - start[1]) ** 2)
    #     c = np.sqrt(
    #         (end[0] - far[0]) ** 2 
    #         + (end[1] - far[1]) ** 2)

    #     angle = np.arccos(
    #         (b ** 2 + c ** 2 - a ** 2) 
    #         / (2 * b * c))  # cosine theorem

    #     if angle <= np.pi / 1.4:  # angle less than 90 degree, treat as fingers
    #         cnt += 1
    #         cv.circle(draw_image, far, 4, [255, 0, 0], -1)

    # if cnt > 0:
    #     cnt = cnt + 1

    # cv.putText(draw_image, str(cnt), (0, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
    return defects

def get_top_of_palm(img: np.ndarray, contours: np.ndarray):
    """Takes the image and the contours of the hand, sees"""
    # if 

# returns the row of pixels containing the most white pixels
def find_center_row(img: Image):
    # TODO height should be top of palm
    height, width = img.size  # get the size of the image
    biggest_row = 0
    maximum = 0
    for _row in range(2, height - 2):
        no_of_black_pixels = 0  # zero out the number of white pixels, because we only count per row
        for _column in range(0, width):
            if img.getpixel((_row, _column)) == 255:
                no_of_black_pixels += 1
                if no_of_black_pixels > maximum:
                    biggest_row = _row
                    maximum = no_of_black_pixels

        # print("line: " + str(y), ": ", blackPixels)
    print(Colors.orange + "row with most white: ", biggest_row, "with ", maximum)
    # return int value of the row containing the most white pixels
    return biggest_row


# returns the column of pixels containing the most white pixels
def find_center_column(img: Image):
    height, width = img.size  # get the size of the image
    biggest_column = 0
    maximum = 0
    for _column in range(2, width - 2):
        no_of_white_pixels = 0
        for _row in range(2, height - 2):
            if img.getpixel((_row, _column)) == 255:
                no_of_white_pixels += 1
                if no_of_white_pixels > maximum:
                    biggest_column = _column
                    maximum = no_of_white_pixels

    return biggest_column


def get_palm_center(img: Image):
    """returns x and y coordinates for the center of the palm"""
    center_x: int = find_center_row(img)
    center_y: int = find_center_column(img)
    
    return center_x, center_y

