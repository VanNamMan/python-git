import tkinter as tk
from tkinter import *
from tkinter import filedialog,messagebox
from libs.myCanvas import * 
from libs.myDefine import * 
import cv2
import os,time
import numpy as np

OPEN = "Open"
DINO = "Dino"



class myGui(tk.Frame):

	def __init__(self):
		super().__init__()
		self.file_types = [".jpg",".bmp",".png",".gif"]
		# self.pilImg = None
		self.image = None
		self.initUI()
	def initUI(self):	
		self.master.title("Gui Tkinter")
		self.master.bind("<Motion>",self.mouseMove)
		# menubar File , Camera , Setting , Font
		menubar = Menu(self.master)
		self.master.config(menu=menubar)

		fileMenu = Menu(menubar)
		fileMenu.add_command(label="Open", command=lambda:self.command(OPEN))
		menubar.add_cascade(label="File", menu=fileMenu)

		cameraMenu = Menu(menubar)
		cameraMenu.add_command(label="Dino", command=lambda:self.command(DINO))
		cameraMenu.add_command(label="Basler", command=lambda:self.command(BASLER))
		menubar.add_cascade(label="Camera", menu=cameraMenu)

		settingMenu = Menu(menubar)
		settingMenu.add_command(label="Parameter", command=lambda:self.command(PARA))
		menubar.add_cascade(label="Setting", menu=settingMenu)

		fontMenu = Menu(menubar)
		menubar.add_cascade(label="Font", menu=fontMenu)

		drawingMenu = Menu(fontMenu)
		fontMenu.add_cascade(label="Drawing",menu=drawingMenu)

		drawingMenu.add_command(label="Text", command=lambda:self.command(TEXT))
		drawingMenu.add_command(label="Line width", command=lambda:self.command(LW))
		drawingMenu.add_command(label="Font scale", command=lambda:self.command(FS))
		
		# frame 

		f1 = Frame(self,width=700,height=600,borderwidth=1,relief="sunken")
		f2 = Frame(self,width=300,height=600)

		for f in [f1,f2]:
			f.pack(fill="both",expand=1,side="left")
			f.pack_propagate(0)

		# f1 Frame 
		# ======== toolbar =========
		toolbar = Frame(f1,height=3,relief=RAISED,bg=LIGHT_BLUE1)
		picontrol = Frame(f1,height=590)
		toolbar.pack(fill="x",side="top")
		picontrol.pack(fill="both",expand=1,side="top",anchor=W)

		self.icon1 = ImageTk.PhotoImage(Image.open("res/rect.png"))
		Button(toolbar,image=self.icon1,relief=FLAT
			,command=lambda:self.command(RECT)).pack(side=LEFT,padx=2,pady=2)
		
		self.icon2 = ImageTk.PhotoImage(Image.open("res/movies.png"))
		Button(toolbar,image=self.icon2,relief=FLAT
			,command=lambda:self.command(MOVIE)).pack(side=LEFT,padx=2,pady=2)

		toolbar.pack(side=TOP,fill=X)
		# ===
		self.label = Label(picontrol,width=50)
		self.label.pack()
		self.canvas = myCanvas(picontrol,bg=BLACK)
		self.canvas.pack(fill="both",expand=1)

		# =======Popup Menu ==========
		popup = Menu(self.master, tearoff=0)
		popup.add_command(label="Add",command=lambda:self.command(ADD))
		popup.add_command(label="Delete",command=lambda:self.command(DELETE))
		popup.add_separator()
		popup.add_command(label="Clear All",command=lambda:self.command(CLEAR_ALL))

		def do_popup(event):
		    try:
		        popup.tk_popup(event.x_root+50, event.y_root+30, 0)
		    finally:
	        	popup.grab_release()

		self.canvas.bind("<Button-3>", do_popup)

		# ============== f2 Frame ==============
		f21 = Frame(f2,width=300,height=550)
		f22 = Frame(f2,width=300,height=50,bg=LIGHT_BLUE1)
		for f in [f21,f22]:
			f.pack(fill="both",expand=1,side="top",anchor="s")
			f.pack_propagate(0)

		font = ("Arial",12,"bold")

		self.icon3 = ImageTk.PhotoImage(Image.open("res/start.png"))
		Button(f22,text="Start",font=font,image=self.icon3,anchor="w",compound=LEFT
			,command=lambda:self.command(START)).pack(side="left",fill="both",expand=1,anchor="s",padx=2,pady=2)

		self.icon4 = ImageTk.PhotoImage(Image.open("res/stop.png"))
		Button(f22,text="Stop",font=font,image=self.icon4,compound=LEFT
			,command=lambda:self.command(STOP)).pack(side="left",fill="both",expand=1,anchor="s",padx=2,pady=2)

		self.icon5 = ImageTk.PhotoImage(Image.open("res/reset.png"))
		Button(f22,text="Reset",font=font,image=self.icon5,compound=LEFT
			,command=lambda:self.command(RESET)).pack(side="left",fill="both",expand=1,anchor="s",padx=2,pady=2)

		self.miniCanvas = myCanvas(f21,bg=BLACK)
		self.miniCanvas.pack(fill="both",expand=1,anchor="s")
		self.logText = tk.Listbox(f21)
		self.logText.pack(fill="both",expand=1,anchor="s")

		# ================= pack ===============
		self.master.bind("<Key>",self.key)
		self.pack(fill="both",expand=1)
		

	# Command
	def command(self,cmd):
		print(cmd)
		if cmd == OPEN:
			self.load()
		elif cmd == RECT:
			self.canvas.bDrawRect = True
			self.canvas.bDrawAlign = True
		elif cmd == ADD:		
			self.canvas.rects.append(self.canvas.rect)
		elif cmd == CLEAR_ALL:
			self.canvas.resetCanvas()
		pass
	# event
	def key(self,e):
		print ("pressed",e.char)   
		if e.char == "a":
			self.command(RECT)
	def mouseMove(self,e):
		if self.image is None:
			return
		r = self.getGeometry(self.canvas)
		p = [e.x,e.y]
		if not self.canvas.ptInRect(p,r):
			return
		if self.canvas.crop:
			x1,y1,x2,y2 = self.canvas.crop
			h,w = self.image.shape[:2]
			x1,y1,x2,y2 = int(x1*w),int(y1*h),int(x2*w),int(y2*h)
			print(x1,y1,x2,y2)
			crop = self.image[y1:y2,x1:x2]
			self.show(self.miniCanvas,crop)
    # function
	def log(self,txt):
		txt = time.strftime("%H:%M:%S ")+txt
		self.logText.insert(END,txt)
		pass
	def load(self):
		filename =  filedialog.askopenfilename(initialdir = os.getcwd()
	                                       ,title = "Select file"
	                                       ,filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
		if filename == "":
			return
		else:
			_, file_extension = os.path.splitext(filename)
			if file_extension in self.file_types:
				self.label["text"] = filename
				self.image = cv2.imread(filename)
				self.show(self.canvas,self.image)
	def getGeometry(self,item):
		r = [item.winfo_x(),item.winfo_y(),item.winfo_width(),item.winfo_height()]
		return r

	def show(self,canvas,img):
	    size = (canvas.winfo_width(),canvas.winfo_height())
	    if len(img.shape) == 2:
	    	cvImg = cv2.resize(img,size)
	    else:
	    	cvImg = cv2.resize(img[...,::-1],size)  # BGR to RGB 

	    pilImg = Image.fromarray(cvImg)
	    photoImg = ImageTk.PhotoImage(image=pilImg)
	    canvas.showImage(photoImg)



