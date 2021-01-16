## Brendan Ind 2020-2021 A-Level CS NEA
## Calibration file

import cv2
import warnings
from win10toast import ToastNotifier

toaster = ToastNotifier()


def get_frame():
    warnings.filterwarnings("ignore", category=FutureWarning)
    cap = cv2.VideoCapture(0)
    ok, frame = cap.read(0)
    if not ok:
        return False
    cap.release()
    warnings.filterwarnings("default", category=FutureWarning)
    return ok, frame


def roi_select(array, toast_title, winName="ERROR YOU HAVEN'T NAMED THIS WINDOW!!"):
    rois = cv2.selectROIs(winName, array, showCrosshair=False, fromCenter=False)
    cv2.destroyAllWindows()
    toaster.show_toast(toast_title, "Captured %s ROI's" % (len(rois)), duration=2)
    return rois
