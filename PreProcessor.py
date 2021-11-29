from dataclasses import dataclass
from enum import Enum, auto
import cv2 as cv
import numpy as np
from copy import copy
from PIL import Image
from PIL import ImageDraw
from numpy.lib.histograms import _histogram_bin_edges_dispatcher
import pandas as pd
import math
from Hand import Hand
import PreProcessing
import Extraction
import Colors

class PreProcessor:
    array: np.array
    image: Image.Image

    canvas: np.array

    def __init__(self, hand: Hand) -> None:
        self.array = Hand.extraction_image
        self.image = Image.fromarray(self.array)
        self.canvas = np.zeros(self.array)
    
    def gray_scale(self):
        pxls = self.image  # load the pixel data from the image
        height, width = self.image.size  # get the size of the image

        for row in range(0, height):
            for column in range(0, width):
                red_channel, blue_channel, green_channel = pxls[row, column]  # capture the color channels
                avg = math.floor((red_channel + blue_channel + green_channel) / 3)  # grayscale image is when all three color values are the same
                # fill the canvas with the new values
                self.canvas.putpixel((row, column), (avg, avg, avg))
        #       TODO this should convert to a single channel (from black to white)

        return self.canvas