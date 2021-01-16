## Brendan Ind 2020

def import_arrays():
    ## Import the arrays that we had from the previous code:
    with open("markers.txt", "r") as file:
        markers = file.read()
        print(markers)
    with open("filament.txt", "r") as file:
        filament = file.read()
        print(filament)
    return markers, filament

markers, filament = import_arrays()

#markers = format_array(markers)
#filament = format_array(filament)


#plt.imshow(markers), plt.show()
#plt.imshow(filament), plt.show()

def select_if_correct(markers, filament):
    pass