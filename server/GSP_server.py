import socket
import threading
from .GSP_server_command_callbacks import GSPServerCommandCallbacks
from command_list import ACK

class GSPServer():
	"""
	GSP Server base class. This class starts the server and handles incoming messages
	from multiple clients by creating a thread to handle each interaction
	"""

	def __init__(self):
		self.TCP_PORT = 1058
		# SERVICE - server has hardcoded ip
		self.host = '192.168.0.102'
		self.sock = None
		self.version = '1.0'
		self.connections = {}

	def start(self):
		"""
		Create Socket to start up the server and handle connetions from multiple clients
		"""
		# Create socket object on binding and listening on the specified port over TCP
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.bind((self.host, self.TCP_PORT))
			self.sock.listen()
		except:
			print("ERROR: Server failed to start")
		
		print("The GSP server is listening")
		GSPServerCommandCallbacks.set_version_and_port(self.version, self.TCP_PORT)

		# CONCURRENT
		# For every client connection spawn a thread to handle further interactions
		while True:
			conn, addr = self.sock.accept()
			self.connections[conn] = addr
			conn.send(bytes(ACK.CONNECTED, "utf-8"))
			print("Received connection from client", addr)
			threading.Thread(target=self.start_listening, args=(conn,)).start()

	def start_listening(self, conn):
		"""
		Once client connection is established, wait and listen for messages from the 
		client and interprest ech command to handle it appropriately
		"""
		while True:
			command = conn.recv(self.TCP_PORT)
			if command:
				# Interpret received message
				return_msg = GSPServerCommandCallbacks.read_client_msg(command, conn, self.connections[conn])
				conn.send(bytes(return_msg, "utf-8"))
				if return_msg == ACK.DSCT_RECEIVED:
					conn.close()
					return
			else:
				print("It is possible the client has disconnected")
				conn.close()
				return

		self.stop()

	def stop(self):
		# close socket
		print("Shutting down GSP server")
		self.sock.close()



