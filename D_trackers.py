## Brendan Ind 2020-2021 A-Level CS NEA
## Tracker GUI File

import cv2


def init_trackers(array, frame, trackertype=cv2.TrackerMIL_create()):
    """

    :param array: This is the array with the bboxes enclosed in it, e.g. marker array
    :param frame: This is the image that the tracker tracks
    :param trackertype: Optional, sets the tracker object
    :return: trackers, an array of all the objects
    """
    out = []
    ok = True
    for bbox in array:
        trackingobject = trackertype
        ok = trackingobject.init(frame, tuple(bbox))
        out.append(trackingobject)

    return ok, out
