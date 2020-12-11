from command_list import CommandList, ACK


class GSPClientCommandCallbacks():
	"""
	This command callback class for clients enables the interpretation of commands received
	by a client
	"""
	version = None

	@classmethod
	def set_version(cls, version):
		cls.version = version
		print("version set")

	@classmethod
	def check_version(cls, version):
		if cls.version == version:
			return True

	@classmethod
	def read_client_msg(cls, message):
		"""
		Break up the received message based on the basic breakdown of messages that
		are sent accross the GSP Network
		The folloing is the basic breakdown of a message:
		<message> ::= <version> <sp> <username> <sp> <command> <sp> <arguments> <crlf>
		"""
		components = message.decode("utf-8").split()

		# if an Ack or Nak was received, handle appropriately
		if components[0] == ACK.ACPT_SENT or components[0] == ACK.DENY_SENT:
			return components[0]

		cls.check_version(components[0])
		# TODO - username hostname check
		username = components[1]
		command = components[2]
		arguments = components[3:]
		return cls.command_callback(username, command, arguments)
	
	@classmethod
	def command_callback(cls, username, command, arguments):
		"""
		Based on the command received call the appropriate callback method
		"""
		if command == CommandList.REQ:
			return cls.REQ_callback(username, arguments);
		elif command == CommandList.STRT:
			return cls.STRT_callback(username, arguments)
		elif command == CommandList.MOVE:
			return cls.MOVE_callback(username, arguments)
		elif command == CommandList.END:
			return cls.END_callback(username, arguments)
		else:
			print("something is wrong")

	@classmethod
	def REQ_callback(cls, username, arguments):
		"""
		Callback method for the REQ command
		"""
		opponent_username = arguments[0]
		requested_game = arguments[1]
		return ACK.REQ_RECV, username, requested_game

	@classmethod
	def STRT_callback(cls, username, arguments):
		"""
		Method to create command message for STRT method
		"""
		opponent_username = username
		game = arguments[1]
		score = arguments[2]
		checksum = arguments[3]
		game_state = arguments[4]
		return ACK.STRT_RECEIVED, arguments

	@classmethod
	def MOVE_callback(cls, username, arguments):
		"""
		Method to create command message for MOVE method
		"""
		# update the opponent name to the username of the sender
		arguments[0] = username
		game = arguments[1]
		score = arguments[2]
		checksum = arguments[3]
		game_state = arguments[4]
		return ACK.MOVE_RECEIVED, arguments

	@classmethod
	def END_callback(cls, username, arguments):
		"""
		Method to create command message for END method
		"""
		print('we out here')
		opponent_username = username
		game = arguments[1]
		winner = arguments[2]
		board = arguments[3]
		return ACK.END_RECEIVED, [opponent_username, game, winner, board]



