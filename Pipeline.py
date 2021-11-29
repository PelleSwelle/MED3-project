import cv2 as cv
import numpy as np
from copy import copy
from PIL import Image
from PIL import ImageDraw
import pandas as pd
import math
import PreProcessing
import Extraction
import Colors


def main():
    
    # LOAD IMAGE
    image = Image.fromarray(cv.imread('reference/Wsign2.jpg'))
    print("loaded image: W")

    image = PreProcessing.downSize(image, 0.4)

    cv.imshow("downsized", np.array(image))
    print("downsized")

    # GAUSSIAN BLUR
    # img_blurred = blur_gaussian(img_color)

    # GRAYSCALE
    array_grayscale = cv.cvtColor(np.array(image), cv.COLOR_BGR2GRAY)
    cv.imshow("grayscaled", array_grayscale)
    print("grayscaled the image")

    # THRESHOLDING
    ret, array_thresh = cv.threshold(array_grayscale, 240, 255, 0)
    cv.imshow("thresholded", array_thresh)
    print("thresholded the image")

    # CONVERT TO SINGLE CHANNEL
    thresholded = PreProcessing.convertToSingleChannel(Image.fromarray(array_thresh))
    print("converted to single channel")

    # INVERT COLORS
    inverted = PreProcessing.invertColor(thresholded)
    array_inverted = np.array(inverted)
    cv.imshow("inverted", array_inverted)
    print("inverted the colors of the image")

    # GET CONTOURS
    contours, hierarchy = cv.findContours(array_inverted, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = max(contours, key=lambda x: cv.contourArea(x))
    print("number of contours: ", len(contours))

    # DRAW THE CONTOURS
    array_original = np.array(image)
    cv.drawContours(array_original, [contours], -1, Colors.contours_color, 2)
    cv.imshow("contours", array_original)

    # GET AND DRAW THE HULL
    convex_hull = []
    for i in range(len(contours)):
        # creating convex hull object for each contour
        hull_point = cv.convexHull(contours[i], False)
        convex_hull.append(hull_point[0])
    # print("hull:", hull)

    convex_hull = cv.convexHull(contours, returnPoints=True)
    cv.drawContours(array_original, [convex_hull], -1, Colors.hull_color, 1)
    cv.imshow("hull", array_original)

    
    # for fingertip in range(len(fingertips)):
    #     cv.line(array_original, centerCoords, fingertip, 4, [0, 0, 255], -1)

    defects = Extraction.get_defects(contours=contours)
    

    no_of_fingers = Extraction.get_number_of_fingers(defects, contours, thresholded, array_original)

    defect_x_values = []
    defect_y_values = []
    defect_coordinates = [tuple()]
    for elmt in defects:
        # print(Colors.red+ "drawing circle at: ", elmt[0][0], ", ", elmt[0][1], "" + Colors.white)
        # cv.circle(array_original, (elmt[0][0], elmt[0][1]), 2, Colors.fingertip_color, -1)
        defect_x_values.append(elmt[0][0])
        defect_y_values.append(elmt[0][1])
        defect_coordinates.append((elmt[0][1], elmt[0][2]))
    print("defect coordinates: ", defect_coordinates)

    
    
    
    # get lowest defect


    cv.imshow("defects", array_original)


    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
