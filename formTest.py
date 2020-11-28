from bottle import Bottle, template, request, run, route

## This control the root directory of the address, e.g. localhost/
@route('/')
def index():
    """Home Page"""
    ## Put the HTML you want to return down here

    ## Template takes html files and lays them out to be POST'ed to the client
    ## "message" arg refers to the html page element that will display that line
    return template("formTest.html", message = "Please enter your name")



## This is the code to RECEIVE the POST from the client when they send some information back
@route('/', method="POST")
def formHandler(): ## This is what is run when server receives POST since its after the @route
    """Handle the form submission"""

    first = request.forms.get('first')
    last = request.forms.get('last')

    message = "Hello " + first + " " + last + "."
    return template("formTest.html", message=message)

run(host='localhost', port = 8080)
