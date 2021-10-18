import numpy as np
import cv2 as cv
from PIL import Image

def detectCenter(src):
    pixls = src.load()

    # run through pixels left to right
    # top to bottom
    # if find black