import os
import cv2 as cv

inFolder = "./in/"
outFolder = "./out/"
this = "./"

def allFiles():
    inFiles = os.listdir(inFolder)
    outFiles = os.listdir(outFolder)

    files = []
    for file in inFiles:
        files.append(file)
    for file in outFiles:
        files.append(file)

    return files

def save(image, letter, descr):
    cv.imwrite(outFolder + letter + descr + ".jpg", image)

