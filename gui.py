from tkinter import *
import socket
import threading

class GUI:
    # client_socket = None
    # last_received_message = None

    def __init__(self, master):
        # self.master = master

        self.close_conn = 'test'

        def exit(): #this lets us exit the window cleanly with the close button
            master.destroy()
            close_conn = 'exit'
            self.close_conn = close_conn
            self.exit_server()

        self.master = Frame(master, width=500, height=300)
        self.master.pack()

        # self.master.title("Tic-Tac-Toe")

        self.label = Label(master, text="Tic-Tac-Toe", padx=5, pady=5)
        self.label.pack()

        self.initialize_socket()

        self.enter = Entry(root)
        self.enter.pack()

        # self.master.bind("<Enter>", self.send_user)

        self.send_button = Button(master, text="Send Username", command=self.send_user)
        self.send_button.pack()

        self.close_button = Button(master, text="Close", command=exit)
        self.close_button.pack()

        # self.to_server()
        # self.client_socket.close()


    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = "127.0.0.1"
        PORT = 2000
        self.client_socket.connect((HOST, PORT))


    def send_user(self):
        self.username = self.enter.get()
        print(self.username)
        self.client_socket.send(self.username.encode('utf-8'))
        self.to_server()

    def to_server(self):
        while True:
            message = input() # we don't have to create another entry, just use
            encoded_message = message.encode("utf-8")
            print(self.close_conn)
            if (message == "exit" or self.close_conn == "exit"):
                exit_message = "Left the session.".encode("utf-8")
                self.client_socket.sendall(exit_message)
                self.client_socket.sendall(encoded_message)
                break
            else:
                self.client_socket.sendall(encoded_message)
        self.client_socket.close()
        #still needs to learn to close after a username is given


    def exit_server(self): # this lets us exit the server if we click the close button
        while True:
            encoded_message_user = self.close_conn.encode("utf-8")
            if (self.close_conn == "exit"):
                exit_message_user = "Left the session.".encode("utf-8")
                self.client_socket.sendall(exit_message_user)
                self.client_socket.sendall(encoded_message_user)
                break
            else:
                self.to_server

        # self.client_socket.close()
        self.client_socket.close()


root = Tk()
gui = GUI(root)
root.mainloop()