## Brendan Ind 2020

## This file is for all the handling of the image realated data point collections,
## for example, this finds the points of the markers and the filament
## For the most part this code comes from  openCVmainpage.py


from functions import *
import os
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
        print("Decreased precision by 10")

    if event == 2:
        ## This is the right button down event
        precision += 10
        print("Increased precision by 10")

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


## THIS IS THE CODE TO ISOLATE THE *MARKER* COLOUR
# ---------------------------------------------------------------------------------------------------------------------
cv2.namedWindow("markers")
cv2.setMouseCallback('markers', callback)
while True:
    ## Capture fame by frame
    # ret, frame = cap.read()

    frame = cv2.imread("../ender.jpg")

    ## Create two arrays which are the two colour thresholds
    lower = np.array([picker_blue - precision, picker_green - precision, picker_red - precision])
    upper = np.array([picker_blue + precision, picker_green + precision, picker_red + precision])

    ## Make a mask from the threshold arrays by combining them
    mask = cv2.inRange(frame, lower, upper)  ##lower, upper

    ## This is the result of the bitwise_and manipulation that is the result of the mask and frame
    result = cv2.bitwise_and(frame, frame, mask=mask)

    ##Turn it black and white if we want:
    # result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    ## Save the resultant array as "markers", which is our future array to refer back to the pointers with
    markers = result

    ## Show that frame with the resulting array on it
    cv2.imshow("markers", result)

    ## Press ENTER to quit
    if cv2.waitKey(1) & 0xFF == 13:  ##13 is the carriage return key, so will break with enter key
        break
cv2.destroyAllWindows()
# ---------------------------------------------------------------------------------------------------------------------


## THIS IS THE CODE TO ISOLATE THE FILAMENT COLOUR
# ---------------------------------------------------------------------------------------------------------------------
cv2.namedWindow("filament")
cv2.setMouseCallback('filament', callback)
while True:
    ## Capture fame by frame
    # ret, frame = cap.read()

    frame = cv2.imread("../ender.jpg")

    ## Create two arrays which are the two colour thresholds
    lower = np.array([picker_blue - precision, picker_green - precision, picker_red - precision])
    upper = np.array([picker_blue + precision, picker_green + precision, picker_red + precision])

    ## Make a mask from the threshold arrays by combining them
    mask = cv2.inRange(frame, lower, upper)  ##lower, upper

    ## This is the result of the bitwise_and manipulation that is the result of the mask and frame
    result = cv2.bitwise_and(frame, frame, mask=mask)

    ## Turn it black and white if we want:
    # result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    ## Save the resultant array as "filament", which is our future array to refer back to the pointers with
    filament = result

    ## Show that frame with the resulting array on it
    cv2.imshow("filament", result)

    ## ENTER to quit
    if cv2.waitKey(1) & 0xFF == 13:  ##13 is the carriage return key, so will break with enter key
        break
# ---------------------------------------------------------------------------------------------------------------------


# cap.release()
cv2.destroyAllWindows()

bw_markers = cv2.cvtColor(markers, cv2.COLOR_BGR2GRAY)
bw_filament = cv2.cvtColor(filament, cv2.COLOR_BGR2GRAY)

plt.imshow(removeNoise(bw_markers)), plt.title("Markers:"), plt.show()
plt.imshow(removeNoise(bw_filament)), plt.title("Filament"), plt.show()



def
print("Are these ok?")
a = input("")

exec(open('../openCVmainpage.py').read())
