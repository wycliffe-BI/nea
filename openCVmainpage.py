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
cv2.namedWindow("markers")
cv2.setMouseCallback('markers', callback)

## THIS IS THE CODE TO ISOLATE THE *MARKER* COLOUR
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

    frame = cv2.imread("ender.jpg")

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

bw_markers = cv2.cvtColor(markers, cv2.COLOR_BGR2GRAY)
bw_filament = cv2.cvtColor(filament, cv2.COLOR_BGR2GRAY)

## Let's store these arrays in a text file
with open("markers.txt", "w") as file:
    file.write(str(markers))
with open("filament.txt", "w") as file:
    file.write(str(filament))

# cap.release()
cv2.destroyAllWindows()


## Lets show the currently captured arrays to the user to see if they are happy with them:
plt.imshow(removeNoise(bw_markers)), plt.title("Markers:"), plt.show()
plt.imshow(removeNoise(bw_filament)), plt.title("Filament"), plt.show()



## If the ARE NOT HAPPY with the current arrays:
if input("Run again? y/N") == "y":
    ## Open a new instace of this file so they can chose the new array:
    exec(open('openCVmainpage.py').read())

## Else they are happy so we read what is currently in the text files (since this contains the array they're happy with)
else:
    with open("markers.txt", "r") as file:
        marker = file.read()
    with open("filament.txt", "r") as file:
        filament = file.read()


## We then show those arrays:
plt.imshow(removeNoise(bw_markers)), plt.title("[recvd from txt] Markers:"), plt.show()
plt.imshow(removeNoise(bw_filament)), plt.title("[recvd from txt] Filament"), plt.show()
