from command_list import CommandList, NAK, ACK
from .GSP_users import GSPUsers

class GSPServerCommandCallbacks():
	"""
	This command callback class for the GSP server enables the interpretation of the
	commands received by the server from clients
	"""
	version = None
	port = None

	@classmethod
	def set_version_and_port(cls, version, port):
		cls.version = version
		cls.port = port

	@classmethod
	def check_version(cls, version):
		if cls.version == version:
			return True

	@classmethod
	def read_client_msg(cls, message, conn=None, addr=None):
		"""
		Break up the received message based on the basic breakdown of messages that
		are sent accross the GSP Network
		The folloing is the basic breakdown of a message:
		<message> ::= <version> <sp> <username> <sp> <command> <sp> <arguments> <crlf>
		"""
		components = message.decode("utf-8").split()
		version = components[0]
		cls.check_version(version)
		username = components[1]
		if not GSPUsers.validate_user(username, addr[0]):
			return
		command = components[2]
		if not GSPUsers.validate_command(username, command):
			return
		arguments = components[3:]

		return_msg = cls.command_callback(username, command, arguments, conn, addr)
		GSPUsers.update_state(username, return_msg)
		return return_msg

	@classmethod
	def command_callback(cls, username, command, arguments, conn, addr):
		"""
		Based on the command received, call the appropriate callback method
		"""
		if command == CommandList.USER:
			return cls.USER_callback(username, arguments);
		elif command == CommandList.PASS:
			return cls.PASS_callback(username, arguments);
		elif command == CommandList.LOGN:
			return cls.LOGN_callback(username, arguments, conn, addr);
		elif command == CommandList.GPO:
			return cls.GPO_callback(username);
		elif command == CommandList.GPG:
			return cls.GPG_callback(username, arguments);
		elif command == CommandList.REQ:
			return cls.REQ_callback(username, arguments);
		elif command == CommandList.ACPT:
			return cls.ACPT_callback(username, arguments);
		elif command == CommandList.DENY:
			return cls.DENY_callback(username, arguments);
		elif command == CommandList.STRT:
			return cls.STRT_callback(username, arguments);
		elif command == CommandList.MOVE:
			return cls.MOVE_callback(username, arguments);
		elif command == CommandList.END:
			return cls.END_callback(username, arguments);
		elif command == CommandList.QUIT:
			return cls.QUIT_callback(username, arguments);
		elif command == CommandList.LGOT:
			return cls.LGOT_callback(username);
		elif command == CommandList.DCNT:
			return cls.DCNT_callback(username);
	
		else:
			print("something is wrong")

	@classmethod
	def USER_callback(cls, username, arguments):
		"""
		Callback method for the USER command
		"""
		username = arguments[0]
		return GSPUsers.check_for_user(username)

	@classmethod
	def PASS_callback(cls, username, arguments):
		"""
		Callback method for the PASS command
		"""
		password = arguments[0]
		return GSPUsers.add_user(username, password)

	@classmethod
	def LOGN_callback(cls, username, arguments, conn, addr):
		"""
		Callback method for the LOGN command
		extracts any specified games from the arguments
		"""
		password = arguments[0]
		if len(arguments)>1:
			remaining = arguments[1:len(arguments)-1]
			games = []
			for game in remaining:
				games.append(game)
		return GSPUsers.log_in(username, password, games, conn, addr)

	@classmethod
	def GPO_callback(cls, username):
		"""
		Callback method for the GPO (Get Possible Opponents) command
		"""
		return GSPUsers.get_possible_opponents(username)

	@classmethod
	def GPG_callback(cls, username, arguments):
		"""
		Callback method for the GPG (Get Possible Games) command
		"""
		opponent_username = arguments[0]
		return GSPUsers.get_possible_games(opponent_username)

	@classmethod
	def REQ_callback(cls, username, arguments):
		"""
		Callback method for the REQ command
		returns an ACK to the user sending the REQ
		"""
		opponent_username = arguments[0]
		requested_game = arguments[1]
		
		# get connection information of desired opponent
		opponent_conn = GSPUsers.get_opponent_address(opponent_username)
		
		# send message to opponent, validate command and update state
		command = cls.REQ(username, opponent_username, requested_game)
		if not GSPUsers.validate_command(username, CommandList.REQ):
			return
		GSPUsers.update_state(opponent_username, CommandList.REQ)
		opponent_conn.send(bytes(command, "utf-8"))

		# update sender state and send reponse 
		GSPUsers.update_state(username, ACK.REQ_SENT)
		return ACK.REQ_SENT
		 
	@classmethod
	def ACPT_callback(cls, username, arguments):
		"""
		Callback method for the ACPT command
		returns an ACK to the user sending the ACPT
		"""
		opponent_username = arguments[0]

		# get connection information of desired opponent
		opponent_conn = GSPUsers.get_opponent_address(opponent_username)
		
		# send message to opponent and update state
		GSPUsers.update_state(opponent_username, ACK.REQ_ACCEPTED)
		opponent_conn.send(bytes(ACK.REQ_ACCEPTED, "utf-8"))

		# update sender state and send reponse 
		GSPUsers.update_state(username, ACK.ACPT_SENT)
		return ACK.ACPT_SENT

	@classmethod
	def DENY_callback(cls, username, arguments):
		"""
		Callback method for the DENY command
		returns an ACK to the user sending the DENY
		"""
		opponent_username = arguments[0]

		# get connection information of desired opponent
		opponent_conn = GSPUsers.get_opponent_address(opponent_username)
		
		# send message to opponent and update state
		GSPUsers.update_state(opponent_username, ACK.REQ_DENIED)
		opponent_conn.send(bytes(ACK.REQ_DENIED, "utf-8"))

		# update sender state and send reponse 
		GSPUsers.update_state(username, ACK.DENY_SENT)
		return ACK.DENY_SENT

	@classmethod
	def STRT_callback(cls, username, arguments):
		"""
		Callback method for the STRT command
		returns an ACK to the user sending the STRT
		"""
		opponent_username = arguments[0]
		game = arguments[1]
		score = arguments[2]
		checksum = arguments[3]
		board = arguments[4]

		# get connection information of desired opponent
		opponent_conn = GSPUsers.get_opponent_address(opponent_username)

		# send message to opponent, validate command and update state
		start_response = cls.STRT(username, opponent_username, game, score, checksum, board)
		if not GSPUsers.validate_command(username, CommandList.STRT):
			return
		GSPUsers.update_state(opponent_username, CommandList.STRT)
		opponent_conn.send(bytes(start_response, "utf-8"))

		# update sender state and send reponse 
		GSPUsers.update_state(username, ACK.STRT_SENT)
		return ACK.STRT_SENT

	@classmethod
	def MOVE_callback(cls, username, arguments):
		"""
		Callback method for the MOVE command
		returns an ACK to the user sending the MOVE
		"""
		opponent_username = arguments[0]
		game = arguments[1]
		score = arguments[2]
		checksum = arguments[3]
		board = arguments[4]

		# get connection information of desired opponent
		opponent_conn = GSPUsers.get_opponent_address(opponent_username)

		# send message to opponent and validate command
		move = cls.MOVE(username, opponent_username, game, score, checksum, board)
		if not GSPUsers.validate_command(username, CommandList.MOVE):
			return
		# GSPUsers.update_state(opponent_username, CommandList.MOVE)
		opponent_conn.send(bytes(move, "utf-8"))

		# update sender state and send reponse 
		GSPUsers.update_state(username, ACK.MOVE_SENT)
		return ACK.MOVE_SENT

	@classmethod
	def END_callback(cls, username, arguments):
		"""
		Callback method for the END command
		returns an ACK to the user sending the END
		"""
		opponent_username = arguments[0]
		game = arguments[1]
		winner = arguments[2]
		board = arguments[3]

		# get connection information of desired opponent
		opponent_conn = GSPUsers.get_opponent_address(opponent_username)

		# send message to opponent, validate command and update state
		msg = cls.END(username, opponent_username, game, winner, board)
		if not GSPUsers.validate_command(username, CommandList.END):
			return
		GSPUsers.update_state(opponent_username, CommandList.END)
		opponent_conn.send(bytes(msg, "utf-8"))

		# update sender state and send reponse 
		GSPUsers.update_state(username, ACK.END_SENT)
		return ACK.END_SENT

	@classmethod
	def QUIT_callback(cls, username, arguments):
		"""
		Callback method for the QUIT command
		returns an ACK to the user sending the QUIT
		"""
		opponent_username = arguments[0]

		# get connection information of desired opponent
		opponent_conn = GSPUsers.get_opponent_address(opponent_username)

		# send message to opponent and update state
		GSPUsers.update_state(opponent_username, ACK.OPPONENT_QUIT)
		opponent_conn.send(bytes(ACK.OPPONENT_QUIT, "utf-8"))

		# update sender state and send reponse 
		GSPUsers.update_state(username, ACK.QUIT_SUCCESSFUL)
		return ACK.QUIT_SUCCESSFUL

	@classmethod
	def LGOT_callback(cls, username):
		"""
		Callback method for the LGOT command
		returns an ACK to the user sending the LGOT
		"""
		print('User',username, 'is now logged out')
		return ACK.LOGGED_OUT

	@classmethod
	def DCNT_callback(cls, username):
		"""
		Callback method for the DCNT command
		returns an ACK to the user sending the DCNT
		"""
		print('User',username, 'is now disconnedted')
		return ACK.DSCT_RECEIVED

	@classmethod
	def REQ(cls, username, opponent_username, game):
		"""

		"""
		return cls.create_command(username, CommandList.REQ, [opponent_username, game])

	@classmethod
	def STRT(cls, username, opponent_username, game, score, checksum, game_state):
		"""
		
		"""
		return cls.create_command(username, CommandList.STRT, [opponent_username, game, score, checksum, game_state])	

	@classmethod
	def MOVE(cls, username, opponent_username, game, score, checksum, game_state):
		"""
		
		"""
		return cls.create_command(username, CommandList.MOVE, [opponent_username, game, score, checksum, game_state])	

	@classmethod
	def END(cls, username, opponent_username, game, winner, board):
		"""
		
		"""
		return cls.create_command(username, CommandList.END, [opponent_username, game, winner, board])

	@classmethod
	def create_command(cls, username, command, arguments):
		"""
		Takes in different command parameters and formats the arguments in a GSP sendable and readable
		command message
		"""
		command = str(cls.version) + " " + username + " " + command
		if arguments:
			for arg in arguments:
				command = command + " " + str(arg)

		command = command + " crlf"
		return command


