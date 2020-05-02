from tkinter import *
import socket, sys, _thread

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
        """
        t: top
        m: middle
        b: bottom
        l: left
        r: right

        Ex.) tm: top-left, mm: middle-middle
        """

        self.tl = Label(self.frame, text="placeholder", width=50, height=15, bg='grey', borderwidth=5, relief="solid")
        self.tm = Label(self.frame, text="placeholder", width=50, height=15, bg='grey', borderwidth=5, relief="solid")
        self.tr = Label(self.frame, text="placeholder", width=50, height=15, bg='grey', borderwidth=5, relief="solid")
        self.ml = Label(self.frame, text="placeholder", width=50, height=15, bg='grey', borderwidth=5, relief="solid")
        self.mm = Label(self.frame, text="placeholder", width=50, height=15, bg='grey', borderwidth=5, relief="solid")
        self.mr = Label(self.frame, text="placeholder", width=50, height=15, bg='grey', borderwidth=5, relief="solid")
        self.bl = Label(self.frame, text="placeholder", width=50, height=15, bg='grey', borderwidth=5, relief="solid")
        self.bm = Label(self.frame, text="placeholder", width=50, height=15, bg='grey', borderwidth=5, relief="solid")
        self.br = Label(self.frame, text="placeholder", width=50, height=15, bg='grey', borderwidth=5, relief="solid")

        #pack gui objects
        self.frame.pack()
        self.enter.pack()
        self.send_button.pack()
        self.close_button.pack()

        #pack grid objects
        self.tl.grid(row=0, column=0)
        self.tm.grid(row=0, column=1)
        self.tr.grid(row=0, column=2)
        self.ml.grid(row=1, column=0)
        self.mm.grid(row=1, column=1)
        self.mr.grid(row=1, column=2)
        self.bl.grid(row=2, column=0)
        self.bm.grid(row=2, column=1)
        self.br.grid(row=2, column=2)

    #begin connection to server
    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = "127.0.0.1"
        PORT = 2000
        self.client_socket.connect((HOST, PORT))

    #deleted the text in the text box so the user doesn't have to
    def text_delete(self):
        self.enter.delete(first=0, last=100)

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