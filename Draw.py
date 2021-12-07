import cv2 as cv
import numpy as np
import Colors




def draw_circle(canvas: np.array, center: tuple, color) -> None:
    cv.circle(canvas, center, 2, color, 1)


def draw_line(canvas: np.array, pt1: tuple, pt2: tuple, color) -> None:
    cv.line(canvas, pt1, pt2, color, 1)
