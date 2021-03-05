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
import E_error_detection as err

## VARIABLES
cap = cv2.VideoCapture
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
current_distances = collections.deque(maxlen=4)
marker_centres = collections.deque(maxlen=4)
distances = collections.deque(maxlen=4)
ideal_distances = [99, 99, 99, 99]
filament_data = {
    "key": "value"
}
marker_data = {
    "key": "value"
}
firstRun = True

## Sets up the capture object and asks if its locally or IP cam
ip = input("Run with IP cam? ")
if ip != "":
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
            cv2.destroyWindow("Instructions")
            break

    ## User now selects ROI for filament
    filament_ROI = cv2.selectROI("Select the FILAMENT. Press ESC to exit, and ENTER to save the ROI", frame)

    ## Now the user chooses the marker ROIs. If they get any amount other than 4 they are asked to redo.
    while not correct_num_of_markers:
        marker_ROIs = cv2.selectROIs("Select 4 MARKER ROIs, pressing ENTER between them, then press ESC when done",
                                     frame)
        correct_num_of_markers = (len(marker_ROIs) == 4)
        if not correct_num_of_markers:
            toaster.show_toast("Marker Capture", "That was not the right amount of markers, please try again.",
                               duration=2, threaded=True)
        else:
            toaster.show_toast("Marker Capture", "Captured the filament and marker ROI's correctly!", duration=2,
                               threaded=True)

    ## Clean up and close the camera
    cv2.destroyAllWindows()
    cv2.waitKey(0)
    sleep(0.1)

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
    ## TODO Make sure that the image doesnt get displayed in invert??!!
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
    trackerLost = False

    ## Read the current frame from the camera and abort if it's bad
    ok, frame = cap.read()
    if not ok:
        print("Capture was bad...")
        break

    ## Update the trackers' values:
    markerTrackerOK, markers = markerTracker.update(frame)
    filamentTrackerOK, filament = filamentTracker.update(frame)
    if (not markerTrackerOK) or (not filamentTrackerOK):
        # print("One of the trackers returned false when called for update")
        trackerLost = True

    ## Draw new filament box now we have updated our trackers:
    centrex = filament[0] + (filament[2] / 2)
    centrey = filament[1] + (filament[3] / 2)
    if (centrex != 0) and (centrey != 0):
        frame = cv2.rectangle(frame, filament, (255, 0, 0), 2, 1)
        frame = cv2.circle(frame, (int(centrex), int(centrey)), 2, (255, 0, 0))
        filament_centre = (centrex, centrey)
        filament_centre_int = (int(centrex), int(centrey))
    else:
        filament_centre = None

    ## Iterate through all the marker points and draw them on.
    for bbox in markers:
        centrex = bbox[0] + (bbox[2] / 2)
        centrey = bbox[1] + (bbox[3] / 2)

        ## The tracking will report zero if lost, so we don't draw if this is the case
        if (centrex != 0) and (centrey != 0):
            frame = cv2.rectangle(frame, bbox, (0, 255, 0), 2, 1)
            frame = cv2.circle(frame, (int(centrex), int(centrey)), 2, (0, 255, 0))
            marker_centres.append((centrex, centrey))
        else:
            ## In the case where the distance is zero, we append a NONE to show this.
            marker_centres.append(None)

    ## Get the distance between marker points and filament AND draw lines
    for centre in marker_centres:
        ## If the centre is actually a valid coord:
        if centre is not None and filament_centre is not None:
            ## Find the distance between the filament and the marker
            distances.append(err.findDistance(centre, filament_centre))

            ## Unpack points and make them not floats so that cv2 can use them
            x, y = centre
            x = int(x)
            y = int(y)
            centre = (x, y)

        else:
            ## The distance is null so we append None
            distances.append(None)

        if centre is not None and filament_centre is not None:
            # noinspection PyUnboundLocalVariable
            cv2.line(frame, filament_centre_int, tuple(centre), (0, 0, 255), 5)

    ## If this is the first time that the loop has run, then those distances should be taken as
    ## The correct ones, hence we save them as such

    ## Round the distances so they're easier to read, but program should still use the precise ones
    human_readable_distances = []
    for dist in distances:
        try:
            human_readable_distances.append(round(dist, 2))
        except:
            human_readable_distances.append(dist)

    if firstRun:
        ideal_distances = distances
        human_readable_ideal_distances = human_readable_distances
        firstRun = False

    ## Get the percentage error of the expected and the actual:
    percentages = err.percentage_error(human_readable_distances, human_readable_ideal_distances)

    ## Display the distances on a separate window
    info_array = np.zeros([512, 512, 3])
    cv2.putText(info_array, "Distances:" + str(human_readable_distances), (10, 15), fontFace=cv2.FONT_HERSHEY_COMPLEX,
                fontScale=0.6, color=(0, 255, 0))

    ## Display the IDEAL distances
    # noinspection PyUnboundLocalVariable
    cv2.putText(info_array, "IDEAL:" + str(human_readable_ideal_distances), (10, 35), fontFace=cv2.FONT_HERSHEY_COMPLEX,
                fontScale=0.6, color=(0, 255, 0))

    ## Display the message that the trackers are lost only if variable says they are
    if trackerLost:
        cv2.putText(info_array, "One of the trackers returned false when called for an update" +
                    str(human_readable_distances), (10, 55), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.6,
                    color=(0, 255, 0))

    ## Display the IDEAL distances
    cv2.putText(info_array, "% Err:" + str(percentages), (10, 75),
                fontFace=cv2.FONT_HERSHEY_COMPLEX,
                fontScale=0.6, color=(0, 255, 0))

    ## At the end of the loop, we need to display the frame, and capture that frame to the recoding device.
    cv2.imshow("Printer Main Page. Press ESC to exit", frame)
    cv2.imshow("Data Page", info_array)
    video_out.write(frame)

    ## Check if the ESC key has been pressed (if it has then we break since user wants so exit)
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        print("User pressed esc button so loop breaking")
        break
