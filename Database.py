from Hand import Hand, Finger, Title
import os
import cv2 as cv
import Colors
import numpy as np
from Extractor import Extractor

class Database:
    extractor = Extractor()
    image_strings: list
    dir = "images/alphabet"
    images: list
    hands: list
    signs_preprocessed: list

    def __init__(self) -> None:
        self.image_strings = []
        self.images = []
        self.hands = []
        self.signs_preprocessed = []
    
    def load(self) -> None:
        #* get filenames from the given directory
        for file in os.listdir(self.dir):
            self.image_strings.append(file)
        
        for title in self.image_strings:
            # print(title)
            #* read the files as images
            image = cv.imread(self.dir + "/" + title)
            
            #* put into list
            self.images.append(image)

            #* use the names and files to instantiate a hand.
            name = title[0]
            self.hands.append(Hand(name=name, image=image))

        self.set_fingers()
        
    def set_fingers(self):
            
        #*A
        self.hands[0].fingers.append(Finger())
        self.hands[0].fingers[0].title = Title.THUMB_FINGER
        for i in range(0, len(self.hands[0].fingers)):
            print(self.hands[0].fingers[i].title)
            
        
        #*B
        self.hands[1].fingers.append(Finger(title=Title.LITTLE_FINGER))
        self.hands[1].fingers.append(Finger(title=Title.RING_FINGER))
        self.hands[1].fingers.append(Finger(title=Title.MIDDLE_FINGER))
        self.hands[1].fingers.append(Finger(title=Title.INDEX_FINGER))
        self.hands[1].fingers[0].title = Title.LITTLE_FINGER
        self.hands[1].fingers[1].title = Title.RING_FINGER
        self.hands[1].fingers[2].title = Title.MIDDLE_FINGER
        self.hands[1].fingers[3].title = Title.INDEX_FINGER
        for i in range(0, len(self.hands[1].fingers)):
            print(self.hands[1].fingers[i].title)
        #*D
        self.hands[2].fingers.append(Finger(title=Title.INDEX_FINGER))
        self.hands[2].fingers[0].title = Title.INDEX_FINGER
        for i in range(0, len(self.hands[2].fingers)):
            print(self.hands[2].fingers[i].title)

        #*F
        self.hands[3].fingers.append(Finger(title=Title.LITTLE_FINGER))
        self.hands[3].fingers.append(Finger(title=Title.RING_FINGER))
        self.hands[3].fingers.append(Finger(title=Title.MIDDLE_FINGER))
        self.hands[3].fingers[0].title = Title.LITTLE_FINGER
        self.hands[3].fingers[1].title = Title.RING_FINGER
        self.hands[3].fingers[2].title = Title.MIDDLE_FINGER
        for i in range(0, len(self.hands[3].fingers)):
            print(self.hands[3].fingers[i].title)

        #*I
        self.hands[4].fingers.append(Finger(title=Title.LITTLE_FINGER))
        self.hands[4].fingers[0].title = Title.LITTLE_FINGER
        for i in range(0, len(self.hands[4].fingers)):
            print(self.hands[4].fingers[i].title)

        #* L
        self.hands[5].fingers.append(Finger(title=Title.INDEX_FINGER))
        self.hands[5].fingers.append(Finger(title=Title.THUMB_FINGER))
        self.hands[5].fingers[0].title = Title.INDEX_FINGER
        self.hands[5].fingers[1].title = Title.THUMB_FINGER
        for i in range(0, len(self.hands[5].fingers)):
            print(self.hands[5].fingers[i].title)

        #* U
        self.hands[6].fingers.append(Finger(title=Title.MIDDLE_FINGER))
        self.hands[6].fingers.append(Finger(title=Title.INDEX_FINGER))
        self.hands[6].fingers[0].title = Title.MIDDLE_FINGER
        self.hands[6].fingers[1].title = Title.INDEX_FINGER
        for i in range(0, len(self.hands[6].fingers)):
            print(self.hands[6].fingers[i].title)

        #* V
        self.hands[7].fingers.append(Finger(title=Title.MIDDLE_FINGER))
        self.hands[7].fingers.append(Finger(title=Title.INDEX_FINGER))
        self.hands[7].fingers[0].title = Title.MIDDLE_FINGER
        self.hands[7].fingers[1].title = Title.INDEX_FINGER

        #* W
        self.hands[8].fingers.append(Finger(title=Title.RING_FINGER))
        self.hands[8].fingers.append(Finger(title=Title.MIDDLE_FINGER))
        self.hands[8].fingers.append(Finger(title=Title.INDEX_FINGER))
        self.hands[8].fingers[0].title = Title.RING_FINGER
        self.hands[8].fingers[1].title = Title.MIDDLE_FINGER
        self.hands[8].fingers[2].title = Title.INDEX_FINGER

        #* Y
        self.hands[9].fingers.append(Finger(title=Title.LITTLE_FINGER))
        self.hands[9].fingers.append(Finger(title=Title.THUMB_FINGER))
        self.hands[9].fingers[0].title = Title.LITTLE_FINGER
        self.hands[9].fingers[1].title = Title.THUMB_FINGER
        # for i in range(0, len(self.hands)):
        #     print("number of fingers in each hand: ", len(self.hands[i].fingers))
        #     for e in range(0, len(self.hands[i].fingers)) :
        #         print("finger title: ", self.hands[i].fingers[e].title)

        print(f"loaded {str(len(self.hands))} images from {self.dir}")
        
    def imshow_database(self):
        # for i in range(0, len(self.image_strings)):
        #     title = self.image_strings[i]
        #     file = self.images[i]
        i = 0
        for hand in self.hands:
            # cv.drawContours(hand.data_canvas, 
            #     contours=hand.contours, 
            #     contourIdx= -1, 
            #     color=Colors.contours_color, 
            #     thickness=1)
        

            cv.imshow(hand.name, hand.data_canvas)





