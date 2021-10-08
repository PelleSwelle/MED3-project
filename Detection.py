import cv2
import numpy as np

#Color range for masking
low_green = np.array([25, 52, 72])
high_green = np.array([102, 255, 255])

#Capture camera feed
cap = cv2.VideoCapture(0)

#Process each frame
    while True:
        ret, frame = cap.read()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, low_green, high_green)
        cv2.imshow('Masked Frame', mask)


        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, contours, -1,(0,0,255),2)
        cv2.imshow('Frame', frame)


