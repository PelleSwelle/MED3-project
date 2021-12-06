from os import name
from numpy.core.defchararray import index

from numpy.core.overrides import verify_matching_signatures
from numpy.lib.type_check import imag
from Hand import DataCanvas, Finger, FingerName, FingerState, Hand
import cv2 as cv
import numpy as np
from Image import Image, ImageVersion
import Colors
from PreProcessor import PreProcessor
from Extractor import Extractor

steps = []

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
        img_array=cv.imread("reference/wSign2.jpg"), 
        version=ImageVersion.ORIGINAL
    )

    img_size: tuple = IMAGE_ORIGINAL.img_array.shape

    steps.append(IMAGE_ORIGINAL)

    # instantiate a hand to eventually fill with data
    hand = Hand(
        height=None, 
        width=None, 
        center=None, 
        orientation=None, 
        index_finger=Finger(FingerName.INDEX_FINGER),
        middle_finger=Finger(FingerName.MIDDLE_FINGER),
        ring_finger=Finger(FingerName.RING_FINGER),
        little_finger=Finger(FingerName.LITTLE_FINGER),
        thumb_finger=Finger(FingerName.THUMB_FINGER),
        contours=None, 
        hull=None, 
        finger_tips=None, 
        finger_vallies=None,
        data_canvas=DataCanvas()
    )
    # set the size of the data canvas to be the size of the image.
    hand.data_canvas.set_size(
        (
            IMAGE_ORIGINAL.img_array.shape[0], 
            IMAGE_ORIGINAL.img_array.shape[1]
        )
    )
    preprocesser = PreProcessor(IMAGE_ORIGINAL)
    extractor = Extractor()

    # PRODUCING THE IMAGES
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

    
    contours, _ = cv.findContours(
        image=get_version(
            version=ImageVersion.BINARIZED
        ).img_array,
        mode=cv.RETR_TREE,
        method=cv.CHAIN_APPROX_SIMPLE
    )
    hand.contours = contours
    # AT THIS POINT WE START ADDING DATA TO THE DATACANVAS
    cv.drawContours(hand.data_canvas.canvas, hand.contours, -1, (255, 255, 255), 3)

    # TODO this should take the contours from just above.
    IMAGE_CONTOURED = Image(
        name="contoured image",
        # pretty sure we can grab the contours from jus above
        img_array=cv.drawContours(
            image=np.zeros(img_size), 
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
    
    hull_canvas = np.zeros(img_size)
    for i in range(len(contours)):
        cv.drawContours(hull_canvas, hull_list, i, Colors.hull_color)
    
    hand.hull = hull_list

    cv.drawContours(hand.data_canvas.canvas, hand.hull, -1, (255, 0, 0), 3)

    IMAGE_HULL = Image(
        name="image with convex hull",
        img_array=hull_canvas,
        version=ImageVersion.WITH_HULL
    )
    steps.append(IMAGE_HULL)


    defects = extractor.extract_defects(
        contours=hand.contours[0]
    )
    print("defects: \n", defects) # yay

    defects_image = np.zeros(img_size)
    extractor.draw_defects(
        defects=defects, 
        cnt=contours[0], 
        output_image=defects_image
    )


    IMAGE_WITH_DEFECTS = extractor.draw_defects(
            defects=defects, 
            cnt=contours[0], 
            output_image=hand.data_canvas.canvas
    )
    cv.imshow("showing defects: ", defects_image)
    # steps.append(IMAGE_WITH_DEFECTS)

    #showing all the current versions
    for step in steps:
        print("image version: ", step.name)
        step.display()


    hand.imshow_data_canvas()
    # hand.old_compare_to_database()


    # hand.imshow_data_canvas()
    cv.imshow("data canvas", hand.data_canvas.canvas)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__=="__main__":
    main()