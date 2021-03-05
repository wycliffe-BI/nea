## Brendan Ind 2020-2021 A-Level CS NEA
## Checker GUI File

import tkinter as tk
import sys
from PIL import ImageTk, Image

global ok


def close():
    sys.exit()


def success():
    global ok
    ok = True
    #print("Success, arrays are good.")


def fail():
    global ok
    ok = False
    print("We need to redo the arrays.")


def checking_page(array):
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

    ## Label to show the photo
    markers_img = ImageTk.PhotoImage(array)  ##Image.open(markers_path)
    markers = tk.Label(window, image=markers_img)
    markers.pack(side="top", fill="none", expand="yes")

    ## Main loop required for tkinter
    window.mainloop()

    return ok
