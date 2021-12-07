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
        cv.drawContours(self.canvas, contours, -1, Colors.contours_color, 3)
    

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
        raise NotImplementedError

@dataclass
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
    hull: Hull
    finger_tips: list
    finger_vallies: list
    data_canvas: DataCanvas

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


    # TODO implement
    def confirm_orientation(self):
        raise NotImplementedError()


    #TODO implement
    def confirm_finger_states(self):
        raise NotImplementedError()


    # TODO implement
    def compare_to_database(self):
        self.confirm_orientation()
        self.confirm_finger_states()


    def old_compare_to_database(self) -> None:
        # compare number of fingers
        no_of_fingers_not_decided = 0
        no_of_fingers_in = 0
        no_of_fingers_out = 0

        for finger in self.fingers:
            if finger.get_state() == FingerState.NOT_DECIDED:
                no_of_fingers_not_decided +=1        
            elif finger.get_state() == FingerState.OUT:
                no_of_fingers_out += 1
            elif finger.get_state() == FingerState.IN:
                no_of_fingers_in += 1
            
            if finger.get_state != FingerState.NOT_DECIDED:
                print("we know that...")
                if finger.get_state == FingerState.OUT:
                    print(finger.name, ": ", finger.get_state())
        
        print(no_of_fingers_not_decided, " are undecided")
        print(no_of_fingers_out, " are out")
        print(no_of_fingers_in, " are int")

        print("hand_w: ", Signs.hand_w)

        
