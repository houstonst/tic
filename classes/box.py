from tkinter import *
from PIL import Image, ImageTk

class box:
    def __init__(self, frame, img, pos, is_set):
        #define image choices
        self.blank_img = Image.open("./graphics/blank.PNG")
        self.x_img = Image.open("./graphics/x.PNG")
        self.o_img = Image.open("./graphics/o.PNG")

        #create blank, X, or O image
        self.graphic = None
        if img == "b":
            self.graphic = ImageTk.PhotoImage(self.blank_img)
        elif img == "x":
            self.graphic = ImageTk.PhotoImage(self.x_img)
        else:
            self.graphic = ImageTk.PhotoImage(self.o_img)

        #create the object
        self.label = Label(frame, image=self.graphic, borderwidth=5, relief="solid")

        #create image reference or it won't display for some reason
        self.label.image = self.graphic

        #pack box into GUI frame
        self.label.grid(row=pos[0], column=pos[1])

        if is_set == False:
            #bind events
            self.label.bind("<Enter>", self.mouse_over)
            self.label.bind("<Leave>", self.mouse_leave)
    
    def mouse_over(self, event):
        self.graphic = ImageTk.PhotoImage(self.x_img)
        self.label.configure(image=self.graphic)

    def mouse_leave(self, event):
        self.graphic = ImageTk.PhotoImage(self.blank_img)
        self.label.configure(image=self.graphic)
