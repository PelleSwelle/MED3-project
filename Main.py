import cv2 as cv
import numpy as np
from Database import Database
import Colors
from Extractor import Extractor
from Hand import Finger, Title, Hand, Orientation

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

def main():
    #* clear the console
    clear()
    print("Welcome to the detect-what-letter-from-the-ASL-alphabet-are-you-signing-program.\n")
    print("At the moment, six letters are implemented, and images of these are stores in ./images/alphabet")
    print("You can choose between the letters: A, F, I, L, W, Y\n")
    letter_chosen = input("enter the letter you wish to proceed with:\n")
    letter_chosen.upper()
    print("You chose: ", letter_chosen)

    #* load the database of signs and images
    
    database = Database()
    database.load()

    for i in range(0, len(database.hands)):
        pprint(database.hands[i].fingers)

    #* load the different tools to be used.
    preprocesser = PreProcessor()
    extractor = Extractor()

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
        
        # #* drawing
        # cv.drawContours(hand.data_canvas, 
        #     contours=hand.contours, 
        #     contourIdx= -1, 
        #     color=Colors.contours_color, 
        #     thickness=1)

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
    #* READ IN IMAGE, INSTANTIATE A HAND AND SHOW IT
    input_image = cv.imread("images/alphabet/" + letter_chosen + ".png")
    print("input_image: ", input_image)
    input_hand = Hand(name="input", image=input_image)
    cv.imshow("raw input", input_hand.image)

    #* PREPROCESS THE IMAGE TO PREPARE IT FOR FEATURE EXTRACTION
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


    input_hand.center, input_hand.palm_radius = extractor.find_center(extraction_image)
    
    
    #* the width of a finger is a approximately a fourth of the width of the palm
    input_hand.finger_width = input_hand.palm_radius / 2

    input_hand.contour_points = extractor.get_list_of_coordinates_from_contours(input_hand.contours)
    
    #* Find the convex hull object for each contour
    hull_list = []
    fill_hull_list(input_hand, hull_list)
    
    input_hand.hull = hull_list

    
    hull_points = extractor.get_list_of_coordinates_from_contours(input_hand.hull)
    print(f"Number of Hull points: {len(hull_points)}")
    for point in hull_points:
        cv.circle(input_hand.data_canvas, point, 2, (240, 20, 10), -1)
        # cv.line(input_hand.data_canvas, input_hand.center, point, (240, 100, 0), 1)
    
    #* DEFECTS ARE NOT UTILIZED IN THE CURRENT FORM OF THE SOFTWARE, 
    #* BUT MIGHT PROVE TO BE ESSENTIAL FOR FURTHER DEVELOPMENT
    input_hand.defects = extractor.extract_defects(
        contours=input_hand.contours[0]
    )

    filtered_points = extractor.filter_points(
        coordinate_list=hull_points, 
        threshold=20)
        
    
    print("number of points after filtering: ", len(filtered_points))
    
    #* sort the points according to their x position
    filtered_points.sort(key=lambda x: x[0])

    #* APPENDING FINGERS TO THE HAND
    extractor.detect_fingers(extractor, filtered_points, input_hand)
                
    
    #* IDENTIFY THE FINGERS AND NAME THEM ACCORDINGLY
    extractor.name_fingers(input_hand)

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
