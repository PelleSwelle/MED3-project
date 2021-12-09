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

# TODO DO THIS
def get_list_of_coordinates_from_contours(contours):
    list_of_coordinates = []
    for numpy_point in contours[0]:
        point = numpy_point.tolist()
        x, y = point[0]
        list_of_coordinates.append([x, y])
    return list_of_coordinates


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

    hand_w.index.position = (11, 41)
    hand_w.middle.position = (113, 0)
    hand_w.ring.position = (222, 59)
    hand_w.index.state = state.OUT
    hand_w.middle.state = state.OUT
    hand_w.ring.state = state.OUT
    hand_w.little.state = state.IN
    hand_w.thumb.state = state.IN
    # cv.circle(hand_w.data_canvas, hand_w.center, 1, (255, 0, 0), 1)


    # instantiate a hand to eventually fill with data
    test_hand = Hand(
        center=None, 
        orientation=None, 
        contour_points=None, 
        hull=None, 
        defects=None)
    
    
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
    
    cv_contours, _ = cv.findContours(
        image=get_version(
            version=ImageVersion.BINARIZED
        ).img_array,
        mode=cv.RETR_TREE,
        method=cv.CHAIN_APPROX_SIMPLE)

    IMAGE_CONTOURED = Image(
        name="contoured image", 
        img_array=cv.drawContours(
            image=IMAGE_THRESHOLDED.img_array, 
            contours=cv_contours, 
            contourIdx= -1, 
            color=(0, 0, 255), 
            thickness=1
        ), 
        version=ImageVersion.CONTOURED)

    contour_coordinates = get_list_of_coordinates_from_contours(cv_contours)
    # print(f"CONTOURS:\n", contour_coordinates)


    test_hand.contour_points = contour_coordinates
    
    for coordinate_set in test_hand.contour_points:
        print(f"x: {coordinate_set[0]}, y: {coordinate_set[1]}")
        cv.circle(test_hand.data_canvas, (coordinate_set[0], coordinate_set[1]), 2, 255, 1)

    # cv.imshow("contour points", test_hand.data_canvas)
    

    # cv.imshow("img_ergh", img_ergh)
    x,y,w,h = cv.boundingRect(cv_contours[0])

    cropped = IMAGE_CONTOURED.img_array[y:y+h, x:x+w]

    cropped_contours, _ = cv.findContours(
        image=cropped, 
        mode=cv.RETR_TREE,
        method=cv.CHAIN_APPROX_SIMPLE)

    cropped_contour_coordinates = get_list_of_coordinates_from_contours(cropped_contours)
    
    IMAGE_CROPPED = Image(
        name="cropped to size", 
        img_array=cropped, 
        version=ImageVersion.CROPPED)
    
    steps.append(IMAGE_CROPPED)

    data_canvas_size = np.zeros((
        IMAGE_CROPPED.img_array.shape[0], 
        IMAGE_CROPPED.img_array.shape[1], 
        3))

    test_hand.data_canvas = data_canvas_size
    
    # this is to be removed.
    hand_w.data_canvas = data_canvas_size

    for coordinate_set in cropped_contour_coordinates:
        cv.circle(hand_w.data_canvas, (coordinate_set[0], coordinate_set[1]), 1, (255, 255, 255), 1)


    # ******************* DRAWING ON THE REFERENCE IMAGE **********************
    # finger tips
    cv.circle(hand_w.data_canvas, hand_w.index.position, 2, Colors.fingertip_color, 2)
    cv.putText(hand_w.data_canvas, "index tip", hand_w.index.position, font, 0.5, Colors.fingertip_color, 1)
    
    cv.circle(hand_w.data_canvas, hand_w.middle.position, 2, Colors.fingertip_color, 2)
    cv.putText(hand_w.data_canvas, "middle tip", hand_w.middle.position, font, 0.5, Colors.fingertip_color, 1)
    
    cv.circle(hand_w.data_canvas, hand_w.ring.position, 2, Colors.fingertip_color, 2)
    cv.putText(hand_w.data_canvas, "ring tip", hand_w.ring.position, font, 0.5, Colors.fingertip_color, 1)

    # vallies
    cv.circle(hand_w.data_canvas, hand_w.index_middle_valley, 2, (255, 255, 255), 2)
    cv.circle(hand_w.data_canvas, hand_w.middle_ring_valley, 2, (255, 255, 255), 2)
    cv.circle(hand_w.data_canvas, hand_w.ring_little_valley, 2, (255, 255, 255), 2)

    # palm center
    cv.circle(hand_w.data_canvas, hand_w.center, 2, Colors.center_color, 2)
    cv.putText(hand_w.data_canvas, "palm center", hand_w.center, font, 0.5, Colors.center_color, 1)
    # cv.circle(hand_w.data_canvas, hand_w.little.position, 2, Colors.fingertip_color, 2)
    # cv.circle(hand_w.data_canvas, hand_w.thumb.position, 2, Colors.fingertip_color, 2)


        # Find the convex hull object for each contour
    hull_list = []
    for i in range(len(cv_contours)):
        hull = cv.convexHull(cv_contours[i])
        hull_list.append(hull)
    

    # defects = extractor.extract_defects(
    #     contours=test_hand.contours[0]
    # )
    # print("defects: \n", defects) # yay
    # TODO add to hand

    defects_image = np.zeros(original_img_size)

    # extractor.draw_defects(
    #     defects=defects, 
    #     cnt=cv_contours[0], 
    #     output_image=defects_image
    # )


    # IMAGE_WITH_DEFECTS = extractor.draw_defects(
    #         defects=defects, 
    #         cnt=cv_contours[0], 
    #         output_image=test_hand.data_canvas.canvas
    # )
    # cv.imshow("showing defects: ", defects_image)
    # steps.append(IMAGE_WITH_DEFECTS)

    # SHOW ALL CURRENT VERSIONS
    # for step in steps:
        # print("image version: ", step.name)
        # step.display()


    # SHOW LATEST VERSION
    # cv.imshow("latest version", len(steps) - 1)

    cv.imshow("DATA IN HAND", test_hand.data_canvas)
    cv.imshow("DATA IN reference", hand_w.data_canvas)
    test_hand.print_data()
    # hand_w.print_data()

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__=="__main__":
    main()
