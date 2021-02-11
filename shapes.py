import cv2


class tracker:
    def __init__(self, initial, roi, trackerobj, type):
        self.initial = initial
        self.roi = roi
        self.trackerobj = trackerobj
        self.type = type

    def create(self):
        if self.type == "multi":
            pass

        if self.type == "single":
            pass
        else:
            print("No type in the instantiated class!!")

    def start(self):
        pass

    def update(self):
        pass
