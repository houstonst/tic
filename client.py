#!/usr/bin/env python

import socket

HOST = "127.0.0.1"
PORT = 2000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Connected to {}\n".format(HOST))
print("Type exit to quit connection\n")

while True:
    message = input()
    if message == "exit":
        break
    else:
        client_socket.sendall(message.encode("utf-8"))
    
client_socket.close()