## Brendan Ind

from functions import *


def findCircles(array=cv2.imread("img/dots_clean.jpg", cv2.IMREAD_GRAYSCALE)):
    img = array  ## cv2.imread("../dots_clean.jpg", cv2.IMREAD_GRAYSCALE) if we not having an array

    ## Get a threshold from that array
    retval, threshold = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)

    ## Create a parameter object
    params = cv2.SimpleBlobDetector_Params()

    # Set up the PIXEL COLOUR threshold
    params.minThreshold = 50
    params.maxThreshold = 255

    ## Set cup the CIRCULARITY thresholds
    params.filterByCircularity = False
    params.minCircularity = 0.000001

    ## Set up the AREA thresholds
    params.filterByArea = False
    params.minArea = 1

    ## Set up the detector
    detector = cv2.SimpleBlobDetector_create(params)

    ## Detect blobs.
    points = detector.detect(threshold)

    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    img_with_circles = cv2.drawKeypoints(img, points, np.array([]), (0, 0, 255),
                                         cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    return points, img_with_circles



frame = cv2.imread("img/blobs.jpg")

points, circled = findCircles(frame)

cv2.imshow("window", circled)

cv2.waitKey(0)