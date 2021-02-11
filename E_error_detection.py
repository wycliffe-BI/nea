## Brendan Ind 2020-2021 A-Level CS NEA
## Error Detection File

import math


def findDistance(pointA: object, pointB: object) -> object:
    ## Note, d before var i.e. "dx" means change in x.

    Ax = pointA[0]
    Ay = pointA[1]

    Bx = pointB[0]
    By = pointB[1]

    print("Coords::     A:(%s, %s)   B:(%s, %s)" % (str(Ax), str(Ay), str(Bx), str(By)))

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
    internal_angle = math.degrees(math.atan(dx / dy))

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
    return [dx, dy], rawDistance, bearing


def pythag(dy, dx):
    aSquared = dy * dy
    bSquared = dx * dx
    cSquared = aSquared + bSquared
    c = math.sqrt(cSquared)

    return c


def bedAdhesion(actual, expected):
    return 0

def filamentOut(actual, expected):
    return 0