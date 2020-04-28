#!/usr/bin/env python

import socket, _thread

HOST = "127.0.0.1"
PORT = 2000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()
conn, addr = server_socket.accept()
print("Connected by" + str(addr) + "\n")
while True:
	data = conn.recv(1024)
	readable_data = data.decode()
	if not data:
		break
	elif readable_data == "exit":
		break
	else:
		print(data.decode())

conn.close()
server_socket.close()