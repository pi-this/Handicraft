import tkinter

from PIL import Image, ImageGrab

paint = tkinter.Tk()
paint.title('paint')
canvas = tkinter.Canvas(paint, width=1100, height=1000, bd=0, highlightthickness=0)
canvas.pack()



def capture():
    x0 = canvas.winfo_rootx()
    y0 = canvas.winfo_rooty()
    x1 = x0 + canvas.winfo_width()
    y1 = y0 + canvas.winfo_height()

    im = ImageGrab.grab((0, 0, 1915, 1000))
    im.save('mypic.png')

capture()
canvas.mainloop()
