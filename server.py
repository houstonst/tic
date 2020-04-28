#!/usr/bin/env python

import socket, _thread

#specify network parameters
HOST = "127.0.0.1"
PORT = 2000

#establish socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))

#connect to client
server_socket.listen()
conn, addr = server_socket.accept()

#receive username
username = conn.recv(1024)
readable_username = username.decode()
print("{} connected.".format(readable_username))

#receive messages
while True:
	data = conn.recv(1024)
	readable_data = data.decode()
	if readable_data == "exit":
		break
	else:
		print("[{}]: {}".format(readable_username, readable_data))

#close the connection
conn.close()
server_socket.close()