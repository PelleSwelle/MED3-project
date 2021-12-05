from os import name
from numpy.core.defchararray import index

from numpy.core.overrides import verify_matching_signatures
from Hand import Finger, FingerState, Hand
import cv2 as cv
import numpy as np
from Image import Image, ImageVersion
import Colors
from PreProcessor import PreProcessor
from Extractor import Extractor

images = []

def print_images():
    print(Colors.green + "current content of images:")
    for image in images:
        print(Colors.green + image.name, ", ", image.version, "" + Colors.white)

def get_version(version: ImageVersion):
    image_to_return: Image
    for image in images:
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

    images.append(IMAGE_ORIGINAL)

    # instantiate a hand from that image
    hand = Hand()

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
    images.append(IMAGE_BLURRED)

    IMAGE_GRAYSCALED = Image(
        name="grayscaled image",
        img_array=preprocesser.gray_scale(
            image=get_version(
                version=ImageVersion.BLURRED)),
        version=ImageVersion.GRAYSCALED
    )
    # TODO should add to images atomatically when instantiating
    images.append(IMAGE_GRAYSCALED)

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
    images.append(IMAGE_THRESHOLDED)

    
    contours, _ = cv.findContours(
        image=get_version(
            version=ImageVersion.BINARIZED
        ).img_array,
        mode=cv.RETR_TREE,
        method=cv.CHAIN_APPROX_SIMPLE
    )
    hand.contours = contours

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
    images.append(IMAGE_CONTOURED)

        # Find the convex hull object for each contour
    hull_list = []
    for i in range(len(contours)):
        hull = cv.convexHull(contours[i])
        hull_list.append(hull)
    
    hull_canvas = np.zeros(img_size)
    for i in range(len(contours)):
        cv.drawContours(hull_canvas, hull_list, i, Colors.hull_color)
    
    hand.convex_hull = hull_list

    IMAGE_HULL = Image(
        name="image with convex hull",
        img_array=hull_canvas,
        version=ImageVersion.WITH_HULL
    )
    images.append(IMAGE_HULL)


    defects = extractor.extract_defects(
        contours=hand.contours[0]
    )
    print("defects: \n", defects) # yay

    IMAGE_DEFECTS = np.zeros(img_size)
    extractor.draw_defects(
        defects=defects, 
        cnt=contours[0], 
        output_image=IMAGE_DEFECTS
    )
    cv.imshow("showing defects: ", IMAGE_DEFECTS)


    #showing all the current versions
    for image in images:
        print("image version: ", image.name)
        image.imshow()


    hand.imshow_data_canvas()
    # hand.old_compare_to_database()


    hand.imshow_data_canvas()
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__=="__main__":
    main()