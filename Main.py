import io

import cv2 as cv

import numpy as np
import PreProcessing
from datetime import datetime  # used to name the images, that are captured

saveDir = "./captures/"

cap = cv.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

grayScaleMode = False
thresholdVal = 128
maxVal = 255
cannyMode = False
binaryMode = False
zeros = np.zeros((512, 512, 3), np.uint8)
subtractor = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=50, detectShadows=True)


def mouseEvent(event, x, y, flags, param):
    if event == cv.EVENT_MOUSEWHEEL:
        print("wheel")



while True:
    now = datetime.now()
    currentTime = now.strftime("%H%M%S")

    ret, input = cap.read()
    mask = subtractor.apply(input)
    output = input


    # ************* MODES *************
    if cannyMode:
        output = cv.Canny(input, 1, 100)
    elif grayScaleMode:
        output = cv.cvtColor(input, cv.COLOR_BGR2GRAY)
    elif binaryMode:
        output = PreProcessing.removeBackground(input)
    else:
        output = input

    c = cv.waitKey(1)

    # **************** KEYBOARD INPUTS ****************
    # capture image
    if c == ord('p'):
        file = "cap" + currentTime + ".jpg"
        cv.imwrite(saveDir + file, output)
        print(file, " is stored in ", saveDir)
    # toggle canny mode
    elif c == ord("c"):
        cannyMode = not cannyMode
    # toggle grayscale
    elif c == ord("g"):
        grayScaleMode = not grayScaleMode
    elif c == ord("b"):
        binaryMode = not binaryMode
        print("binaryMode: ", binaryMode)
    # exit
    elif c == 27:
        break

    cv.imshow("Camera feed", output)
    cv.imshow("masked", mask)

cap.release()
cv.destroyAllWindows()
