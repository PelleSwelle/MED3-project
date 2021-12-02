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


class FingerState(Enum):
    """states that a finger can be in"""
    IN = auto()
    OUT = auto()
    NOT_DECIDED = auto()

    # for now only intended for the thumb
    TOUCHING_INDEX = auto()
    TOUCHING_MIDDLE = auto()
    TOUCHING_RING = auto()
    TOUCHING_LITTLE = auto()


class FingerName(Enum):
    INDEX_FINGER = auto()
    MIDDLE_FINGER = auto()
    RING_FINGER = auto()
    LITTLE_FINGER = auto()
    THUMB_FINGER = auto()


class Finger:
    """Generic class for each finger on the hand."""
    name: FingerName
    state: FingerState

    fingertip_position: tuple

    def __init__(self, name: FingerName) -> None:
        self.name = name
        self.state = FingerState.NOT_DECIDED
        self.fingertip_position = None

    def get_state(self) -> FingerState:
        return self.state

    def set_finger_state(self, state:FingerState) -> None:
        self.state = state

    def set_finger_tip_position(self, position: tuple) -> None:
        self.fingertip_position = position


class Orientation(Enum):
    """ orientations for the hand"""
    FINGERS_LEFT = auto()
    FINGERS_UP = auto()
    FINGERS_RIGHT = auto()


class DataCanvas:
    """A blank canvas able to draw on it self"""
    canvas: np.array

    def __init__(self) -> None:
        self.canvas = np.zeros((0, 0))
    
    def get_size(self):
        return (self.canvas.shape[0], self.canvas.shape[1])
    
    def set_size(self,size: tuple):
        self.canvas = np.zeros(size)

    def add_contours(self, contours: list) -> None:
        cv.drawContours(self.canvas, contours, -1, Colors.contours_color, 1)
    
    def add_finger_point(self, coordinate: tuple) -> None:
        # TODO write the name of the finger on the canvas
        cv.circle(self.canvas, coordinate, 2, Colors.fingertip_color, -1)

    def add_center_point(self, center_point: tuple) -> None:
        # TODO write on the image
        cv.circle(self.canvas, center_point, 2, Colors.center_color, -1)

    def add_hull(self, hull) -> None:
        cv.drawContours(
            image=self.canvas, 
            contours=hull, 
            contourIdx=-1, 
            color=Colors.hull_color, 
            thickness=1
        )

    def add_defects(self, defects) -> None:
        pass



class Hand:
    """Generic class containing all the data that the hand should contain."""
    
    height: int
    width: int
    center: tuple
    orientation: Orientation
    
    index_finger: Finger
    middle_finger: Finger
    ring_finger: Finger
    little_finger: Finger
    thumb_finger: Finger

    contours: tuple
    convex_hull: list
    finger_tips: list
    finger_vallies: list

    def __init__(self) -> None:
        self.width = None
        self.height = None
        self.orientation = None
        self.center = None

        # self.extraction_image: Image.Image = image
        
        self.data_canvas = DataCanvas()

        # data to be extracted from the image
        self.index_finger = Finger(FingerName.INDEX_FINGER)
        self.middle_finger = Finger(FingerName.MIDDLE_FINGER)
        self.ring_finger = Finger(FingerName.RING_FINGER)
        self.little_finger = Finger(FingerName.LITTLE_FINGER)
        self.thumb_finger = Finger(FingerName.THUMB_FINGER)
        
        self.fingers: list = [
            self.index_finger, 
            self.middle_finger, 
            self.ring_finger, 
            self.little_finger, 
            self.thumb_finger
        ]
        

    def print_finger_states(self) -> None:
        for finger in self.fingers:
            print(Colors.blue + "", finger.name, ", ", finger.state, "" +Colors.white)


    def imshow_data_canvas(self) -> None:
        cv.imshow("data extracted", self.data_canvas.canvas)


    def imshow_all_versions(self) -> None:
        for version in self.versions:
            cv.imshow(version, version.img)


    def print_hand(self) -> None:
        print("height: ", self.height)
        print("width: ",self.width)
        print("center: ", self.center)
        print("orientation: ", self.orientation)
        print("contours: ", len(self.contours))
        self.print_finger_states()
