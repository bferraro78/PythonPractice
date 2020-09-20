#!/usr/bin/env python3
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import os
import time

# GLOBAL INDEX VARIABLE
i = 0
x = 0
y = 0
canvasImage = 0
dragData = {}

class VerticalScrolledFrame(tk.Frame):
    """
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, height, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set, height = height)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


## Inital POP UP BOX
class MyInitialDialog:
	def __init__(self, parent):
		self.passWord = ""
		self.top = Toplevel(parent)

		Label(self.top, text="Password").pack()

		self.e = Entry(self.top)
		self.e.pack(padx=5)

		b = Button(self.top, text="OK", command=self.ok)
		b.pack(pady=5)

	def ok(self):
		self.passWord = self.e.get()
		self.top.destroy()

## Exit POP UP BOX
class MyExitDialog:
	def __init__(self, parent):
		self.exitPassWord = ""
		self.top = Toplevel(parent)
		Label(self.top, text="Password").pack()

		self.e = Entry(self.top)
		self.e.pack(padx=5)

		b = Button(self.top, text="OK", command=self.ok)
		b.pack(pady=5)

	def ok(self):
		self.exitPassWord = self.e.get()
		self.top.destroy()


def show_toggle(mylabel, index):
	print("Show button was clicked!") 
	global i
	global x
	global y
	global canvasImage

	mylabel.delete("all")
	x = 0
	y = 0
	canvasImage = mylabel.create_image(int(mylabel.winfo_width()/2), int(mylabel.winfo_height()/2), anchor=CENTER, image=imgArr[index])
	
	i = index
	
def resizeOut(mylabel):
	print("Resize!") 

	index = i
	print(str(index))

	# Determine height/width
	newHeight = imgArr[int(index)].height()/2
	newWidth = imgArr[int(index)].width()/2

	print(newHeight)
	print(newWidth)

	imgOGArr[int(index)] = imgTemplateArr[int(index)].resize((int(newWidth), int(newHeight)))
	imgArr[int(index)] = ImageTk.PhotoImage(imgOGArr[int(index)])

	if x == 0 or y == 0:
		mylabel.itemconfig(canvasImage, image=imgArr[index])
		# mylabel.create_image(int(mylabel.winfo_width()/2), int(mylabel.winfo_height()/2), anchor=CENTER, image=imgArr[index])
	# else:
		# mylabel.create_image(x, y, anchor=CENTER, image=imgArr[index])

def resizeIn(mylabel):
	print("Resize!") 

	index = i
	print(str(index))

	# Determine height/width
	newHeight = imgArr[int(index)].height()*2
	newWidth = imgArr[int(index)].width()*2

	imgOGArr[int(index)] = imgTemplateArr[int(index)].resize((int(newWidth), int(newHeight)), Image.ANTIALIAS)
	imgArr[int(index)] = ''
	imgArr[int(index)] = ImageTk.PhotoImage(imgOGArr[int(index)])

	if x == 0 or y == 0:
		mylabel.itemconfig(canvasImage, image=imgArr[index])
		# mylabel.create_image(int(mylabel.winfo_width()/2), int(mylabel.winfo_height()/2), anchor=CENTER, image=imgArr[index])
	# else:
		# mylabel.create_image(x, y, anchor=CENTER, image=imgArr[index])


def onPress(event):
	global dragData
	print("B2 PRESSED")

	dragData["item"] = mylabel.find_closest(event.x, event.y)
	dragData["x"] = event.x
	dragData["y"] = event.y

def onRelease(event):
	global dragData
	print("RELEASED")
	dragData["item"] = None
	dragData["x"] = 0
	dragData["y"] = 0

def inMotion(event):
	global dragData

	delta_x = event.x - dragData["x"]
	delta_y = event.y - dragData["y"]
	# move the object the appropriate amount
	mylabel.move(dragData["item"], delta_x, delta_y)
	# record the new position
	dragData["x"] = event.x
	dragData["y"] = event.y

# Hides picture when canvas is left clicked
def hide_toggle(mylabel): 
	print("Hide button was clicked!") 
	global canvasImage
	mylabel.delete("all")
	canvasImage = 0
	#SET INSTRUCTION TEXT
	mylabel.create_text(mylabel.winfo_width()/2, mylabel.winfo_height()/2, anchor=CENTER, font=("Helvetica bold", 75),  text= "Click Any Image\n on the Left")


## EXIT BUTTON FUNCTION, COMPARES INITIAL PASSWORDS
def exit(d):
	newPassWord = MyExitDialog(root)
	root.wait_window(newPassWord.top)
	if d.passWord == newPassWord.exitPassWord:
		root.destroy()

##### Start Of Main Loop ######
root = Tk()
root.overrideredirect(True)
root.resizable(False,False)

# Title of Window
root.title("EvidenceView")

# Full Screen
# root.attributes('-fullscreen', True)

root.update()

# Get Screen Size 
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Get Inital Password
d = MyInitialDialog(root)
root.wait_window(d.top)


# Add a Size Pane
p1 = Frame(root)
p1.pack(side=LEFT)

p2 = PanedWindow(root, orient=VERTICAL, bd = 2, bg = "#000000")
p2.pack(side=RIGHT)

# Picture Label
mylabel = Canvas(p2, width=screen_width, height=screen_height)
mylabel.bind("<Button-1>", lambda e:hide_toggle(mylabel))
# Click and Drag
mylabel.bind("<ButtonPress-3>", onPress)
mylabel.bind("<ButtonRelease-3>", onRelease)
mylabel.bind("<B3-Motion>", inMotion)
mylabel.pack(side=RIGHT)

# Update so mylabel width/height is registered
root.update() 

# Set Instruction Text
mylabel.create_text(mylabel.winfo_width()/2, mylabel.winfo_height()/2, font=("Helvetica bold", 75),  text= "Click Any Image\n on the Left")

# Get CWD Command Directory
rootdir = os.getcwd() + '/Pictures'
directory = os.fsencode(rootdir)

imgOGArr = []
imgArr = []
imgTemplateArr = []

# Read from Pictures Directory
count = 0

# Scroll Bar
scframe = VerticalScrolledFrame(p1, int(screen_height/1.5))
scframe.pack(side = RIGHT, fill=Y)

for file in os.listdir(directory):
	filename = os.fsdecode(file)
	
	if filename != ".DS_Store":
# filename.endswith(".store") or filename.endswith(".PNG"): 
		count += 1
		imgFile = rootdir+'/'+filename
		pic = 'Picture ' + str(count)
		
		# Get Only Image File Name
		imgFileName = imgFile.split("/")[-1]
		imgFileName = imgFileName.split(".")[0]

		image = Image.open(imgFile)

		img = ImageTk.PhotoImage(image)

		index = count-1
		imgOGArr.append(image)
		imgArr.append(img)
		imgTemplateArr.append(image)

		# 30 characters is when it starts to get funky
		b = Button(scframe.interior, text=imgFileName)
		b.configure(command = lambda index=index: show_toggle(mylabel, index))
		b.pack(side=TOP)
	

#ZOOM BUTTON
zoomOutButton = Button(p1, text="Zoom Out")
zoomOutButton.configure(command = lambda: resizeOut(mylabel))
zoomOutButton.pack(side=TOP)

zoomInButton = Button(p1, text="Zoom In")
zoomInButton.configure(command = lambda: resizeIn(mylabel))
zoomInButton.pack(side=TOP)

# Exit Button
exitButton = Button(p1, text="Exit Viewer", command=lambda d=d: exit(d))
exitButton.pack(side=TOP)

root.mainloop()