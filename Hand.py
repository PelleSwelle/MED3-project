from dataclasses import dataclass, field
from enum import Enum, auto
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

class state(Enum):
    """states that a finger can be in"""
    IN = auto()
    OUT = auto()
    NOT_SET = auto()

    # for now only intended for the thumb
    TOUCHING_INDEX = auto()
    TOUCHING_MIDDLE = auto()
    TOUCHING_RING = auto()
    TOUCHING_LITTLE = auto()


class Name(Enum):
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
    """
    Generic class for each finger on the hand. 
    Instatiates with the state set to not set. 
    """
    def __init__(self, name: Name) -> None:
        self.name: name
        self.position: tuple = (-1, -1)

        self.state: state = state.NOT_SET


class Orientation(Enum):
    """ orientations for the hand"""
    FINGERS_LEFT = auto()
    FINGERS_UP = auto()
    FINGERS_RIGHT = auto()
    NOT_SET = auto()

class Hand:
    """Generic class containing all the data that the hand should contain."""
    name: str
    # FINGERS
    index: Finger
    middle: Finger
    ring: Finger
    little: Finger
    thumb: Finger
    fingers: list

    # FINGER VALLIES
    thumb_index_valley: tuple = (0, 0)
    index_middle_valley: tuple = (0, 0)
    middle_ring_valley: tuple = (0, 0)
    ring_little_valley: tuple = (0, 0)
    
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
    
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.thumb = Finger(name=Name.THUMB_FINGER)
        self.index = Finger(name=Name.INDEX_FINGER)
        self.ring = Finger(name=Name.RING_FINGER)
        self.middle = Finger(name=Name.MIDDLE_FINGER)
        self.little = Finger(name=Name.LITTLE_FINGER)

        self.width = 0
        self.height = 0
        self.palm_radius = 1
        self.fingers = [self.thumb, self.index, self.middle, self.ring, self.little]
        self.data_canvas = np.zeros((self.width, self.height))
        self.finger_width = self.palm_radius / 4

    

    # TODO this could be a dict


    def imshow_data_canvas(self) -> None:
        cv.imshow(winname="data extracted", mat=self.data_canvas)


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
        print(f"Finger: {self.index.state}")
        print(f"Finger: {self.middle.state}")
        print(f"Finger: {self.ring.state}")
        print(f"Finger: {self.little.state}")
        print(f"Finger: {self.thumb.state}")
        print("**************************************")


    # TODO implement
    def confirm_orientation(self):
        raise NotImplementedError()


    #TODO implement
    def confirm_finger_states(self):
        raise NotImplementedError()


        
