import cv2
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from random import randint

frame = np.zeros((512, 512, 3), dtype="uint8")

## Initialise some variables that we can change during the loop
center = [120, 120]
radius = 5

while True:
    ## Reset frame back to original toa void shadows of past circles
    modified = np.zeros((512, 512, 3), dtype="uint8")

    # Lil break
    sleep(0.001)

    ## change the x and y coordinates about a bit (or maybe not, depends on rand)
    newx = center[0] + randint(-1, 1)
    newy = center[1] + randint(-1, 1)

    ## Distance between bed points
    seperation = 300

    center = (newx, newy)  ## circle to the top left (the one that we base everything else off of
    center2 = (newx + seperation, newy)  ## Circle to the top right
    center3 = (newx, newy + seperation)  ## Circle to the bottom left
    center4 = (newx + seperation, newy + seperation)  ## Circle to the bottom right
    cv2.circle(modified, center=center, radius=radius, color=(255, 0, 0), thickness=-1)
    cv2.circle(modified, center=center2, radius=radius, color=(255, 0, 0), thickness=-1)
    cv2.circle(modified, center=center3, radius=radius, color=(255, 0, 0), thickness=-1)
    cv2.circle(modified, center=center4, radius=radius, color=(255, 0, 0), thickness=-1)

    ## Make a dot that can signify the part that is printing
    cv2.circle(modified, center=(int(512 / 2), int(512 / 2)), radius=radius, color=(0, 255, 0), thickness=-1)

    cv2.imshow("Circlzzz", modified)

    k = cv2.waitKey(1) & 0xff
    if k == 27: break

