##gui file

## Imports
# -------------------------------------#
from tkinter import *
from random import randint


# -------------------------------------#

def newUser():
    print("Creating a new user")


def c():
    print("Something clicked!")


def changeLabel(label, text):
    label.config(text=str(text))


def main_page():
    mainPage = Tk()
    mainPage.title("Overview")
    mainPage.geometry("800x800")

    testLabel = Label(mainPage, text="main page for all the overview stuff")

    return mainPage

def login_page():
    loginPage = Tk()
    loginPage.title("Login")
    loginPage.geometry("800x800")

    uname = StringVar()
    pword = StringVar()

    ## Setting up the buttons:

    testLabel = Label(loginPage, text=uname)
    testLabel.place(relx=0.5, rely=0.8, anchor=CENTER)

    UsernameInput = Entry(loginPage, relief=SUNKEN, textvariable=uname)
    PasswordInput = Entry(loginPage, relief=SUNKEN, textvariable=pword)
    createUserButton = Button(loginPage, relief=RIDGE, text="Create User", command=c, width=50)
    loginButton = Button(loginPage, text="Login", relief=RIDGE, command=changeLabel(testLabel, uname), width=50)

    ## Placing these Buttons and entry fields correctly
    loginButton.place(relx=0.5, rely=0.55, anchor=CENTER)
    UsernameInput.place(relx=0.5, rely=0.4, anchor=CENTER, width=500, height=30)
    PasswordInput.place(relx=0.5, rely=0.45, anchor=CENTER, width=500, height=30)
    createUserButton.place(relx=0.5, rely=0.6, anchor=CENTER)

    if randint(1, 2) == 1:
        noEntry = Label(loginPage, text="Bad username or password, please try again")
        noEntry.place(relx=0.5, rely=0.65, anchor=CENTER)
    else:
        ##Continues
        print("continue")

    return loginPage


loginPage = login_page()

## The Tkinter command that makes the mainloop and display happen. Must be last
loginPage.mainloop()
