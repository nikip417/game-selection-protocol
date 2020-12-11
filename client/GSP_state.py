from command_list import CommandList, ACK, NAK

class State():
	""""
	STATEFULNESS
	The state object holds current user state information as well as performs all necessary checks to 
	ensure the user is using the network in the appropriate way
	"""


	def __init__(self):
		# client is not connected to GSP server, this is the initial state
		self.DISCONNECTED = 'DISCONNECTED'
		# client is connected to GSP server
		self.CONNECTED = 'CONNECTED'
		# user already has an account
		self.REGISTERED_USER = 'REGISTERED_USER'
		# user does not have an account
		self.UNREGISTERED_USER = 'UNREGISTERED_USER'
		# user is logged into GSP system
		self.LOGGED_IN = 'LOGGED_IN'
		# user has already accepted a game request but is awaiting game start
		self.COMMITED_TO_GAME = 'COMMITED_TO_GAME'
		# user has received a game request and is 'contemplating'
		self.CONTEMPLATING_GAME_PLAY = 'CONTEMPLATING_GAME_PLAY'
		# user is currently participating in a game
		self.PARTICIPATING_IN_GAME = 'PARTICIPATING_IN_GAME'

		# set the current state to disconnected
		self.current_state = self.DISCONNECTED

		# dictionary indicating what commands can be accepted in which states. This
		# provides the DFA validation enabling a layer of security for the client and 
		# the system
		self.state_map = {
			self.DISCONNECTED: [],
			self.CONNECTED: [CommandList.USER, CommandList.DCNT],
			self.UNREGISTERED_USER: [CommandList.PASS],
			self.REGISTERED_USER: [CommandList.LOGN],
			self.LOGGED_IN: [CommandList.GPO, CommandList.GPG, CommandList.REQ, CommandList.LGOT],
			self.COMMITED_TO_GAME: [CommandList.STRT, CommandList.QUIT],
			self.CONTEMPLATING_GAME_PLAY: [CommandList.ACPT, CommandList.DENY],
			self.PARTICIPATING_IN_GAME: [CommandList.MOVE, CommandList.END]
			}

	def initialize_server(self, user):
		"""
		When the server is initializing the state for a user the starting state is
		registered rather than disconnected which is the case when a client is 
		initializing state
		"""
		if user == 'server':
			self.current_state = self.REGISTERED_USER

	def command_validation(self, command):
		"""
		Check against state map to validate is a given command can be sent in a 
		given state
		"""
		valid_commands = self.state_map[self.current_state]
		if command in valid_commands:
			return True
		print('ERROR: Command', command, 'can not be sent in state', self.current_state)

	def update_state(self, msg):
		"""
		through the comparison of message received as well as the current state
		states are updated as a client goes through the protocol
		"""
		# print('NRP - Original State:', self.current_state)
		if msg == ACK.CONNECTED and self.current_state == self.DISCONNECTED:
			self.current_state = self.CONNECTED
		elif msg == ACK.USR_EXISTS and self.current_state == self.CONNECTED:
			self.current_state = self.REGISTERED_USER
		elif msg == NAK.NO_USR_EXISTS and self.current_state == self.CONNECTED:
			self.current_state = self.UNREGISTERED_USER
		elif msg == ACK.ACCT_CREATED and self.current_state == self.UNREGISTERED_USER:
			self.current_state = self.REGISTERED_USER
		elif msg == ACK.LOGGED_IN and self.current_state == self.REGISTERED_USER:
			self.current_state = self.LOGGED_IN
		elif msg == ACK.REQ_ACCEPTED and self.current_state == self.LOGGED_IN:
			self.current_state = self.COMMITED_TO_GAME
		elif (msg == ACK.REQ_RECV or msg == CommandList.REQ) and self.current_state == self.LOGGED_IN:
			self.current_state = self.CONTEMPLATING_GAME_PLAY
		elif msg == ACK.ACPT_SENT and self.current_state == self.CONTEMPLATING_GAME_PLAY:
			self.current_state = self.COMMITED_TO_GAME
		elif msg == ACK.DENY_SENT and self.current_state == self.CONTEMPLATING_GAME_PLAY:
			self.current_state = self.LOGGED_IN
		elif (msg == ACK.QUIT_SUCCESSFUL or msg == ACK.OPPONENT_QUIT) and self.current_state == self.COMMITED_TO_GAME:
			self.current_state = self.LOGGED_IN
		elif msg == NAK.REQ_DENIED and self.current_state == self.CONTEMPLATING_GAME_PLAY:
			self.current_state = self.LOGGED_IN
		elif (msg == ACK.STRT_SENT or msg == ACK.STRT_RECEIVED or msg == CommandList.STRT) and self.current_state == self.COMMITED_TO_GAME:
			self.current_state = self.PARTICIPATING_IN_GAME
		elif (msg == ACK.END_SENT or msg == ACK.END_RECEIVED or msg == CommandList.END) and self.current_state == self.PARTICIPATING_IN_GAME:
			self.current_state = self.LOGGED_IN
		elif msg == ACK.LOGGED_OUT and self.current_state == self.LOGGED_IN:
			self.current_state = self.CONNECTED
		elif msg == ACK.DSCT_RECEIVED and self.current_state == self.CONNECTED:
			self.current_state = self.DISCONNECTED

		# print('NRP - New State:', self.current_state)
				