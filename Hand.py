from dataclasses import dataclass, field
from enum import Enum, auto
from os import stat
import cv2 as cv
from cv2 import bitwise_not, data
import numpy as np
from PIL import Image
from PIL import ImageDraw
from numpy.core.defchararray import center
from numpy.lib.histograms import _histogram_bin_edges_dispatcher
import math
import Colors
import Draw
import Image
from typing import Tuple

font = cv.FONT_HERSHEY_COMPLEX

class State(Enum):
    """states that a finger can be in"""
    IN = auto()
    OUT = auto()
    NOT_SET = auto()

    # for now only intended for the thumb
    TOUCHING_INDEX = auto()
    TOUCHING_MIDDLE = auto()
    TOUCHING_RING = auto()
    TOUCHING_LITTLE = auto()


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
    """Generic class for each finger on the hand."""
    title: Title
    position: tuple
    state: State
    def __init__(self, title: Title = Title.NOT_SET, position: tuple = (-1, -1), state: State = State.NOT_SET) -> None:
        self.title: title
        self.position = position

        self.state = state
        

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
    
    
    def __init__(
        self, 
        image: np.ndarray,
        name: str = "", 
        width: int = 0, 
        height: int = 0, 
        palm_radius: int = 0, 
        fingers: list = []) -> None:

        self.image = cv.imread(f"images/alphabet/{image}.png")
        self.name = name
        self.image
        self.width = width
        self.height = height
        self.palm_radius = palm_radius
        self.fingers = []
        self.data_canvas: np.zeros((300, 300, 3))
        # self.fingers = [self.finger1, self.finger2, self.finger3, self.finger4, self.finger5]
        self.finger_width = self.palm_radius / 4

    

    # TODO this could be a dict


    def imshow_data_canvas(self) -> None:
        self.data_canvas = np.zeros((self.width, self.height, 3))
        print("self.height", self.height)
        cv.putText(self.data_canvas, self.name, (0, self.height), font, 0.6, (255, 0, 100), 2)
        if self.center != None:
            cv.circle(self.data_canvas, self.center, 2, (200, 100, 50), -1)
        cv.imshow("data extracted", self.data_canvas)


    def print_data(self) -> None:
        """Prints all the fields of the instance of the hand and wether they are filled."""
        print(f"************ {self.name} *************")
        print("center: ", self.center)
        
        if (self.orientation != None):
            print("orientation: ", self.orientation)
        else:
            print("no orientation")
        
        if self.contour_points != None:
            print("contours: ", len(self.contour_points))
        # if self.defects != None:
        # print("defects: ", len(self.defects))
        # print("hull: ", len(self.hull))
        # print("vallies")
        for finger in self.fingers:
            print(finger.name)
        print("**************************************")


    # TODO implement
    def confirm_orientation(self):
        raise NotImplementedError()


    #TODO implement
    def confirm_finger_states(self):
        raise NotImplementedError()


        
