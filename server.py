#!/usr/bin/env python

import socket, _thread
from tkinter import Tk, Label, Button, Entry

#specify network parameters
HOST = "127.0.0.1"
PORT = 2000

#specify server parameters
users = []
is_turn = {0: True, 1: False}

#establish socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))

#define this as a listening socket
server_socket.listen(2)

#close server socket if users have all left the session
def close_session():
    print("Closing session...")
    server_socket.close()

#remove user function
def remove_user(conn):
    if conn in users:
        conn.close()
        users.remove(conn)
        if (len(users) == 0):
            close_session()

#user functionality
def handle_user(conn, addr, num):
    #receive username
    username = conn.recv(1024)
    readable_username = username.decode()
    print("{} connected.".format(readable_username))

    #receive messages
    while True:
        data = conn.recv(1024)
        readable_data = data.decode()
        if readable_data == "exit":
            remove_user(conn)
            break
        else:
            if is_turn[num] == False:
                print("Wait until the other user takes their turn...")
            else:
                print("[{}]: {}".format(readable_username, readable_data))
            if num == 0:
                is_turn[num] = False
                is_turn[num+1] = True
            else:
                is_turn[num] = False
                is_turn[num-1] = True
            #after they print something, is_turn = false
            #other users is_turn = true
        #run the server
while True:
    try:
        #accept new users
        conn, addr = server_socket.accept()
        # if conn.recv(1024).decode() == "exit":
        #     break
        # break
        users += [conn]
        num = users.index(conn)

        #start a thread for the new client
        _thread.start_new_thread(handle_user, (conn, addr, num))
    except:
        break
