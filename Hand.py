from dataclasses import dataclass, field
from enum import Enum, auto
import cv2 as cv
from cv2 import bitwise_not, data
import numpy as np
from copy import copy
from PIL import Image
from PIL import ImageDraw
from numpy.lib.histograms import _histogram_bin_edges_dispatcher
import math
import Extraction
import Colors
import Draw
import Image


class FingerState(Enum):
    """states that a finger can be in"""
    IN = auto()
    OUT = auto()
    NOT_DECIDED = auto()


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

    def get_state(self):
        return self.state

    def set_finger_state(self, state:FingerState):
        self.state = state


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
    contours: list
    

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

class PreProcessor:

    def __init__(self, hand: Hand) -> None:
        self.processing_image = hand.extraction_image.img_array
        self.canvas = np.zeros((self.processing_image.shape[0], self.processing_image.shape[1]))
    
    def gray_scale(self, image: Image.Image):
        """Method for grayscaling an image. Returns the grayscaled image"""
        self.canvas = cv.cvtColor(image.img_array, cv.COLOR_BGR2GRAY)
        cv.imshow("grayscaled", self.canvas)
        return self.canvas
    
    def binarize(self, image: Image.Image):
        th, otsu_thresh = cv.threshold(image.img_array, 240, 255, cv.THRESH_OTSU)
        inverted = bitwise_not(otsu_thresh)
        return inverted

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

        
    def convex_hull(self, contours):
        # create hull array for convex hull points
        hull = cv.convexHull(contours, returnPoints=False)

        cv.drawContours(self.canvas, hull, -1, (0, 255, 0), 1)
        

        return self.canvas

    # def get_convex_hull_points(self, hull):