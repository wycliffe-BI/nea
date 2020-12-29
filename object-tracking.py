import cv2


def init_tracking(frame, bbox, tracker=cv2.TrackerMIL_create()):
    ok = tracker.init(frame, bbox)

    if ok:
        return tracker
    else:
        return False


def putBox(array, bbox):
    top_left_corner = (
        int(bbox[0]), int(bbox[1])
    )

    bottom_right_corner = (
        int(bbox[0]+bbox[2]), int(bbox[1]+bbox[3])
    )

    return cv2.rectangle(array, top_left_corner, bottom_right_corner, (0, 0, 255), 2, 1)