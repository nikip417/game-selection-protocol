from command_list import CommandList

class GSPCommands():
	"""
	This class holds information on all commands that can be sent by a client on a GSP system.
	The primary goal of this class is to properly format all commands being sent from the client
	by ingesting the arguments required and returning the command to be sent
	"""

	version = None
	username = None

	@classmethod
	def set_version(cls, version):
		cls.version = version

	@classmethod
	def set_username(cls, username):
		cls.username = username

	@classmethod
	def create_command(cls, command, arguments):
		"""
		Takes in different command parameters and formats the arguments in a GSP sendable and readable
		command message
		"""
		command = str(cls.version) + " " + cls.username + " " + command
		if arguments:
			for arg in arguments:
				command = command + " " + str(arg)

		command = command + " crlf"
		return command
	
	@classmethod
	def USER(cls, username, hostname, servername):
		"""
		Method to create command message for USER method
		"""
		if not cls.username:
			cls.set_username(username)
		return cls.create_command(CommandList.USER, [cls.username, hostname, servername])

	@classmethod
	def PASS(cls, username, password):
		"""
		Method to create command message for PASS method
		"""
		if not cls.username:
			cls.set_username(username)
		return cls.create_command(CommandList.PASS, [password])

	@classmethod
	def LOGN(cls, username, password, games=None):
		"""
		Method to create command message for LOGN method
		"""
		if not cls.username:
			cls.set_username(username)
		args = [password]
		if games:
			args.extend(games)

		return cls.create_command(CommandList.LOGN, args)

	@classmethod
	def GPO(cls):
		"""
		Method to create command message for GPO method
		"""
		return cls.create_command(CommandList.GPO, [])

	@classmethod
	def GPG(cls, opponent_username):
		"""
		Method to create command message for GPG method
		"""
		return cls.create_command(CommandList.GPG, [opponent_username])

	@classmethod
	def REQ(cls, opponent_username, game):
		"""
		Method to create command message for REQ method
		"""
		return cls.create_command(CommandList.REQ, [opponent_username, game])

	@classmethod
	def ACPT(cls, opponent_username, game):
		"""
		Method to create command message for ACPT method
		"""
		print("Please wait for player one to start the game, you are player 2")
		return cls.create_command(CommandList.ACPT, [opponent_username, game])

	@classmethod
	def DENY(cls, opponent_username, game):
		"""
		Method to create command message for DENY method
		"""
		print('NRP - denied')
		return cls.create_command(CommandList.DENY, [opponent_username, game])

	@classmethod
	def STRT(cls, opponent_username, game, score, checksum, game_state):
		"""
		Method to create command message for STRT method
		"""
		# return cls.create_command(CommandList.STRT, [opponent_username, game])
		return cls.create_command(CommandList.STRT, [opponent_username, game, score, checksum, game_state])

	@classmethod
	def MOVE(cls, opponent_username, game, score, checksum, game_state):
		"""
		Method to create command message for MOVE method
		"""
		return cls.create_command(CommandList.MOVE, [opponent_username, game, score, checksum, game_state])

	@classmethod
	def END(cls, opponent_username, game, winner, board):
		"""
		Method to create command message for END method
		"""
		return cls.create_command(CommandList.END, [opponent_username, game, winner, board])

	@classmethod
	def QUIT(cls, opponent_username):
		"""
		Method to create command message for QUIT method
		"""
		return cls.create_command(CommandList.QUIT, [opponent_username])

	@classmethod
	def LGOT(cls):
		"""
		Method to create command message for LGOT method
		"""
		return cls.create_command(CommandList.LGOT, [])

	@classmethod
	def DCNT(cls, username, version):
		"""
		Method to create command message for DCNT method
		"""
		return str(version) + " " + username + " " + CommandList.DCNT
		# return cls.create_command(CommandList.DCNT, [])



