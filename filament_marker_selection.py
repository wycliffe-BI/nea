## Brendan Ind

from functions import *

def select(windowName="ERROR: Window name not set"):

    global precision
    precision = 150

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
    cv2.namedWindow(windowName)
    cv2.setMouseCallback(windowName, callback)

    ## THIS IS THE CODE TO ISOLATE THE COLOUR WE WANT
    # ---------------------------------------------------------------------------------------------------------------------
    ## Capture fame by frame
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    unedited = frame

    while True:
        frame = unedited
        #frame = cv2.imread("img/ender_proper.jpg")

        ## Create two arrays which are the two colour thresholds
        lower = np.array([picker_blue - precision, picker_green - precision, picker_red - precision])
        upper = np.array([picker_blue + precision, picker_green + precision, picker_red + precision])

        ## Make a mask from the threshold arrays by combining them
        mask = cv2.inRange(frame, lower, upper)  ##lower, upper

        ## This is the result of the bitwise_and manipulation that is the result of the mask and frame
        result = cv2.bitwise_and(frame, frame, mask=mask)

        ## Save the resultant array as "arrays", which is our future array to refer back to the pointers with
        out_original = frame
        out = result
        out_bw = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
        out_clean = removeNoise(out, its=1)

        ## Show that frame with the resulting array on it
        cv2.imshow(windowName, out)

        ## Press ENTER to quit
        if cv2.waitKey(1) & 0xFF == 13:  ##13 is the carriage return key, so will break with enter key
            break
    cv2.destroyAllWindows()
    cap.release()
    # ---------------------------------------------------------------------------------------------------------------------

    return out, out_bw, out_clean, out_original
