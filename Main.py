from os import name

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
    original_image = Image(
        name="original image", 
        img_array=cv.imread("reference/wSign2.jpg"), 
        version=ImageVersion.ORIGINAL
    )

    images.append(original_image)

    # instantiate a hand from that image
    hand = Hand()

    hand.data_canvas.set_size(
        (
            original_image.img_array.shape[0], 
            original_image.img_array.shape[1]
        )
    )
    print("hand data canvas size: ", hand.data_canvas.get_size())
    preprocesser = PreProcessor(original_image)
    extractor = Extractor()

    # PRODUCING THE IMAGES
    blurred_image = Image(
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
    images.append(blurred_image)

    grayscaled_image = Image(
        name="grayscaled image",
        img_array=preprocesser.gray_scale(
            image=get_version(
                version=ImageVersion.BLURRED)),
        version=ImageVersion.GRAYSCALED
    )
    # TODO should add to images atomatically when instantiating
    images.append(grayscaled_image)

    binarized_image = Image(
        name="binarized image",
        img_array=preprocesser.binarize(
            image=get_version(
                version=ImageVersion.GRAYSCALED
            ),
            threshold=240
        ),
        version=ImageVersion.BINARIZED 
    )
    images.append(binarized_image)

    
    contours = extractor.extract_contours(
        image=get_version(
            version=ImageVersion.BINARIZED
        )
    )
    hand.contours = contours

    # print("root: contours", contours)
    print("root: contours:, ", hand.contours)
    
    # TODO this should take the contours from just above.
    contoured_image = Image(
        name="contoured image",
        # pretty sure we can grab the contours from jus above
        img_array=extractor.contour_image(
            get_version(ImageVersion.BINARIZED), 
            contours=contours[0],
            hieararchy=contours[1]
        ),
        version=ImageVersion.CONTOURED
    )
    images.append(contoured_image)

    cv.drawContours(
        image=hand.data_canvas.canvas,
        contours=contours, 
        contourIdx=-1, 
        color=Colors.contours_color, 
        thickness=1
    )

    convex_hull = extractor.extract_convex_hull(
        image=get_version(
            version=ImageVersion.CONTOURED
        )
    )

    convex_hull_image = Image(
        name="image with convex hull",
        
        img_array=extractor.convex_hull(
            image=get_version(ImageVersion.BINARIZED)
        ),
        version=ImageVersion.WITH_HULL
    )
    images.append(convex_hull_image)
    
    # defects = extractor.get_defects(contours=contours)
    # print("defects: \n", defects)

    #showing all the current versions
    for image in images:
        image.imshow()

    hand.data_canvas.add_hull(hull=convex_hull)

    hand.imshow_data_canvas()
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__=="__main__":
    main()