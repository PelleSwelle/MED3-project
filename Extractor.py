from dataclasses import dataclass
from enum import Enum, auto
import cv2 as cv
import numpy as np
from copy import copy
from PIL import Image
from PIL import ImageDraw
from numpy.lib.histograms import _histogram_bin_edges_dispatcher
import math
import PreProcessing
import Colors

class Extractor:

    def find_center(self, image: np.ndarray):
         # gets the center of mass (palm)
        mask = image
        dist_transform = cv.distanceTransform(mask, cv.DIST_L2, 5)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(dist_transform, mask)

        # // Output image
        # cv::Mat3b out;
        # cv::cvtColor(img, out, cv::COLOR_GRAY2BGR);
        # cv::circle(out, max_loc, max_val, cv::Scalar(0, 255, 0));

        # (maxDT[1], maxDT[0])

        # cv.circle(
        #     img=mask, 
        #     center=max_loc,
        #     radius=int(max_val), 
        #     color=(100,100,100),
        #     thickness= 1)
        
        cv.imshow("distance transform", mask)

        return max_loc, int(max_val)

    def extract_contours(self, image: Image) -> list:
        contours, hierarchy = cv.findContours(
            image=image.img_array, 
            mode=cv.RETR_TREE, 
            method=cv.CHAIN_APPROX_SIMPLE
        )
        contours = max(contours, key=lambda x: cv.contourArea(x))
        
        # return contours, hierarchy
        return contours


    def draw_contours(self, image: Image, contours: list) -> np.ndarray:
        self.canvas = np.zeros(
            (image.img_array.shape[0], 
            image.img_array.shape[1]
            )
        )
        cv.drawContours(
            image=self.canvas, 
            contours=contours, 
            contourIdx=-1, 
            color=255, 
            thickness=2
        )
        return self.canvas


    def extract_hull(self, contours: list) -> list:
        hull = []

        # calculate points for each contour
        for i in range(len(contours)):
            # creating convex hull object for each contour
            hull.append(
                cv.convexHull(
                    points=contours[i], #aaaaaaaaaaaa
                    returnPoints=False
                )
            )
        print("length of hull: ", len([hull]))
        return hull


    def draw_hull(self, image: Image, contours: list) -> np.array:
        canvas_height = image.img_array.shape[0]
        canvas_width = image.img_array.shape[1]

        canvas = np.zeros(
            (
                canvas_width, 
                canvas_height
            )
        )

        # Find the convex hull object for each contour
        hull_list = []
        for i in range(len(contours)):
            hull = cv.convexHull(contours[i])
            hull_list.append(hull)

        for i in range(len(contours)):
            cv.drawContours(
                image=canvas, 
                contours=hull_list, 
                contourIdx=i, 
                color=Colors.hull_color, 
                thickness=2
            )
        return canvas

        # NONE OF THIS UNDER HERE WORKS YET


    def extract_defects(self, contours):
        hull_indices = cv.convexHull(contours, returnPoints=False)
        defects = cv.convexityDefects(contours, hull_indices)
        # returns an array containing the convexity defects as output
        # start point, endpoint, farthest point, approximate distance to the farthest point
        
        # print("get_defects: defects type: ", type(defects))
        return defects



    def get_defects_starts(self, defects: np.ndarray, cnt) -> list:
        hull = cv.convexHull(cnt, returnPoints=False)
        defects = cv.convexityDefects(cnt, hull)
        start_points = []
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(cnt[s][0])
            start_points.append(start)
        return start_points

    def get_defects_ends(self, defects: np.ndarray, cnt) -> list:
        hull = cv.convexHull(cnt, returnPoints=False)
        defects = cv.convexityDefects(cnt, hull)
        end_points = []
        
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            end = tuple(cnt[e][0])
            end_points.append(end)
        return end_points
    
    def get_defects_fars(self, defects: np.ndarray, cnt) -> list:
        hull = cv.convexHull(cnt, returnPoints=False)
        defects = cv.convexityDefects(cnt, hull)
        far_points = []
        
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            far = tuple(cnt[e][0])
            far_points.append(far)
        return far_points


    def draw_defects(
        self, 
        defects: np.ndarray, 
        cnt, 
        output_image: np.ndarray) -> None:
        
        hull = cv.convexHull(cnt, returnPoints = False)
        defects = cv.convexityDefects(cnt, hull)

        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            distance = d
            print(f"distance, {distance}")

            # cv.line(output_image,start,end,[0,255,0],1)
            
            # LINES FROM VALLIES TO TIPS
            # cv.line(
            #     img=output_image,
            #     pt1=start,
            #     pt2=far,
            #     color=Colors.defect_color,
            #     thickness=1)
            cv.line(
                img=output_image,
                pt1=far,
                pt2=end,
                color=Colors.defect_color,
                thickness=1)
            cv.line(output_image,start,end,[0,255,0],2)
            
            cv.circle(
                img=output_image,
                center=start,
                radius=1,
                color=(200, 100, 0),
                thickness=-1)
            cv.circle(
                img=output_image,
                center=end,
                radius=1,
                color=(0, 200, 100),
                thickness=-1)
            # cv.line(output_image,start,end,[0,255,0],2)
            # cv.circle(points_canvas,far,5,Colors.defect_color,-1)
            # cv.putText(
            #     img=output_image, 
            #     text="end", 
            #     org=end, 
            #     fontFace=cv.FONT_HERSHEY_SIMPLEX, 
            #     fontScale=1, 
            #     color=(100, 100, 100)
            # )

        return start


    # TODO DO THIS
    def get_list_of_coordinates_from_contours(self, contours):
        list_of_coordinates = []
        for numpy_point in contours[0]:
            point = numpy_point.tolist()
            x, y = point[0]
            list_of_coordinates.append([x, y])
        return list_of_coordinates


    def get_number_of_fingers(self, defects, contours, analyze_image, draw_image: np.ndarray):
        """Uses hull defects to count the nmber of fingers outside of the palm."""

        if defects is not None:
            cnt = 0

        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(contours[s][0])
            end = tuple(contours[e][0])
            far = tuple(contours[f][0])
            # cv.line(draw_image, start, end, Colors.hull_color, 2)

            # TODO put center of hand in this function
            cv.line(draw_image, get_palm_center(analyze_image), end, Colors.hull_color, 1)
            cv.circle(draw_image, far, 5, Colors.defect_color, -1)

        # THIS PART CALCULATES THE ANGLES BETWEEN THE DEFECTS
        # for i in range(defects.shape[0]):  # calculate the angle
        #     s, e, f, d = defects[i][0]
        #     start = tuple(contours[s][0])
        #     end = tuple(contours[e][0])
        #     far = tuple(contours[f][0])
        #     print(Colors.blue+"start: ", start, " end: ", end, " far ", far, "" + Colors.white)
        #     cv.circle(draw_image, start, 4, [0, 255, 0], -1)

        #     a = np.sqrt(
        #         (end[0] - start[0]) ** 2 
        #         + (end[1] - start[1]) ** 2)
        #     b = np.sqrt(
        #         (far[0] - start[0]) ** 2 
        #         + (far[1] - start[1]) ** 2)
        #     c = np.sqrt(
        #         (end[0] - far[0]) ** 2 
        #         + (end[1] - far[1]) ** 2)

        #     angle = np.arccos(
        #         (b ** 2 + c ** 2 - a ** 2) 
        #         / (2 * b * c))  # cosine theorem

        #     if angle <= np.pi / 1.4:  # angle less than 90 degree, treat as fingers
        #         cnt += 1
        #         cv.circle(draw_image, far, 4, [255, 0, 0], -1)

        # if cnt > 0:
        #     cnt = cnt + 1

        # cv.putText(draw_image, str(cnt), (0, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
        return defects

    # helper function to draw on the image.
    # def draw_point(_img: Image, _x: int, _y: int, color):

        rad = 2
        draw = ImageDraw.Draw(_img)
        draw.ellipse(
            (
                _x - rad, _y - rad,
                _x + rad, _y + rad
            ), 
            fill=color, 
            outline=100, 
            width=1
        )

    # takes a thresholded Image
    # def detectBlobs(_img):
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

    