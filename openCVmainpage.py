import cv2
import numpy as np
import datetime
from functions import *

from numpy import zeros

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cv2.namedWindow("main")


def putTimestamp():
    ## Put a timestamp on it
    timestamp = datetime.datetime.now()
    cv2.putText(frame, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)


createTrackbars("main")


def draw_dot(event, x, y, flags, param, **kwargs):
    centre = (x, y)
    radius = 1000
    colour = (0, 0, 255)
    thickness = 10
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img, (x, y), 100, (255, 0, 0), -1)
        ##cv2.circle(result, centre, radius, colour, thickness)
        print("done callback", x, y)


cv2.setMouseCallback("main", draw_dot)

while True:

    ## Get the latest trackbar values
    redVal, greenVal, blueVal = updateTrackbarValues()

    ## Capture fame by frame
    ret, frame = cap.read()

    ## Put a timestamp on that frame
    putTimestamp()

    ## Create two arrays which are the two colour thresholds
    lower = np.array([blueVal, greenVal, redVal])
    upper = np.array([blueVal + 100, greenVal + 100, redVal + 100])

    ## Make a mask from the threshold arrays by combining them
    mask = cv2.inRange(frame, lower, upper)  ##lower, upper

    ## This is the result of the bitwise_and manipulation that is the result of the mask and frame
    result = cv2.bitwise_and(frame, frame, mask=mask)

    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    ## Show that frame with the resulting array on it
    cv2.imshow("main", result)

    ## Press q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

## Once the button breaks the while loop, this will close the windows.

plt.imshow(result)
plt.title("normal:")
plt.show()

col = contain_colour(result, [0,0,0])
newArray = removeNoise(result)

plt.imshow(newArray)
plt.show()

# cap.release()
# cv2.destroyAllWindows()
