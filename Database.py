from Hand import Hand 
import os
import cv2 as cv

class Database:
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
        print(f"loaded {str(len(self.hands))} images from {self.dir}")
        
    def imshow_database(self):
        for i in range(0, len(self.image_strings)):
            title = self.image_strings[i]
            file = self.images[i]
            cv.imshow(title, file)


