import cv2 as cv
from datetime import datetime

saveDir = "./captures/"

cap = cv.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# TODO make this
# def getDeviceOrientation():
#     pass

while True:
    now = datetime.now()
    currentTime = now.strftime("%H%M%S")

    ret, frame = cap.read()
    frame = cv.flip(frame, -1)
    cv.imshow('Input', frame)

    c = cv.waitKey(1)

    if c == ord('p'):
        file = "cap" + currentTime + ".jpg"
        cv.imwrite(saveDir + file, frame)
        print(file, " is stored in ", saveDir)
    elif c == 27:
        break

cap.release()
cv.destroyAllWindows()
