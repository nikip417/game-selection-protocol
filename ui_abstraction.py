from client.GSP_client import GSPClient
from command_list import ACK, NAK 

class UIAbstract():
	gsp_client = None

	@classmethod
	def connect_to_GSP_server(cls, host_name=None, ip=None):
		cls.gsp_client = GSPClient()
		if not cls.gsp_client.start(host_name, ip):
			return
		return cls.gsp_client

	@classmethod
	def disconnect_from_GSP_server(cls, username):
		cls.gsp_client.disconnect(username)
		cls.gsp_client = None

	@classmethod
	def user_log_in(cls, username, password, game):
		if not cls.gsp_client.does_account_exist(username)[0]:
			if not cls.gsp_client.create_account(username, password)[0]:
				return False, 'Unfortunately your account could not be created, please try again later'
			print('An account has been created for user', username)

		if not cls.gsp_client.log_in(username, password, game):
			return False, "There was an error logging into your account"

		return True, 'User', username, 'has successfully logged in \n'

	@classmethod
	def log_out(cls):
		return cls.gsp_client.log_out()

	@classmethod
	def listen_for_req(cls):
		message = cls.gsp_client.start_listening()
		return message[0] == ACK.REQ_RECV, message

	@classmethod
	def send_req_resp(cls, response, opponent, game):
		if response:
			return cls.gsp_client.send_req_accept(opponent, game)
		# return cls.gsp_client.send_req_deny(opponent, game)
		return cls.gsp_client.send_req_deny(opponent, game)

	@classmethod
	def get_opponent_for_game(cls, game):
		opponent, game = cls.gsp_client.find_random_opponent(game)
		if not opponent:
			return False, None, 'No opponents found, will wait for for an opponent to iniate a game'
		return cls.gsp_client.send_req_to_opponent(opponent, game), opponent, game

	@classmethod
	def quit_game(cls, opponent):
		return cls.gsp_client.quit(opponent)

	@classmethod
	def start_game(cls, opponent, game, score, board):
		return cls.gsp_client.send_start_message(opponent, game, score, board)

	@classmethod
	def send_move(cls, opponent, game, score, board):
		return cls.gsp_client.send_move(opponent, game, score, board)

	@classmethod
	def recv_move(cls):
		message, args = cls.gsp_client.start_listening()
		if message == ACK.END_RECEIVED:
			return args[0], args[1], args[2], args[3]
		return args[0], args[1], args[2], args[4]

	@classmethod
	def game_over_msg(cls, opponent, game, winner, board):
		return cls.gsp_client.send_end_msg(opponent, game, winner, board)



