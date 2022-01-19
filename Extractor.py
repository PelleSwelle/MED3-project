from dataclasses import dataclass
from enum import Enum, auto
import cv2 as cv
import numpy as np
import Colors
from math import sqrt
from Hand import Hand, Finger, Title

class Extractor:

    def find_center(self, image: np.ndarray):
         # gets the center of mass (palm)
        mask = image
        dist_transform = cv.distanceTransform(mask, cv.DIST_L2, 5)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(dist_transform, mask)
        
        return max_loc, int(max_val)

    
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


    def extract_defects(self, contours):
        hull_indices = cv.convexHull(contours, returnPoints=False)
        defects = cv.convexityDefects(contours, hull_indices)
        # returns an array containing the convexity defects as output
        # start point, endpoint, farthest point, approximate distance to the farthest point
        
        # print("get_defects: defects type: ", type(defects))
        return defects


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


    def get_list_of_coordinates_from_contours(self, contours):
        list_of_coordinates = []
        for numpy_point in contours[0]:
            point = numpy_point.tolist()
            x, y = point[0]
            list_of_coordinates.append([x, y])
        print("get_list_of_coordinates returns: ", len(list_of_coordinates))
        return list_of_coordinates


    def name_fingers(self, hand: Hand):
        palm_top = hand.center[1] - hand.palm_radius
        thumb_threshold = palm_top - 30
        
        for i in range(0, len(hand.fingers)):
            #* x and y values for comparing
            finger_x: int = hand.fingers[i].position[0]
            finger_y: int = hand.fingers[i].position[1]
            finger_length = hand.fingers[i].length
            #* SHORTER VARIABLES FOR EFFICIENCY
            palm_center = hand.center
            palm_radius = hand.palm_radius
            approx_little_length = palm_radius * 2.6
            
            buffer = 10
            
            left_of_palm = finger_x < palm_center[0] - hand.palm_radius
            right_of_palm = finger_x > palm_center[0] + hand.palm_radius
            
            at_palm_center_x = finger_x > palm_center[0] - 10 and finger_x < hand.center[0] + 10
            ring_finger_position = left_of_palm and finger_length > hand.palm_radius * 1.2
            little_finger_position = left_of_palm and finger_length < hand.palm_radius * 1.2
            
            left_of_center = finger_x < palm_center[0]
            right_of_center = palm_center[0] + buffer < finger_x
            
            straight_above = palm_center[0] - buffer < finger_x < palm_center[0] + buffer
            center_to_left = palm_center[0] - palm_radius - buffer < finger_x < palm_center[0] + palm_radius

            if finger_length < approx_little_length and left_of_center:
                hand.fingers[i].title = Title.LITTLE_FINGER

            elif finger_length < approx_little_length and right_of_palm:
                hand.fingers[i].title = Title.THUMB_FINGER

            elif right_of_center:
                hand.fingers[i].title = Title.INDEX_FINGER

            elif straight_above:
                hand.fingers[i].title = Title.MIDDLE_FINGER

            elif center_to_left:
                hand.fingers[i].title = Title.RING_FINGER

            else:
                hand.fingers[i].title = Title.NOT_SET
    