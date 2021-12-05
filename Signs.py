from Hand import Hand, Finger, FingerName, FingerState
from Image import Image, ImageVersion
import cv2 as cv
# hole in shape: O
# noOfFingersout:
# 0
# E, M, S
# 1
# A, D, I, N, T, X
# 2
# G, H, K, L, P, Q, R, U, V, Y
# 3
# F, W
# 4
# B
# 5
# C, O

# B: 4 but together
# excluding J and Z because they are not static

hand_a = Hand.Hand(
    image=Image(
        name="a", 
        img_array=cv.imread(
            "reference/A1008.jpg"
        ), 
    version=ImageVersion.REFERENCE
    )
)
hand_a.index_finger.set_finger_state(FingerState.IN)
hand_a.middle_finger.set_finger_state(FingerState.IN)
hand_a.ring_finger.set_finger_state(FingerState.IN)
hand_a.little_finger.set_finger_state(FingerState.IN)
hand_a.thumb_finger.set_finger_state(FingerState.OUT)

hand_f = Hand(
    image=Image(
        name="f", 
        img_array=cv.imread(
            "reference/F1001.jpg"
        ), 
    version=ImageVersion.REFERENCE
    )
)
hand_f.index_finger.set_finger_state(FingerState.OUT)
hand_f.middle_finger.set_finger_state(FingerState.OUT)
hand_f.ring_finger.set_finger_state(FingerState.OUT)
hand_f.little_finger.set_finger_state(FingerState.OUT)
hand_f.thumb_finger.set_finger_state(FingerState.TOUCHING_INDEX)


hand_w = Hand(
    image=Image(
        name="W", 
        img_array=cv.imread(
            "reference/Wsign2"
        ), 
    version=ImageVersion.REFERENCE
    )
)

hand_w.index_finger.set_finger_state(FingerState.OUT)
hand_w.middle_finger.set_finger_state(FingerState.OUT)
hand_w.ring_finger.set_finger_state(FingerState.OUT)
hand_w.little_finger.set_finger_state(FingerState.IN)
hand_w.thumb_finger.set_finger_state(FingerState.TOUCHING_LITTLE)
hand_w.center = (100, 100)
hand_w.index_tip_coords = (100, 100)
hand_w.index_middle_coords = (100, 100)
hand_w.index_ring_coords = (100, 100)

error_threshold = 20

# for finger in comparisonHand:
#     if comparisonHand.index_tip_coords > hand_w.index_tip_coords - error_threshold && 
#         comparisonHand.index_tip_coords < hand_w.index_tip_coords + error_threshold
