import cv2

def get_frame():
    cap = cv2.VideoCapture(0)
    frame = cap.read()
    _, frame = cap.read(0)
    cap.release()
    return frame