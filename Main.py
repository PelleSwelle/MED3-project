import cv2 as cv
import numpy as np
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

        cv.drawContours(hand.data_canvas, hand.hull, -2, Colors.hull_color, 1)

        filtered_points = extractor.filter_points(hull_points, 20)
        
        for point in filtered_points:
            # if point is above the circle on the palm of the hand
            if point[1] < hand.center[1] - hand.palm_radius:
                # cv.putText(hand.data_canvas, "finger", (point[0] - 20, point[1] + 20), font, 0.4, (255, 100, 100), 1)
                cv.line(hand.data_canvas, hand.center, point, (255, 100, 100), 1)

                cv.circle(hand.data_canvas, point, 2, (255, 255, 0), 2)



        cv.circle(hand.data_canvas, hand.center, 2, Colors.center_color, -1)
        cv.circle(hand.data_canvas, hand.center, hand.palm_circumference, Colors.center_color, 2)
        cv.imshow(hand.name + " datacanvas", hand.data_canvas)
        i+=1



    # ***************READ IMAGE AND PREPROCESS*********************

    # instantiate a hand to eventually fill with data
    hand = Hand(name="test hand", image="W")
    

    # image_read = cv.imread("images/alphabet/W.png")

    # cv.imshow("original", hand.image)
    
    

    extraction_image = preprocesser.preprocess(hand.image)
    
    cv.imshow("image ready to be extracted", extraction_image)

    # ****************** SET DATA CANVAS SIZE************************
    # ref_w.width = extraction_image.shape[0]
    # ref_w.height = extraction_image.shape[1]
    # ref_w.data_canvas = np.zeros((ref_w.width, ref_w.height, 3), dtype=np.uint8)
    
    hand.width = extraction_image.shape[0]
    hand.height = extraction_image.shape[1]
    hand.data_canvas = np.zeros((hand.width, hand.height, 3), dtype=np.uint8)
    

    # # ************** FEATURE EXTRACTION ******************
    
    cv_contours, _ = cv.findContours(
        image=extraction_image,
        mode=cv.RETR_TREE,
        method=cv.CHAIN_APPROX_SIMPLE)



    cv.drawContours(
            image=hand.data_canvas, 
            contours=cv_contours, 
            contourIdx= -1, 
            color=Colors.contours_color, 
            thickness=1)

    hand.center, hand.palm_radius = extractor.find_center(extraction_image)
    
    
    palm_circumference = cv.circle(
        img=hand.data_canvas, 
        center=hand.center, 
        radius=hand.palm_radius, 
        color=Colors.center_color,
        thickness= 1)
    palm_center = cv.circle(
        img=hand.data_canvas, 
        center=hand.center, 
        radius=2, 
        color=Colors.center_color, 
        thickness=1)


    contour_coordinates = extractor.get_list_of_coordinates_from_contours(cv_contours)
    

    hand.contour_points = contour_coordinates
    
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
    
    hand.hull = hull_list

    cv.drawContours(hand.data_canvas, hand.hull, -2, Colors.hull_color, 1)

    hull_points = extractor.get_list_of_coordinates_from_contours(hand.hull)
    print(f"Number of Hull points: {len(hull_points)}")
    # for point in hull_points:
    #     cv.circle(test_hand.data_canvas, point, 2, (240, 20, 10), -1)
    #     cv.line(test_hand.data_canvas, test_hand.center, point, (240, 100, 0), 1)
    

    hand.defects = extractor.extract_defects(
        contours=cv_contours[0]
    )

    # *get the ends value of the defects
    defect_ends = extractor.get_defects_ends(hand.defects, cv_contours[0])

    #* sort the list according to their x value
    defect_ends.sort(key=lambda x: x[0])
    
    # TODO this is where I am at. 
    
    filtered_points = extractor.filter_points(
        coordinate_list=hull_points, 
        threshold=20)
        
    
    print("no of points after filtering: ", len(filtered_points))

    for point in filtered_points:
        # if point is above the circle on the palm of the hand
        if point[1] < hand.center[1] - hand.palm_radius:
            cv.putText(hand.data_canvas, "finger", (point[0] - 20, point[1] + 20), font, 0.4, (255, 100, 100), 1)
            cv.line(hand.data_canvas, hand.center, point, (255, 100, 100), 1)

            cv.circle(hand.data_canvas, point, 2, (255, 255, 0), 2)
            #*classifier.name_finger(point, test_hand.center)

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

    # cv.imshow("HAND DATA", test_hand.data_canvas)
    hand.imshow_data_canvas()
    # cv.imshow("REF DATA", REFERENCE_W.data_canvas)
    # ref_w.imshow_data_canvas()
    hand.print_data()
    # ref_w.print_data()

    # print(classifier.compare_states(test_hand, REFERENCE_W))
    

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__=="__main__":
    main()
