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
        

        #*F
        self.hands[1].fingers.append(Finger(title=Title.LITTLE_FINGER))
        self.hands[1].fingers.append(Finger(title=Title.RING_FINGER))
        self.hands[1].fingers.append(Finger(title=Title.MIDDLE_FINGER))
        self.hands[1].fingers[0].title = Title.LITTLE_FINGER
        self.hands[1].fingers[1].title = Title.RING_FINGER
        self.hands[1].fingers[2].title = Title.MIDDLE_FINGER
        

        #*I
        self.hands[2].fingers.append(Finger(title=Title.LITTLE_FINGER))
        self.hands[2].fingers[0].title = Title.LITTLE_FINGER
        

        #* L
        self.hands[3].fingers.append(Finger(title=Title.INDEX_FINGER))
        self.hands[3].fingers.append(Finger(title=Title.THUMB_FINGER))
        self.hands[3].fingers[0].title = Title.INDEX_FINGER
        self.hands[3].fingers[1].title = Title.THUMB_FINGER
        

        #* W
        self.hands[4].fingers.append(Finger(title=Title.RING_FINGER))
        self.hands[4].fingers.append(Finger(title=Title.MIDDLE_FINGER))
        self.hands[4].fingers.append(Finger(title=Title.INDEX_FINGER))
        self.hands[4].fingers[0].title = Title.RING_FINGER
        self.hands[4].fingers[1].title = Title.MIDDLE_FINGER
        self.hands[4].fingers[2].title = Title.INDEX_FINGER


        #* Y
        self.hands[5].fingers.append(Finger(title=Title.LITTLE_FINGER))
        self.hands[5].fingers.append(Finger(title=Title.THUMB_FINGER))
        self.hands[5].fingers[0].title = Title.LITTLE_FINGER
        self.hands[5].fingers[1].title = Title.THUMB_FINGER
        
        print(f"loaded {str(len(self.hands))} images from {self.dir}")
        

    def imshow_database(self):
        for hand in self.hands:
            hand.imshow_data_canvas





