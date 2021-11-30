import cv2 as cv
import numpy as np
import Colors

class Draw:
    canvas: np.array


    def __init__(self, canvas: np.array) -> None:
        self.canvas = canvas


    def draw_circle(self, center: tuple, color):
        cv.circle(self.canvas, center, 2, color, 1)


    def draw_line(self, pt1: tuple, pt2: tuple, color):
        cv.line(self.canvas, pt1, pt2, color, 1)
