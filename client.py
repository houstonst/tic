#!/usr/bin/env python

import socket, _thread

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

#receive message thread
def receive_messages():
    while True:
        try:
            encoded_message = client_socket.recv(1024)
            print(encoded_message.decode())
        except:
            break

#run client
while True:
    #talk and listen simultaneously
    _thread.start_new_thread(receive_messages, ())
    
    #form message
    message = input()
    encoded_message = message.encode("utf-8")
    
    #interpret message
    if message == "exit":
        client_socket.sendall(encoded_message) #gives "exit" to server which handles the message as a close socket command
        break
    else:
        client_socket.sendall(encoded_message)
        
    
#close the connection
client_socket.close()