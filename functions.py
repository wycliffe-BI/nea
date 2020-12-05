import cv2
from sklearn.feature_extraction import image
from sklearn.cluster import spectral_clustering
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from PIL import Image
import math
import time
import datetime
import skimage.util as skimage

def PILconvert(array):
    ## Converting images from the np format (bool and 3 channels for RGB)
    ## To PIL compatible images with 0-255

    return Image.fromarray((array * 255).astype(np.uint8))

def img_to_uint8(array):
    return skimage.img_as_ubyte(array)


def information(array):
    if str(type(array)) == "<class 'PIL.Image.Image'>":
        TYPE = "PILLOW IMAGE"
        ## It is a PIL image
        size = str(array.size)
        tpe = "PIL array <class 'PIL.Image.Image'>"
        data = array.getdata()
    else:
        TYPE = "NUMPY IMAGE"
        ## It is a numpy image
        size = str(len(array)) + " " + str(len(array[0])) + " " + str(len(array[0][0]))
        tpe = array.dtype
        data = "none"
        print(array.shape)

    print("----------------------")
    print('''
    Information about this array:
    
    %s
    
    Size:       %s
    Datatype:   %s
    type(ary):  %s
    Adtl Data:  %s
    
    '''%(TYPE, size, tpe, str(type(array)), data))
    print("----------------------")


def format_array(array, dtype="int8"):
    numpy_array = np.array(array, dtype=dtype)
    print("array returned in format %s" % (numpy_array.dtype))

    return numpy_array


def red(val):
    print("Changed Red to: ", val)


def green(val):
    print("Changed Green to: ", val)


def blue(val):
    print("Changed Blue to: ", val)


def createTrackbars(window):
    cv2.createTrackbar("Red", window, 0, 255, red)
    cv2.createTrackbar("Green", window, 0, 255, green)
    cv2.createTrackbar("Blue", window, 0, 255, blue)


def updateTrackbarValues():
    redVal = cv2.getTrackbarPos("Red", "main")
    greenVal = cv2.getTrackbarPos("Green", "main")
    blueVal = cv2.getTrackbarPos("Blue", "main")
    return redVal, greenVal, blueVal


def removeNoise(array):
    """
    :rtype: object
    """

    array = Image.fromarray(convert_to_uint(array))
    eroded = ndimage.binary_erosion(array)
    reconstruction = ndimage.binary_propagation(eroded, mask=array)

    ##Output to the console:
    plt.title("Removed Noise:"), plt.imshow(reconstruction)

    return reconstruction


def whiteimg(size=[512, 512, 3]):
    """

    :param size: size: By default the size is [512, 512, 3] meaning 512x512 image with colour density of 3 pixels.
    :return: canvas, the white nparray
    """

    ##Make completely back canvas with np.zeros[]
    canvas = np.zeros(size)
    height = len(canvas)
    width = len(canvas[0])

    ## Scan thorough each y and x pixel and change them to white
    for y in range(height):
        for x in range(width):
            ## Replace them all with white pixels
            canvas[y, x] = [255, 255, 255]

    ##Output to the console:
    plt.title("White:"), plt.imshow(canvas), plt.show()

    return canvas


def blackimg(size=[512, 512, 3]):
    """
    :param size: By default the size is [512, 512, 3] meaning 512x512 image with colour density of 3 pixels.
    :return: canvas, the black nparray.
    """
    canvas = np.zeros(size)

    ##Output to the console:
    plt.title("Black:"), plt.imshow(canvas), plt.show()

    return canvas


def returnpixels(array):
    for i in array:
        for j in i:
            ## Will return the individual rgb values of a pixel, one at a time.
            yield j


def convert_to_uint(array):
    ## TODO Learning opportunity of data types
    return (array * 255).astype(np.uint8)


def monochrome(array):
    ## Convert into something pillow can understand:
    ## numpy and others use rgb trio array with Trues and falses
    ## to represent colour, whereas PIL wants it as uint8 i.e. val out of 255
    ## TODO LEarning opepertunity: converting between uint and True/False, so i made a funciton to do it for me
    array = np.asarray(convert_to_uint(array))

    ## Pillow does its magic:
    img = Image.fromarray(array)
    mono = img.convert('1')  # convert image to black and white

    ##Output to the console:
    plt.title("Monochrome:"), plt.imshow(mono), plt.show()
    return mono


def findDistance(pointA, pointB):
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


def contain_colour(array, colour=[255, 255, 255]):
    mask = np.all(array == colour, axis=-1)

    # This gives us the values of the mask which arent zero, i.e. the ones that contain the colour we want.
    output = mask.nonzero()

    output = format_array(output)

    ##Output to the console:
    plt.title("Colour Mask:"), plt.imshow(output), plt.show()

    return output


def erosionExample():
    square = np.zeros((32, 32))
    square[10:-10, 10:-10] = 1
    np.random.seed(2)
    x, y = (32 * np.random.random((2, 20))).astype(np.int)
    square[x, y] = 1

    open_square = ndimage.binary_opening(square)

    eroded_square = ndimage.binary_erosion(square)
    reconstruction = ndimage.binary_propagation(eroded_square, mask=square)

    plt.figure(figsize=(9.5, 3))
    plt.subplot(131)
    plt.imshow(square, cmap=plt.cm.gray, interpolation='nearest')
    plt.axis('off')
    plt.subplot(132)
    plt.imshow(open_square, cmap=plt.cm.gray, interpolation='nearest')
    plt.axis('off')
    plt.subplot(133)
    plt.imshow(reconstruction, cmap=plt.cm.gray, interpolation='nearest')
    plt.axis('off')

    plt.subplots_adjust(wspace=0, hspace=0.02, top=0.99, bottom=0.01, left=0.01, right=0.99)
    plt.show()


def current_time():
    return str(datetime.datetime.now())
