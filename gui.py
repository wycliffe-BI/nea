##gui file

from tkinter import *

app = Tk()

app.title("Login")

app.geometry("800x800")

def c():
    print("Clicked!")

l = Button(app, text="Text of the button", command=c)

l.pack()

app.mainloop()

