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

class PreProcessor:

    def __init__(self, hand: Hand) -> None:
        self.processing_image = hand.extraction_image.img_array
        self.canvas = np.zeros((self.processing_image.shape[0], self.processing_image.shape[1]))
    

    def gray_scale(self, image: Image):
        """Method for grayscaling an image. Returns the grayscaled image"""
        self.canvas = cv.cvtColor(image.img_array, cv.COLOR_BGR2GRAY)
        cv.imshow("grayscaled", self.canvas)
        return self.canvas


    def blur_gaussian(self, image: Image):
        output_image = cv.GaussianBlur(
            image.img_array, 
            [7, 7], cv.BORDER_DEFAULT)
        cv.imshow("from gaussian blur", output_image)
        return output_image


    # TODO this is used to calculate the correct threshold for the otsu algorithm
    # def calculate_threshold():
        # https://learnopencv.com/otsu-thresholding-with-opencv/


    def binarize(self, image: Image, threshold: int):
        th, thresh = cv.threshold(
            src=image.img_array, 
            thresh=threshold, 
            maxval=255, 
            type=cv.THRESH_BINARY
        )
        inverted = cv.bitwise_not(thresh)
        return inverted
