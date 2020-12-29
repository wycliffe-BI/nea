## Brendan Ind

from functions import *


def select(marker=True, filament=False):
    if (marker == True) and (filament == False):
        windowName = "Select the marker colour"

    elif (filament == True) and (marker == False):
        windowName = "Select the colour of the filament"

    else:
        ##Housten we have a problem since if this branch happens either neither were true, or both were. Das bad.
        return False

    ## ACTUAL USEFUL CODE STARTS:
    global precision
    precision = 255

    def callback(event, x, y, flags, param):
        global picker_blue, picker_green, picker_red, precision
        if event == cv2.EVENT_MOUSEMOVE:  # checks mouse moves
            colorsBGR = frame[y, x]
            picker_blue = colorsBGR[0]
            picker_green = colorsBGR[1]
            picker_red = colorsBGR[2]

        if event == 1:
            ##This is the left button down event
            precision -= 10
            print("Decreased precision by 10 (%s)" %(precision))

        if event == 2:
            ## This is the right button down event
            precision += 10
            print("Increased precision by 10(%s)" %(precision))

    # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.namedWindow("markers")
    cv2.setMouseCallback('markers', callback)

    ## THIS IS THE CODE TO ISOLATE THE COLOUR WE WANT
    # ---------------------------------------------------------------------------------------------------------------------
    while True:
        ## Capture fame by frame
        # ret, frame = cap.read()

        frame = cv2.imread("ender.jpg")

        ## Create two arrays which are the two colour thresholds
        lower = np.array([picker_blue - precision, picker_green - precision, picker_red - precision])
        upper = np.array([picker_blue + precision, picker_green + precision, picker_red + precision])

        ## Make a mask from the threshold arrays by combining them
        mask = cv2.inRange(frame, lower, upper)  ##lower, upper

        ## This is the result of the bitwise_and manipulation that is the result of the mask and frame
        result = cv2.bitwise_and(frame, frame, mask=mask)

        ## Save the resultant array as "markers", which is our future array to refer back to the pointers with
        markers = result
        bw_markers = cv2.cvtColor(markers, cv2.COLOR_BGR2GRAY)
        clean_markers = removeNoise(bw_markers)

        ## Show that frame with the resulting array on it
        cv2.imshow("markers", markers)

        ## Press ENTER to quit
        if cv2.waitKey(1) & 0xFF == 13:  ##13 is the carriage return key, so will break with enter key
            break
    cv2.destroyAllWindows()
    # ---------------------------------------------------------------------------------------------------------------------


print(select())
