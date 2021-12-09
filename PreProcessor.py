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
    # def __init__(self) -> None:
    #     self.processing_image = image.img_array
    #     self.canvas = np.zeros((self.processing_image.shape[0], self.processing_image.shape[1]))
    
    def blur_gaussian(self, image: np.ndarray) -> np.ndarray:
        raise NotImplementedError


    def gray_scale(self, image: np.ndarray) -> np.ndarray: 
        """Method for grayscaling an image. Returns the grayscaled image"""
        return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    
    # TODO this is used to calculate the correct threshold for the otsu algorithm
    # def calculate_threshold() -> int?:
        # https://learnopencv.com/otsu-thresholding-with-opencv/


    def binarize(self, image: np.ndarray, threshold: int) -> np.ndarray:
        th, thresh = cv.threshold(
            src=image, 
            thresh=threshold, 
            maxval=255, 
            type=cv.THRESH_BINARY
        )
        inverted = cv.bitwise_not(thresh)
        return inverted
    
    def crop(self, image: Image):
        # TODO set a standard size to make it into
        raise NotImplementedError

    def preprocess(self, image: np.ndarray) -> np.ndarray:
        """ combining blurring, grayscalling, thresholding, contouring, and cropping into one"""

        gaussian_blurred = cv.GaussianBlur(image, [5, 5], 1)
        
        grayscaled = cv.cvtColor(gaussian_blurred, cv.COLOR_BGR2GRAY)
        
        ret, thresh = cv.threshold(grayscaled, 245, 255, cv.THRESH_BINARY_INV)
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        
       
        contours_drawn = np.zeros(thresh.shape, dtype=np.uint8)
        
        x, y, w, h = cv.boundingRect(contours[0])
        cropped_binarized_image = thresh[y:y+h, x:x+w]
        # cropped_contoured_image = contours_drawn[y:y+h, x:x+w]
        
        
        print(f"image size is now: {cropped_binarized_image.shape[0]} x {cropped_binarized_image.shape[1]}")
        
        # TODO here goes normalize to size of palm 

        return cropped_binarized_image
   