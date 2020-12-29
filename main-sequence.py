## Brendan Ind

from functions import *
from filament_marker_selection import select
from gui import *
import sys

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