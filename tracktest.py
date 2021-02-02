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

markers = []
filament = []
clean = []
proceed = False

multiTracker = cv2.MultiTracker_create()

cap = cv2.VideoCapture(0)


while True:
    ## MAIN LOOP

    ## Update the frame
    ok, frame = cap.read()

    (success, boxes) = multiTracker.update(frame)

    ## If frame is False bool then camera not captured correctly
    if not ok:
        print("Capture Error")
        break

    cv2.imshow("PRINTER", frame)

    k = cv2.waitKey(1) & 0xff
    if k == ord("c"):
        bbox = cv2.selectROI("Select Frame", frame)

        ok = multiTracker.add(cv2.TrackerMIL_create(), frame, bbox)
