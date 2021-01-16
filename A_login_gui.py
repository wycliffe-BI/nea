## Brendan Ind 2020-2021 A-Level CS NEA
## Login GUI file
import tkinter as tk
from random import randint


def c():
    print("Something clicked!")


def changeLabel(label, text):
    label.config(text=str(text))


def newUser():
    print("Creating a new user")


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
