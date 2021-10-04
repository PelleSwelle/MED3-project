import cv2 as cv
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


def binarize():
    pass


while True:
    now = datetime.now()
    currentTime = now.strftime("%H%M%S")

    ret, input = cap.read()

    if cannyMode:
        # TODO upper and lower threshold
        output = cv.Canny(input, 1, 100)
    else:
        output = input
    if grayScaleMode:
        output = cv.cvtColor(input, cv.COLOR_BGR2GRAY)

    c = cv.waitKey(1)

    # **************** INPUTS ****************
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
    # exit
    elif c == 27:
        break

    cv.imshow("Camera feed", output)

cap.release()
cv.destroyAllWindows()
