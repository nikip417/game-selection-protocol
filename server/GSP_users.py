import threading
from command_list import ACK, NAK
from client.GSP_state import State


class GSPUsers():
	"""
	This is a class that is used by a server to track the users of the GSP Protocol. All user information is stored in the
	users dictionary. Within the dictionary the username, state information, available games, connection object and address 
	are stored
	"""

	sem = threading.Semaphore()
	users = {}

	@classmethod
	def check_for_user(cls, username):
		"""
		Ensure user exists in system
		"""
		if username in cls.users:
			return ACK.USR_EXISTS	
		return NAK.NO_USR_EXISTS

	@classmethod
	def add_user(cls, username, password):
		"""
		add user to the GSP system
		"""
		if username in cls.users:
			return NAK.USERNAME_EXISTS

		cls.sem.acquire()
		cls.users[username] = {}
		cls.users[username]['password'] = password
		cls.users[username]['games'] = []

		# initialize state obj and add to user information
		state = State()
		state.initialize_server('server')
		cls.users[username]['state'] = state

		cls.users[username]['connection'] = None
		cls.users[username]['address'] = None
		cls.sem.release()
		return ACK.ACCT_CREATED

	@classmethod
	def log_in(cls, username, password, games, conn, addr):
		"""
		log the user in on the system
		"""
		# ensure user exists
		user_exists = cls.check_for_user(username)
		if user_exists != ACK.USR_EXISTS:
			return user_exists
		
		# validate provided password
		user = cls.users[username]
		if password != user['password']:
			return NAK.LOG_IN_FAILED
		
		# update the connection information for the logged in user
		cls.sem.acquire()
		user['connection'] = conn
		user['address'] = addr
		if games:
			user['games'] = games
		cls.sem.release()
		print('User', username, 'has been logged in')

		# return an ack indicating successful login
		return ACK.LOGGED_IN

	@classmethod
	def get_possible_opponents(cls, username):
		"""
		Get and return all opponents that are in the logged in state
		"""
		possible_opponents = ""
		for user, user_info in cls.users.items():
			if user_info and user_info['state'].current_state == 'LOGGED_IN' and user != username:
				possible_opponents = possible_opponents + " " + user
		if not possible_opponents:
			return NAK.NO_OPPONENTS
		return possible_opponents

	@classmethod
	def get_possible_games(cls, opponent_username):
		"""
		Returns the games a user has provided that it can play
		"""
		# check if user exists in system
		opponent_status = cls.check_for_user(opponent_username)
		if opponent_status == NAK.NO_USR_EXISTS:
			return opponent_status
		games = cls.users[opponent_username]['games']
		
		# return a nak if no games have been specified
		if not games:
			return NAK.NO_GAMES_SPECIFIED
		return ' '.join(games)

	@classmethod
	def get_opponent_address(cls, opponent_username):
		"""
		returns the connection object for a user on the network enabling client to client
		communication using the server as a proxy
		"""
		return cls.users[opponent_username]['connection']

	@classmethod
	def validate_user(cls, username, hostname):
		"""
		On every interation the username of the client user is checked against the information
		the server already has on the user
		"""
		# check to see if there is user data to do checking against
		if username not in cls.users or not cls.users[username]['address']:
			return True
		# validate hostname with database
		if cls.users[username]['address'][0] == hostname:
			return True

	@classmethod
	def update_state(cls, username, message):
		"""
		Updates the state object associated with each user
		"""
		if username in cls.users:
			cls.users[username]['state'].update_state(message)

	@classmethod
	def validate_command(cls, username, command):
		"""
		validates if a command can be sent in the current users state
		"""
		if username in cls.users:
			return cls.users[username]['state'].command_validation(command)
		return True

