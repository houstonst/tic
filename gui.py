from tkinter import *
import socket
import threading

class GUI:
    # client_socket = None
    # last_received_message = None

    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.master = Frame(self.master, width=500, height=300)
        self.master.pack()

        self.label = Label(master, text="Tic-Tac-Toe", padx=5, pady=5)
        self.label.pack()

        self.initialize_socket()

        self.enter = Entry(root)
        self.enter.pack()

        # self.master.bind("<Enter>", self.send_user)

        self.send_button = Button(master, text="Send Username", command=self.send_user)
        self.send_button.pack()

        self.close_button = Button(master, text="Close", command=master.destroy)
        self.close_button.pack()

        self.to_server()
        self.client_socket.close()

    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = "127.0.0.1"
        PORT = 2000
        self.client_socket.connect((HOST, PORT))


    def send_user(self):
        self.username = self.enter.get()
        self.client_socket.send(self.username.encode('utf-8'))


    def to_server(self):
        while True:
            message = input() # we don't have to create another entry, just use this
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