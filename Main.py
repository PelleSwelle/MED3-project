import cv2 as cv
import numpy as np
from numpy.lib.type_check import imag

import Colors
from Extractor import Extractor
from Hand import DataCanvas, Finger, FingerName, FingerState, Hand, Orientation
from Image import Image, ImageVersion
from PreProcessor import PreProcessor
from pynput.keyboard import Key, Listener

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
    # TODO I think I might be loading the image both as a separate image and through the hand class

    # load an image as the original image
    IMAGE_ORIGINAL = Image(
        name="original image", 
        img_array=cv.imread("images/wSign2.jpg"), 
        version=ImageVersion.ORIGINAL
    )

    original_img_size: tuple = IMAGE_ORIGINAL.img_array.shape

    steps.append(IMAGE_ORIGINAL)


    # ************** DATABASE ******************

    hand_w = Hand(
        center=(154, 316),
        orientation=Orientation.FINGERS_UP,
        index_finger=Finger(FingerName.INDEX_FINGER),
        middle_finger=Finger(FingerName.MIDDLE_FINGER),
        ring_finger=Finger(FingerName.RING_FINGER),
        little_finger=Finger(FingerName.LITTLE_FINGER),
        thumb_finger=Finger(FingerName.THUMB_FINGER),
        contours=None,
        hull=None,
        defects=None,
        data_canvas=DataCanvas(),
        thumb_index_valley=None,
        index_middle_valley=(100, 200),
        middle_ring_valley=(150, 200),
        ring_little_valley= (196, 226))

    hand_w.index_finger.state = FingerState.OUT
    hand_w.middle_finger.state = FingerState.OUT
    hand_w.ring_finger.state = FingerState.OUT
    hand_w.little_finger.state = FingerState.IN
    hand_w.thumb_finger.state = FingerState.IN


    # instantiate a hand to eventually fill with data
    test_hand = Hand(
        center=None, 
        orientation=None, 
        index_finger=Finger(FingerName.INDEX_FINGER),
        middle_finger=Finger(FingerName.MIDDLE_FINGER),
        ring_finger=Finger(FingerName.RING_FINGER),
        little_finger=Finger(FingerName.LITTLE_FINGER),
        thumb_finger=Finger(FingerName.THUMB_FINGER),
        contours=None, 
        hull=None, 
        defects=None,
        data_canvas=DataCanvas(),
        thumb_index_valley=None,
        index_middle_valley=None,
        middle_ring_valley=None,
        ring_little_valley=None
    )
    # set the size of the data canvas to be the size of the image.
    test_hand.data_canvas.set_size(
        (
            IMAGE_ORIGINAL.img_array.shape[0], 
            IMAGE_ORIGINAL.img_array.shape[1]
        )
    )
    
    
    # The two currently implemented processors.
    preprocesser = PreProcessor(IMAGE_ORIGINAL)
    extractor = Extractor()
    # TODO implement Classifier

    # ************** PREPROCESSING ******************
    IMAGE_BLURRED = Image(
        name="blurred with gaussian blur",
        img_array=(
            preprocesser.blur_gaussian(
                image=get_version(
                    version=ImageVersion.ORIGINAL
                )
            )
        ),
        version=ImageVersion.BLURRED
    )
    steps.append(IMAGE_BLURRED)

    IMAGE_GRAYSCALED = Image(
        name="grayscaled image",
        img_array=preprocesser.gray_scale(
            image=get_version(
                version=ImageVersion.BLURRED)),
        version=ImageVersion.GRAYSCALED
    )
    # TODO should add to images atomatically when instantiating
    steps.append(IMAGE_GRAYSCALED)

    IMAGE_THRESHOLDED = Image(
        name="binarized image",
        img_array=preprocesser.binarize(
            image=get_version(
                version=ImageVersion.GRAYSCALED
            ),
            threshold=240
        ),
        version=ImageVersion.BINARIZED 
    )
    steps.append(IMAGE_THRESHOLDED)

    # ************** FEATURE EXTRACTION ******************
    
    contours, _ = cv.findContours(
        image=get_version(
            version=ImageVersion.BINARIZED
        ).img_array,
        mode=cv.RETR_TREE,
        method=cv.CHAIN_APPROX_SIMPLE
    )
    test_hand.contours = contours

    print(f"contours data type: {type(contours)}")
    # print(f"hand.contours:\n{test_hand.contours}")
    
    

    # Going through every contours found in the image.
    for cnt in test_hand.contours :
    
        approx = cv.approxPolyDP(cnt, 0.009 * cv.arcLength(cnt, True), True)

        print(f"approx: {approx}")
        # draws boundary of contours.
        cv.drawContours(test_hand.data_canvas.canvas, [approx], 0, (0, 0, 255), 5) 
    
        # Used to flatten the array containing
        # the coordinates of the vertices.
        flattened = approx.ravel() 
        print(f"flattened array: {flattened}")
        i = 0
    
        for j in flattened:
            if(i % 2 == 0):
                # get coordinates of the contours
                x = flattened[i]
                y = flattened[i + 1]
    
                # String containing the co-ordinates.
                string = str(x) + " " + str(y) 
                coordinate: tuple = (x, y)

                # the first pixel found vertically
                if i == 0:
                    # text on topmost co-ordinate.
                    cv.putText(
                        test_hand.data_canvas.canvas, 
                        "Arrow tip", 
                        (x, y),
                        font, 0.5, 
                        (255, 0, 0)) 
                else:
                    # text on remaining co-ordinates.
                    cv.putText(
                        test_hand.data_canvas.canvas, 
                        str(coordinate), (x, y), 
                        font, 2, 
                        (0, 0, 255)) 
            i = i + 1


    
    
    # AT THIS POINT WE START ADDING DATA TO THE DATACANVAS
    cv.drawContours(
        image=test_hand.data_canvas.canvas, 
        contours=test_hand.contours, 
        contourIdx=-1, 
        color=(255, 255, 255), 
        thickness=3
    )

    # TODO this should take the contours from just above.
    IMAGE_CONTOURED = Image(
        name="contoured image",
        # pretty sure we can grab the contours from jus above
        img_array=cv.drawContours(
            image=np.zeros(original_img_size), 
            contours= contours, 
            contourIdx=-1, 
            color=Colors.contours_color,
            thickness=2
        ),
        version=ImageVersion.CONTOURED
    )
    steps.append(IMAGE_CONTOURED)

        # Find the convex hull object for each contour
    hull_list = []
    for i in range(len(contours)):
        hull = cv.convexHull(contours[i])
        hull_list.append(hull)
    
    hull_canvas = np.zeros(original_img_size)
    for i in range(len(contours)):
        cv.drawContours(hull_canvas, hull_list, i, Colors.hull_color)
    
    test_hand.hull = hull_list

    # cv.drawContours(hand.data_canvas.canvas, hand.hull, -1, (255, 0, 0), 3)

    IMAGE_HULL = Image(
        name="image with convex hull",
        img_array=hull_canvas,
        version=ImageVersion.WITH_HULL
    )
    steps.append(IMAGE_HULL)


    defects = extractor.extract_defects(
        contours=test_hand.contours[0]
    )
    # print("defects: \n", defects) # yay
    # TODO add to hand

    defects_image = np.zeros(original_img_size)

    extractor.draw_defects(
        defects=defects, 
        cnt=contours[0], 
        output_image=defects_image
    )


    IMAGE_WITH_DEFECTS = extractor.draw_defects(
            defects=defects, 
            cnt=contours[0], 
            output_image=test_hand.data_canvas.canvas
    )
    # cv.imshow("showing defects: ", defects_image)
    # steps.append(IMAGE_WITH_DEFECTS)

    #showing all the current versions
    for step in steps:
        print("image version: ", step.name)
        step.display()


    # hand.imshow_data_canvas()
    # hand.old_compare_to_database()


    cv.imshow("data canvas", test_hand.data_canvas.canvas)
    # test_hand.print_data()
    print("test_hand", test_hand)
    # hand_w.print_data()

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__=="__main__":
    main()
