## Brendan Ind 2020-2021 A-Level CS NEA
## Error Detection File

import math
from collections import deque


def findDistance(pointA: object, pointB: object, fullInfo=False) -> object:
    ## Note, d before var i.e. "dx" means change in x.

    Ax = pointA[0]
    Ay = pointA[1]

    Bx = pointB[0]
    By = pointB[1]

    # print("Coords::     A:(%s, %s)   B:(%s, %s)" % (str(Ax), str(Ay), str(Bx), str(By)))

    # larger minus smaller gives the difference

    if Ax >= Bx:
        dx = float(Ax - Bx)
    else:
        dx = float(Bx - Ax)

    if Ay >= By:
        dy = float(Ay - By)
    else:
        dy = float(By - Ay)

    ## Use pythag to find the distance between the points
    rawDistance = pythag(dx, dy)

    ## Find the tan of the internal angle of the triangle relating to dx/dy
    try:
        internal_angle = math.degrees(math.atan(dx / dy))
    except:
        print("TAN ERROR!!!")

    ## This defined the bearing and will be returned if we can't find the bearing.
    bearing = False

    ## We can devise four 'scenarios' that the lines could take with two coord points, A and B.
    ## Scenario 1:      A is LOW and LEFT,      B is HIGH and right
    if (Ay < By) and (Ax < Bx):
        bearing = 90 - internal_angle

    ## Scenario 2:      A is HIGH and left,     B is LOW and right
    if (Ay > By) and (Ax < Bx):
        bearing = 180 - internal_angle

    ## Scenario 3:      A is LOW and right,     B is HIGH and LEFT
    if (Ay < By) and (Ax > Bx):
        bearing = 360 - internal_angle
        ## We assume the centre is point A
        ## bearing = 180 - internal_angle

    ## Scenario 4:      A is HIGH and right,    B is LOW and LEFT
    if (Ay > By) and (Bx < Ax):
        bearing = 180 + internal_angle

    ## Return all our values in a list and two variables
    fulldict = {
        "dy": dx,
        "dx": dy,
        "dist": rawDistance,
        "bearing": bearing
    }
    if fullInfo:
        return fulldict
    else:
        return rawDistance


def pythag(dy, dx):
    aSquared = dy * dy
    bSquared = dx * dx
    cSquared = aSquared + bSquared
    c = math.sqrt(cSquared)

    return c


def filamentOut(actual, expected, thresh):
    return 0


def percentage_error(actualArray, idealArray):
    ## Iterate though n times:
    percentages = []

    ## Iterate through a zipped up version  (combines two arrays):
    for actual, ideal in zip(actualArray, idealArray):
        ## Make sure that they're actually numbers firstly:
        if actual is not None and ideal is not None:
            ## This will be true if actual is larger, else its false
            actual_is_larger = (actual > ideal)

            if actual_is_larger:
                difference = float(actual) - float(ideal)
                percentages.append(round(((difference / float(ideal)) * 100), 2))

            if not actual_is_larger:
                difference = float(ideal) - float(actual)
                percentages.append(round(((difference / float(ideal)) * 100), 2))
        else:
            ## Else its not a number, instead its NoneType
            percentages.append(None)

    return percentages
