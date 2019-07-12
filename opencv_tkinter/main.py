import tkinter as tk
from tkinter import *
from myGui import myGui

def main():
    root = Tk()
    root.geometry("1000x600+30+30")
    app = myGui()
    root.mainloop()

if __name__ == '__main__':
    main()