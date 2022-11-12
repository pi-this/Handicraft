from tkinter import *


def enable_mouseposition():
    window.bind("<Button-1>", get_mouseposition)
    window.config(cursor="crosshair")


def get_mouseposition(event):
    print(event.x, event.y)
    window.unbind("<Button-1>")
    window.config(cursor="arrow")

window = Tk()
window.geometry("700x500")
window.title("Testing")

b = Button(window, text="OK", command=enable_mouseposition)
b.grid(row=0, column=2, sticky=W)


window.mainloop()