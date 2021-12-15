from dataclasses import dataclass, field
from enum import Enum, auto
import cv2 as cv
from cv2 import bitwise_not, data
import numpy as np
import Colors
from typing import Tuple
from pprint import pprint

font = cv.FONT_HERSHEY_COMPLEX

class Title(Enum):
    NOT_SET = auto()
    INDEX_FINGER = auto()
    MIDDLE_FINGER = auto()
    RING_FINGER = auto()
    LITTLE_FINGER = auto()
    THUMB_FINGER = auto()

@dataclass
class Hull:
    points: np.ndarray
    line_color: tuple
    point_color: tuple

    def display_points(self):
        raise NotImplementedError

    def display_points(self):
        raise NotImplementedError


class Finger:
    """Generic class for a finger detected on the hand (outside of the palm)."""
    title: Title
    position: tuple
    length: int
    def __init__(
        self, 
        title: Title = Title.NOT_SET, 
        position: tuple = (-1, -1), length: int = 1):
        self.title: title
        self.position = position
        self.length = length
    
    def __eq__(self, other):
        return self.title == other.title
        

class Orientation(Enum):
    """ orientations for the hand"""
    FINGERS_LEFT = auto()
    FINGERS_UP = auto()
    FINGERS_RIGHT = auto()
    NOT_SET = auto()


class Hand:
    """Generic class containing all the data that the hand should contain.
    always takes a picture of a hand"""
    name: str
    
    #* fingers will be added when found 
    fingers: list
    
    #DIMENSIONS
    width: int
    height: int
    data_canvas: np.ndarray

    # FEATURES
    center: tuple
    palm_radius: int
    contour_points: list
    hull: Hull
    defects: list
    orientation: Orientation = Orientation.NOT_SET
    finger_width: int

    # UTIL
    image: np.ndarray
    
    
    def __init__(self, image: np.ndarray, name: str = "", width: int = 0, height: int = 0, palm_radius: int = 0, fingers: list = []) -> None:

        # self.image = cv.imread(f"images/{image}.jpg")
        self.image = image
        self.name = name
        self.image = image
        self.width = width
        self.height = height
        self.palm_radius = palm_radius
        self.fingers = []
        self.data_canvas: np.zeros((300, 300, 3))
        self.finger_width = self.palm_radius / 4



    # TODO this could be a dict


    def imshow_data_canvas(self) -> None:
        # cv.putText(self.data_canvas, self.name, (0, self.height), font, 0.6, (255, 0, 100), 2)
        

        # print("number of fingers: ", len(self.fingers))
        # for finger in self.fingers:
        #     print("fingername: ", finger.title)
            
        #* draw fingers
        for finger in self.fingers:
            #* choosing a color
            if finger.title == Title.THUMB_FINGER:
                line_color = Colors.thumb_color
            elif finger.title == Title.INDEX_FINGER:
                line_color = Colors.index_finger_color
            elif finger.title == Title.MIDDLE_FINGER:
                line_color = Colors.middle_finger_color
            elif finger.title == Title.RING_FINGER:
                line_color = Colors.ring_finger_color
            elif finger.title == Title.LITTLE_FINGER:
                line_color = Colors.little_finger_color
            elif finger.title == Title.NOT_SET:
                line_color = Colors.not_set_color

            #* drawing a line with the given color
            cv.line(self.data_canvas, self.center, finger.position, line_color, 1)
            cv.putText(self.data_canvas, str(finger.title.name), (finger.position[0], (finger.position[1] + 30)), font, 0.4, line_color, 1)
            cv.circle(self.data_canvas, finger.position, 8, line_color, -1)
        if self.center != None:
            cv.circle(self.data_canvas, self.center, 2, (200, 100, 50), -1)
            # cv.circle(self.data_canvas, self.center, self.palm_radius, (200, 100, 50), 1)
        cv.imshow("input data canvas", self.data_canvas)


    def print_data(self) -> None:
        """Prints all the fields of the instance of the hand and wether they are filled."""
        print(f"************ {self.name} *************")
        printout = "{:<2}: {:>50}"
        
        #* CENTER POINT
        print(printout.format("center", str(self.center)))
        
        #* ORIENTATION
        if (self.orientation != None):
            print(printout.format("orientation", str(self.orientation)))
        else:
            print(printout.format("orientation", "nope"))
        
        #* CONTOUR POINTS
        if self.contour_points != None:
            print(printout.format("contours", len(self.contour_points)))
            # print("contours: ", len(self.contour_points))
        # if self.defects != None:
        # print("defects: ", len(self.defects))
        if self.hull != None:
            print(printout.format("Hull", len(self.hull)))    
        # print("vallies")
        #* FINGERS
        for finger in self.fingers:
            if finger.position != None:
                print(printout.format("finger position", str(finger.position)))
                
        print("**************************************")


    # TODO implement
    def confirm_orientation(self):
        raise NotImplementedError()


    #TODO implement
    def confirm_finger_states(self):
        raise NotImplementedError()


        
