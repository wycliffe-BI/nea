## Brendan Ind
## Main launch file

## RUN ME!!!!!!
## (Ensure you have the requirements.txt installed.)

from functions import *
from filament_marker_selection import select
from object_tracking import *
from gui import *
import sys
from finding_blobs import *

## RUN LOGIN PAGE
##---------------------------------------------------------------##


##---------------------------------------------------------------##


## GET THE CORRECT ARRAYS:
##---------------------------------------------------------------##
proceed = False
while not proceed:
    markers, markers_bw, markers_clean, markers_original = select("Select the marker colour")
    print("Got the marker array")
    filament, filament_bw, filament_clean, filament_original = select("Select the filament colour")
    print("Got the filament array")

    proceed = checking_page(PILconvert(markers_clean), PILconvert(filament_clean))

    if proceed == 3:
        print("Exit button was clicked in the tkinter window")
        sys.exit()
print("Exited the loop with the correct arrays")
##---------------------------------------------------------------##


## IMAGE RESIZING
##---------------------------------------------------------------##
filament_clean = resize(filament_clean, 300, 200)
markers_clean = resize(markers_clean, 300, 200)

filament = resize(filament, 300, 200)
markers = resize(markers, 300, 200)
print("Finished resizing images")
##---------------------------------------------------------------##


## FIND BBOX AND CIRCLES IN THE ARRAYS:
##---------------------------------------------------------------##
##MARKERS:
marker_points, marker_circle_array = findCircles(markers_bw)
print("Marker points:", marker_points)

##FILAMENT:
# filament_clean = cv2.imread("filament_example.png")
lowest, highest, rightmost, leftmost = find_filament(filament_clean)
filament_box_array = putBox(filament, (highest, leftmost), (lowest, rightmost))
##---------------------------------------------------------------##


## SHOW THE IMAGES
##---------------------------------------------------------------##
plt3("Normal:", filament_original, "Filament-BW", filament_bw, "Marker-BW", markers_bw)
plt3("Normal:", filament_original, "Filament ROI:", filament_box_array, "Markers Circled:", marker_circle_array)
##---------------------------------------------------------------##