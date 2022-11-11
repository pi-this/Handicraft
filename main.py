from webbrowser import open as link
from tkinter import *
from PIL import Image,ImageDraw
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
class ImageGenerator:
    
    def __init__(self,parent,posx,posy,*kwargs):
        self.parent = parent
        self.posx = posx
        self.posy = posy
        self.sizex = 2000
        self.sizey = 1000
        self.b1 = "up"
        self.w = Canvas(self.parent,width=self.sizex,height=self.sizey)
        self.w.pack(expand = 1, fill = BOTH)
        self.w.place(x=self.posx,y=self.posy)
        self.w.bind("<Motion>", self.motion)
        self.w.bind("<ButtonPress-1>", self.b1down)
        self.w.bind("<Enter>", lambda x: self.introExit())
        self.w.bind("<ButtonRelease-1>", self.b1up)
        root.bind("<Control-Shift-S>", lambda x: self.saveAs_file())
        root.bind("<Control-s>", lambda x: self.save())
        root.bind("<Control-n>", lambda x: self.clear())
        root.bind("<Escape>", lambda x: self.Quit())
        root.bind("<Control-Shift-O>", lambda x: self.open_file())
        root.bind("<Control-o>", lambda x: self.openRecent_file())
        self.menubar = Menu(root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New    CTRL+N", command=self.clear)
        self.filemenu.add_command(label="Open    CTRL+O", command=self.open_file)
        self.filemenu.add_command(label="Open as...    CTRL+SHIFT+O", command=self.openAs_file)
        self.filemenu.add_command(label="Save    CTRL+S", command=self.save)
        self.filemenu.add_command(label="Save as...    CTRL+SHIFT+S", command=self.saveAs_file)
        self.destroy = False
        self.filemenu.add_separator()

        self.filemenu.add_command(label="Exit    ESC", command=self.Quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.editmenu = Menu(self.menubar, tearoff=0)

        self.editmenu.add_separator()

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Home Page", command=self.homepage)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        root.config(menu=self.menubar)
        
        self.image=Image.new("RGB",(self.sizex,self.sizey),(255,255,255))
        self.draw=ImageDraw.Draw(self.image)
        
        self.openINTROimage()
    def clear(self):
        self.w.delete("all")
        self.image=Image.new("RGB",(self.sizex,self.sizey),(255,255,255))
        self.draw=ImageDraw.Draw(self.image)
    def b1down(self,event):
        self.b1 = "down"
        event.widget.create_oval(self.xold,self.yold,event.x,event.y,width=3,fill='black')
    def introExit(self):
        if self.destroy == False:
            self.clear()
            self.destroy = True
            
    def b1up(self,event):
        self.b1 = "up"
        self.xold = None
        self.yold = None
    def motion(self,event):
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                event.widget.create_line(self.xold,self.yold,event.x,event.y,smooth='true',width=3,fill='black')
                self.draw.line(((self.xold,self.yold),(event.x,event.y)),(0,0,0),width=3)

        self.xold = event.x
        self.yold = event.y
    def homepage(self):
        link("https://pi-this.github.io/handicraft.html")
    def Quit(self):
        root.destroy()
     
    def openAs_file(self):
    
        filepathopen = askopenfilename(title="Open File", filetypes=[("png files", "*.png")]
        )
        if not filepathopen:
            return
        self.IMAGEopen=tk.PhotoImage(file=filepathopen)
        self.MYimage = self.w.create_image(0, 0, anchor=tk.NW, image=self.IMAGEopen)
        self.filepathopen = filepathopen
    def open_file(self):
        try:
            self.IMAGEopen=tk.PhotoImage(file=self.filepathopen)
            self.MYimage = self.w.create_image(0, 0, anchor=tk.NW, image=self.IMAGEopen)
        except:
            self.open_file()
    def saveAs_file(self):
        filepathsave = asksaveasfilename(title="Save File", filetypes=[("png files", "*.png")]
        )
        if not filepathsave:
            return
        self.image.save(filepathsave)
        self.filename = filepath
    def save(self):
        try:
            self.image.save(self.filename)
        except:
            self.saveAs_file()
    def openINTROimage(self):
        self.IMAGEopenINTRO=tk.PhotoImage(file='Base_images/intro.png')
        self.MYimageINTRO = self.w.create_image(0, 0, anchor=tk.NW, image=self.IMAGEopenINTRO)
                                
root=Tk()
root.wm_geometry("%dx%d+%d+%d" % (500, 500, 500, 100))
root.config(bg='white')
root.title( "Handicraft" )
ImageGenerator(root,0,0)
root.mainloop()