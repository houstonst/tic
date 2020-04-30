from tkinter import *
import socket
import threading

class GUI:
    # client_socket = None
    last_received_message = None

    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.destroy)
        self.close_button.pack()

        self.initialize_socket()

        self.enter = Entry()
        self.username = self.enter.get()
        self.enter.pack()

        self.send_button = Button(master, text="Send", command=self.send_user)
        self.send_button.pack()

        # username = enter.get()
        # username.pack()
        # self.client_socket.send(enter.get().encode('utf-8'))

        # self.get_username()
        self.to_server()
        self.client_socket.close()

    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = "127.0.0.1"
        PORT = 2000
        self.client_socket.connect((HOST, PORT))

    def greet(self):
        print("Greetings!")

    def send_user(self):
        print("test")
        print(self.username) #it doesn't print anything
        self.client_socket.send(self.username.encode('utf-8'))

    # def get_username(event):
    #     # print(event)
    #     self.client_socket.send(username).encode('utf-8')
    #     username = Entry()
    #     self.client_socket.send(username.encode('utf-8'))
    
    def to_server(self):
        while True:
            message = input()
            encoded_message = message.encode("utf-8")
            if message == "exit":
                exit_message = "Left the session.".encode("utf-8")
                client_socket.sendall(exit_message)
                client_socket.sendall(encoded_message)
                break
            else:
                client_socket.sendall(encoded_message)



root = Tk()
gui = GUI(root)
root.mainloop()