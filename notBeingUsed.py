# takes a thresholded Image
def detectBlobs(_img):
    # Setup SimpleBlobDetector parameters.
    params = cv.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 10
    params.maxThreshold = 200

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 1500

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.87

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.01

    # Create a detector with the parameters
    detector = cv.SimpleBlobDetector_create(params)

    # Detect blobs.
    keypoints = detector.detect(np.array(_img))

    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
    # the size of the circle corresponds to the size of blob
    im_with_keypoints = cv.drawKeypoints(np.array(np.array(_img)), keypoints, np.array([]), (0, 0, 0),
                                         cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return im_with_keypoints

# for now this is not used, removed background by hand
def removeThingsNotHand(src):
    img = Image.fromarray(src)  # convert array to image
    height, width = img.size  # get width and height
    for x in range(0, height):
        for y in range(0, height):
            if img.getpixel((x, y)) == 0:
                img.putpixel((x, y), 255)
            elif img.getpixel((x, y)) == 255:
                img.putpixel((x, y), 0)
    return np.array(img)

# calculate moments of binary image
def findCenter(img):
    # if input is 3 channels, convert to 1
    singleChannel = convertToSingleChannel(img)
    print("number of channels: ", len(singleChannel.split()))

    # Binarize the image
    inverted = invertColor(singleChannel)
    # Find the contours
    contours, hierarchy = cv.findContours(np.array(singleChannel), 1, 2)

    cnt = contours[0]
    # Calculate the moments
    M = cv.moments(cnt)

    # Calculate centroid
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
    else:
        # set values as what you need in the situation
        cx, cy = 0, 0

    cv.circle(np.array(inverted), (cx, cy), 5, (0, 0, 255), 2)
    return inverted
