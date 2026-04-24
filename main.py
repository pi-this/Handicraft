from webbrowser import open as link
from time import sleep as wait
from tkinter import *
from PIL import Image, ImageDraw, ImageDraw2, ImageGrab, ImageTk, ImageColor
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.colorchooser import askcolor as ASK
from random import randrange as From
import pickle

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
        self.w = Canvas(self.parent,width=self.sizex,height=self.sizey, highlightthickness=0, bd=0)
        self.w.pack(expand = True, fill = BOTH)
        self.w.place(x=self.posx,y=self.posy)
        root.rowconfigure(0, minsize=80, weight=1)
        root.columnconfigure(0, minsize=80, weight=1)
        


        self.openButtonImages()

        self.fr_buttons = tk.Frame(root, relief=tk.RAISED, bd=2, bg="white")
        fillall_button = tk.Button(self.fr_buttons, image=self.Y, command=self.fill_tool)
        fillall_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        btn_pixel = tk.Button(self.fr_buttons, image=self.O, command=self.pixel)
        btn_pencil = tk.Button(self.fr_buttons, image=self.I, command=self.pencil)
        btn_touch = tk.Button(self.fr_buttons, image=self.mouse, command=self.touch)
        btn_touch.grid(row=0, column=0, sticky="ew", padx=5)
        btn_paintbrush = tk.Button(self.fr_buttons, image=self.T, command=self.paintbrush)
        btn_pixel.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        btn_pencil.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        btn_paintbrush.grid(row=0, column=4, sticky="ew", padx=5)
        
        img_pick = Image.open('Base_images/pick.png')
        new_size_pick = img_pick.resize((35,35))
        self.p = ImageTk.PhotoImage(new_size_pick)

        # Use self.p here instead of self.pz
        picker_button = tk.Button(self.fr_buttons, image=self.p, command=self.activate_eyedropper)
        picker_button.grid(row=0, column=5, sticky="ew", padx=5, pady=5)

        # Keep this only if you ALSO need the image to appear on a canvas
        self.pz = self.w.create_image(0, 0, anchor=tk.NW, image=self.p)

        self.choose_size_button = Scale(self.fr_buttons, from_=1, to=300, orient=HORIZONTAL, bg="white")
        self.choose_size_button.grid(row=0, column=7, sticky="ew", padx=5, pady=5)
        
        self.color_button = Button(self.fr_buttons, image=self.C, command=self.choose_color)
        self.color_button.grid(row=0, column=6)
        self.color = 'black'
        
        root.bind_all("I", lambda x: self.activate_eyedropper())
        root.bind_all("Y", lambda x: self.pixel())
        root.bind_all("N", lambda x: self.pencil())
        root.bind_all("B", lambda x: self.paintbrush())
        root.bind_all("F", lambda x: self.fill_tool())
        
        root.bind("<Control-E>", lambda x: self.saveAs_file()) # Export
        root.bind("<Control-I>", lambda x: self.openAs_file()) # Import
        

        
        self.fr_buttons.grid(row=1, column=0, sticky="ns")
        self.w.bind("<Motion>", self.motion)
        self.w.bind("<ButtonPress-1>", self.b1down)
        self.w.bind("<ButtonRelease-1>", self.b1up)
        self.w.bind("<Enter>", lambda x: self.introExit())
        #root.bind("<Control-Shift-S>", lambda x: self.saveAs_file())
        root.bind("<Control-c>", lambda x: self.clear())
        root.bind("<Control-s>", lambda x: self.save_project())
        root.bind("<Control-n>", lambda x: self.new())
        root.bind("<Escape>", lambda x: self.Quit())
        #root.bind("<Control-o>", lambda x: self.load_project())
        #root.bind("<Control-Shift-O>", lambda x: self.openAs_file())
        root.bind("<Control-z>", lambda x: self.undo())
        root.bind("<Control-y>", lambda x: self.redo())
        #root.bind("<s>", lambda x: self.opensticker())
        self.menubar = Menu(root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        #self.filemenu.add_command(label="screenshot    F2", command=self.capture)
        #self.filemenu.add_command(label="placeimage    S", command=self.opensticker)
        #self.filemenu.add_separator()
        
        
        self.filemenu.add_command(
            label="New",
            accelerator="CTRL+N",
            command=self.new
        )
        #self.filemenu.add_command(label="Open    CTRL+O", command=self.open_file)
        
        self.filemenu.add_command(label="Save (.hcraft)", accelerator="CTRL+S", command=self.save_project)
        self.filemenu.add_command(label="Open (.hcraft)", accelerator="CTRL+O", command=self.load_project)
        
        self.recent_files = [] # Stores file paths
        self.recent_menu = Menu(self.filemenu, tearoff=0)
        self.filemenu.add_cascade(label="Open Recent", menu=self.recent_menu)
   
   
        self.filemenu.add_command(label="Import (.png)", accelerator="CTRL+I", command=self.openAs_file)
        self.filemenu.add_command(label="Export (.png)", accelerator="CTRL+E", command=self.saveAs_file)
        
        
        
        
        
        
        #self.filemenu.add_command(label="Save Project (.hcraft)", command=self.save_project)
        #self.filemenu.add_command(label="Open Project (.hcraft)", command=self.load_project)

        #self.filemenu.add_separator()
        
        #self.filemenu.add_command(label="Open as...    CTRL+SHIFT+O", command=self.openAs_file)
        #self.filemenu.add_command(label="Save    CTRL+S", command=self.save)
        #self.filemenu.add_command(label="Save as...    CTRL+SHIFT+S", command=self.saveAs_file)
        self.destroy = False
        self.filemenu.add_separator()
        
        self.filemenu.add_command(label="Exit", accelerator="ESC", command=self.Quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        
        self.editmenu = Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="clear", accelerator="CTRL+C", command=self.new)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="undo", accelerator="CTRL+Z", command=self.undo)
        self.editmenu.add_command(label="redo", accelerator="CTRL+Y", command=self.redo)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        root.config(menu=self.menubar)
        
        self.fullcolor = 'white'
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Handicraft Home Page", command=self.homepage)
        root.config(menu=self.menubar)
        
        self.viewmenu = Menu(self.menubar, tearoff=0)
        self.viewmenu.add_command(label="Full screen", accelerator="F1", command=self.toggleFullScreen)
        self.menubar.add_cascade(label="View", menu=self.viewmenu)
        root.config(menu=self.menubar)
        
        self.toolsmenu = Menu(self.menubar, tearoff=0)
        self.toolsmenu.add_command(label="paint brush", accelerator="B", command=self.paintbrush)
        self.toolsmenu.add_command(label="pencil", accelerator="N", command=self.pencil)
        self.toolsmenu.add_command(label="pixel", accelerator="Y", command=self.pixel)
        
        
        self.toolsmenu.add_command(label="fill", accelerator="F", command=self.fill_tool)
        self.toolsmenu.add_command(label="choose color", accelerator="C", command=self.choose_color)
        self.toolsmenu.add_command(label="touch", accelerator="V", command=self.touch)
        self.toolsmenu.add_command(label="color picker", accelerator="I", command=self.eyedropper)
        
        self.menubar.add_cascade(label="Tools", menu=self.toolsmenu)
        root.config(menu=self.menubar)
        
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        root.config(menu=self.menubar)
        
        self.choose_size_button.set(5) 
        self.line_width = self.choose_size_button.get()
        
        self.toolsmenu.bind("<Enter>", self.arrow)
        
        self.image=Image.new("RGB",(self.sizex,self.sizey),(self.fullcolor))
        self.draw=ImageDraw.Draw(self.image)
        
        self.openINTROimage()
        self.tool_option = 'pencil'
        self.pencil()
        
        
        self.stack = []       # Undo history
        self.redo_stack = []  # NEW: Redo history

        
    def openImagesticker(self):
        root.bind("<Button-1>", self.get_mouseposition)
        root.config(cursor="crosshair")
        
    def activate_eyedropper(self):
        self.tool_option = "eyedropper"
        root.config(cursor="target") # Use a built-in or custom cursor
        
    def fill_tool(self):
        print("fill")
        self.tool_option = 'fill'
        root.config(cursor="plus") # Or use a custom bucket icon

    def apply_fill(self, event):
        # 1. Coordinate Safety: Ensure the click is within image boundaries
        # event.x and event.y can sometimes be slightly outside if the user clicks the edge
        x = min(max(event.x, 0), self.sizex - 1)
        y = min(max(event.y, 0), self.sizey - 1)
        seed_point = (x, y)

        # 2. Color Conversion: Convert your string color (e.g., 'black' or '#000000') 
        # into an RGB tuple (e.g., (0, 0, 0)) that Pillow's math can understand.
        try:
            from PIL import ImageColor
            rgb_color = ImageColor.getrgb(self.color)
        except:
            rgb_color = (0, 0, 0) # Fallback to black if conversion fails

        # 3. Perform the Flood Fill on the background PIL image
        # thresh=10 allows for slight "fuzziness" to fill near edges
        ImageDraw.floodfill(self.image, seed_point, rgb_color, thresh=10)

        # 4. Update the Canvas: To show the fill, we must display the background image
        # We save a reference to prevent the image from being deleted by memory cleanup
        self.IMAGE_snapshot = ImageTk.PhotoImage(self.image)
        self.w.create_image(0, 0, anchor=tk.NW, image=self.IMAGE_snapshot)

        # 5. History for Undo: We save the state of the image
        # This tells the undo function that a 'fill' happened
        # In apply_fill:
        # Inside apply_fill:
        self.stack.append(([], [{'type': 'fill', 'image': self.image.copy()}]))


        
        print(f"Filled area at {seed_point} with {self.color}")

    def eyedropper(self, event):
        # 1. Ensure coordinates are within image boundaries
        x = min(max(event.x, 0), self.sizex - 1)
        y = min(max(event.y, 0), self.sizey - 1)
        
        # 2. Get the RGB tuple from the background PIL image
        rgb = self.image.getpixel((x, y))
        
        # 3. Convert the (R, G, B) tuple to a Hex string (e.g., "#ffffff")
        self.color = '#%02x%02x%02x' % rgb
        
        # 4. Give visual feedback: switch back to the previous tool
        # so the user can immediately draw with the new color
        print(f"Picked color: {self.color}")
        self.paintbrush() # Or whatever your default tool is

        
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
        
    def sync_pil_image(self):
        # 1. Reset the PIL image to the current background color
        self.image = Image.new("RGB", (self.sizex, self.sizey), (self.fullcolor))
        self.draw = ImageDraw.Draw(self.image)

        # 2. Re-build the background from the history stack
        # Each stroke is now a tuple: (list_of_canvas_ids, list_of_stroke_data)
        for stroke_ids, stroke_data in self.stack:
            
            # Check if this action was a Paint Bucket Fill
            if len(stroke_data) > 0 and stroke_data[0].get('type') == 'fill':
                # If we found a fill, use the saved image state as our new background
                self.image = stroke_data[0]['image'].copy()
                self.draw = ImageDraw.Draw(self.image)
            
            else:
                # Otherwise, it's a standard stroke, so re-paint every segment
                for item in stroke_data:
                    # Get the width for this specific segment
                    try:
                        w = int(item['width'])
                    except:
                        w = 1
                    r = w / 2
                    
                    coords = item['coords'] # (x1, y1, x2, y2)

                    # --- DRAW PIXEL BLOCKS ---
                    if item['type'] == 'pixel':
                        self.draw.rectangle(coords, fill=item['color'], outline=item['color'])

                    # --- DRAW PAINTBRUSH OR PENCIL ---
                    else:
                        # Draw the thick line bridge
                        self.draw.line(coords, fill=item['color'], width=w, joint="curve")
                        
                        # Add rounded caps at the start and end of the segment
                        self.draw.ellipse([coords[0]-r, coords[1]-r, coords[0]+r, coords[1]+r], 
                                          fill=item['color'], outline=item['color'])
                        self.draw.ellipse([coords[2]-r, coords[3]-r, coords[2]+r, coords[3]+r], 
                                          fill=item['color'], outline=item['color'])

        # 3. Final Step: Show the updated image on the canvas
        # This keeps the screen perfectly in sync with the save-file data
        self.IMAGE_snapshot = ImageTk.PhotoImage(self.image)
        self.w.create_image(0, 0, anchor=tk.NW, image=self.IMAGE_snapshot)
        print("PIL Background successfully synchronized with History Stack.")



    def undo(self, event=None):
        try:
            # 1. Pop the last action from the stack
            # Each entry is a tuple: (list_of_ids, list_of_data_dictionaries)
            last_action = self.stack.pop()
            last_stroke_ids, last_stroke_data = last_action
            
            # 2. Save it to the redo stack so we can bring it back later
            self.redo_stack.append(last_action)
            
            # 3. Handle the removal based on tool type
            # Check if the FIRST item in our data list is a 'fill'
            if len(last_stroke_data) > 0 and last_stroke_data[0].get('type') == 'fill':
                # For a Fill: We don't delete IDs (there aren't any).
                # We just need to trigger a sync to rebuild the image 
                # from the items remaining in the stack.
                print("Undoing Paint Bucket fill...")
            else:
                # For Pencil/Paintbrush/Pixel: 
                # Loop through the IDs we collected and delete them from the screen.
                for segment_id in last_stroke_ids:
                    self.w.delete(segment_id)
                print(f"Undoing stroke with {len(last_stroke_ids)} segments.")

            # 4. CRITICAL: Rebuild the background PIL image 
            # This wipes the 'fill' or 'lines' from the background save-image.
            self.sync_pil_image()

        except Exception as e:
            # This triggers if the stack is empty
            print(f"Undo stack empty or error: {e}")

        
    
    def redo(self, event=None):
        try:
            # 1. Get the last undid action from the redo stack
            last_undone_ids, last_undone_data = self.redo_stack.pop()
            
            # 2. Check if the undone action was a Paint Bucket Fill
            # We check the first item in the data list
            if len(last_undone_data) > 0 and last_undone_data[0].get('type') == 'fill':
                # Re-apply the saved fill image to our background
                self.image = last_undone_data[0]['image'].copy()
                self.draw = ImageDraw.Draw(self.image)
                
                # Show the filled image on the canvas
                self.IMAGE_snapshot = ImageTk.PhotoImage(self.image)
                self.w.create_image(0, 0, anchor=tk.NW, image=self.IMAGE_snapshot)
                
                print("Redoing Paint Bucket fill...")
            else:
                # 3. Standard Redo logic for Pencil/Paintbrush/Pixel
                new_stroke_ids = []
                for item in last_undone_data:
                    if item['type'] == 'pixel':
                        new_id = self.w.create_rectangle(*item['coords'], fill=item['color'], outline=item['color'])
                    else:
                        new_id = self.w.create_line(*item['coords'], fill=item['color'], 
                                                   width=item['width'], capstyle=ROUND, smooth=True)
                    new_stroke_ids.append(new_id)
                
                # Update the IDs so we can undo this redo later
                last_undone_ids = new_stroke_ids

            # 4. Put it back in the main stack and sync the background
            self.stack.append((last_undone_ids, last_undone_data))
            self.sync_pil_image()
            
        except Exception as e:
            print(f"Redo failed: {e}")






        
    
            


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
    def touch(self):
        self.tool_option = 'touch'
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
        self.tool_option = 'pencil'
        self.pencil()
        self.choose_size_button.set(5) 
        self.choose_size_button = Scale(self.fr_buttons, from_=1, to=300, orient=HORIZONTAL, bg="white")
        self.choose_size_button.grid(row=0, column=7, sticky="ew", padx=5, pady=5)
    def clear(self):
        self.w.delete("all")
        self.w.configure(bg='white')
        self.fullcolor = 'white'
        self.image=Image.new("RGB",(self.sizex,self.sizey),(self.fullcolor))
        self.draw=ImageDraw.Draw(self.image)
    def b1down(self, event):
        # 1. Update brush settings and state
        self.line_width = self.choose_size_button.get()
        self.b1 = "down"
        
        # 2. Reset coordinates
        self.xold = event.x
        self.yold = event.y
        
        # 3. INITIALIZE HISTORY (Crucial for Undo/Redo)
        self.redo_stack = []           # Wipes redo history because timeline diverged
        self.current_stroke_ids = []    # Container for canvas objects
        self.current_stroke_data = []   # Container for redo instructions
        
        r = self.line_width / 2 # Radius for centering

        if self.tool_option == "eyedropper":
            self.eyedropper(event)
            return  # Stop here so it doesn't draw a dot
        
        if self.tool_option == "fill":
            self.apply_fill(event)
            return # Don't draw lines if filling
        
        elif self.tool_option == "paintbrush":
            # Screen
            self.x = event.widget.create_oval(self.xold, self.yold, event.x, event.y, 
                                             width=self.line_width, outline=self.color, fill=self.color)
            # Background Save
            self.draw.ellipse([event.x - r, event.y - r, event.x + r, event.y + r], fill=self.color)
            
            # Save ID and Data
            self.current_stroke_ids.append(self.x)
            # In b1down and motion for PAINTBRUSH:
            # For ALL tools in b1down, save a 4-point coordinate box
            self.current_stroke_data.append({
                'type': self.tool_option,
                'coords': (self.xold, self.yold, event.x + 0.1, event.y + 0.1), # +0.1 ensures it's a valid line
                'color': self.color,
                'width': self.line_width
            })



        elif self.tool_option == "pencil":
            # Screen
            self.x = event.widget.create_line(self.xold, self.yold, event.x, event.y, 
                                             width=self.line_width, fill=self.color, capstyle=ROUND, smooth=True)
            # Background Save
            self.draw.line(((self.xold, self.yold), (event.x, event.y)), fill=self.color, width=self.line_width)
            self.draw.ellipse([event.x - r, event.y - r, event.x + r, event.y + r], fill=self.color)
            
            # Save ID and Data
            self.current_stroke_ids.append(self.x)
            
            # For ALL tools in b1down, save a 4-point coordinate box
            self.current_stroke_data.append({
                'type': self.tool_option,
                'coords': (self.xold, self.yold, event.x + 0.1, event.y + 0.1), # +0.1 ensures it's a valid line
                'color': self.color,
                'width': self.line_width
            })

        elif self.tool_option == "pixel":
            # Screen
            x1, y1 = self.xold, self.yold
            x2, y2 = event.x + self.line_width, event.y + self.line_width
            self.x = event.widget.create_rectangle(x1, y1, x2, y2, outline=self.color, fill=self.color)
            
            # Background Save
            self.draw.rectangle([x1, y1, x2, y2], fill=self.color)
            
            # Save ID and Data
            self.current_stroke_ids.append(self.x)
            
            # For ALL tools in b1down, save a 4-point coordinate box
            # In b1down for Pixel:
            self.current_stroke_data.append({
                'type': 'pixel',
                'coords': (self.xold, self.yold, event.x + self.line_width, event.y + self.line_width),
                'color': self.color,
                'width': self.line_width
            })


        
    def introExit(self):
        if self.destroy == False:
            self.clear()
            self.destroy = True
            
    def b1up(self,event):
        self.b1 = "up"
        # Push the bundle of IDs we collected to the main stack
        if hasattr(self, 'current_stroke_ids') and self.current_stroke_ids:
            # Store a tuple of (IDs, raw_data_for_redrawing)
            self.stack.append((self.current_stroke_ids, self.current_stroke_data))
            
        self.xold = None
        self.yold = None

    def motion(self, event):
        self.line_width = self.choose_size_button.get()
        
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                r = self.line_width / 2 # Radius for rounding
                
                # --- PAINTBRUSH ---
                if self.tool_option == 'paintbrush':
                    # 1. Screen
                    self.x = event.widget.create_oval(self.xold, self.yold, event.x, event.y, 
                                                     width=self.line_width, outline=self.color, fill=self.color)
                    # 2. Background Save
                    self.draw.line([self.xold, self.yold, event.x, event.y], fill=self.color, width=self.line_width)
                    self.draw.ellipse([event.x - r, event.y - r, event.x + r, event.y + r], fill=self.color)
                    
                    # 3. Store ID and Data
                    self.current_stroke_ids.append(self.x)
                    # In b1down and motion for PAINTBRUSH:
                            # For ALL tools in motion, save the segment from xold to event.x
                    self.current_stroke_data.append({
                        'type': self.tool_option,
                        'coords': (self.xold, self.yold, event.x, event.y),
                        'color': self.color,
                        'width': self.line_width
                    })


                # --- PENCIL ---
                elif self.tool_option == 'pencil':
                    # 1. Screen
                    self.x = event.widget.create_line(self.xold, self.yold, event.x, event.y, 
                                                     width=self.line_width, fill=self.color, capstyle=ROUND, smooth=True)
                    # 2. Background Save
                    self.draw.line([self.xold, self.yold, event.x, event.y], fill=self.color, width=self.line_width)
                    self.draw.ellipse([event.x - r, event.y - r, event.x + r, event.y + r], fill=self.color)
                    
                    # 3. Store ID and Data
                    self.current_stroke_ids.append(self.x)
        
                    # For ALL tools in motion, save the segment from xold to event.x
                    self.current_stroke_data.append({
                        'type': self.tool_option,
                        'coords': (self.xold, self.yold, event.x, event.y),
                        'color': self.color,
                        'width': self.line_width
                    })

                # --- PIXEL ---
                elif self.tool_option == 'pixel':
                    # 1. Screen
                    x1, y1 = self.xold, self.yold
                    x2, y2 = event.x + self.line_width, event.y + self.line_width
                    self.x = event.widget.create_rectangle(x1, y1, x2, y2, outline=self.color, fill=self.color)
                    
                    # 2. Background Save
                    self.draw.rectangle([x1, y1, x2, y2], fill=self.color)
                    
                    # 3. Store ID and Data
                    self.current_stroke_ids.append(self.x)
                    # For ALL tools in motion, save the segment from xold to event.x
                    self.current_stroke_data.append({
                        'type': 'pixel', 
                        'coords': (x1, y1, x2, y2), 
                        'color': self.color, 
                        'width': self.line_width
                    })

        # Update coordinates for the next segment
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
        
        self.update_recent_menu(filepathopen)
        self.IMAGEopen=tk.PhotoImage(file=filepathopen)
        self.MYimage = self.w.create_image(0, 0, anchor=tk.NW, image=self.IMAGEopen)
        self.filepathopen = filepathopen
    def open_file(self):
        try:
            self.IMAGEopen=tk.PhotoImage(file=self.filepathopen)
            self.MYimage = self.w.create_image(0, 0, anchor=tk.NW, image=self.IMAGEopen)
        except:
            self.openAs_file()
            
    def update_recent_menu(self, filepath):
        # Prevent duplicates and keep only the latest 5 files
        if filepath in self.recent_files:
            self.recent_files.remove(filepath)
        self.recent_files.insert(0, filepath)
        self.recent_files = self.recent_files[:5]
        
        # Clear and rebuild the submenu
        self.recent_menu.delete(0, END)
        for path in self.recent_files:
            # Use os.path.basename if you imported os, or split like this:
            filename = path.split('/')[-1] 
            # Note: f=path captures the current value of the path for the lambda
            self.recent_menu.add_command(label=filename, command=lambda f=path: self.load_recent(f))

    def load_recent(self, path):
        self.filepathopen = path
        self.open_file()

    def saveAs_file(self):
        filepathsave = asksaveasfilename(title="Save File", filetypes=[("png files", "*.png")]
        )
        if not filepathsave:
            return
        
        self.update_recent_menu(filepathsave)
        self.image.save(filepathsave)
        self.filename = filepathsave
        Rnumber = From(1000,5000)
        root.config(cursor="watch")
        self.tool_option = 'touch'
        root.after(Rnumber,self.change)
    def change(self):
        if self.tool_option == 'pixel':
            self.pixel()
        if self.tool_option == 'paintbrush':
            self.paintbrush()
        if self.tool_option == 'pencil':
            self.pencil()
        if self.tool_option == 'touch':
            self.touch()
    def save(self):
        try:
            self.image.save(self.filename)
            
            self.update_recent_menu(self.filename)
            
            
            Rnumber = From(1000,5000)
            root.config(cursor="watch")
            self.tool_option = 'touch'
            root.after(Rnumber,self.change)
        except:
            self.saveAs_file()
            

    def save_project(self):
        file_path = asksaveasfilename(
            defaultextension=".hcraft", 
            filetypes=[("Handicraft Project", "*.hcraft")]
        )
        
        if not file_path:
            return 

        try:
            # Bundle everything including your undo/redo stacks
            project_data = {
                "image": self.image,
                "stack": self.stack,
                "redo_stack": self.redo_stack,
                "current_color": self.color,
                "current_tool": self.tool_option,
                "brush_size": self.choose_size_button.get() # Don't forget your scale value!
            }

            with open(file_path, "wb") as f:
                pickle.dump(project_data, f)
            
            self.update_recent_menu(file_path)
            print(f"Project successfully saved to {file_path}")
        
        except Exception as e:
            print(f"Error saving project: {e}")

            
    def load_project(self):
        file_path = askopenfilename(filetypes=[("Handicraft Project", "*.hcraft")])
        if not file_path:
            return

        with open(file_path, "rb") as f:
            project_data = pickle.load(f)
            
        self.update_recent_menu(file_path)

        # Restore the data
        self.image = project_data["image"]
        self.stack = project_data["stack"]
        self.redo_stack = project_data["redo_stack"]
        self.color = project_data["current_color"]
        self.tool_option = project_data["current_tool"]
        self.choose_size_button.set(project_data["brush_size"]) 
        
        
        # Refresh the canvas (essential so you actually see the loaded image)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.w.create_image(0, 0, image=self.tk_image, anchor=NW)


    def openINTROimage(self):
        self.IMAGEopenINTRO=tk.PhotoImage(file='Base_images/intro.png')
        self.MYimageINTRO = self.w.create_image(0, 0, anchor=tk.NW, image=self.IMAGEopenINTRO)
    def openButtonImages(self):
        

        
        img_draw = Image.open('Base_images/lines.png')
        new_size_draw = img_draw.resize((35,35))
        self.I = ImageTk.PhotoImage(new_size_draw)
        self.M = self.w.create_image(0, 0, anchor=tk.NW, image=self.I)
        
        img_cup_pix = Image.open('Base_images/pixels.png')
        new_size_pix = img_cup_pix.resize((35,35))
        self.O = ImageTk.PhotoImage(new_size_pix)
        self.K = self.w.create_image(0, 0, anchor=tk.NW, image=self.O)
        
        img_cup_b = Image.open('Base_images/dots.png')
        new_size_t = img_cup_b.resize((35,35))
        self.T = ImageTk.PhotoImage(new_size_t)
        self.B = self.w.create_image(0, 0, anchor=tk.NW, image=self.T)
        
        self.C=tk.PhotoImage(file='Base_images/color.png')
        self.A = self.w.create_image(0, 0, anchor=tk.NW, image=self.C)
        
        img_chooseC = Image.open('Base_images/chooseColor.png')
        new_size_chooseC = img_chooseC.resize((35,35))
        self.C = ImageTk.PhotoImage(new_size_chooseC)
        self.A = self.w.create_image(0, 0, anchor=tk.NW, image=self.C)
        

        img_cup = Image.open('Base_images/cup.png')
        new_size = img_cup.resize((35,35))
        self.Y = ImageTk.PhotoImage(new_size)
        self.Z = self.w.create_image(0, 0, anchor=tk.NW, image=self.Y)
        
        img_cursor = Image.open('Base_images/cursorArt.png')
        new_size_cursor = img_cursor.resize((35,35))
        self.mouse = ImageTk.PhotoImage(new_size_cursor)
        self.esuoM = self.w.create_image(0, 0, anchor=tk.NW, image=self.mouse)

                                
root=Tk()
root.wm_geometry("%dx%d+%d+%d" % (500, 550, 500, 100))
root.config(bg='white')
root.title( "Handicraft" )
ImageGenerator(root,0,0)
root.mainloop()

