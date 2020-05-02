from tkinter import *
from PIL import Image, ImageTk

class Box:
    def __init__(self, frame, img, pos):
        #variable for whether the box can be changed
        self.is_set = False

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

        #bind events. Saved ID's so they can be unbinded later
        if self.is_set == False:
            self.mouse_over_id = self.label.bind("<Enter>", self.mouse_over)
            self.mouse_leave_id = self.label.bind("<Leave>", self.mouse_leave)
            self.mouse_click_id = self.label.bind("<Button-1>", self.mouse_click)            
    
    def mouse_over(self, event):
        self.graphic = ImageTk.PhotoImage(self.x_img)
        self.label.configure(image=self.graphic)

    def mouse_leave(self, event):
        self.graphic = ImageTk.PhotoImage(self.blank_img)
        self.label.configure(image=self.graphic)

    def mouse_click(self, event):
        self.graphic = ImageTk.PhotoImage(self.x_img)
        self.label.configure(image=self.graphic)
        self.unbind()

    #unbind events so a set box cannot be changed
    def unbind(self):
        self.label.unbind("<Enter>", self.mouse_over_id)
        self.label.unbind("<Leave>", self.mouse_leave_id)
        self.label.unbind("<Button-1>", self.mouse_click_id)