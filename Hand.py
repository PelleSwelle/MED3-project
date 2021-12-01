from dataclasses import dataclass, field
from enum import Enum, auto
import cv2 as cv
from cv2 import bitwise_not, data
import numpy as np
from PIL import Image
from PIL import ImageDraw
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

    def get_state(self):
        return self.state

    def set_finger_state(self, state:FingerState):
        self.state = state

    def set_finger_tip_position(self, position: tuple):
        self.fingertip_position = position


class Orientation(Enum):
    """ orientations for the hand"""
    BOTTOM_UP = auto()
    RIGHT_LEFT = auto()
    LEFT_RIGHT = auto()
    TOP_DOWN = auto()


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

    contours: list
    convex_hull: list
    finger_tips: list
    finger_vallies: list



    def __init__(self, image: Image.Image) -> None:
        self.width = None
        self.height = None
        self.orientation = None
        self.center = None

        self.extraction_image: Image.Image = image
        
        self.data_canvas: np.array = np.zeros((
            self.extraction_image.img_array.shape[0], 
            self.extraction_image.img_array.shape[1])
        )

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
        

    def print_finger_states(self):
        for finger in self.fingers:
            print(Colors.blue + "", finger.name, ", ", finger.state, "" +Colors.white)


    def imshow_all_versions(self):
        for version in self.versions:
            cv.imshow(version, version.img)


    def print_hand(self):
        print("height: ", self.height)
        print("width: ",self.width)
        print("center: ", self.center)
        print("orientation: ", self.orientation)
        print("contours: ", len(self.contours))
        self.print_finger_states()
