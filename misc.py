## Brendan Ind 2020-2021 A-Level CS NEA
## Misc. Functions File
import datetime
import cv2
from PIL import Image
import numpy as np

def putBox(array, topLeft, bottomRight, colour=(255, 0, 0)):
    return cv2.rectangle(array, topLeft, bottomRight, colour, 2)


# noinspection SpellCheckingInspection
def PILconvert(array):
    ## Converting images from the np format (bool and 3 channels for RGB)
    ## To PIL compatible images with 0-255

    return Image.fromarray((array * 255).astype(np.uint8))


def putTimestamp(array):
    ## Put a timestamp on it
    timestamp = datetime.datetime.now()
    cv2.putText(array, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, array.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    return array
