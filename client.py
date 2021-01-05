from tkinter import *
import socket, sys, _thread
from PIL import Image, ImageTk

class Box:
    def __init__(self, frame, img, pos, sym, sock, is_set):
        #sets variables to be used in other functions
        self.is_set = is_set
        self.sym = sym
        self.pos = pos
        self.img = img
        self.sock = sock
        self.turn_locked = False #controls whether the box can be played (based on who's turn it is)

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

    #display potential move
    def mouse_over(self, event):
        if self.turn_locked == False:
            if self.sym == 'X':
                self.i = self.x_img
            else:
                self.i = self.o_img
            self.graphic = ImageTk.PhotoImage(self.i)
            self.label.configure(image=self.graphic)

    #clear potential move
    def mouse_leave(self, event):
        if self.turn_locked == False:
            self.graphic = ImageTk.PhotoImage(self.blank_img)
            self.label.configure(image=self.graphic)

    #make a move
    def mouse_click(self, event):
        if self.turn_locked == False:
            if self.sym == 'X':
                self.img = 'x'
                client.x_positions.add(self.pos)
            else:
                self.img = 'o'
                client.o_positions.add(self.pos)
            client.check_win()
            self.graphic = ImageTk.PhotoImage(self.i)
            self.label.configure(image=self.graphic)
            self.send_message()
            self.is_set == True
            self.unbind()
    
    #send move to server
    def send_message(self):
        if self.turn_locked == False:
            msg = ''
            for i in self.pos:
                msg += str(i)
            encoded_message = (msg).encode("utf-8")
            self.sock.send(encoded_message)
            client.lock_boxes()
        
    #unbind events so a set box cannot be changed
    def unbind(self):
        self.label.unbind("<Enter>", self.mouse_over_id)
        self.label.unbind("<Leave>", self.mouse_leave_id)
        self.label.unbind("<Button-1>", self.mouse_click_id)

#########################################################################################################

class Client:
    def __init__(self):
        #define logic attributes
        self.username = None
        self.turn = False

        #define gui attributes
        self.root = Tk()
        self.root.title("Tic-Tac-Toe")
        self.root.iconbitmap("./graphics/favicon.ico")
        
        #create gui objects
        self.frame = Frame(self.root, width=500, height=300)
        self.enter = Entry(self.frame)
        self.send_button = Button(self.frame, text="Send Username", command=self.send_message)
        self.close_button = Button(self.frame, text="Close", command=self.leave_session)
        self.root.bind("<Return>", self.send_message)

    #initialize all instances of the Box class
    def init_grid(self, symbol):
        #assigns X's or O's for the user
        self.symbol = symbol 

        #create grid
        self.tl = Box(self.frame, "b", (0,0), self.symbol, self.client_socket, False)
        self.tm = Box(self.frame, "b", (0,1), self.symbol, self.client_socket, False)
        self.tr = Box(self.frame, "b", (0,2), self.symbol, self.client_socket, False)
        self.ml = Box(self.frame, "b", (1,0), self.symbol, self.client_socket, False)
        self.mm = Box(self.frame, "b", (1,1), self.symbol, self.client_socket, False)
        self.mr = Box(self.frame, "b", (1,2), self.symbol, self.client_socket, False)
        self.bl = Box(self.frame, "b", (2,0), self.symbol, self.client_socket, False)
        self.bm = Box(self.frame, "b", (2,1), self.symbol, self.client_socket, False)
        self.br = Box(self.frame, "b", (2,2), self.symbol, self.client_socket, False)

        #place boxes in matrix
        self.gridList = [[self.tl, self.tm, self.tr], [self.ml, self.mm, self.mr], [self.bl, self.bm, self.br]]

        #create sets to check against win conditions
        self.x_positions = set()
        self.o_positions = set()

        #pack gui objects
        self.enter.grid(row=3, column=0)
        self.send_button.grid(row=4, column=0)
        self.close_button.grid(row=3, column=2)
        self.frame.pack()

    #compares running positional sets with win condition sets
    def check_win(self):
        win_conditions = [
            {(0,0),(0,1),(0,2)},    #horizontal wins
            {(1,0),(1,1),(1,2)},
            {(2,0),(2,1),(2,2)},
            {(0,0),(1,0),(2,0)},    #vertical wins
            {(0,1),(1,1),(2,1)},
            {(2,0),(1,2),(2,2)},
            {(0,0),(1,1),(2,2)},    #diagonal wins
            {(2,0),(1,1),(0,2)}
        ]

        for condition in win_conditions:
            if condition.issubset(self.x_positions):
                print("X wins with {}".format(condition))
                self.lock_boxes()
            elif condition.issubset(self.o_positions):
                print("O wins with {}".format(condition))
                self.lock_boxes()

    #begin connection to server
    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #connect to server's address and port
        HOST = "127.0.0.1"
        PORT = 2000
        self.client_socket.connect((HOST, PORT))

    #delete the text in the text box after message is sent
    def text_delete(self):
        self.enter.delete(first=0, last=200)

    #send messages to server
    def send_message(self, *event):
        #accept username as first message
        if self.username == None:
            self.username = self.enter.get()
            print("Hello " + self.username + ".")
            print("You are {}'s".format(self.symbol))
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
    
    #reconfigure particular box according to other user's move
    def handle_pos(self, pos):
        string = str(pos)
        tup = (int(string[0]), int(string[1]))
        if (self.symbol == 'X'):
            self.gridList[tup[0]][tup[1]] = Box(self.frame, "o", tup, self.symbol, self.client_socket, True)
            self.o_positions.add(tup)
        else:
            self.gridList[tup[0]][tup[1]] = Box(self.frame, "x", tup, self.symbol, self.client_socket, True)
            self.x_positions.add(tup)
        self.check_win()

    #prevent unsolicited move
    def lock_boxes(self):
        for row in self.gridList:
            for box in row:
                box.turn_locked = True

    #allow a move
    def unlock_boxes(self):
        for row in self.gridList:
            for box in row:
                box.turn_locked = False

    #receive message thread
    def receive_messages(self):
        while True:
            try:
                encoded_message = self.client_socket.recv(1024)
                self.msg = encoded_message.decode()
                if self.msg == 'X':
                    print("YOU ARE PLAYER 1")
                    self.turn = True #ensure they go first
                    self.init_grid(self.msg)
                    self.unlock_boxes()
                elif self.msg == 'O':
                    print("YOU ARE PLAYER 2")
                    self.turn = False #already false by default
                    self.init_grid(self.msg)
                    self.lock_boxes()
                else:
                    self.handle_pos(self.msg)
                    self.unlock_boxes()
            except:
                break    

    #destroy program after clicking "close" button
    def leave_session(self):
        exit_message = "exit".encode("utf-8")
        self.client_socket.sendall(exit_message)

        #quit the gui, connection, and program respectively
        self.root.destroy()
        self.client_socket.close()
        sys.exit()

#script
client = Client()
client.initialize_socket()
_thread.start_new_thread(client.receive_messages, ())
client.root.mainloop()