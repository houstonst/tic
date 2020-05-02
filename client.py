from tkinter import *
from PIL import Image, ImageTk
import socket, sys, _thread

class box:
    def __init__(self, frame, img, pos):
        graphic = None

        #create blank, X, or O image
        if img == "b":
            blank_img = Image.open("./graphics/blank.PNG")
            graphic = ImageTk.PhotoImage(blank_img)
        elif img == "x":
            x_img = Image.open("./graphics/x.PNG")
            graphic = ImageTk.PhotoImage(x_img)
        else:
            o_img = Image.open("./graphics/o.PNG")
            graphic = ImageTk.PhotoImage(o_img)

        #create the object
        self.label = Label(frame, image=graphic, borderwidth=5, relief="solid")

        #create image reference or it won't display for some reason
        self.label.image = graphic

        #pack box into GUI frame
        self.label.grid(row=pos[0], column=pos[1])

class GUI:
    def __init__(self):
        #define logic attributes
        self.username = None

        #define gui attributes
        self.root = Tk()
        self.root.title("Tic-Tac-Toe")
        self.root.iconbitmap("./graphics/favicon.ico")
        
        #create gui objects
        self.frame = Frame(self.root, width=500, height=300)
        self.enter = Entry(self.root)
        self.send_button = Button(self.root, text="Send Username", command=self.send_message)
        self.close_button = Button(self.root, text="Close", command=self.leave_session)
        self.root.bind("<Return>", self.send_message)
        
        #create grid
        self.tl = box(self.frame, "x", (0,0))
        self.tm = box(self.frame, "o", (0,1))
        self.tr = box(self.frame, "b", (0,2))
        self.ml = box(self.frame, "b", (1,0))
        self.mm = box(self.frame, "x", (1,1))
        self.mr = box(self.frame, "x", (1,2))
        self.bl = box(self.frame, "b", (2,0))
        self.bm = box(self.frame, "o", (2,1))
        self.br = box(self.frame, "x", (2,2))

        #pack gui objects
        self.frame.pack()
        self.enter.pack()
        self.send_button.pack()
        self.close_button.pack()

    #begin connection to server
    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = "127.0.0.1"
        PORT = 2000
        self.client_socket.connect((HOST, PORT))

    #deleted the text in the text box so the user doesn't have to
    def text_delete(self):
        self.enter.delete(first=0, last=200)

    #send messages to server
    def send_message(self, *event):
        #accept username as first message
        if self.username == None:
            self.username = self.enter.get()
            print("Hello " + self.username + ".")
            self.client_socket.send(self.username.encode('utf-8'))
            self.send_button.config(text = "Send Message")
            self.text_delete()

        #all follow on entries are normal messages
        else:
            message = self.enter.get()
            encoded_message = message.encode("utf-8")
            print("[you]: {}".format(message))
            self.client_socket.send(encoded_message)
            self.text_delete()
        
    #receive message thread
    def receive_messages(self):
        while True:
            try:
                encoded_message = self.client_socket.recv(1024)
                print(encoded_message.decode())
            except:
                break

    def leave_session(self):
        exit_message = "exit".encode("utf-8")
        self.client_socket.sendall(exit_message)

        #quit the gui, connection, and program respectively
        self.root.destroy()
        self.client_socket.close()
        sys.exit()

#script
gui = GUI()
gui.initialize_socket()
_thread.start_new_thread(gui.receive_messages, ())
gui.root.mainloop()