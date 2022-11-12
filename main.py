"""
New:
undo
color choose button
pen button
paint button
size button
pixel button
fill all button
clear button
new button
fullscreen
screenshot
toutch button
select where to put the image
cursor icons for eatch tool
"""
from webbrowser import open as link
from time import sleep as wait
from tkinter import *
from PIL import Image,ImageDraw,ImageDraw2
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.colorchooser import askcolor as ASK
from random import randrange as From
class ImageGenerator:
    
    def __init__(self,parent,posx,posy,*kwargs):
         
        root.attributes('-fullscreen', False)  
        self.fullScreenState = False
        root.bind("<F1>", lambda x: self.toggleFullScreen())
        root.bind("<F2>", lambda x: self.capture())
        self.parent = parent
        self.posx = posx
        self.posy = posy
        self.sizex = 2000
        self.sizey = 1000
        self.b1 = "up"
        self.w = Canvas(self.parent,width=self.sizex,height=self.sizey)
        self.w.pack(expand = True, fill = BOTH)
        self.w.place(x=self.posx,y=self.posy)
        root.rowconfigure(0, minsize=80, weight=1)
        root.columnconfigure(0, minsize=80, weight=1)

        self.openButtonImages()

        self.fr_buttons = tk.Frame(root, relief=tk.RAISED, bd=2)
        fillall_button = tk.Button(self.fr_buttons, image=self.Y, command=self.fill_all)
        fillall_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        btn_pixel = tk.Button(self.fr_buttons, image=self.W, command=self.pixel)
        btn_pencil = tk.Button(self.fr_buttons, image=self.I, command=self.pencil)
        btn_toutch = tk.Button(self.fr_buttons, image=self.Mouse, command=self.toutch)
        btn_toutch.grid(row=0, column=0, sticky="ew", padx=5)
        btn_paintbrush = tk.Button(self.fr_buttons, image=self.T, command=self.paintbrush)
        btn_pixel.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        btn_pencil.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        btn_paintbrush.grid(row=0, column=4, sticky="ew", padx=5)
        

        self.choose_size_button = Scale(self.fr_buttons, from_=1, to=300, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=6, sticky="ew", padx=5, pady=5)
        
        self.color_button = Button(self.fr_buttons, image=self.C, command=self.choose_color)
        self.color_button.grid(row=0, column=5)
        self.color = 'black'
        
        self.fr_buttons.grid(row=1, column=0, sticky="ns")
        self.w.bind("<Motion>", self.motion)
        self.w.bind("<ButtonPress-1>", self.b1down)
        self.w.bind("<ButtonRelease-1>", self.b1up)
        self.w.bind("<Enter>", lambda x: self.introExit())
        root.bind("<Control-Shift-S>", lambda x: self.saveAs_file())
        root.bind("<Control-c>", lambda x: self.clear())
        root.bind("<Control-s>", lambda x: self.save())
        root.bind("<Control-n>", lambda x: self.new())
        root.bind("<Escape>", lambda x: self.Quit())
        root.bind("<Control-o>", lambda x: self.open_file())
        root.bind("<Control-Shift-O>", lambda x: self.openAs_file())
        root.bind("<Control-z>", lambda x: self.undo())
        root.bind("<s>", lambda x: self.opensticker())
        self.menubar = Menu(root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="screenshot    F2", command=self.capture)
        self.filemenu.add_command(label="placeimage    S", command=self.opensticker)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="New    CTRL+N", command=self.new)
        self.filemenu.add_command(label="clear    CTRL+C", command=self.new)
        self.filemenu.add_command(label="Open    CTRL+O", command=self.open_file)
        self.filemenu.add_command(label="Open as...    CTRL+SHIFT+O", command=self.openAs_file)
        self.filemenu.add_command(label="Save    CTRL+S", command=self.save)
        self.filemenu.add_command(label="Save as...    CTRL+SHIFT+S", command=self.saveAs_file)
        self.destroy = False
        self.filemenu.add_separator()
        
        self.filemenu.add_command(label="Exit    ESC", command=self.Quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        
        self.editmenu = Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="undo    CTRL+Z", command=self.undo)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        root.config(menu=self.menubar)
        
        self.fullcolor = 'white'
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Handicraft Home Page", command=self.homepage)
        root.config(menu=self.menubar)
        
        self.viewmenu = Menu(self.menubar, tearoff=0)
        self.viewmenu.add_command(label="Full screen    F1", command=self.toggleFullScreen)
        self.menubar.add_cascade(label="View", menu=self.viewmenu)
        root.config(menu=self.menubar)
        
        self.toolsmenu = Menu(self.menubar, tearoff=0)
        self.toolsmenu.add_command(label="paint brush", command=self.paintbrush)
        self.toolsmenu.add_command(label="pencil", command=self.pencil)
        self.toolsmenu.add_command(label="pixel", command=self.pixel)
        
        self.toolsmenu.add_command(label="fill all", command=self.fill_all)
        self.toolsmenu.add_command(label="choose color", command=self.choose_color)
        self.toolsmenu.add_command(label="toutch", command=self.toutch)
        
        self.menubar.add_cascade(label="Tools", menu=self.toolsmenu)
        root.config(menu=self.menubar)
        
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        root.config(menu=self.menubar)
        
        self.line_width = self.choose_size_button.get()
        self.toolsmenu.bind("<Enter>", self.arrow)
        
        self.image=Image.new("RGB",(self.sizex,self.sizey),(self.fullcolor))
        self.draw=ImageDraw.Draw(self.image)
        
        self.openINTROimage()
        self.stack = []
        self.tool_option = 'toutch'
        
    def openImagesticker(self):
        root.bind("<Button-1>", self.get_mouseposition)
        root.config(cursor="crosshair")
        
    def pencil(self):
        root.config(cursor="pencil")
    def arrow(self):
        root.config(cursor="left_ptr")
    def get_mouseposition(self,event):
        self.cy = event.y
        self.cx = event.x
        root.unbind("<Button-1>")
        root.config(cursor="arrow")
        self.stickerOpenC()
    def undo(self):
        try:
            
            self.x = self.stack.pop()
            self.w.delete(self.x)
        except:
            pass
    def capture(self):
        x0 = self.w.winfo_rootx()
        y0 = self.w.winfo_rooty()
        x1 = x0 + self.w.winfo_width()
        y1 = y0 + self.w.winfo_height()
        
        saveCapture = asksaveasfilename(title="Save File", filetypes=[("png files", "*.png")]
        )
        if not saveCapture:
            return
        
        wait(1)
        im = ImageGrab.grab((0, 0, 1915, 1000))
        im.save(saveCapture)
    def toggleFullScreen(self):
        self.fullScreenState = not self.fullScreenState
        root.attributes("-fullscreen", self.fullScreenState)
    def fill_all(self):
         self.w.configure(bg=self.color)
         self.fullcolor = self.color
         self.image=Image.new("RGB",(self.sizex,self.sizey),(self.fullcolor))
         self.draw=ImageDraw.Draw(self.image)
    def toutch(self):
        self.tool_option = 'toutch'
        root.config(cursor="left_ptr")
    def choose_color(self):
        self.color = ASK(color=self.color)[1]
    def paintbrush(self):
        self.tool_option = 'paintbrush'
        root.config(cursor="spraycan")
    def pencil(self):
        self.tool_option = 'pencil'
        root.config(cursor="pencil")
    def pixel(self):
        self.tool_option = 'pixel'
        root.config(cursor="dot")
    def new(self):
        self.fullcolor = 'white'
        self.image=Image.new("RGB",(self.sizex,self.sizey),(self.fullcolor))
        self.draw=ImageDraw.Draw(self.image)
        self.w.delete("all")
        root.config(cursor="left_ptr") 
        self.w.configure(bg='white')
        self.color = 'black'
        self.filepathopen = False
        self.tool_option = 'toutch'
        self.choose_size_button = Scale(self.fr_buttons, from_=1, to=300, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=6, sticky="ew", padx=5, pady=5)
    def clear(self):
        self.w.delete("all")
        self.w.configure(bg='white')
        self.fullcolor = 'white'
        self.image=Image.new("RGB",(self.sizex,self.sizey),(self.fullcolor))
        self.draw=ImageDraw.Draw(self.image)
    def b1down(self,event):
            
        self.line_width = self.choose_size_button.get()
        self.b1 = "down"
        if self.tool_option == "paintbrush":
            self.x = event.widget.create_oval(self.xold,self.yold,event.x,event.y,width=self.line_width,outline=self.color,fill=self.color)
            self.draw.ellipse((self.xold,self.yold,event.x+self.line_width,event.y+self.line_width), fill=self.color, outline=self.color)
            self.stack.append(self.x)
        elif self.tool_option == "pencil":
            self.x = event.widget.create_line(self.xold,self.yold,event.x,event.y,width=self.line_width,fill=self.color)
            self.draw.line(((self.xold,self.yold),(event.x,event.y)),(self.color),width=self.line_width)
            self.stack.append(self.x)
        elif self.tool_option == "pixel":
            self.x = event.widget.create_rectangle(self.xold,self.yold,event.x,event.y,outline=self.color,fill=self.color,width=self.line_width)
            self.draw.rectangle(((self.xold,self.yold),(event.x+self.line_width,event.y+self.line_width)),(self.color))
            self.stack.append(self.x)
        
    def introExit(self):
        if self.destroy == False:
            self.clear()
            self.destroy = True
            
    def b1up(self,event):
        self.b1 = "up"
        self.xold = None
        self.yold = None
    def motion(self,event):
        self.line_width = self.choose_size_button.get()
        if self.b1 == "down":
            if self.tool_option == 'paintbrush':
                
                if self.xold is not None and self.yold is not None:
                    
                    self.x = event.widget.create_oval(self.xold,self.yold,event.x,event.y,width=self.line_width,outline=self.color,fill=self.color)
                    self.draw.ellipse((self.xold,self.yold,event.x+self.line_width,event.y+self.line_width), fill=self.color, outline=self.color)
                    self.stack.append(self.x)
            elif self.tool_option == 'pencil':
                if self.xold is not None and self.yold is not None:
                    
                    self.x = event.widget.create_line(self.xold,self.yold,event.x,event.y,width=self.line_width,fill=self.color)
                    self.draw.line(((self.xold,self.yold),(event.x,event.y)),(self.color),width=self.line_width)
                    self.stack.append(self.x)
            elif self.tool_option == 'pixel':
                
                if self.xold is not None and self.yold is not None:
                    
                    self.x = event.widget.create_rectangle(self.xold,self.yold,event.x,event.y,outline=self.color,fill=self.color,width=self.line_width)
                    self.draw.rectangle((self.xold,self.yold,event.x+self.line_width,event.y+self.line_width), fill=self.color, outline=self.color)
                    self.stack.append(self.x)
        self.xold = event.x
        self.yold = event.y
    def homepage(self):
        link("https://pi-this.github.io/handicraft.html")
    def Quit(self):
        root.destroy()
    
    def opensticker(self):
    
        self.filepathopensticker = askopenfilename(title="Open File", filetypes=[("png files", "*.png")]
        )
        if not self.filepathopensticker:
            return
        
        
        self.openImagesticker()
        
    def stickerOpenC(self):
        self.IMAGEopen=tk.PhotoImage(file=self.filepathopensticker)
        self.Sticker = self.w.create_image(self.cx, self.cy, anchor=tk.NW, image=self.IMAGEopen)
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
            self.openAs_file()
    def saveAs_file(self):
        filepathsave = asksaveasfilename(title="Save File", filetypes=[("png files", "*.png")]
        )
        if not filepathsave:
            return
        self.image.save(filepathsave)
        self.filename = filepathsave
        Rnumber = From(1000,5000)
        root.config(cursor="watch")
        self.tool_option = 'toutch'
        root.after(Rnumber,self.change)
    def change(self):
        if self.tool_option == 'pixel':
            self.pixel()
        if self.tool_option == 'paintbrush':
            self.paintbrush()
        if self.tool_option == 'pencil':
            self.pencil()
        if self.tool_option == 'toutch':
            self.toutch()
    def save(self):
        try:
            self.image.save(self.filename)
            Rnumber = From(1000,5000)
            root.config(cursor="watch")
            self.tool_option = 'toutch'
            root.after(Rnumber,self.change)
        except:
            self.saveAs_file()
    def openINTROimage(self):
        self.IMAGEopenINTRO=tk.PhotoImage(file='Base_images/intro.png')
        self.MYimageINTRO = self.w.create_image(0, 0, anchor=tk.NW, image=self.IMAGEopenINTRO)
    def openButtonImages(self):
        
        self.I=tk.PhotoImage(file='Base_images/draw.png')
        self.M = self.w.create_image(0, 0, anchor=tk.NW, image=self.I)
        
        self.W=tk.PhotoImage(file='Base_images/pixel.png')
        self.K = self.w.create_image(0, 0, anchor=tk.NW, image=self.W)
        
        self.T=tk.PhotoImage(file='Base_images/paint.png')
        self.B = self.w.create_image(0, 0, anchor=tk.NW, image=self.T)
        
        self.C=tk.PhotoImage(file='Base_images/color.png')
        self.A = self.w.create_image(0, 0, anchor=tk.NW, image=self.C)
        
        self.Y=tk.PhotoImage(file='Base_images/fill_all.png')
        self.Z = self.w.create_image(0, 0, anchor=tk.NW, image=self.Y)
        
        self.Mouse=tk.PhotoImage(file='Base_images/mouse.png')
        self.esuoM = self.w.create_image(0, 0, anchor=tk.NW, image=self.Y)

                                
root=Tk()
root.wm_geometry("%dx%d+%d+%d" % (500, 550, 500, 100))
root.config(bg='white')
root.title( "Handicraft" )
ImageGenerator(root,0,0)
root.mainloop()
