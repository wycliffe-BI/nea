from bottle import route, run

## @route will basically make a new 'instance' of the function with the extra stuff we need to run the code with.
@route("/hello")
def page1function():
    return "Hello World!"

## @route will relate to the next function below it, and we don't have to name them the same thing:
@route("/page2")
def page2function():
    return "lol lmao"


## This starts the whole process and starts the server, etc..
run(host = "localhost", port = 8080)