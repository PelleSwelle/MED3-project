from enum import Enum, auto
import numpy as np
import cv2 as cv

class ImageVersion(Enum):
    """An attribute that every image should have to keep track of different versions"""
    ORIGINAL = auto()
    BLURRED = auto()
    GRAYSCALED = auto()
    BINARIZED = auto()
    CONTOURED = auto()
    CROPPED = auto()
    WITH_HULL = auto()
    WITH_FINGERTIPS = auto()
    WITH_DEFECTS = auto()
    WITH_NUMBER_OF_FINGERS = auto()
    
    REFERENCE = auto()
    # add more

class Image:
    name: str
    img_array: np.ndarray
    version: ImageVersion


    def __init__(self, name: str, img_array: np.array, version: ImageVersion) -> None:
        self.name = name
        self.img_array = img_array
        self.version = version


    def display(self):
        cv.imshow(
            winname=str(self.name),
            mat=self.img_array
        )

    # def process_image(self):
        # grayscale
        # apply gaussian blur
        # binarize
        # contour