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

proceed = False

while not proceed:
    ## Get a frame of the camera
    clean = calib.get_frame()

    ## Get the ROI's for the filament and the markers
    filament = calib.roi_select(clean, "Filament Selection", "Select the FILAMENT. Press C to cancel, ESC to exit, "
                                                             "and ENTER to save a ROI")
    markers = calib.roi_select(clean, "Marker Selection",
                               "Select the MARKERS. Press C to cancel, ESC to exit, and ENTER to "
                               "save a ROI")

    ## Clean up and allow camera to close.
    cv2.waitKey(0)
    sleep(1)

    ## Put all the ROIs into a dictionary for easy access
    rois = {
        "markers": markers,
        "filament": filament
    }
    '''
    We can use:
    dict.get("key") to return the array coresponding to that key.
    
    e.g. rois.get("filament") returns [filament]
    '''

    ## Copy the clean (no roi's) array to one we can add ROI rectangles to.
    frame_with_boxes = clean

    for i in filament:
        '''
        i is array in form (x,y,w,h)
        >> print("RT:", (x, y), "   LB:", (x + w, y + h))
        will return the points we need to plt
        '''

        x, y, w, h = i
        print("RT:", (x, y), "   LB:", (x + w, y + h))
        colour = (0, 0, 255)
        frame_with_boxes = cv2.rectangle(frame_with_boxes, (x, y), (x + w, y + h), colour, 2)

    for i in markers:
        ## Unpack the values
        x, y, w, h = i

        ## Colour of these boxes:
        colour = (255, 0, 0)

        ## Draw the rects.
        frame_with_boxes = cv2.rectangle(frame_with_boxes, (x, y), (x + w, y + h), colour, 2)

    ## Clean up
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    proceed = checker.checking_page(misc.PILconvert(frame_with_boxes))

    if proceed == 3:
        print("Exit button was clicked in the tkinter window")
        sys.exit()
print("Exited the loop with the correct arrays")
##---------------------------------------------------------------##

## Initiate some trackers:

## A dictionary to store all the tracker objects in
trackers = {}

while True:
    ##MAINLOOP

    ## Update the frame
    frame = calib.get_frame()

    ## If frame is False bool then camera not captured correctly
    if not frame:
        print("Capture Error")