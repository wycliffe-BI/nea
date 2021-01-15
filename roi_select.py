from functions import *
from win10toast import ToastNotifier
import threading
toaster = ToastNotifier()

## threading.Thread(target=worker).start()

def notif(array, toast_title):
    toaster.show_toast(duration=2, title=toast_title, msg="Captured %s marker(s)" % (len(array)))

def getSuffix(rois):
    digit = len(rois)
    if digit == 1:
        return "st"
    elif digit == 2:
        return "nd"
    elif digit == 3:
        return "rd"
    elif digit == 4:
        return "th"
    else:
        return "*****"

def roi_select(array, toast_title="UNSET TITLE", winName="ERROR YOU HAVEN'T NAMED THIS WINDOW!!"):
    rois = cv2.selectROIs(winName, array, showCrosshair=False, fromCenter=False)
    cv2.destroyAllWindows()
    threading.Thread(target=notif(rois, toast_title)).start()
    return rois