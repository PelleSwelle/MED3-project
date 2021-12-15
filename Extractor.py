from dataclasses import dataclass
from enum import Enum, auto
import cv2 as cv
import numpy as np
from copy import copy
from PIL import Image
from PIL import ImageDraw
from numpy.lib.histograms import _histogram_bin_edges_dispatcher
import math
import PreProcessing
import Colors
from math import sqrt
from Hand import Finger

class Extractor:

    def find_center(self, image: np.ndarray):
         # gets the center of mass (palm)
        mask = image
        dist_transform = cv.distanceTransform(mask, cv.DIST_L2, 5)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(dist_transform, mask)
        
        # cv.imshow("distance transform", mask)

        return max_loc, int(max_val)

    def extract_contours(self, image: Image) -> list:
        contours, hierarchy = cv.findContours(
            image=image.img_array, 
            mode=cv.RETR_TREE, 
            method=cv.CHAIN_APPROX_SIMPLE
        )
        contours = max(contours, key=lambda x: cv.contourArea(x))
        
        # return contours, hierarchy
        return contours


    def draw_contours(self, image: Image, contours: list) -> np.ndarray:
        self.canvas = np.zeros(
            (image.img_array.shape[0], 
            image.img_array.shape[1]
            )
        )
        cv.drawContours(
            image=self.canvas, 
            contours=contours, 
            contourIdx=-1, 
            color=255, 
            thickness=2
        )
        return self.canvas


    def extract_hull(self, contours: list) -> list:
        hull = []

        # calculate points for each contour
        for i in range(len(contours)):
            # creating convex hull object for each contour
            hull.append(
                cv.convexHull(
                    points=contours[i], #aaaaaaaaaaaa
                    returnPoints=False
                )
            )
        print("length of hull: ", len([hull]))
        return hull


    def draw_hull(self, image: Image, contours: list) -> np.array:
        canvas_height = image.img_array.shape[0]
        canvas_width = image.img_array.shape[1]

        canvas = np.zeros(
            (
                canvas_width, 
                canvas_height
            )
        )

        # Find the convex hull object for each contour
        hull_list = []
        for i in range(len(contours)):
            hull = cv.convexHull(contours[i])
            hull_list.append(hull)

        for i in range(len(contours)):
            cv.drawContours(
                image=canvas, 
                contours=hull_list, 
                contourIdx=i, 
                color=Colors.hull_color, 
                thickness=2
            )
        return canvas

        # NONE OF THIS UNDER HERE WORKS YET


    def extract_defects(self, contours):
        hull_indices = cv.convexHull(contours, returnPoints=False)
        defects = cv.convexityDefects(contours, hull_indices)
        # returns an array containing the convexity defects as output
        # start point, endpoint, farthest point, approximate distance to the farthest point
        
        # print("get_defects: defects type: ", type(defects))
        return defects



    def get_defects_starts(self, defects: np.ndarray, cnt) -> list:
        hull = cv.convexHull(cnt, returnPoints=False)
        defects = cv.convexityDefects(cnt, hull)
        start_points = []
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(cnt[s][0])
            start_points.append(start)
            print("get_defect_starts returns: ", start_points)
        return start_points

    def get_defects_ends(self, defects: np.ndarray, cnt) -> list:
        hull = cv.convexHull(cnt, returnPoints=False)
        defects = cv.convexityDefects(cnt, hull)
        end_points = []
        
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            end = tuple(cnt[e][0])
            end_points.append(end)
            print("get_defect_ends returns: ", end_points)
        return end_points
    
    def get_defects_fars(self, defects: np.ndarray, cnt) -> list:
        hull = cv.convexHull(cnt, returnPoints=False)
        defects = cv.convexityDefects(cnt, hull)
        far_points = []
        
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            far = tuple(cnt[e][0])
            far_points.append(far)
            print("get_defect_fars returns: ", far_points)
        return far_points


    def draw_defects(
        self, 
        defects: np.ndarray, 
        cnt, 
        output_image: np.ndarray) -> None:
        
        hull = cv.convexHull(cnt, returnPoints = False)
        defects = cv.convexityDefects(cnt, hull)

        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            distance = d
            print(f"distance, {distance}")

            # cv.line(output_image,start,end,[0,255,0],1)
            
            # LINES FROM VALLIES TO TIPS
            # cv.line(
            #     img=output_image,
            #     pt1=start,
            #     pt2=far,
            #     color=Colors.defect_color,
            #     thickness=1)
            cv.line(
                img=output_image,
                pt1=far,
                pt2=end,
                color=Colors.defect_color,
                thickness=1)
            cv.line(output_image,start,end,[0,255,0],2)
            
            cv.circle(
                img=output_image,
                center=start,
                radius=1,
                color=(200, 100, 0),
                thickness=-1)
            cv.circle(
                img=output_image,
                center=end,
                radius=1,
                color=(0, 200, 100),
                thickness=-1)
            # cv.line(output_image,start,end,[0,255,0],2)
            # cv.circle(points_canvas,far,5,Colors.defect_color,-1)
            # cv.putText(
            #     img=output_image, 
            #     text="end", 
            #     org=end, 
            #     fontFace=cv.FONT_HERSHEY_SIMPLEX, 
            #     fontScale=1, 
            #     color=(100, 100, 100)
            # )
        
        print("draw_defects returns: ", start)

        return start

    def filter_points(self, coordinate_list: list, threshold: int):
        filtered_points = []
        for point in coordinate_list:
            is_valid = True
            for compare_point in filtered_points:
                dist = self.length(compare_point, point)
                
                if dist < threshold:
                    is_valid = False
                    break
            
            if is_valid:
                filtered_points.append(point)
        
        print("filter_points returns: ", len(filtered_points), " points")
        return filtered_points

    def detect_fingers(self, extractor, filtered_points, input_hand):
        for point in filtered_points:
            point_y = point[1]
            #* if point is above the center of the palm
            if point_y < input_hand.center[1]:
                #* length from palm center to fingertip
                dist_from_center = extractor.length(point, input_hand.center)
                if (dist_from_center > input_hand.palm_radius* 1.8):
                # if (line_length > input_hand.palm_radius * 2.0):
                    #* here we finally add a finger to the hand.
                    input_hand.fingers.append(Finger(position=point, length=dist_from_center))
                    print("detected a finger on the input")

    def length(self, point1: tuple, point2: tuple) -> int:
        # * pythagoras to find length from center to point
        len_hori = point1[0] - point2[0]
        len_vert = point1[1] - point2[1]

        length_squared = pow(len_hori, 2) + pow(len_vert, 2)
        length = int(sqrt(length_squared))
        # print("length returns: ", length)
        return length

    # TODO DO THIS
    def get_list_of_coordinates_from_contours(self, contours):
        list_of_coordinates = []
        for numpy_point in contours[0]:
            point = numpy_point.tolist()
            x, y = point[0]
            list_of_coordinates.append([x, y])
        print("get_list_of_coordinates returns: ", len(list_of_coordinates))
        return list_of_coordinates

    