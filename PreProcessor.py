from dataclasses import dataclass
from enum import Enum, auto
import cv2 as cv
import numpy as np
from copy import copy
from PIL import Image
from PIL import ImageDraw
from numpy.lib.histograms import _histogram_bin_edges_dispatcher
import math
import Colors
from Hand import Hand
from Image import Image

# TODO this should be an interface
class PreProcessor:

    def __init__(self, image: Image) -> None:
        self.processing_image = image.img_array
        self.canvas = np.zeros((self.processing_image.shape[0], self.processing_image.shape[1]))
    

    def gray_scale(self, image: Image) -> np.ndarray: 
        """Method for grayscaling an image. Returns the grayscaled image"""
        return cv.cvtColor(image.img_array, cv.COLOR_BGR2GRAY)


    def blur_gaussian(self, image: Image) -> np.ndarray:
        output_image = cv.GaussianBlur(
            image.img_array, 
            [7, 7], cv.BORDER_DEFAULT)
        return output_image

    # TODO this is used to calculate the correct threshold for the otsu algorithm
    # def calculate_threshold() -> int?:
        # https://learnopencv.com/otsu-thresholding-with-opencv/


    def binarize(self, image: Image, threshold: int) -> np.ndarray:
        th, thresh = cv.threshold(
            src=image.img_array, 
            thresh=threshold, 
            maxval=255, 
            type=cv.THRESH_BINARY
        )
        inverted = cv.bitwise_not(thresh)
        return inverted
    
    def crop(self, image: Image):
        # TODO set a standard size to make it into
        raise NotImplementedError
