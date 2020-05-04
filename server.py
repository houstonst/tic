#!/usr/bin/env python

import socket, _thread

class Server:
	def __init__(self):
		#specify network parameter
		HOST = "127.0.0.1"
		PORT = 2000

		#specify server parameters
		self.users = {} #stored as {socket connection: boolean} to indicate whether it's their turn
		self.symbols = ["X", "O"]
		#establish socket
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_socket.bind((HOST, PORT))

		#define this as a listening socket
		self.server_socket.listen()

	#close server socket if users have all left the session
	def close_session(self):
	    print("Closing session...")
	    self.server_socket.close()

	#remove user function
	def remove_user(self, conn):
		if conn in self.users:
			conn.close()
			self.users.pop(conn)
			if (len(self.users) == 0):
				self.close_session()

	#send a message from one user to another
	def forward_message(self, conn, encoded_message):
		for user_conn in self.users.keys():
			if user_conn != conn:
				user_conn.send(encoded_message)

	def symbol_message(self, conn, encoded_message):
		conn.send(encoded_message)

	#user functionality
	def handle_user(self, conn):
		#receive username
		user_symbol = self.symbols[list(self.users).index(conn)]
		self.symbol_message(conn, user_symbol.encode('utf-8'))
		encoded_username = conn.recv(1024)
		username = encoded_username.decode()
		print("{} connected.".format(username))
		print("{} is {}'s".format(username, user_symbol))

		#receive messages
		while True:
			encoded_message = conn.recv(1024)
			message = encoded_message.decode()
			if message == "exit":
				print("[{}]: {}".format(username, "Left the session."))
				self.remove_user(conn)
				break
			elif self.users[conn] == False:
				print("Wait until the other user takes their turn...")
			else:
				#send message to other user
				modified_message = message
				mod_encoded_message = modified_message.encode("utf-8")
				self.forward_message(conn, mod_encoded_message)

				#print message to server
				print("[{}]: {}".format(username, message))
				self.users = {key: True for key in self.users}
				self.users[conn] = False

	#run the server
	def run_server(self):
		while True:
			try:
				#accept new user connection
				conn, addr = self.server_socket.accept()

				#populate dictionary
				if True in self.users.values():
					self.users[conn] = False
				else:
					self.users[conn] = True

				#start a thread for the new client
				_thread.start_new_thread(self.handle_user, (conn,))

			#no client connected. Quietly halt server.
			except:
				break

#starts the server
server = Server()
server.run_server()