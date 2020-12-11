import socket
import threading
from command_list import CommandList, ACK, NAK
from .GSP_commands import GSPCommands
from .GSP_client_command_callbacks import GSPClientCommandCallbacks
from .GSP_state import State


class GSPClient():
	"""
	This class handles all interactions with the GSP client including its creation
	and the sending of messages
	"""

	def __init__(self):
		self.TCP_PORT = 1058
		self.host = None
		self.servername = 'servername'
		self.sock = None
		self.version = '1.0'
		self.state = State()

	# SERVICE - defaults to hardoded ip
	def start(self, host_name=None, ip='127.0.0.1'):
		"""
		start client and connect to the GSP server
		argument name can be an ip or a hostname
		"""

		# CLIENT
		# If the user provided a hostname or ip use that to bind to the server
		if host_name:
			self.host = socket.gethostbyname(host_name)
		else:
			self.host = ip

		# create socket object
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((self.host, self.TCP_PORT))
			msg_recv = self.sock.recv(self.TCP_PORT).decode("utf-8")
			self.state.update_state(msg_recv)
			print("Successfully connected to the server")
		except:
			print("ERROR: There was an error trying to connect to the server")
			return

		GSPCommands.set_version(self.version)
		return True

	def send_command(self, command, command_msg):
		"""
		method to send commands to the server and wait for a response
		"""
		if not self.state.command_validation(command):
			return
		self.sock.send(bytes(command_msg, "utf-8"))
		msg_recv = self.sock.recv(self.TCP_PORT).decode("utf-8")
		if msg_recv == ACK.REQ_SENT:
			msg_recv = self.sock.recv(self.TCP_PORT).decode("utf-8")
		self.state.update_state(msg_recv)
		return msg_recv

	def does_account_exist(self, username):
		"""
		check if an account for the user exists
		"""
		command_msg = GSPCommands.USER(username, socket.gethostname(), self.servername)
		status = self.send_command(CommandList.USER, command_msg)
		return status == ACK.USR_EXISTS, status

	def log_in(self, username, password, games=None):
		"""
		log user in 
		"""
		command_msg = GSPCommands.LOGN(username, password, games)
		status = self.send_command(CommandList.LOGN, command_msg)
		return status == ACK.LOGGED_IN, status

	def create_account(self, username, password):
		"""
		create account for user
		"""
		command_msg = GSPCommands.PASS(username, password)
		status = self.send_command(CommandList.PASS, command_msg)
		return status == ACK.ACCT_CREATED, status

	def get_possible_opponents(self):
		"""
		get all possible opponents that are logged in
		return type is a list
		"""
		command_msg = GSPCommands.GPO()
		possible_opponents = self.send_command(CommandList.GPO, command_msg).split()
		return possible_opponents

	def get_possible_games(self, opponent_username):
		"""
		get the possible games that a user can play
		return type is a list
		"""
		command_msg = GSPCommands.GPG(opponent_username)
		possible_games = self.send_command(CommandList.GPG, command_msg).split()
		return possible_games

	def find_random_opponent(self, game):
		"""
		find all opponents that can participate in specified game
		"""
		opponents = self.get_possible_opponents()
		if opponents == NAK.NO_OPPONENTS:
			return False
		for opponent in opponents:
			games = self.get_possible_games(opponent)
			if game in games:
				return opponent, game

	def send_req_to_opponent(self, opponent_username, game):
		"""
		send request to opponent
		"""
		command_msg = GSPCommands.REQ(opponent_username, game)
		request_response = self.send_command(CommandList.REQ, command_msg)
		return request_response == ACK.REQ_ACCEPTED

	def send_req_accept(self, opponent_username, game):
		"""
		send accept response to game request
		"""
		command_msg = GSPCommands.ACPT(opponent_username, game)
		response = self.send_command(CommandList.ACPT, command_msg)
		return response

	def send_req_deny(self, opponent, game):
		"""
		send deny response to game request
		"""
		command_msg = GSPCommands.DENY(opponent, game)
		response = self.send_command(CommandList.DENY, command_msg)
		return response

	def send_start_message(self, opponent_username, game, starting_score, board):
		"""
		send message to start game to opponent
		"""
		checksum = 'checksum'
		command_msg = GSPCommands.STRT(opponent_username, game, starting_score, checksum, board)
		response = self.send_command(CommandList.STRT, command_msg)
		return response

	def send_move(self, opponent_username, game, starting_score, board):
		"""
		send game move to opponent
		"""
		checksum = 'checksum'
		command_msg = GSPCommands.MOVE(opponent_username, game, starting_score, checksum, board)
		response = self.send_command(CommandList.MOVE, command_msg)
		return response

	def start_listening(self):
		"""
		listen and wait for server messages
		"""
		print("Listening:")
		while True:
			msg_recv = self.sock.recv(self.TCP_PORT)
			if msg_recv:
				msg = GSPClientCommandCallbacks.read_client_msg(msg_recv)
				self.state.update_state(msg[0])
				if msg_recv == ACK.MOVE_SENT:
					msg_recv = self.sock.recv(self.TCP_PORT).decode("utf-8")
					msg = GSPClientCommandCallbacks.read_client_msg(msg_recv)
				return msg
			else:
				print('We seem to have lost connection with the server')
				self.stop()
				return

	def send_end_msg(self, opponent_username, game, winner, board):
		"""
		send command to end game
		"""
		command_msg = GSPCommands.END(opponent_username, game, winner, board)
		return self.send_command(CommandList.END, command_msg)

	def quit(self, opponent_username):
		"""
		send command to quit game
		"""
		command_msg = GSPCommands.QUIT(opponent_username)
		return self.send_command(CommandList.QUIT, command_msg)

	def log_out(self):
		"""
		send command to log out client user
		"""
		command_msg = GSPCommands.LGOT()
		return self.send_command(CommandList.LGOT, command_msg)

	def disconnect(self, username):
		"""
		send message to dicsonned client from the server
		"""
		# close socket
		command_msg = GSPCommands.DCNT(username, self.version)
		response = self.send_command(CommandList.DCNT, command_msg)
		self.stop()
		return response == ACK.DSCT_RECEIVED

	def stop(self):
		self.sock.close()


