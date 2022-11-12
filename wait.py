from tkinter import *
def waithere():
    print ("waiting...")
    print("hello")
root = Tk()

print ("1")
root.after(7000,waithere)
print ("2")

root.mainloop()