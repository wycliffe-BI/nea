## Main v2 Brendan Ind

## IMPORTS:
import cv2
from win10toast import ToastNotifier
from time import sleep
import C_checker_gui as checker
import misc
import sys
import numpy as np
import collections

## VARIABLES
cap = cv2.VideoCapture
ip = "127.0.0.1"
i = -1
happy_with_images = False
correct_num_of_markers = False
toaster = ToastNotifier()
frame = np.array(0)
marker_ROIs = []
filament_ROI = []
filamentTracker = cv2.TrackerKCF_create()
## To change type of marker tracker, change line 105 ish, labelled A
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter(filename='output.avi', apiPreference=cv2.CAP_FFMPEG, fourcc=fourcc, fps=20.0, frameSize=(
    frame.shape[1], frame.shape[0]))
current_distances = collections.deque(maxlen=4)
expected_distances = [99, 99, 99, 99]
filament_data = {
    "key":"value"
}
marker_data = {
    "key":"value"
}


## Sets up the capture object and asks if its locally or IP cam
if input("Run with IP cam? ") != "":
    cap = cv2.VideoCapture(ip)
else:
    cap = cv2.VideoCapture(0)

## Warms up the camera
camera_warmed = False
while not camera_warmed:
    camera_warmed, frame = cap.read()

## Warm up the recording equipment:
video_out = cv2.VideoWriter(filename='output.avi', apiPreference=cv2.CAP_FFMPEG, fourcc=fourcc, fps=20.0, frameSize=(
    frame.shape[1], frame.shape[0]))

## This is so we can iterate back though later if the user want to repeat this process:
while not happy_with_images:

    ## This will loop until the user decides that they want to record regions of interest:
    while True:
        # noinspection PyRedeclaration
        camera_warmed, frame = cap.read()
        cv2.imshow("Press 'c' to record Regions Of Interest", frame)
        k = cv2.waitKey(1) & 0xff
        if k == ord("c"):
            break

    ## The user is now shown instructions of how to select ROIs
    while True:
        instructions = cv2.imread("img/instructions1.png")
        cv2.imshow("Instructions", instructions)
        k = cv2.waitKey(5) & 0xff
        if k == 13:  ## (a carriage return)
            break

    ## User now selects ROI for filament
    filament_ROI = cv2.selectROI("Select the FILAMENT. Press ESC to exit, and ENTER to save the ROI", frame)

    ## Now the user chooses the marker ROIs. If they get any amount other than 4 they are asked to redo.
    while not correct_num_of_markers:
        marker_ROIs = cv2.selectROIs("Select 4 MARKER ROIs, pressing ENTER between them, then press ESC when done",
                                     frame)
        correct_num_of_markers = (len(marker_ROIs) == 4)
        if not correct_num_of_markers:
            toaster.show_toast("Marker Capture", "That was not the right amount of markers, please try again.")
        else:
            toaster.show_toast("Marker Capture", "Captured the filament and marker ROI's correctly!")

    ## Clean up and close the camera
    cv2.destroyAllWindows()
    cv2.waitKey(0)
    sleep(1)

    ## Create some editable copies of the main frame
    clean_frame = frame
    frame_with_ROIs = frame

    ## Draw the ROI box for the filament:
    x, y, w, h = filament_ROI
    frame_with_ROIs = cv2.rectangle(frame_with_ROIs, (x, y), (x + w, y + h), (0, 0, 255), 2)

    ## Draw the ROI boxes for the markers:
    for bbox in marker_ROIs:
        x, y, w, h = bbox
        frame_with_ROIs = cv2.rectangle(frame_with_ROIs, (x, y), (x + w, y + h), (255, 0, 0), 2)

    ## Clean Up
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    ## Open the checker GUI and check that these images are all ok
    ## TODO Change the misc function here to local page and make syntax of checker gui look better
    happy_with_images = checker.checking_page(misc.PILconvert(frame_with_ROIs))
    if happy_with_images == 3:
        print("User has exited the program")
        sys.exit(1)

## We have now exited the calibration loop with success! The user has their desired regions of interest and
## now we can focus on the tracking and etc..

## Initialise the single filament tracker
filamentTracker.init(frame, tuple(filament_ROI))

## Make the marker tracker (this is a multi tracker form legacy parts)
markerTracker = cv2.legacy.MultiTracker_create()

## Add some trackers to that multiple tracker:
for bbox in marker_ROIs:
    markerTracker.add(cv2.legacy.TrackerKCF_create(), frame, tuple(bbox))

while True:

    ## These variables will reset each iteration of the main while loop
    status = ''
    i += 1

    ## Read the current frame from the camera and abort if it's bad
    ok, frame = cap.read()
    if not ok:
        print("Capture was bad...")
        break

    ## Update the trackers' values:
    markerTrackerOK, markers = markerTracker.update(frame)
    filamentTrackerOK, filament = filamentTracker.update(frame)
    if (not markerTrackerOK) or (not filamentTrackerOK):
        print("One of the trackers returned false when called for update")

    ## Draw new filament box now we have updated our trackers:
    centrex = filament[0] + (filament[2] / 2)
    centrey = filament[1] + (filament[3] / 2)
    frame = cv2.rectangle(frame, filament, (255, 0, 0), 2, 1)
    frame = cv2.circle(frame, (int(centrex), int(centrey)), 2, (255, 0, 0))
    filament_centre = (centrex, centrey)