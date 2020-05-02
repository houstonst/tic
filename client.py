from tkinter import *
from classes.Box import Box
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
        
        #create grid
        self.tl = Box(self.frame, "x", (0,0))
        self.tm = Box(self.frame, "o", (0,1))
        self.tr = Box(self.frame, "b", (0,2))
        self.ml = Box(self.frame, "b", (1,0))
        self.mm = Box(self.frame, "x", (1,1))
        self.mr = Box(self.frame, "x", (1,2))
        self.bl = Box(self.frame, "b", (2,0))
        self.bm = Box(self.frame, "o", (2,1))
        self.br = Box(self.frame, "x", (2,2))

        #pack gui objects
        self.enter.grid(row=3, column=0)
        self.send_button.grid(row=4, column=0)
        self.close_button.grid(row=3, column=2)
        self.frame.pack()

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
client = Client()
client.initialize_socket()
_thread.start_new_thread(client.receive_messages, ())
client.root.mainloop()