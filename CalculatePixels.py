import cv2
import numpy as np



# read image
image = cv2.imread('bw.jpg', cv2.IMREAD_GRAYSCALE)
n_white_pix = np.sum(image == 255)
print('Number of white pixels:', n_white_pix)

# show the image, provide window name first
cv2.imshow('image window', image)


#
cv2.waitKey(0)
cv2.destroyAllWindows()