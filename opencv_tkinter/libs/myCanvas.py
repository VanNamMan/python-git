import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk

class myRect:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.tl = [x,y]
        self.br = [w,h]
class myCanvas(tk.Canvas):
    def __init__(self,parent,bg="black",w=300,h=200):
        super(myCanvas,self).__init__(parent,bg=bg,width=w,height=h)
        self.bDrawAlign = False
        self.bDrawRect = False
        self.bDrawLine = False
        self.bActiveRect = False
        self.start = None
        self.image = None
        self.rect = [0,0,0,0]
        self.rect_active = [0,0,0,0]
        self.id_rect_active = -1
        self.rects = []
        self.color = "red"
        self.lw = 3

        self.bind("<ButtonPress-1>",self.lButtonDown)
        self.bind("<Motion>",self.mouseMove)
        self.bind("<ButtonRelease-1>",self.lButtonUp)
    def lButtonDown(self,e):
        p = [e.x,e.y]
        for r in self.rects:
            if self.ptInRect(p,r):
                self.id_rect_active = self.rects.index(r)
                self.bActiveRect = True
                self.bDrawRect = True
                self.rect_active = r
                self.create_rectangle(r[0],r[1],r[2],r[3]
                                    ,outline="yellow",width=self.lw)
                
                break
        if not self.bDrawRect:
            return
        self.bDrawAlign = False
        self.start = e

    def lButtonUp(self,e):
        if not self.bDrawRect:
            return
        self.bDrawAlign = False
        self.bDrawRect = False
        self.bActiveRect = False
        
    def mouseMove(self,e):
        if not self.bDrawRect:
            return
        self.delete("all")
        if self.bDrawAlign:
            self.create_line(0,e.y,self.winfo_width(),e.y
                                ,fill=self.color,width=self.lw)
            self.create_line(e.x,0,e.x,self.winfo_height()
                                ,fill=self.color,width=self.lw)
        if self.bActiveRect:
            dx = e.x - self.start.x
            dy= e.y - self.start.y
            r = self.rect_active
            self.rects[self.id_rect_active] = [r[0]+dx,r[1]+dy,r[2]+dx,r[3]+dy]
            self.create_rectangle(r[0]+dx,r[1]+dy,r[2]+dx,r[3]+dy
                                    ,outline="yellow",width=self.lw)
            for i in range(len(self.rects)):
                if i != self.id_rect_active:
                    r = self.rects[i]
                    self.create_rectangle(r[0],r[1],r[2],r[3]
                                    ,outline=self.color,width=self.lw)
            pass
        elif not self.bDrawAlign:
            if self.image:
                self.showImage(self.image)

            for r in self.rects:
                self.create_rectangle(r[0],r[1],r[2],r[3]
                                ,outline=self.color,width=self.lw)
            if self.start:
                self.rect = [self.start.x,self.start.y,e.x,e.y]
                self.create_rectangle(self.start.x,self.start.y,e.x,e.y
                                ,outline=self.color,width=self.lw)
    def ptInRect(self,p,r):
        if r[0] < p[0] < r[2] and r[1] < p[1] < r[3]:
            return True
        else:
            return False
        pass
    def resetCanvas(self):
        self.delete("all")
        self.rects = []
    def toCvRect(self):
        print(self.image.width())
        pass
    def showImage(self,img):
        self.image = img
        self.create_image(1,1,anchor="nw",image=img)
            


            





