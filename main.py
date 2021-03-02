## Brendan Ind 2020-2021 A-Level CS NEA
## Main launch file

## RUN ME!!!!!!
## (Ensure you have the requirements.txt installed.)
import collections
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
thresh = 100
expected_distance_set = False


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
        markers = cv2.selectROIs("Select the 4 MARKERS, pressing enter between them. Press Esc to exit once you have "
                                 "selected 4 regions", clean)
        if len(markers) == 4:
            four_markers = True
            toaster.show_toast("Markers Capture", "Captured %s ROI's" % (len(filament)), duration=2)
        else:
            toaster.show_toast("Error", "You selected %s ROIs, there must only be 4 selected" % (len(filament)),
                               duration=2)

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

    ## Open the checker GUI and ensure that the user is happy with the selection
    proceed = checker.checking_page(misc.PILconvert(frame_with_boxes))

    ## If user clicked the xit button:
    if proceed == 3:
        print("Exit button was clicked in the tkinter window")
        sys.exit()

print("Exited the calibration loop with the correct arrays")

print("Marker Locations:" + str(markers), "\nFilament Locations:" + str(filament))

## Initiate some trackers:
frame = clean

marker_tracker_init_ok, markerTracker = tracking.tracker_init(markers, frame, multi=True)
filament_tracker_init_ok, filamentTracker = tracking.tracker_init(filament, frame, multi=False)

print('''
    Tracker inits:
    Marker OK: %s
    Filment OK: %s
''' % (marker_tracker_init_ok, filament_tracker_init_ok))

## Set up some video IO objects
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(filename='output.avi', apiPreference=cv2.CAP_FFMPEG, fourcc=fourcc, fps=20.0, frameSize=(
    frame.shape[1], frame.shape[0]))  # Make sure (width,height) is the shape of input frame from video

## This is a fixed length array to ensure no more than 4 values are reported here
current_dictionaries = collections.deque(maxlen=4)
current_distances = collections.deque(maxlen=4)

## expected contains the expected distance values that we want
expected = [100, 100, 100, 100]

i = -1
while True:
    status = ""
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

    ## Draw the new FILAMENT boxes on the frame
    centrex = filament[0] + (filament[2] / 2)
    centrey = filament[1] + (filament[3] / 2)
    frame = cv2.rectangle(frame, filament, (255, 0, 0), 2, 1)
    frame = cv2.circle(frame, (int(centrex), int(centrey)), 2, (255, 0, 0))
    filament_centre = (centrex, centrey)

    ## Draw the new MARKER boxes on the frame and find their centres
    marker_centres = []
    for bbox in markers:
        ## Unless we specify otherwise, these values are good.
        fil_tracker_good = True
        marker_tracker_good = True

        ## find centre points and append them to an array for later
        ##centre x or y = bbox[1] + (bbox[3]/2)
        centrex = bbox[0] + (bbox[2] / 2)
        centrey = bbox[1] + (bbox[3] / 2)
        marker_centres.append((centrex, centrey))

        # print("bbox number %s: %s "% (markers.indexOf(markers)+1, bbox))
        frame = cv2.rectangle(frame, bbox, (0, 0, 255), 2, 1)
        # print("Done %s out of %s markers" % (markers.indexOf(markers)+1, len(markers)))
        frame = cv2.circle(frame, (int(centrex), int(centrey)), 5, (0, 0, 255))

        ## Draw line from fils to centre, but make sure that they are actually points that the
        ## object tracking has given us. If they are (0, 0) then dont use them since they are
        ## a "lack" of coords, not actual points. Its unlikely that they're actually points to be used.
        if centrex != 0 and centrey != 0 and filament_centre[0] != 0 and filament_centre[1] != 0:
            frame = cv2.line(frame, (int(centrex), int(centrey)), (int(filament_centre[0]), int(filament_centre[1])),
                             (0, 255, 0), 5)
        if centrex == 0 and centrey == 0:
            cv2.putText(frame, "ERROR A MARKER TRACKER LOST", (150, 300),
                        fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.8, color=(0, 0, 255))
            marker_tracker_good = False
        if filament_centre[0] == 0 and filament_centre[0] == 0:
            cv2.putText(frame, "ERROR FIL TRACKER LOST", (150, 350),
                        fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.8, color=(0, 0, 255))
            fil_tracker_good = False

        if fil_tracker_good and marker_tracker_good:
            ## If both of our inputs are ok, then we record them to queue else we report zero:

            # This line appends all the data bout the relations between the points to a dict then that's saved to a
            # fixed length array:
            current_dictionaries.append(err.findDistance([centrex, centrey], filament_centre))

            ## This appends just the "dist" key form the dictionary, not the whole dictionary:
            current_distances.append(err.findDistance([centrex, centrey], filament_centre)["dist"])
        else:
            current_distances.append("N.D")
            current_dictionaries.append("N.D")

    ## When we exit this loop we should always have the "current" array with 4 values in it of the latest distances.
    ## And that value will be zero if something is wrong.

    if (not expected_distance_set) and current_distances[0] != "N.D." and current_distances[1] != "N.D." and current_distances[2] != "N.D." and current_distances[3] != "N.D.":
        ## This means that all the points have good distances
        ## Set the expected as the INITIAL distances
        expected = current_distances

        ## Ensures that this doesnt run again and reset the expected values
        expected_distance_set = True


    bed_adhesion = err.bedAdhesion(current_dictionaries, current_distances, expected, thresh)
    filament_run_out = err.filamentOut(current_dictionaries, expected, thresh)

    ## Show the percentage error of the current vs expected
    cv2.putText(frame, "%Err bed_adhesion: " + str(bed_adhesion["percentages"]), (100, 120), fontFace=cv2.FONT_HERSHEY_COMPLEX,
                fontScale=0.8, color=(0, 255, 0))
    #cv2.putText(frame, "%Err filament_run_out: " + str(filament_run_out["percentages"]), (100, 190), fontFace=cv2.FONT_HERSHEY_COMPLEX,
    #            fontScale=0.8, color=(0, 255, 0))
    cv2.putText(frame, "DISTS:" + str(current_distances), (0, 210), fontFace=cv2.FONT_HERSHEY_COMPLEX,
                fontScale=0.4, color=(0, 0, 255))

    cv2.putText(frame, "STATUS:"+ status, (0, 250), fontFace=cv2.FONT_HERSHEY_COMPLEX,
                fontScale=0.4, color=(0, 200, 200))

    ## Write that frame to the video object and display that frame to the GUI
    out.write(frame)
    cv2.imshow("PRINTER MAIN PAGE: Press Esc to exit", frame)

    ## Check if the waitkey has been pressed:
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

## Release and close everything:
cap.release()
out.release()
cv2.destroyAllWindows()
