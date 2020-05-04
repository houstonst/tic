from tkinter import *
from classes.box import Box
import socket, sys, _thread

class Client:
    def __init__(self):
        #define logic attributes
        self.username = None

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

        #pack gui objects
        self.enter.grid(row=3, column=0)
        self.send_button.grid(row=4, column=0)
        self.close_button.grid(row=3, column=2)
        self.frame.pack()

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
    
    #sent coordinate of clicked box to other user
    def handle_pos(self, pos):
        string = str(pos)
        tup = (int(string[0]), int(string[1]))
        if (self.symbol == 'X'):
            Box(self.frame, "o", tup, self.symbol, self.client_socket, True)
        else:
            Box(self.frame, "x", tup, self.symbol, self.client_socket, True)

    #receive message thread
    def receive_messages(self):
        while True:
            try:
                encoded_message = self.client_socket.recv(1024)
                self.msg = encoded_message.decode()
                if (self.msg == 'X' or self.msg == 'O'):
                    self.init_grid(self.msg)
                else:
                    self.handle_pos(self.msg)
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