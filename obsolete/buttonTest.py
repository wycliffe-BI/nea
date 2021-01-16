from obsolete.functions import *

cv2.startWindowThread()

def back(*args):
    pass

cv2.namedWindow("Frame")
cv2.createButton("Back", onChange=back, userData=None, buttonType=cv2.QT_PUSH_BUTTON, initialButtonState=1)
cv2.createButton()
