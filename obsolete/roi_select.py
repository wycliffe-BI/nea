from obsolete.functions import *
from win10toast import ToastNotifier
toaster = ToastNotifier()


def roi_select(array, toast_title, winName="ERROR YOU HAVEN'T NAMED THIS WINDOW!!"):
    rois = cv2.selectROIs(winName, array, showCrosshair=False, fromCenter=False)
    cv2.destroyAllWindows()
    toaster.show_toast(toast_title, "Captured %s ROI's" % (len(rois)), duration=2)
    return rois