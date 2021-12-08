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
    NOT_DECIDED = auto()

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

@dataclass
class Finger:
    """
    Generic class for each finger on the hand. 
    Instatiates with the state set to not set. 
    """
    name: Name
    position: tuple = (-1, -1)

    state: state = state.NOT_DECIDED


class Orientation(Enum):
    """ orientations for the hand"""
    FINGERS_LEFT = auto()
    FINGERS_UP = auto()
    FINGERS_RIGHT = auto()


@dataclass
class Hand:
    """Generic class containing all the data that the hand should contain."""
    
    orientation: Orientation


    contour_points: list
    hull: Hull
    defects: list
    

    # TODO this could be a dict
    thumb_index_valley: tuple = (-1, -1)
    index_middle_valley: tuple = (-1, -1)
    middle_ring_valley: tuple = (-1, -1)
    ring_little_valley: tuple = (-1, -1)

    index: Finger = Finger(Name.INDEX_FINGER)
    middle: Finger = Finger(Name.MIDDLE_FINGER)
    ring: Finger = Finger(Name.RING_FINGER)
    little: Finger = Finger(Name.LITTLE_FINGER)
    thumb: Finger = Finger(Name.THUMB_FINGER)
     
    width: int = 1
    height: int = 1
    data_canvas: np.ndarray = np.zeros((width, height))
    center: tuple = (-1, -1)


    def imshow_data_canvas(self) -> None:
        cv.imshow(winname="data extracted", mat=self.data_canvas)


    def print_data(self) -> None:
        print("************ HAND DATA *************")
        print("center: ", self.center)
        print("orientation: ", self.orientation)
        print("contours: ", len(self.contour_points))
        print("defects: ", self.defects)
        # print("hull: ", len(self.hull))
        print("vallies")
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


    # TODO implement
    def compare_to_database(self):
        self.confirm_orientation()
        self.confirm_finger_states()


    # def old_compare_to_database(self) -> None:
        # compare number of fingers
        no_of_fingers_not_decided = 0
        no_of_fingers_in = 0
        no_of_fingers_out = 0

        for finger in self.fingers:
            if finger.get_state() == state.NOT_DECIDED:
                no_of_fingers_not_decided +=1        
            elif finger.get_state() == state.OUT:
                no_of_fingers_out += 1
            elif finger.get_state() == state.IN:
                no_of_fingers_in += 1
            
            if finger.get_state != state.NOT_DECIDED:
                print("we know that...")
                if finger.get_state == state.OUT:
                    print(finger.name, ": ", finger.get_state())
        
        print(no_of_fingers_not_decided, " are undecided")
        print(no_of_fingers_out, " are out")
        print(no_of_fingers_in, " are int")

        print("hand_w: ", Signs.hand_w)

        
