import cv2 as cv
import numpy as np
from numpy.lib.type_check import imag

import Colors
from Extractor import Extractor
from Hand import Finger, Name, state, Hand, Orientation
from Image import Image, ImageVersion
from PreProcessor import PreProcessor

steps = []
font = cv.FONT_HERSHEY_COMPLEX

def print_images():
    print(Colors.green + "current content of images:")
    for image in steps:
        print(Colors.green + image.name, ", ", image.version, "" + Colors.white)


def get_version(version: ImageVersion):
    image_to_return: Image
    for image in steps:
        if image.version == version:
            image_to_return = image
    return image_to_return


def main():

    # ************** DATABASE ******************

    REFERENCE_W = Hand(
        center=(154, 316),
        orientation=Orientation.FINGERS_UP,
        index=Finger(Name.INDEX_FINGER),
        middle=Finger(Name.MIDDLE_FINGER),
        ring=Finger(Name.RING_FINGER),
        little=Finger(Name.LITTLE_FINGER),
        thumb=Finger(Name.THUMB_FINGER),
        contour_points=None,
        hull=None,
        defects=None,
        thumb_index_valley=None,
        index_middle_valley=(100, 200),
        middle_ring_valley=(150, 200),
        ring_little_valley= (196, 226))

    REFERENCE_W.index.position = (11, 41)
    REFERENCE_W.middle.position = (113, 0)
    REFERENCE_W.ring.position = (222, 59)
    REFERENCE_W.index.state = state.OUT
    REFERENCE_W.middle.state = state.OUT
    REFERENCE_W.ring.state = state.OUT
    REFERENCE_W.little.state = state.IN
    REFERENCE_W.thumb.state = state.IN

    # ******************* DRAWING ON THE REFERENCE IMAGE **********************
    # finger tips
    cv.circle(REFERENCE_W.data_canvas, REFERENCE_W.index.position, 2, Colors.fingertip_color, 2)
    cv.putText(REFERENCE_W.data_canvas, "index tip", REFERENCE_W.index.position, font, 0.5, Colors.fingertip_color, 1)
    
    cv.circle(REFERENCE_W.data_canvas, REFERENCE_W.middle.position, 2, Colors.fingertip_color, 2)
    cv.putText(REFERENCE_W.data_canvas, "middle tip", REFERENCE_W.middle.position, font, 0.5, Colors.fingertip_color, 1)
    
    cv.circle(REFERENCE_W.data_canvas, REFERENCE_W.ring.position, 2, Colors.fingertip_color, 2)
    cv.putText(REFERENCE_W.data_canvas, "ring tip", REFERENCE_W.ring.position, font, 0.5, Colors.fingertip_color, 1)

    # vallies
    cv.circle(REFERENCE_W.data_canvas, REFERENCE_W.index_middle_valley, 2, (255, 255, 255), 2)
    cv.circle(REFERENCE_W.data_canvas, REFERENCE_W.middle_ring_valley, 2, (255, 255, 255), 2)
    cv.circle(REFERENCE_W.data_canvas, REFERENCE_W.ring_little_valley, 2, (255, 255, 255), 2)

    # palm center
    cv.circle(REFERENCE_W.data_canvas, REFERENCE_W.center, 2, Colors.center_color, 2)
    cv.putText(REFERENCE_W.data_canvas, "palm center", REFERENCE_W.center, font, 0.5, Colors.center_color, 1)
    # cv.circle(REFERENCE_W.data_canvas, REFERENCE_W.little.position, 2, Colors.fingertip_color, 2)
    # cv.circle(REFERENCE_W.data_canvas, REFERENCE_W.thumb.position, 2, Colors.fingertip_color, 2)


    # ***************READ IMAGE AND PREPROCESS*********************

    # instantiate a hand to eventually fill with data
    test_hand = Hand(
        center=None, 
        orientation=None, 
        contour_points=None, 
        hull=None, 
        defects=None)

    image_read = cv.imread("images/alphabet/W.png")

    cv.imshow("original", image_read)
    
    preprocesser = PreProcessor()

    extraction_image = preprocesser.preprocess(image_read)

    cv.imshow("image ready to be extracted", extraction_image)

    # ****************** SET DATA CANVAS SIZE************************
    
    REFERENCE_W.data_canvas = np.zeros([extraction_image.shape[0], extraction_image.shape[1], 3], dtype=np.uint8)
    test_hand.data_canvas = np.zeros([extraction_image.shape[0], extraction_image.shape[1], 3], dtype=np.uint8)
    
    extractor = Extractor()
    # # TODO implement Classifier

    # # ************** FEATURE EXTRACTION ******************
    
    cv_contours, _ = cv.findContours(
        image=extraction_image,
        mode=cv.RETR_TREE,
        method=cv.CHAIN_APPROX_SIMPLE)



    cv.drawContours(
            image=test_hand.data_canvas, 
            contours=cv_contours, 
            contourIdx= -1, 
            color=Colors.contours_color, 
            thickness=1)

    test_hand.center, test_hand.palm_radius = extractor.find_center(extraction_image)
    
    cv.circle(test_hand.data_canvas, test_hand.center, test_hand.palm_radius, Colors.center_color, 1)
    cv.circle(test_hand.data_canvas, test_hand.center, 2, Colors.center_color, 1)

    contour_coordinates = extractor.get_list_of_coordinates_from_contours(cv_contours)
    

    test_hand.contour_points = contour_coordinates
    
    for coordinate_set in test_hand.contour_points:
        cv.circle(
            img=test_hand.data_canvas, 
            center=(coordinate_set[0], coordinate_set[1]), 
            radius=1, 
            color=Colors.contours_color, 
            thickness=1)

    

    #     # Find the convex hull object for each contour
    hull_list = []
    for i in range(len(cv_contours)):
        hull = cv.convexHull(cv_contours[i])
        hull_list.append(hull)
    
    test_hand.hull = hull_list

    cv.drawContours(test_hand.data_canvas, test_hand.hull, -2, Colors.hull_color, 1)
    

    test_hand.defects = extractor.extract_defects(
        contours=cv_contours[0]
    )
    # print("defects: \n", defects) # yay
    # # TODO add to hand

    # defects_image = np.zeros(original_img_size)

    extractor.draw_defects(
        defects=test_hand.defects, 
        cnt=cv_contours[0], 
        output_image=test_hand.data_canvas
    )

    cv.imshow("HAND DATA", test_hand.data_canvas)
    cv.imshow("REF DATA", REFERENCE_W.data_canvas)
    # test_hand.print_data()
    # # hand_w.print_data()

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__=="__main__":
    main()
