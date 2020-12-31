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


proceed = False
while not proceed:
    markers, markers_bw, markers_clean = select("Select the marker colour")
    print("Got the marker array")
    filament, filament_bw, filament_clean = select("Select the filament colour")
    print("Got the filament array")

    proceed = checking_page(PILconvert(markers_clean), PILconvert(filament_clean))

    if proceed == 3:
        print("Exit button was clicked in the tkinter window")
        sys.exit()
print("Exited the loop with the correct arrays")


## Code to draw circles around the MARKERS
marker_points, marker_circle_array = findCircles(markers_clean)

print(marker_points)


filament_clean = cv2.imread("filament_example.png")

## Code to draw a box around the FILAMENT
lowest, highest, rightmost, leftmost = find_filament(filament_clean)
filament_box_array = putBox(filament_clean, (highest, leftmost), (lowest, rightmost))


plt.imshow(marker_circle_array), plt.show()
plt.imshow(filament_box_array), plt.show()



