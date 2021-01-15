## Brendan Ind

from functions import *
import sys



def findCircles(array=cv2.imread("img/dots_clean.jpg", cv2.IMREAD_GRAYSCALE)):
    img = array  ## cv2.imread("../dots_clean.jpg", cv2.IMREAD_GRAYSCALE) if we not having an array

    ## Get a threshold from that array
    retval, threshold = cv2.threshold(img, 160, 180, cv2.THRESH_BINARY_INV) ##140 and 255 for side view

    def side_params():

        ## Create a parameter object
        side_view_params = cv2.SimpleBlobDetector_Params()

        # Set up the PIXEL COLOUR threshold
        side_view_params.minThreshold = 0
        side_view_params.maxThreshold = 255

        ## Set cup the CIRCULARITY thresholds
        side_view_params.filterByCircularity = True
        side_view_params.minCircularity = 0.1
        side_view_params.maxCircularity = 0.9

        ## Set up the AREA thresholds
        side_view_params.filterByArea = True
        side_view_params.minArea = 140
        side_view_params.maxArea = 700

        side_view_params.filterByInertia = True
        side_view_params.minInertiaRatio = 0.265
        side_view_params.maxInertiaRatio = 0.7

        side_view_params.filterByConvexity = True
        side_view_params.minConvexity = 0.93
        side_view_params.maxConvexity = 1

        return side_view_params
    side_view_params = side_params()



    ## TOP VIEW PARAMS
    def top_params():

        top_view_params = cv2.SimpleBlobDetector_Params()

        # Set up the PIXEL COLOUR threshold
        top_view_params.minThreshold = 0
        top_view_params.maxThreshold = 255

        ## Set cup the CIRCULARITY thresholds
        top_view_params.filterByCircularity = False
        top_view_params.minCircularity = 0.1
        top_view_params.maxCircularity = 0.9

        ## Set up the AREA thresholds
        top_view_params.filterByArea = True
        top_view_params.minArea = 120
        top_view_params.maxArea = 550

        top_view_params.filterByInertia = True
        top_view_params.minInertiaRatio = 0
        top_view_params.maxInertiaRatio = 1

        top_view_params.filterByConvexity = True
        top_view_params.minConvexity = 0.93
        top_view_params.maxConvexity = 1

        return top_view_params
    top_view_params = top_params()


    ## Set up the detector
    detector = cv2.SimpleBlobDetector_create(top_view_params)

    ## Detect blobs.
    points = detector.detect(threshold)

    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    img_with_circles = cv2.drawKeypoints(img, points, np.array([]), (0, 0, 255),
                                         cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    return points, img_with_circles

#
#
# cap = cv2.VideoCapture(0)
#
# frame = cap.read()
#
# ret, frame = cap.read()
#
# #frame = cv2.imread("img/ender_webcam.jpeg")
#
# points, circled = findCircles(frame)
#
# while True:
#     cv2.imshow("window", circled)
#
#     if cv2.waitKey(1) & 0xFF == 13:  ##13 is the carriage return key, so will break with enter key
#         break
#
# cv2.destroyAllWindows()
# cap.release()