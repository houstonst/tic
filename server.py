#!/usr/bin/env python

import socket, _thread

#specify network parameters
HOST = "127.0.0.1"
PORT = 2000

#specify server parameters
users = {} #stored as {conn: boolean} to indicate whether it's their turn

#establish socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))

#define this as a listening socket
server_socket.listen()

#close server socket if users have all left the session
def close_session():
	print("Closing session...")
	server_socket.close()

#remove user function
def remove_user(conn):
	if conn in users:
		conn.close()
		users.pop(conn)
		if (len(users) == 0):
			close_session()

#user functionality
def handle_user(conn, addr):
	global users

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
			if users[conn] == False:
				print("Wait until the other user takes their turn...")
			else:
				print("[{}]: {}".format(readable_username, readable_data))
				users = {key: True for key in users}
				users[conn] = False

#run the server
while True:
	try:
		#accept new user connection
		conn, addr = server_socket.accept()

		#populate dictionary
		if True in users.values():
			users[conn] = False
		else:
			users[conn] = True

		#start a thread for the new client
		_thread.start_new_thread(handle_user, (conn, addr))

	#no client connected. Quietly halt server.
	except:
		break