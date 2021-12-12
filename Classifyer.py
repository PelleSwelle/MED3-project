import cv2 as cv
import numpy as np

from Hand import Finger, Hand
from Extractor import Extractor

class Classifier:
    # this
    def __init__(self) -> None:
        pass

    def compare_hand(self, hand: Hand, ref: Hand):
        print("********* COMPARING ************")
        if hand.center == ref.center:
            print("center MATCH")
        if hand.finger1.state == ref.finger1.state:
            print("index state MATCH")
        if hand.finger2.state == ref.finger2.state:
            print("middle state MATCH")
        if hand.finger3.state == ref.finger2.state:
            print("middle state MATCH")

    def compare_finger_state(self, finger: Finger, ref: Finger):
        """compare two fingers, used in the "compare_states" function"""
        if finger.state != ref.state:
            return False
        else: 
            return True

    def compare_states(self, hand: Hand, ref: Hand) -> bool:
        if (
            self.compare_finger_state(hand.finger1, ref.finger1) and 
            self.compare_finger_state(hand.finger2, ref.finger2) and
            self.compare_finger_state(hand.finger3, ref.finger3) and
            self.compare_finger_state(hand.finger4, ref.finger4) and
            self.compare_finger_state(hand.finger, ref.finger)):
            return True
        else:
            return False
        
    def name_finger(self, finger: Finger, center_point: tuple):
        if finger.position[0] < center_point[0]:
            print(f"fingertip is to the left of center")
        elif finger.position[0] == center_point[0]:
            print(f"fingertip is right above center point")
        elif finger.position[0] > center_point[0]:
            print(f"fingertip is to the right of the center")
