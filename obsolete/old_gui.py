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
    filament_img = ImageTk.PhotoImage(filament)  ##Image.open(filament_path)
    filament = tk.Label(window, image=filament_img)
    filament.pack(side="right", fill="none", expand="yes")

    ## MAINLOOP
    window.mainloop()

    return ok