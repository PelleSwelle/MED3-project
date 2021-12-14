import cv2 as cv

def rescale_frame(frame, scale = 0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

image = cv.imread("images/demo/w_black2.jpg")

rescaled_image = rescale_frame(image, scale=0.1)

gaussian_blurred = cv.GaussianBlur(rescaled_image, [5, 5], 1)
cv.imshow("gaussian blurred", gaussian_blurred)
        
grayscaled = cv.cvtColor(gaussian_blurred, cv.COLOR_BGR2GRAY)
cv.imshow("grayscaled", grayscaled)
ret, thresh = cv.threshold(grayscaled, 245, 255, cv.THRESH_OTSU)
cv.imshow("thresholded", thresh)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)


cv.imshow("image", rescaled_image)

cv.waitKey(0)

cv.destroyAllWindows()