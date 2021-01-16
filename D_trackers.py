## Brendan Ind 2020-2021 A-Level CS NEA
## Tracker GUI File

import cv2


def init_tracking(frame, bbox, tracker=cv2.TrackerMIL_create()):
    ok = tracker.init(frame, bbox)

    if ok:
        return tracker
    else:
        return False
