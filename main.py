## Brendan Ind 2020-2021 A-Level CS NEA
## Main launch file

## RUN ME!!!!!!
## (Ensure you have the requirements.txt installed.)

import sys
import cv2
from time import sleep
import A_login_gui as login
import B_calibration as calib
import C_checker_gui as checker
import D_trackers as tracking
import E_error_detection as err
import F_user_alert as alerts
import G_3dp_control as control
import misc
from win10toast import ToastNotifier

markers = []
filament = []
clean = []
proceed = False
toaster = ToastNotifier()
cap = cv2.VideoCapture(0)

while not proceed:
    ok = False
    while not ok:
        ok, frame = cap.read()
    while True:
        ok, frame = cap.read()
        cv2.imshow("PRNT", frame)
        k = cv2.waitKey(1) & 0xff
        if k == ord("c"):
            break

    ## Get a frame of the camera
    clean = frame

    ## Get the one ROI for the filament:
    filament = cv2.selectROI("Select the FILAMENT. Press ESC to exit, and ENTER to save the ROI", clean)
    toaster.show_toast("Filament Capture", "Captured the ROI", duration=2)

    ## Validation to make sure that there were only four ROI's selected.
    four_markers = False
    while not four_markers:
        markers = cv2.selectROIs("Select the 4 MARKERS. Press C to cancel, ESC to exit, and ENTER to "
                               "save a ROI", clean)
        if len(markers) == 4:
            four_markers = True
            toaster.show_toast("Markers Capture", "Captured %s ROI's" % (len(filament)), duration=2)
        else:
            toaster.show_toast("Error", "You selected %s ROIs, there must only be 4 selected" % (len(filament)), duration=2)

    ## Clean up and allow camera to close.
    cv2.destroyAllWindows()
    cv2.waitKey(0)
    sleep(1)

    ## Copy the clean (no roi's) array to one we can add ROI rectangles to.
    frame_with_boxes = clean


    ## Draw the box around the FILAMENT:
    ## Unpack the values
    x, y, w, h = filament
    ## Draw the rects.
    frame_with_boxes = cv2.rectangle(frame_with_boxes, (x, y), (x + w, y + h), (0, 0, 255), 2)

    ## Draw the boxes for the MARKERS:
    for bbox in markers:
        ## Unpack the values
        x, y, w, h = bbox

        ## Draw the rects.
        frame_with_boxes = cv2.rectangle(frame_with_boxes, (x, y), (x + w, y + h), (255, 0, 0), 2)

    ## Clean up
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    proceed = checker.checking_page(misc.PILconvert(frame_with_boxes))

    if proceed == 3:
        print("Exit button was clicked in the tkinter window")
        sys.exit()
print("Exited the calibration loop with the correct arrays")

print("Marker Locations:" + str(markers), "\nFilament Locations:" + str(filament))

## Initiate some trackers:
frame = clean

marker_tracker_init_ok, markerTracker = tracking.tracker_init(markers, frame, multi=True)
filament_tracker_init_ok, filamentTracker = tracking.tracker_init(filament, frame, multi=False)

## Set up some video IO objects
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(filename='output.avi', apiPreference=cv2.CAP_FFMPEG, fourcc=fourcc, fps=20.0, frameSize=(
frame.shape[1], frame.shape[0]))  # Make sure (width,height) is the shape of input frame from video

i = -1
while True:
    i += 1
    print("Mainloop Run #%s" % i)

    ## Update the frame
    ok, frame = cap.read()

    ## If frame is False bool then camera not captured correctly
    if not ok:
        print("Capture Error")
        break

    ##Put text (optional)
    # cv2.putText(frame, "text", (120, 120), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=(0, 255, 0))

    ## Update the trackers
    marker_tracker_update_ok, markers = markerTracker.update(frame)
    filament_tracker_update_ok, filament = filamentTracker.update(frame)

    if not marker_tracker_update_ok or not filament_tracker_update_ok:
        print("Tracker Lost: MKrs:" + str(marker_tracker_update_ok) + " Fil:" + str(filament_tracker_update_ok))

    ## Draw the new MARKER boxes on the frame
    for bbox in markers:
        # print("bbox number %s: %s "% (markers.indexOf(markers)+1, bbox))
        frame = cv2.rectangle(frame, bbox, (0, 0, 255), 2, 1)
        # print("Done %s out of %s markers" % (markers.indexOf(markers)+1, len(markers)))

    ## Draw the new FILAMENT boxes on the frame
    frame = cv2.rectangle(frame, filament, (255, 0, 0), 2, 1)

    ## Write that frame to the video object and siplay that frame to the GUI
    out.write(frame)
    cv2.imshow("PRINTER", frame)

    ## Check if the waitkey has been pressed:
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break


## Release and close everything:
cap.release()
out.release()
cv2.destroyAllWindows()
