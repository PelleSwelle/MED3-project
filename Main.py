from os import name
import Hand
import cv2 as cv
import numpy as np
import Image
import Colors

images = []

def print_images():
    print(Colors.green + "current content of images:")
    for image in images:
        print(Colors.green + image.name, ", ", image.version, "" + Colors.white)

def get_version(version: Image.ImageVersion):
    image_to_return: Image.Image
    for image in images:
        if image.version == version:
            image_to_return = image
    return image_to_return

def main():

    # load an image as the original image
    original_image = Image.Image(
        name="original image", 
        img_array=cv.imread("reference/wSign2.jpg"), 
        version=Image.ImageVersion.ORIGINAL
    )

    images.append(original_image)

    # instantiate a hand from that image
    hand = Hand.Hand(original_image)

    hand.print_finger_states()

    preprocesser = Hand.PreProcessor(hand)
    
    # PRODUCING THE IMAGES
    grayscaled_image = Image.Image(
        name="grayscaled image",
        img_array=preprocesser.gray_scale(get_version(Image.ImageVersion.ORIGINAL)),
        version=Image.ImageVersion.GRAYSCALED
    )
    # TODO should add to images atomatically when instantiating
    images.append(grayscaled_image)

    binarized_image = Image.Image(
        name="binarized image",
        img_array=preprocesser.binarize(
            get_version(
                Image.ImageVersion.GRAYSCALED
            )
        ),
        version=Image.ImageVersion.BINARIZED 
    )
    images.append(binarized_image)

    hand.contours = preprocesser.get_contours(
        get_version(Image.ImageVersion.BINARIZED)
    )
    
    contoured_image = Image.Image(
        name="contoured image",
        img_array=preprocesser.contour(
            get_version(
                Image.ImageVersion.BINARIZED
            )
        ),
        version=Image.ImageVersion.CONTOURED
    )
    images.append(contoured_image)
    print_images()


    # convex_hull_image = Image.Image(
    #     name="image with convex hull",
        
    #     img_array=preprocesser.convex_hull(
    #         contours=preprocesser.get_contours(
    #             image=get_version(
    #                 version=Image.ImageVersion.BINARIZED
    #             )
    #         )[0]
    #     ),
    #     version=Image.ImageVersion.WITH_HULL
    # )
    # images.append(convex_hull_image)
    
    #showing all the current versions
    for image in images:
        image.imshow()

    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__=="__main__":
    main()