## Brendan Ind
## GUI File

## Imports
# -------------------------------------#
import tkinter as tk
from random import randint
from PIL import ImageTk, Image
import numpy as np
import sys
from functions import *
# -------------------------------------#

global ok

def newUser():
    print("Creating a new user")


def c():
    print("Something clicked!")


def close():
    sys.exit()


def changeLabel(label, text):
    label.config(text=str(text))


def success():
    global ok
    ok = True
    print("Success, arrays are good.")


def fail():
    global ok
    ok = False
    print("We need to redo the arrays.")


def login_page():
    window = tk.Tk()
    window.title("Login")
    window.geometry("800x800")

    uname = tk.StringVar()
    pword = tk.StringVar()

    ## Setting up the buttons:

    testLabel = tk.Label(window, text=uname)
    testLabel.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    UsernameInput = tk.Entry(window, relief=tk.SUNKEN, textvariable=uname)
    PasswordInput = tk.Entry(window, relief=tk.SUNKEN, textvariable=pword)
    createUserButton = tk.Button(window, relief=tk.RIDGE, text="Create User", command=c, width=50)
    loginButton = tk.Button(window, text="Login", relief=tk.RIDGE, command=changeLabel(testLabel, uname), width=50)

    ## Placing these Buttons and entry fields correctly
    loginButton.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
    UsernameInput.place(relx=0.5, rely=0.4, anchor=tk.CENTER, width=500, height=30)
    PasswordInput.place(relx=0.5, rely=0.45, anchor=tk.CENTER, width=500, height=30)
    createUserButton.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    if randint(1, 2) == 1:
        noEntry = tk.Label(window, text="Bad username or password, please try again")
        noEntry.place(relx=0.5, rely=0.65, anchor=tk.CENTER)
    else:
        ## Continues
        print("continue")

    return window


def main_page():
    mainPage = tk.Tk()
    mainPage.title("Overview")
    mainPage.geometry("800x800")


def checking_page(markers, filament):
    global ok
    ok = 3

    window = tk.Tk()
    window.attributes('-fullscreen', True)
    window.title("Confirmation")
    window.geometry("800x800")
    window.configure(background='grey')

    ## EXIT BUTTON
    exit_btn = tk.Button(window, text="X", relief=tk.RIDGE, command=window.destroy, width=50)
    exit_btn.pack(side="top", fill="y")

    ## OK BUTTON
    ok_btn = tk.Button(window, text="ok", relief=tk.RIDGE, command=lambda: [success(), window.destroy()], width=50)
    ok_btn.pack(side="bottom", fill="y")

    ## REDO BUTTON
    redo_btn = tk.Button(window, text="redo", relief=tk.RIDGE, command=lambda: [fail(), window.destroy()], width=50)
    redo_btn.pack(side="bottom", fill="y")

    ## MARKERS LABEL
    markers_path = "img/ender.jpg"
    markers_img = ImageTk.PhotoImage(markers)  ##Image.open(markers_path)
    markers = tk.Label(window, image=markers_img)
    markers.pack(side="left", fill="none", expand="yes")

    ## FILAMENT LABEL
    filament_path = "img/ender.jpg"
    filament_img = ImageTk.PhotoImage(filament) ##Image.open(filament_path)
    filament = tk.Label(window, image=filament_img)
    filament.pack(side="right", fill="none", expand="yes")


    ## MAINLOOP
    window.mainloop()

    return ok