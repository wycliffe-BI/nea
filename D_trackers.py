## Brendan Ind 2020-2021 A-Level CS NEA
## Tracker GUI File

import cv2


def tracker_init(array, frame, multi=True, multiTracker=cv2.legacy.MultiTracker_create(),
                 singleTracker=cv2.TrackerKCF_create(), legacySingleTracker=cv2.legacy.TrackerMIL_create()):
    ok = []



    if multi:
        ## We create a multi tracker object that efficiently tracks multiple points.
        for bbox in array:
            state = multiTracker.add(cv2.legacy.TrackerKCF_create(), frame, tuple(bbox))
            ok.append(state)
        out = multiTracker

    else:
        ## Only a single tracker is initiated and returned, and it takes the first of the array
        state = singleTracker.init(frame, tuple(array))
        ok.append(state)
        out = singleTracker
    return ok, out
