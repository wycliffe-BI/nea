## Brendan Ind
## Object Tracking code

import cv2


def find_non_black_pixels(array):
    #file = open("logs.txt", "w")

    flag = False
    changed_leftmost = False
    changed_rightmost = False
    changed_highest = False
    changed_lowest = False

    ## NOTE THAT THESE LARGE NUMBERS MUST BE ALRGER THAN THE PX count OF THE IAMGE OTHERWISE IT WONT WORK LOLLL
    highest, lowest, leftmost, rightmost = 10000, 0, 10000, 0

    # The basic idea of those variables above is that the lowest and rightmost are "counting up" and beating each others
    # Previous scores when they reach a new number that is higher (i.e. a pix that is more to the right or more lower
    # down.

    # the highest and the leftmost variables work in the opposite: they want the lowest numbers possible and start
    # on a large number and work their way downards beating their previous variables' score if the value is lower than
    # previously.

    xPos = -1
    yPos = -1

    for x in array:
        xPos += 1
        yPos = -1
        for y in x:
            yPos += 1
            current_pixel = str(array[xPos][yPos])

            ## BE AWARE THAT WE WILL NEED TO CHANGE THIS IF STATEMENT DEPENDING ON THE FORMAT OF THE ARRAY SEARCHING
            ## some have other s like [0, 0, 0,] not [0 0 0]:
            ## TODO
            print(current_pixel)
            if current_pixel != "[0 0 0]":
                ## We dont have a black pixel. We need to do something with the x and y values here.
                flag = True

                if highest > yPos:
                    highest = yPos
                    ## Set the pixel we identified to neon pink so we can look at it later

                    array[xPos][yPos] = [255, 0, 0]
                    #changed_highest = True

                if leftmost > xPos:
                    leftmost = xPos
                    ## Set the array that we are looking at as neon pink:

                    array[xPos][yPos] = [255, 0, 0]
                    #changed_leftmost = True

                if rightmost < xPos:
                    ## We have a new righmost pixel so we update counter:
                    rightmost = xPos

                    array[xPos][yPos] = [255, 0, 0]
                    #changed_rightmost = True

                if lowest < yPos:
                    ## Same reason, we have a new lower pixel so we update that var with te lowest so far
                    lowest = yPos

                    array[xPos][yPos] = [255, 0, 0]
                    #changed_lowest = True

    print("low:%s, high:%s, right:%s, left:%s" %(lowest, highest, rightmost, leftmost))

    array[rightmost][highest] = [0, 0, 255]
    array[leftmost][highest] = [0, 0, 255]
    array[rightmost][lowest] = [0, 0, 255]
    array[leftmost][lowest] = [0, 0, 255]

    ##plt.imshow(array), plt.title("Look for blues"), plt.show()

    return lowest, highest, rightmost, leftmost, array


def init_tracking(frame, bbox, tracker=cv2.TrackerMIL_create()):
    ok = tracker.init(frame, bbox)

    if ok:
        return tracker
    else:
        return False


def putBox(array, topLeft, bottomRight, colour=(255, 0, 0)):
    return cv2.rectangle(array, topLeft, bottomRight, colour, 2)