from Hand import Hand 
import os
import cv2 as cv

class Database:
    image_strings: list
    dir = "images/alphabet/"
    images: list
    signs: list

    def __init__(self) -> None:
        self.image_strings = []
        self.images = []
        self.signs = []
    
    def load(self) -> None:
        # get filenames from the given directory
        for file in os.listdir(self.dir):
            self.image_strings.append(file)
        
        for title in self.image_strings:
            # print(title)
            image = cv.imread(self.dir + "/" + title)
            
            # print("image:", image)
            self.images.append(image)
            name = title[0]

            self.signs.append(Hand(name=name, image=image))
        

        # print("file names:", file_names)

    def imshow_database(self):
        for i in range(0, len(self.image_strings)):
            title = self.image_strings[i]
            file = self.images[i]
            cv.imshow(title, file)

