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
    return {
        "dy": dx,
        "dx": dy,
        "dist": rawDistance,
        "bearing": bearing
    }


def pythag(dy, dx):
    aSquared = dy * dy
    bSquared = dx * dx
    cSquared = aSquared + bSquared
    c = math.sqrt(cSquared)

    return c


def bedAdhesion(actual_dicts, actual_lengths, expected_lengths, thresh):
    actual_is_larger = True
    result = True
    ayes_nays = []
    percentage_results = []
    a_number = False

    ## Iterate though n times:
    for i in range(0, len(actual_lengths)):

        try:
            actual_is_larger = (actual_lengths[i] > expected_lengths[i])
            a_number = True
        except:
            a_number = False

        ## We have now ascertained if it is a number, or a failed tracker.
        if not a_number:
            if actual_is_larger:
                difference = float(actual_lengths[i]) - float(expected_lengths[i])
                percentage = (difference / float(expected_lengths[i])) * 100

            if not actual_is_larger:
                difference = float(expected_lengths[i]) - float(actual_lengths[i])
                percentage = (difference / float(expected_lengths[i])) * 100

            else:
                ## Actual is exactly the same as the expected, therefore zero percentage error!
                percentage = 0

            ## Now we compare the percentages against the threshold:
            if percentage > thresh:
                ## This is bad, the percentage error is larger than we hoped.
                result = False

        else:
            ## This is if it's NOT a number:
            percentage = "N/N"

        ## Add this to the results
        percentage_results.append(percentage)
        ayes_nays.append(result)

    ## We now need to analyse ayes_nays and decide out verdict:
    ayes = 0
    nays = 0
    for i in ayes_nays:
        ## We only count it if the eye/nay actually is one!
        if i == True or i == False:
            ## if i is false:
            if not i:
                nays += 1
            ## Else if its True:
            else:
                ayes += 1

    # Verdict is whoever wins. I.e. if the ayes win, then it will return true to the dict.
    verdict = ayes > nays

    return {
        "percentages": percentage_results,
        "verdict": verdict,
        "ayes or nays": ayes_nays
    }


def filamentOut(actual, expected, thresh):
    return {
        "percentages": 0.0

    }
