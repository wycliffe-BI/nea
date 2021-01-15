## Brendan Ind
from functions import *
from roi_select import *
from get_frame import get_frame
from gui import *
from time import sleep


proceed = False

while not proceed:
    clean = get_frame()
    frame = clean

    filament = roi_select(frame, "Filament Selection",
                          "Select the FILAMENT. Press C to cancel, ESC to exit, and ENTER to save a ROI")
    markers = roi_select(frame, "Marker Selection", "Select the MARKERS. Press C to cancel, ESC to exit, and ENTER to save a ROI")

    cv2.waitKey(0)
    sleep(1)

    print("Markers:", markers, "\n Filament:", filament)

    marker_frame = clean
    filament_frame = clean
    for i in filament:
        ## i is array in form (x,y,w,h)
        x, y, w, h = i
        print("RT:", (x, y), "   LB:", (x + w, y + h))
        colour = (0, 0, 255)
        filament_frame = cv2.rectangle(filament_frame, (x, y), (x + w, y + h), colour, 2)

    for i in markers:
        ## i is array in form (x,y,w,h)
        x, y, w, h = i
        print("RT:", (x, y), "   LB:", (x + w, y + h))
        colour = (0, 0, 255)
        marker_frame = cv2.rectangle(marker_frame, (x, y), (x + w, y + h), colour, 2)

    cv2.imshow("marker", marker_frame)
    cv2.imshow("fil", filament_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    proceed = checking_page(PILconvert(filament_frame), PILconvert(marker_frame))

    if proceed == 3:
        print("Exit button was clicked in the tkinter window")
        sys.exit()
print("Exited the loop with the correct arrays")
##---------------------------------------------------------------##
