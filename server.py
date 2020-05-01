#!/usr/bin/env python

import socket, _thread
from tkinter import Tk, Label, Button, Entry

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

#send a message from one user to another
def forward_message(conn, encoded_message):
	for user_conn in users.keys():
		if user_conn != conn:
			user_conn.send(encoded_message)

#user functionality
def handle_user(conn):
	global users

	#receive username
	encoded_username = conn.recv(1024)
	username = encoded_username.decode()
	print("{} connected.".format(username))

	#receive messages
	while True:
		encoded_message = conn.recv(1024)
		message = encoded_message.decode()
		if message == "exit":
			print("[{}]: {}".format(username, "* Left the session *"))
			remove_user(conn)
			break
		elif users[conn] == False:
			print("Wait until the other user takes their turn...")
		else:
			#send message to other user
			modified_message = "[{}]: {}".format(username, message)
			mod_encoded_message = modified_message.encode("utf-8")
			forward_message(conn, mod_encoded_message)

			#print message to server
			print("[{}]: {}".format(username, message))
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
		_thread.start_new_thread(handle_user, (conn,))

	#no client connected. Quietly halt server.
	except:
		break
