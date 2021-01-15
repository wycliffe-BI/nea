from functions import *

def roi_select(array, windName="ERROR YOU HAVEN'T NAMED THIS WINDOW!!"):
    tr = cv2.selectROIs()

cap = cv2.VideoCapture(0)
frame = cap.read()

_, frame =cap.read(0)

roi_select(frame)
