import cv2 as cv
import numpy as np
from numpy.lib.type_check import imag
from Classifyer import Classifier

import Colors
from Extractor import Extractor
from Hand import Finger, Name, state, Hand, Orientation
from Image import Image, ImageVersion
from PreProcessor import PreProcessor
from math import dist, sqrt

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

    REFERENCE_W = Hand("DATABASE: W")

    REFERENCE_W.center=(154, 316)
    REFERENCE_W.contour_points=None
    REFERENCE_W.hull=None
    REFERENCE_W.defects=None
    REFERENCE_W.thumb_index_valley=(0, 0)
    REFERENCE_W.index_middle_valley=(100, 200)
    REFERENCE_W.middle_ring_valley=(150, 200)
    REFERENCE_W.ring_little_valley= (196, 226)


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

    # # vallies
    cv.circle(REFERENCE_W.data_canvas, REFERENCE_W.index_middle_valley, 2, (255, 255, 255), 2)
    cv.circle(REFERENCE_W.data_canvas, REFERENCE_W.middle_ring_valley, 2, (255, 255, 255), 2)
    cv.circle(REFERENCE_W.data_canvas, REFERENCE_W.ring_little_valley, 2, (255, 255, 255), 2)

    # palm center
    cv.circle(REFERENCE_W.data_canvas, REFERENCE_W.center, 2, Colors.center_color, 2)
    cv.putText(REFERENCE_W.data_canvas, "palm center", REFERENCE_W.center, font, 0.5, Colors.center_color, 1)
    cv.circle(REFERENCE_W.data_canvas, REFERENCE_W.little.position, 2, Colors.fingertip_color, 2)
    cv.circle(REFERENCE_W.data_canvas, REFERENCE_W.thumb.position, 2, Colors.fingertip_color, 2)


    # ***************READ IMAGE AND PREPROCESS*********************

    # instantiate a hand to eventually fill with data
    test_hand = Hand("test hand")
    
    test_hand.index.state = state.NOT_SET
    test_hand.middle.state = state.NOT_SET
    test_hand.ring.state = state.NOT_SET
    test_hand.little.state = state.NOT_SET
    test_hand.thumb.state = state.NOT_SET

    image_read = cv.imread("images/alphabet/W.png")

    cv.imshow("original", image_read)
    
    preprocesser = PreProcessor()

    extraction_image = preprocesser.preprocess(image_read)
    extractor = Extractor()
    classifier = Classifier()
    cv.imshow("image ready to be extracted", extraction_image)

    # ****************** SET DATA CANVAS SIZE************************
    
    REFERENCE_W.data_canvas = np.zeros([extraction_image.shape[0], extraction_image.shape[1], 3], dtype=np.uint8)
    test_hand.data_canvas = np.zeros([extraction_image.shape[0], extraction_image.shape[1], 3], dtype=np.uint8)
    

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
    
    
    palm_circumference = cv.circle(
        img=test_hand.data_canvas, 
        center=test_hand.center, 
        radius=test_hand.palm_radius, 
        color=Colors.center_color,
        thickness= 1)
    palm_center = cv.circle(
        img=test_hand.data_canvas, 
        center=test_hand.center, 
        radius=2, 
        color=Colors.center_color, 
        thickness=1)


    contour_coordinates = extractor.get_list_of_coordinates_from_contours(cv_contours)
    

    test_hand.contour_points = contour_coordinates
    
    # for coordinate_set in test_hand.contour_points:
    #     cv.circle(
    #         img=test_hand.data_canvas, 
    #         center=(coordinate_set[0], coordinate_set[1]), 
    #         radius=10, 
    #         color=Colors.contours_color, 
    #         thickness=1)

    

    #     # Find the convex hull object for each contour
    hull_list = []
    for i in range(len(cv_contours)):
        hull = cv.convexHull(cv_contours[i])
        hull_list.append(hull)
    
    test_hand.hull = hull_list

    cv.drawContours(test_hand.data_canvas, test_hand.hull, -2, Colors.hull_color, 1)

    hull_points = extractor.get_list_of_coordinates_from_contours(test_hand.hull)
    print(f"Hull points: {hull_points}")
    # for point in hull_points:
    #     cv.circle(test_hand.data_canvas, point, 2, (240, 20, 10), -1)
    #     cv.line(test_hand.data_canvas, test_hand.center, point, (240, 100, 0), 1)
    

    test_hand.defects = extractor.extract_defects(
        contours=cv_contours[0]
    )

    # *get the ends value of the defects
    defect_ends = extractor.get_defects_ends(test_hand.defects, cv_contours[0])

    #* sort the list according to their x value
    defect_ends.sort(key=lambda x: x[0])

    ends_copy = list(defect_ends)
    print(f"sorted defect ends: \n{defect_ends}")

    # filtered = extractor.filter_arr(defect_ends, 2)
    # print(f"filtered:\n{filtered}")
    
    # TODO this is where I am at. 
    filtered_ends = []
    thresh = 20
    for point in hull_points:
        is_valid = True
        for compare_point in filtered_ends:
            dist = extractor.length(compare_point, point)
            print(f"distance: {dist}")
            
            if dist < thresh:
                is_valid = False
                break
                # filtered_ends.append(point)
        
        if is_valid:
            filtered_ends.append(point)
        
    
    print("filtered ends: ", filtered_ends)

    for point in filtered_ends:
        if point[1] < test_hand.center[1]:
            cv.line(test_hand.data_canvas, test_hand.center, point, (255, 100, 100), 1)

            cv.circle(test_hand.data_canvas, point, 2, (255, 255, 0), 2)

            #* maybe implement if there is a valley in between, detect a finger
    
    # for point in defect_fars:
    #     cv.circle(test_hand.data_canvas, point, 2, 
    #     (100, 0, 100), 2)

    # # TODO add to hand

    # defects_image = np.zeros(original_img_size)

    # extractor.draw_defects(
    #     defects=test_hand.defects, 
    #     cnt=cv_contours[0], 
    #     output_image=test_hand.data_canvas
    # )

    cv.imshow("HAND DATA", test_hand.data_canvas)
    # cv.imshow("REF DATA", REFERENCE_W.data_canvas)
    test_hand.print_data()
    REFERENCE_W.print_data()

    print(classifier.compare_states(test_hand, REFERENCE_W))
    

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__=="__main__":
    main()
