import tkinter as tk
from tkinter import *
from tkinter import filedialog,messagebox

from libs.myCanvas import * 
from libs.myDefine import * 

import os,time
import threading

import cv2
import numpy as np

from libs.myCameraDlg import *
import libs.myCamera as myCam



class myGui(tk.Frame):

	def __init__(self):
		super().__init__()
		self.file_types = [".jpg",".bmp",".png",".gif"]
		self.cameraDlgs = []
		self.image = None
		self.bLock = True
		self.bGetDevices = True
		self.baslerDevices = myCam.getBaslerDevices()
		self.usbDevices = myCam.getAllDeviceUSB()
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

		self.icont1 = ImageTk.PhotoImage(Image.open("res/rect.png"))
		self.toolRect = Button(toolbar,image=self.icont1,relief=FLAT
			,command=lambda:self.command(RECT))
		self.toolRect.pack(side=LEFT,padx=2,pady=2)
		
		self.icont2 = ImageTk.PhotoImage(Image.open("res/movies.png"))
		self.toolMovie = Button(toolbar,image=self.icont2,relief=FLAT
			,command=lambda:self.command(MOVIE))
		self.toolMovie.pack(side=LEFT,padx=2,pady=2)

		self.icont3 = ImageTk.PhotoImage(Image.open("res/reload.png"))
		self.toolReload = Button(toolbar,image=self.icont3,relief=FLAT
			,command=lambda:self.command(RELOAD))
		self.toolReload.pack(side=LEFT,padx=2,pady=2)

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
		wB,hB = 90,30

		self.icon3 = ImageTk.PhotoImage(Image.open("res/start.png"))
		Button(f22,text="Start",font=font,image=self.icon3,anchor="w",compound=LEFT,height=hB,width=wB
			,command=lambda:self.command(START)).grid(column=0,row=0,padx=2,pady=2)

		self.icon4 = ImageTk.PhotoImage(Image.open("res/stop.png"))
		Button(f22,text="Stop",font=font,image=self.icon4,compound=LEFT,height=hB,width=wB
			,command=lambda:self.command(STOP)).grid(column=1,row=0,padx=2,pady=2)

		self.icon5 = ImageTk.PhotoImage(Image.open("res/reset.png"))
		Button(f22,text="Reset",font=font,image=self.icon5,compound=LEFT,height=hB,width=wB
			,command=lambda:self.command(RESET)).grid(column=2,row=0,padx=2,pady=2)

		self.icon6 = ImageTk.PhotoImage(Image.open("res/data.png"))
		Button(f22,text="Log",font=font,image=self.icon6,compound=LEFT,height=hB,width=wB
			,command=lambda:self.command(LOG)).grid(column=3,row=0,padx=2,pady=2)

		self.lbClock = Label(f21,bg=LIGHT_BLUE1,fg=ORANGE,font=("Arial 40 bold"))
		self.lbClock.pack(fill="both",expand=1,anchor="s")
		self.miniCanvas = myCanvas(f21,bg=BLACK)
		self.miniCanvas.pack(fill="both",expand=1,anchor="s")
		self.logText = tk.Listbox(f21)
		self.logText.pack(fill="both",expand=1,anchor="s")

		# ================= pack and binding==============
		
		self.master.bind("<Key>",self.key)
		self.master.protocol("WM_DELETE_WINDOW",self.on_closing)
		self.pack(fill="both",expand=1)
		self.master.state('zoomed')
		# start thread
		self.threadClock()
		
	# Command
	def command(self,cmd):
		print(cmd)
		if cmd == OPEN:
			self.load()
		elif cmd == MOVIE:
			pass
		elif cmd == RECT:
			self.canvas.bDrawRect = True
			self.canvas.bDrawAlign = True
		elif cmd == ADD:		
			self.canvas.rects.append(self.canvas.rect)
		elif cmd == CLEAR_ALL:
			self.canvas.resetCanvas()
		elif cmd == BASLER:
			dlg = cameraDlg("Basler Camera",BASLER,self.baslerDevices)
			self.cameraDlgs.append(dlg)
			pass
		elif cmd == DINO:
			dlg = cameraDlg("USB Camera",DINO,self.usbDevices)
			self.cameraDlgs.append(dlg)
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
		p = [e.x_root,e.y_root]

		rReload = self.getGeometry(self.toolReload)

		if self.canvas.ptInRect(p,rReload):
			print("reload")
		else:
			print(False ,r, rReload, p)
		
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
		r = [item.winfo_rootx(),item.winfo_rooty(),item.winfo_width(),item.winfo_height()]
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
	# threading
	def threadClock(self):
		thread = threading.Thread(target=self.loopClock)
		thread.start()
		pass
	def loopClock(self):
		while self.bLock:
			strtime = time.strftime("%H:%M:%S")
			self.lbClock["text"] = strtime
			time.sleep(1)
		pass
	def threadGetDevices(self):
		thread = threading.Thread(target=self.loopGetDevices)
		thread.start()
		pass
	def loopGetDevices(self):
		while self.bGetDevices:
			self.releaseAllDevices()
			self.baslerDevices = myCam.getBaslerDevices()
			self.usbDevices = myCam.getAllDeviceUSB()
			time.sleep(1)
		pass
	# ========== Closing ========
	def __del__(self):
		print ('GUI destructor called')
	def releaseAllDevices(self):
		if self.baslerDevices is not None:
			for device in self.baslerDevices:
				dev,bGrabbing,sn = device
				if bGrabbing :
					dev.StopGrabbing()
		if self.usbDevices is not None:
			for device in self.usbDevices:
				dev,bOpened,sn = device
				if bOpened :
					dev.release()
		pass
	def on_closing(self):
		print ('GUI closing called')
		self.bLock = False
		self.bGetDevices = False
		for dlg in self.cameraDlgs:
			if dlg.bLive:
				messagebox.showinfo("Warnig!!!","Please stop camera before close!")
				return
		self.releaseAllDevices()
		self.master.destroy()



