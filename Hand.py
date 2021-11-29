from dataclasses import dataclass, field
from enum import Enum, auto
import cv2 as cv
from cv2 import data
import numpy as np
from copy import copy
from PIL import Image
from PIL import ImageDraw
from numpy import version
from numpy.lib.histograms import _histogram_bin_edges_dispatcher
import pandas as pd
import math
import PreProcessing
import Extraction
import Colors
import Draw



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

@dataclass
class Finger:
    name: FingerName
    state: FingerState

    def get_state(self):
        return self.state

    def set_finger_state(self, state:FingerState):
        self.state = state
    
    
class ImageVersion(Enum):
    """An attribute that every image should have to keep track of different versions"""
    ORIGINAL = auto()
    GRAYSCALED = auto()
    BINARIZED = auto()
    CONTOURED = auto()
    WITH_HULL = auto()
    WITH_FINGERTIPS = auto()
    WITH_DEFECTS = auto()
    WITH_NUMBER_OF_FINGERS = auto()
    # add more

@dataclass
class Image:
    name: str
    img_array: np.array
    version: ImageVersion

class Orientation(Enum):
    """ orientations for the hand"""
    BOTTOM_UP = auto()
    RIGHT_LEFT = auto()
    LEFT_RIGHT = auto()
    TOP_DOWN = auto()

@dataclass
class Hand:
    """
    Generic class containing all the data that the hand should contain.
    
    contains a list of current versions
    """
    # TODO for the image, this should be the Image datatype
    extraction_image: np.array
    data_canvas: np.array
    width: int
    height: int
    
    # data to be extracted from the image
    index_finger: Finger
    middle_finger: Finger
    ring_finger: Finger
    little_finger: Finger
    thumb_finger: Finger
    
    # field(init=false) does that this is not a part of the implicit constructor
    versions: list = field(init=False)
    def print_finger_states(self):
        for finger in self.fingers:
            print(Colors.blue + "", finger.name, ", ", finger.state, "" +Colors.white)

    def imshow_all_versions(self):
        for version in self.versions:
            cv.imshow(version, version.img)
            

class PreProcessor:
    processing_image: Image
    canvas: np.array
    hand: Hand

    def __init__(self, hand: Hand) -> None:
        self.processing_image = hand.extraction_image
        self.canvas = np.zeros((self.processing_image.shape[0], self.processing_image.shape[1]))
    
    def gray_scale(self):
        """Method for grayscaling an image. Returns the grayscaled image"""
        self.canvas = cv.cvtColor(self.processing_image, cv.COLOR_BGR2GRAY)
        cv.imshow("grayscaled", self.canvas)
        return self.canvas
    
    def binarize(self, hand: Hand):
        for image in hand.versions:
            if image.version == ImageVersion.GRAYSCALED:
                th, otsuThresh = cv.threshold(image.img_array, 128, 192, cv.THRESH_OTSU)
            
        return otsuThresh

def main():
    img = Image (
        name="original image", 
        img_array=cv.imread("reference/Wsign2.jpg"), 
        version=ImageVersion.ORIGINAL)

    hand = Hand(
        extraction_image=img.img_array, 

        width=img.img_array.shape[0], 
        height=img.img_array.shape[1], 

        data_canvas=np.zeros((
            img.img_array.shape[0], 
            img.img_array.shape[1])), 
        index_finger=Finger(FingerName.INDEX_FINGER, FingerState.NOT_DECIDED),
        middle_finger=Finger(FingerName.MIDDLE_FINGER, FingerState.NOT_DECIDED),
        ring_finger=Finger(FingerName.RING_FINGER, FingerState.NOT_DECIDED),
        little_finger=Finger(FingerName.LITTLE_FINGER, FingerState.NOT_DECIDED),
        thumb_finger=Finger(FingerName.THUMB_FINGER, FingerState.NOT_DECIDED)
    )

    preprocesser = PreProcessor(hand)
    grayscaled_image = Image(
        name="grayscaled image",
        img_array=preprocesser.gray_scale(),
        version=ImageVersion.GRAYSCALED
    )

    
    # hand.print_finger_states()

    # hand.imshow_all_versions()

    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__=="__main__":
    main()