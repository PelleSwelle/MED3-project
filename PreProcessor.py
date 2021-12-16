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

# TODO this should be an interface
class PreProcessor:
    # def __init__(self) -> None:
    #     self.processing_image = image.img_array
    #     self.canvas = np.zeros((self.processing_image.shape[0], self.processing_image.shape[1]))
 
 
  
    def preprocess(self, image: np.ndarray) -> np.ndarray:
        """ combining blurring, grayscalling, thresholding, contouring, and cropping into one"""

        gaussian_blurred = cv.GaussianBlur(image, [5, 5], 1)
        cv.imshow("gaussian blurred", gaussian_blurred)
        
        grayscaled = cv.cvtColor(gaussian_blurred, cv.COLOR_BGR2GRAY)
        cv.imshow("gaussian_blurred,  grayscaled", grayscaled)
        ret, thresh = cv.threshold(grayscaled, 245, 255, cv.THRESH_BINARY_INV)
        cv.imshow("blurred, grayscaled, thresholded", thresh)
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        

        
        x, y, w, h = cv.boundingRect(contours[0])

        cropped_binarized_image = thresh[y:y+h, x:x+w]
        
        
        print(Colors.blue + f"cropped input image to: {cropped_binarized_image.shape[0]} x {cropped_binarized_image.shape[1]}" + Colors.white)
        
        return cropped_binarized_image
   