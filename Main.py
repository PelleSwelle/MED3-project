import cv2 as cv
import numpy as np
from numpy.core.defchararray import center
from numpy.lib.type_check import imag
from Classifyer import Classifier
from Database import Database
import Colors
from Extractor import Extractor
from Hand import Finger, Title, State, Hand, Orientation
from Image import Image, ImageVersion
from PreProcessor import PreProcessor
from math import dist, sqrt
import os

def clear(): os.system('cls') #on Windows System

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
    #* clear the console
    clear()
    #* load the database of signs and images
    database = Database()
    database.load()

    #* load the different tools to be used.
    preprocesser = PreProcessor()
    extractor = Extractor()
    classifier = Classifier()

    #* filling database with data
    i = 0
    for image in database.images:
        processed_image = preprocesser.preprocess(image)
        database.images[i] = processed_image
        i+=1
    
    
    i = 0
    for hand in database.hands:
        hand.width = database.images[i].shape[0]
        hand.height = database.images[i].shape[1]
        hand.data_canvas = np.zeros((hand.width, hand.height, 3))
        hand.center, hand.palm_circumference = extractor.find_center(database.images[i])
        print("hand.center: ", hand.center)
        hand.contours, _ = cv.findContours(database.images[i], cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        
        #* drawing
        cv.drawContours(hand.data_canvas, 
            contours=hand.contours, 
            contourIdx= -1, 
            color=Colors.contours_color, 
            thickness=1)

        #     # Find the convex hull object for each contour
        hull_list = []
        for e in range(len(hand.contours)):
            hull = cv.convexHull(hand.contours[e])
            hull_list.append(hull)
        
        hand.hull = hull_list

        hull_points = extractor.get_list_of_coordinates_from_contours(hand.hull)

        #* drawing
        cv.drawContours(hand.data_canvas, hand.hull, -2, Colors.hull_color, 1)

        filtered_points = extractor.filter_points(hull_points, 25)
        
        for point in filtered_points:
            top_of_palm = hand.center[1] - hand.palm_radius
            # if point is above the circle on the palm of the hand
            if point[1] < top_of_palm:
                # cv.putText(hand.data_canvas, "finger", (point[0] - 20, point[1] + 20), font, 0.4, (255, 100, 100), 1)
                #* drawing
                cv.line(hand.data_canvas, hand.center, point, (255, 100, 100), 1)

                #* drawing
                cv.circle(hand.data_canvas, point, 2, (255, 255, 0), 2)



        cv.circle(hand.data_canvas, hand.center, 2, Colors.center_color, -1)
        cv.circle(hand.data_canvas, hand.center, hand.palm_circumference, Colors.center_color, 2)
        
        #* show the database images
        # cv.imshow(hand.name + " datacanvas", hand.data_canvas)
        i+=1

    

    # ***************READ IMAGE AND PREPROCESS*********************

    input_hand = Hand(name="test hand", image="W")

    extraction_image = preprocesser.preprocess(input_hand.image)
    
    cv.imshow("image ready to be extracted", extraction_image)

    # ****************** SET DATA CANVAS SIZE************************
    
    input_hand.width = extraction_image.shape[0]
    input_hand.height = extraction_image.shape[1]
    input_hand.data_canvas = np.zeros((input_hand.width, input_hand.height, 3), dtype=np.uint8)
    

    # # ************** FEATURE EXTRACTION ******************
    
    input_hand.contours, _ = cv.findContours(
        image=extraction_image,
        mode=cv.RETR_TREE,
        method=cv.CHAIN_APPROX_SIMPLE)



    cv.drawContours(
            image=input_hand.data_canvas, 
            contours=input_hand.contours, 
            contourIdx= -1, 
            color=Colors.contours_color, 
            thickness=1)

    input_hand.center, input_hand.palm_radius = extractor.find_center(extraction_image)
    
    
    input_hand.palm_circumference = cv.circle(
        img=input_hand.data_canvas, 
        center=input_hand.center, 
        radius=input_hand.palm_radius, 
        color=Colors.center_color,
        thickness= 1)
    input_hand.palm_center = cv.circle(
        img=input_hand.data_canvas, 
        center=input_hand.center, 
        radius=2, 
        color=Colors.center_color, 
        thickness=1)
    

    input_hand.contour_points = extractor.get_list_of_coordinates_from_contours(input_hand.contours)
    
    # for coordinate_set in test_hand.contour_points:
    #     cv.circle(
    #         img=test_hand.data_canvas, 
    #         center=(coordinate_set[0], coordinate_set[1]), 
    #         radius=10, 
    #         color=Colors.contours_color, 
    #         thickness=1)

    

    #     # Find the convex hull object for each contour
    hull_list = []
    for i in range(len(input_hand.contours)):
        hull = cv.convexHull(input_hand.contours[i])
        hull_list.append(hull)
    
    input_hand.hull = hull_list

    cv.drawContours(input_hand.data_canvas, input_hand.hull, -2, Colors.hull_color, 1)

    hull_points = extractor.get_list_of_coordinates_from_contours(input_hand.hull)
    print(f"Number of Hull points: {len(hull_points)}")
    # for point in hull_points:
    #     cv.circle(test_hand.data_canvas, point, 2, (240, 20, 10), -1)
    #     cv.line(test_hand.data_canvas, test_hand.center, point, (240, 100, 0), 1)
    

    input_hand.defects = extractor.extract_defects(
        contours=input_hand.contours[0]
    )

    # *get the ends value of the defects
    defect_ends = extractor.get_defects_ends(input_hand.defects, input_hand.contours[0])

    #* sort the list according to their x value
    defect_ends.sort(key=lambda x: x[0])
    
    # TODO this is where I am at. 
    
    filtered_points = extractor.filter_points(
        coordinate_list=hull_points, 
        threshold=20)
        
    
    print("no of points after filtering: ", len(filtered_points))

    for point in filtered_points:
        # if point is above the circle on the palm of the hand
        if point[1] < input_hand.center[1] - input_hand.palm_radius:
            #* length from palm center to fingertip
            line_length = extractor.length(point, input_hand.center)
            if (line_length > input_hand.palm_radius * 2.5):
                #* here we finally add a finger to the hand.
                input_hand.fingers.append(Finger(position=point))
                print(f"line length: {line_length}")

            cv.line(input_hand.data_canvas, input_hand.center, point, (255, 100, 100), 1)

            cv.circle(input_hand.data_canvas, point, 2, (255, 255, 0), 2)
            #*classifier.name_finger(point, test_hand.center)

            #* maybe implement if there is a valley in between, detect a finger
    
    for finger in input_hand.fingers:
        xpos = finger.position[0]
        center_line = input_hand.center[0]
        
        #* measuring x values to determine which finger it is
        if xpos < center_line:
            finger.title = Title.INDEX_FINGER
            cv.line(input_hand.data_canvas, input_hand.center, finger.position, Colors.little_finger_color, 2)
        elif xpos > center_line - 10:
            if xpos < center + 10:
                finger.title = Title.MIDDLE_FINGER
                cv.line(input_hand.data_canvas, input_hand.center, finger.position, Colors.middle_finger_color, 2)
        elif xpos > center_line:
            finger.title = Title.RING_FINGER
            cv.line(input_hand.data_canvas, input_hand.center, finger.position, Colors.index_finger_color, 2)
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

    # cv.imshow("HAND DATA", test_hand.data_canvas)
    # input_hand.imshow_data_canvas()

    cv.imshow("input hand", input_hand.data_canvas)
    input_hand.print_data()

    # for reference in database:
        # if input_hand.

    # print(classifier.compare_states(test_hand, REFERENCE_W))
    

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__=="__main__":
    main()
