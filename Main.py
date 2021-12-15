import cv2 as cv
import numpy as np
from numpy.core.defchararray import center
from numpy.lib.type_check import imag
from Classifyer import Classifier
from Database import Database
import Colors
from Extractor import Extractor
from Hand import Finger, Title, Hand, Orientation
from Image import Image, ImageVersion
from PreProcessor import PreProcessor
from math import dist, sqrt
import os
from pprint import pprint

def clear(): os.system('cls')

steps = []
font = cv.FONT_HERSHEY_COMPLEX

def print_images():
    print(Colors.green + "current content of images:")
    for image in steps:
        print(Colors.green + image.name, ", ", image.version, "" + Colors.white)

def fill_hull_list(hand, hull_list):
    for e in range(len(hand.contours)):
        hull = cv.convexHull(hand.contours[e])
        hull_list.append(hull)


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

    for i in range(0, len(database.hands)):
        pprint(database.hands[i].fingers)

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
        # print("hand.center: ", hand.center)
        hand.contours, _ = cv.findContours(database.images[i], cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        
        #* drawing
        cv.drawContours(hand.data_canvas, 
            contours=hand.contours, 
            contourIdx= -1, 
            color=Colors.contours_color, 
            thickness=1)

        #     # Find the convex hull object for each contour
        hull_list = []
        fill_hull_list(hand, hull_list)
        
        hand.hull = hull_list

        hull_points = extractor.get_list_of_coordinates_from_contours(hand.hull)

        #* drawing
        cv.drawContours(hand.data_canvas, hand.hull, -2, Colors.hull_color, 1)

        filtered_points = extractor.filter_points(hull_points, 25)
        
        #* show the database images
        # cv.imshow(hand.name + " datacanvas", hand.data_canvas)
        i+=1

    

    # ***************READ IMAGE AND PREPROCESS*********************
    input_image = cv.imread("images/alphabet/L.png")
    input_hand = Hand(name="input", image=input_image)
    cv.imshow("raw input", input_hand.image)


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

    #* the width of a finger is a approximately a fourth of the width of the palm
    input_hand.finger_width = input_hand.palm_radius / 2

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
    fill_hull_list(input_hand, hull_list)
    # for i in range(len(input_hand.contours)):
    #     hull = cv.convexHull(input_hand.contours[i])
    #     hull_list.append(hull)
    
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
    # defect_ends = extractor.get_defects_ends(input_hand.defects, input_hand.contours[0])

    #* sort the list according to their x value
    # defect_ends.sort(key=lambda x: x[0])
    
    filtered_points = extractor.filter_points(
        coordinate_list=hull_points, 
        threshold=20)
        
    
    print("no of points after filtering: ", len(filtered_points))
    
    #* sort the points according to their x position
    filtered_points.sort(key=lambda x: x[0])

    #* APPENDING FINGERS TO THE HAND
    extractor.detect_fingers(extractor, filtered_points, input_hand)
                # print(f"line length: {line_length}")

                # cv.line(input_hand.data_canvas, input_hand.center, point, (255, 100, 100), 1)

            
            #*classifier.name_finger(point, test_hand.center)

            #* maybe implement if there is a valley in between, detect a finger
    
    #* CHECKING X VALUE OF FINGER TIP TO DETERMINE FINGER IDENTITY
    


    # center_x: int = input_hand.center[0]
    # grid_width = center_x * 2 / 5
    # left2 = int(grid_width)
    # left1 = int(grid_width * 2)
    # middle = int(grid_width * 3)
    # right1 = int(grid_width * 4)
    # right2 = int(grid_width * 5)
    palm_top = input_hand.center[1] - input_hand.palm_radius
    thumb_threshold = palm_top - 30
    # #* GUIDELINES - ONLY FOR DEBUGGING
    # guideline_color = (50, 50, 50)
    # cv.line(input_hand.data_canvas, (0, thumb_threshold), (input_hand.width, thumb_threshold), (255, 255, 255), 1)
    # cv.line(input_hand.data_canvas, (left2, 0), (left2, 200), guideline_color, 1)
    # cv.line(input_hand.data_canvas, (left1, 0), (left1, 200), guideline_color, 1)
    # cv.line(input_hand.data_canvas, (middle, 0), (middle, 200), guideline_color, 1)
    # cv.line(input_hand.data_canvas, (right1, 0), (right1, 200), guideline_color, 1)
    # cv.line(input_hand.data_canvas, (right2, 0), (right2, 200), guideline_color, 1)
    

    


    for i in range(0, len(input_hand.fingers)):

        #* x and y values for comparing
        finger_x: int = input_hand.fingers[i].position[0]
        finger_y: int = input_hand.fingers[i].position[1]
        finger_length = input_hand.fingers[i].length
        palm_center = input_hand.center
        palm_radius = input_hand.palm_radius
        approx_little_length = palm_radius * 2.6
        
        buffer = 10
        left_of_palm = finger_x < palm_center[0] - input_hand.palm_radius
        right_of_palm = finger_x > palm_center[0] + input_hand.palm_radius
        above_palm_line = finger_y < thumb_threshold
        under_palm_line = finger_y > thumb_threshold
        at_palm_center_x = finger_x > palm_center[0] - 10 and finger_x < input_hand.center[0] + 10
        ring_finger_position = left_of_palm and finger_length > input_hand.palm_radius * 1.2
        little_finger_position = left_of_palm and finger_length < input_hand.palm_radius * 1.2
        left_of_center = finger_x < palm_center[0]
        right_of_center = palm_center[0] + buffer < finger_x
        straight_above = palm_center[0] - buffer < finger_x < palm_center[0] + buffer
        center_to_left = palm_center[0] - palm_radius - buffer < finger_x < palm_center[0] + palm_radius
        # < palm_center[0] + palm_radius + buffer


        # down_and_right = finger_x > input_hand.center[0] + input_hand.palm_radius and finger_y > thumb_threshold  
        # left_and_down = finger_x < input_hand.center[0] - input_hand.fingers[i].length
        # if right_of_palm and under_palm_line:
        #     input_hand.fingers[i].title = Title.THUMB_FINGER
        # elif right_of_palm and above_palm_line:
        #     input_hand.fingers[i].title = Title.INDEX_FINGER
        # elif at_palm_center_x and above_palm_line:
        #     input_hand.fingers[i].title = Title.MIDDLE_FINGER
        # elif ring_finger_position:
        #     input_hand.fingers[i].title = Title.RING_FINGER
        # elif little_finger_position:
        #     input_hand.fingers[i].title = Title.LITTLE_FINGER
        if finger_length < approx_little_length and left_of_center:
            input_hand.fingers[i].title = Title.LITTLE_FINGER
        elif finger_length <approx_little_length and right_of_palm:
            input_hand.fingers[i].title = Title.THUMB_FINGER
        elif right_of_center:
            input_hand.fingers[i].title = Title.INDEX_FINGER
        elif straight_above:
            input_hand.fingers[i].title = Title.MIDDLE_FINGER
        elif center_to_left:
            input_hand.fingers[i].title = Title.RING_FINGER

        else:
            input_hand.fingers[i].title = Title.NOT_SET

    for i in range(0, len(input_hand.fingers)):
        pprint(vars(input_hand.fingers[i]))

    input_hand.imshow_data_canvas()

    input_hand.print_data()

    #* comparing against the database
   
    for hand in database.hands:
        if hand.fingers == input_hand.fingers:
            print("*********** MATCH! *********** ")
            print("You signed the letter: ", hand.name, "!")

    cv.waitKey(0)
    cv.destroyAllWindows()





if __name__=="__main__":
    main()
