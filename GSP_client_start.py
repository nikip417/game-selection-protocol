from ui_abstraction import UIAbstract
from tic_tac_toe_app import TicTacToe
import time

# NRP - All the hardcoded vars I will be deleting later
# username = 'nikip417'
# password = 'heynow'
games = 'tic_tac_toe'.split(" ")
desired_game = 'tic_tac_toe'


def main():
	"""
	UI
	This is the user interface integrated with a test tic-tac-toe application. The user will connect to, create an account with and
	then log into the GSP server through this interface simply by answering prompts. 
	"""

	# create a commenction with the GSP server
	ip = '192.168.0.102'
	print('connecting to GSP server through address',ip)
	gsp_client = UIAbstract.connect_to_GSP_server(host_name=ip)
	if not gsp_client:
		return

	# Log in to the GSP system
	print('Please begin by entering a username, password and any games you will be willing to play', 
		'\nIf an account does not exist, one will be created for you',
		'\nGames should be entered in a space seperated list. Ex. hi_five tic_tac_toe connect_four\n')	
	username = input('Username: ')
	password = input('Password: ')
	# games = input('Games: ').split(" ")
	
	log_in_stat = UIAbstract.user_log_in(username, password, games)
	print(log_in_stat)
	if not log_in_stat[0]:
		return

	# start a loop that will allow users to play multiple games
	while True:
		initiate_game = input('\nWould you like to initiate a game? (yes/no): ')

		# if the user does not want to initiate just sit and wait
		if initiate_game != 'yes':
			print('Waiting for an opponent to iniate a game')
			while True:
				req = UIAbstract.listen_for_req()
				
				# request has been received, please reject or accept
				if req[0]:
					 UIAbstract.send_req_resp(input('Would you like to play a game of ' + str(req[1][2]) + ' with opponent ' + str(req[1][1]) + ' (yes/no)\n') == 'yes', str(req[1][1]), str(req[1][2]))
				else:
					print('\nStarting Game')
					args = req[1][1]
					if args[1] == 'tic_tac_toe':
						game_obj = TicTacToe()
					else:
						print("You do not have this game")
						return

					# exit once the game has ended
					start_game(username, args[0], game_obj, False)
					break

		else:
			# search for opponents to play games with
			print('Searching for an opponent who can play', desired_game)
			success, opponent, game = UIAbstract.get_opponent_for_game(desired_game)
			
			if not success:
				print('\n', game)
				return

			# initialize the game
			if game == 'tic_tac_toe':
				game_obj = TicTacToe()
			else:
				print("You do not have this game")
				return
			print('Your opponent will be', opponent, 'and you will be playing', game)

			# give signal to start game when ready
			if input('\nWould you like to start the game? (yes/no) ') == 'yes':
				if not UIAbstract.start_game(opponent, game, game_obj.score, game_obj.board):
					return
				start_game(username, opponent, game_obj, True)

		print('GAME OVER')

		if input('\nWould you like to play another game? (yes/no): ') != 'yes':
			break
			
	# when the user no longer wants to play games they will log out and then disconnect
	UIAbstract.log_out()
	UIAbstract.disconnect_from_GSP_server(username)

def start_game(username, opponent, game_obj, first_player):
	# if you are the first player take the first turn
	if first_player:
		game_obj.start('x')
		new_board = game_obj.take_turn()
		UIAbstract.send_move(opponent, game_obj.name, game_obj.score, new_board)
	else:
		game_obj.start('o')

	# loop where the players keep taking turns until someone wins
	while game_obj.check_winner()==False:
		print("Waiting for player to take their turn")
		opponent, game, score, board = UIAbstract.recv_move()

		# check to see if the other opponent won or you guys tied
		if score == opponent or score == 'draw':
			print("You lost")
			game_obj.print_final_board(board)
			return True

		# take turn
		new_board = game_obj.take_turn(board)
		if game_obj.check_winner()!=False:
			break 
		UIAbstract.send_move(opponent, game_obj.name, game_obj.score, new_board)
	
	if game_obj.check_winner():
		# if you won
		UIAbstract.game_over_msg(opponent, game_obj.name, username, game_obj.uninterpret_board())
	else:
		# if you tied
		UIAbstract.game_over_msg(opponent, game_obj.name, 'draw', game_obj.uninterpret_board())

if __name__ == "__main__":
	main()
