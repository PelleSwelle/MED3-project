# MED3-project

Group project for the third semester of Medialogy, AAU CPH

Takes an input image of a hand and tries to classify that image as a sign from the ASL dictionary

Run the program simply by navigating to the directory and entering

python Main.py

this will run the program on the currently loaded image.

## The algorithm

1. An image is loaded in at the beginning.
   from this image a *hand* is instantiated.
2. This hand is run through preprocessing, including gaussian blur, grayscaling, edge detection, thresholding and cropping. At the end of this process, a binary image is returned with the area of the hand being white and everything else being black. The image is cropped to only contain the hand without any unnecessary background
3. The contours of the hand are extracted.
4. from the contours the convex hull is extracted.
5. The center of the palm is found by creating the largest possible circle inside the shape of the hand. The center of this circle is treated as the center of the palm.
6. The fingertips are defined as the places where the convex hull bends. (this by default excludes recognision of signs, where fingers would be found inside the hull), but for this proof of concept it is sufficient.
7. depending on the position of the individual fingertip as well as its distance from the center of the palm (normalised to the radius of the palm) the finger is given the proper title.
8. If the names of the fingers match the fingers of a hand in the database, a match is returned.

## Current limitations

The image of the hand must be right hand, palm towards the camera. This in theory includes the signs: A, B, D, E, F, I, K, L, M, N, S, T, U, V, W, Y

However, the signs currently implemented are:

A, F, I, L, W, Y

Fingers are at this point identified from their position and length. More sophisticated features, such as comparing to the convexity defects, checking finger thickness and implementing the ability to detect fingers inside the radius of the palm, the algorithm could feasibly work with several more signs.
