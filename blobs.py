##Blob detection work

from finding_blobs import findCircles
import cv2
import numpy as np

cap = cv2.VideoCapture(0)


def nothing():
    pass


cv2.namedWindow("window")

cv2.createTrackbar("min_area", "window", 0, 100, nothing)
cv2.createTrackbar("min_circularity", "window", 0, 100, nothing)
cv2.createTrackbar("min_inertia", "window", 0, 100, nothing)
cv2.createTrackbar("min_threshold", "window", 0, 100, nothing)
cv2.createTrackbar("min_convexity", "window", 0, 100, nothing)

frame = cap.read()
i = 5
while i > 0:
    i -= 1
    ret, frame = cap.read()

cap.release()

## Create a parameter object
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.filterByCircularity = True
params.filterByConvexity = True
params.filterByInertia = True

params.minThreshold = 50
params.maxThreshold = 255

frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

## Get a threshold from that array
retval, threshold = cv2.threshold(frame, 200, 255, cv2.THRESH_BINARY_INV)

print("entering while loop")
while True:
    print("Into while loop")
    cv2.imshow("window", frame)
    if cv2.waitKey(1) & 0xFF == 13:  ##13 is the carriage return key, so will break with enter key
        break


    min_area = cv2.getTrackbarPos("min_area", "window") / 100
    min_circularity = cv2.getTrackbarPos("min_circularity", "window") / 100
    min_inertia = cv2.getTrackbarPos("min_inertia", "window") / 100
    #min_threshold = cv2.getTrackbarPos("min_threshold", "window") / 100
    min_convexity = cv2.getTrackbarPos("min_convexity", "window") / 100

    print("got positions")


    params.minArea = min_area
    params.minCircularity = min_circularity
    params.minInertiaRatio = min_inertia
    #params.minThreshold = min_threshold
    params.minConvexity = min_convexity

    print("set params")

    detector = cv2.SimpleBlobDetector(params)
    print("made detector")
    points = detector.detect(threshold)
    print("detected")
    img_with_circles = cv2.drawKeypoints(frame, points, np.array([]), (0, 0, 255),
                                         cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


    print("drew")


cv2.destroyAllWindows()