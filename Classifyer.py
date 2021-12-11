import cv2 as cv
import numpy as np

from Hand import Finger, Hand

class Classifier:
    # this
    def __init__(self) -> None:
        pass

    def compare_hand(self, hand: Hand, ref: Hand):
        print("********* COMPARING ************")
        if hand.center == ref.center:
            print("center MATCH")
        if hand.index.state == ref.index.state:
            print("index state MATCH")
        if hand.middle.state == ref.middle.state:
            print("middle state MATCH")
        if hand.ring.state == ref.middle.state:
            print("middle state MATCH")

    def compare_finger_state(self, finger: Finger, ref: Finger):
        """compare two fingers, used in the "compare_states" function"""
        if finger.state != ref.state:
            return False
        else: 
            return True

    def compare_states(self, hand: Hand, ref: Hand) -> bool:
        if (
            self.compare_finger_state(hand.index, ref.index) and 
            self.compare_finger_state(hand.middle, ref.middle) and
            self.compare_finger_state(hand.ring, ref.ring) and
            self.compare_finger_state(hand.little, ref.little) and
            self.compare_finger_state(hand.thumb, ref.thumb)):
            return True
        else:
            return False
        
