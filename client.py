#!/usr/bin/env python

import socket

#request username
print("Enter a username:")
username = input()

#specify network parameters
HOST = "127.0.0.1"
PORT = 2000

#establish socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Connected to {}.".format(HOST))
print("Type exit to quit connection.\n")

#send username
client_socket.send(username.encode("utf-8"))

#send messages
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
    
#close the connection
client_socket.close()