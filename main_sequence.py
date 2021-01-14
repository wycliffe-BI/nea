## Brendan Ind 2020-2021 A-Level CS NEA
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


## FIND MARKER ROIs:
##---------------------------------------------------------------##
##Split into 4 quadrants
tr, tl, br, bl = quadrant(markers_clean)

##Return the ROI's for each quadrant:
tr_lowest, tr_highest, tr_right, tr_left, tr = find_non_black_pixels(tr)
tl_lowest, tl_highest, tl_right, tl_left, tl = find_non_black_pixels(tl)
br_lowest, br_highest, br_right, br_left, br = find_non_black_pixels(br)
bl_lowest, bl_highest, bl_right, bl_left, bl = find_non_black_pixels(bl)
##---------------------------------------------------------------##


##FIND FILAMENT ROIs:
##---------------------------------------------------------------##
# filament_clean = cv2.imread("filament_example.png")
fil_lowest, fil_highest, fil_rightmost, fil_leftmost = find_non_black_pixels(filament_clean)
filament_box_array = putBox(filament, (fil_highest, fil_leftmost), (fil_lowest, fil_rightmost))
##---------------------------------------------------------------##
