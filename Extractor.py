from dataclasses import dataclass
from enum import Enum, auto
import cv2 as cv
import numpy as np
from copy import copy
from PIL import Image
from PIL import ImageDraw
from numpy.lib.histograms import _histogram_bin_edges_dispatcher
import pandas as pd
import math
import PreProcessing
import Colors

class Extractor:
    def get_contours(self, image: Image.Image):
        contours, hierarchy = cv.findContours(image.img_array, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours = max(contours, key=lambda x: cv.contourArea(x))
        return contours, hierarchy

    def contour(self, image: Image.Image):
        # GET CONTOURS
        contours, hierarchy = cv.findContours(image.img_array, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours = max(contours, key=lambda x: cv.contourArea(x))
        self.canvas = np.zeros((image.img_array.shape[0], image.img_array.shape[1]))
        cv.drawContours(self.canvas, [contours], -1, 100, 2)

        return self.canvas

    def get_convex_hull_points(self, image:Image.Image, contours: list):
        # create hull array for convex hull points
        contour_list =self.get_contours(image=image)
        hull = []

        # calculate points for each contour
        for i in range(len(contours)):
            # creating convex hull object for each contour
            hull.append(cv.convexHull(contours[i], returnPoints=False))
        return hull
        
    def convex_hull(self, image:Image.Image):
        # eeeeeeerrrrrrrrggghhhh
        contours, hierarchy = self.get_contours(image)
        # create an empty black image
        canvas = np.zeros(
            (
                image.img_array.shape[0], 
                image.img_array.shape[1], 
                3
            ), 
            np.uint8
        )

        hull = self.get_convex_hull_points(
            image=image, 
            contours=self.get_contours(image)
        )

        # draw contours and hull points
        for i in range(len(contours)):
    
            color = (255, 0, 0) # blue - color for convex hull
            # draw ith contour
            # cv.drawContours(
            #     image=drawing, 
            #     contours=contours, 
            #     contourIdx=i, 
            #     color=color_contours, 
            #     thickness=1, 
            #     lineType=8, 
            #     hierarchy=hierarchy
            # )
            # draw ith convex hull object
            cv.drawContours(canvas, hull, i, color, 1, 8)

# NONE OF THIS UNDER HERE WORKS YET

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

