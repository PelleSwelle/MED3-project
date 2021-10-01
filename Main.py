import cv2 as cv
from datetime import datetime # used to name the images, that are captured

saveDir = "./captures/"

cap = cv.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# TODO make this
# def getDeviceOrientation():
#     pass

cannyMode = False
grayScaleMode = False

while True:
    now = datetime.now()
    currentTime = now.strftime("%H%M%S")

    ret, input = cap.read()
    input = cv.flip(input, -1)

    if cannyMode:
        # TODO upper and lower threshold
        output = cv.Canny(input, 1, 100)
    else:
        output = input
    if grayScaleMode:
        output = cv.cvtColor(input, cv.COLOR_BGR2GRAY)

    c = cv.waitKey(1)

    # capture image
    if c == ord('p'):
        file = "cap" + currentTime + ".jpg"
        cv.imwrite(saveDir + file, output)
        print(file, " is stored in ", saveDir)

    # toggle canny mode
    elif c == ord("c"):
        if cannyMode == False:
            cannyMode = True
        else:
            cannyMode = False

    # toggle grayscale
    elif c == ord("g"):
        if not grayScaleMode:
            grayScaleMode = True
        else:
            grayScaleMode = False



    # exit
    elif c == 27:
        break

    cv.imshow("Camera feed", output)

cap.release()
cv.destroyAllWindows()
