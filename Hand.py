from enum import Enum, auto
import cv2 as cv
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
    """Generic class containing all the data that the hand should contain."""
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
    hull: list
    defects: list
    orientation: Orientation = Orientation.NOT_SET
    finger_width: int

    # UTIL
    image: np.ndarray
    
    
    def __init__(self, image: np.ndarray, name: str = "", width: int = 0, height: int = 0, palm_radius: int = 0, fingers: list = []) -> None:
        self.image = image
        self.name = name
        self.image = image
        self.width = width
        self.height = height
        self.palm_radius = palm_radius
        self.fingers = []
        self.data_canvas: np.zeros((300, 300, 3))
        self.finger_width = self.palm_radius / 4


    def imshow_data_canvas(self) -> None:
        """Draws all the available data to the data canvas and displays it in a openCV window"""
        for finger in self.fingers:
            #* CHOOSING COLORS
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
            
            #* DRAW FINGER LINES
            cv.line(self.data_canvas, self.center, finger.position, line_color, 1)
            #* DRAW POINT AT FINGERTIP
            cv.circle(self.data_canvas, finger.position, 8, line_color, -1)
            #* WRITE NAME OF FINGER ON FINGER
            cv.putText(self.data_canvas, str(finger.title.name), (finger.position[0], (finger.position[1] + 30)), font, 0.4, line_color, 1)
        

        #* DRAWING THE CONTOURS
        cv.drawContours(
            image=self.data_canvas, 
            contours=self.contours, 
            contourIdx= -1, 
            color=Colors.contours_color, 
            thickness=1)

        #* DRAWING THE CENTER POINT
        cv.circle(
            img=self.data_canvas, 
            center=self.center, 
            radius=2, 
            color=Colors.center_color, 
            thickness=1)
        
        #* DRAWING THE PALM CIRCUMFERENCE
        cv.circle(
            img=self.data_canvas, 
            center=self.center, 
            radius=self.palm_radius, 
            color=Colors.center_color,
            thickness= 1)
        
        #* DRAWING THE HULL
        cv.drawContours(
            image=self.data_canvas, 
            contours=self.hull, 
            contourIdx= -2, 
            color=Colors.hull_color,
            thickness=1)

        cv.imshow("input data canvas", self.data_canvas)


    def print_data(self) -> None:
        """Prints all the fields of the instance of the hand and wether they are filled."""
        print(f"************ {self.name} *************")
        #* PLACEHOLDER FOR OUTPUT TEXT
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
        #* HULL    
        if self.hull != None:
            print(printout.format("Hull", len(self.hull)))    
        #* FINGERS
        for finger in self.fingers:
            if finger.position != None:
                print(printout.format("finger position", str(finger.position)))
                
        print("**************************************")



        
