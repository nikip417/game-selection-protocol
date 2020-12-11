class TicTacToe():
	"""
	TicTacToe game application lives inside of this class. The methods in this method are called bu the GSP UI to successfully play a game
	of tic-tac-toe and determine a winner
	"""

	def __init__(self):
		self.score = '0-0'
		self.initial_board = [['-','-','-'],['-','-','-'],['-','-','-']]
		self.board = self.initial_board
		self.name = 'tic_tac_toe'

	def start(self, marker):
		"""
		Begin the game by printing the instructions for the user to read and recording the marker that will be
		used by the player
		"""
		self.marker = marker
		self.print_instructions()

	def print_instructions(self):
		"""
		Print the instrctions for the user to see
		"""
		print('\n\n==========================================================================')
		print('==========================================================================\n')
		print('Welcome to Tic Tac Toe, the came you know and love. \nThe rules are the same ones you know and love. \nTo make a move just type the coordinates of the spot like so - row,column. \nNo spaces please! Lets go ahead and start! Here is a picuter of the board with some coordinates just in case!\n')
		print('=====================')
		print('|| 0,0 | 0,1 | 0,2 ||')
		print('  -----------------')
		print('|| 1,0 | 1,1 | 1,2 ||')
		print('  -----------------')
		print('|| 2,0 | 2,1 | 2,2 ||')
		print('=====================')
		print('\n==========================================================================')
		print('==========================================================================\n\n')

	def print_board(self, board=None):
		"""
		Print the current board or a board for the user to be able to see the state of the game in a easily 
		readable way
		"""
		if not board:
			board = self.board

		for i in range(len(board)):
			row = '|'
			for j in range(len(board[i])):
				row = row + str(board[i][j]) + '|'
			print(row)
		print()

	def make_move(self, row, column):
		"""
		Takes the move given by user and reflects it in the game state
		"""
		if self.board[int(row)][int(column)] == '-':
			self.board[int(row)][int(column)] = self.marker
		else:
			print("That spot is occupied, you messed up, you lose your turn for doing bad things")

	def check_winner(self):
		"""
		Check the board to see if there is a winner
		"""
		if self.check_diagonals() or self.check_rows() or self.check_columns():
			return True
		elif self.board_is_full():
			print("There was a draw, everyone lost")
			return None
		return False

	def take_turn(self, updated_board=None):
		"""
		This method gives the user any information they need to take a turn and then
		prompts them to make a move. Returns a string interprettion of the game state
		"""

		# print the current board for the user to see the current state of the game
		print("You are player", self.marker)
		if updated_board:
			self.board = self.interpret_board(updated_board)
		self.print_board()

		# Record the move a user wants to take and execute it
		row, col = input("Make your move: ").split(',')
		print("\nYour input was:", row, col)
		self.make_move(row, col)
		print('Your move has been recorded')

		# print board so user can see the updated game state
		self.print_board()
		return self.uninterpret_board()

	def board_is_full(self):
		"""
		Check to see if all spaces on the board have been occupied resulting
		in a draw
		"""
		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				if self.board[i][j] == '-':
					return False
		return True


	def check_diagonals(self):
		"""
		Check the diagonals to see if current player has won
		"""
		diags = [[(0,0), (1,1), (2,2)], [(0,2), (1,1), (2,0)]]

		for diag in diags:
			pts = 0
			for loc in diag:
				if self.board[loc[0]][loc[1]] == self.marker:
					pts+=1
			if pts == 3:
				print('WE WON')
				return True

	def check_rows(self):
		"""
		Check the rows to see if current player has won
		"""
		for i in range(len(self.board)):
			pts = 0
			for j in range(len(self.board[i])):
				if self.board[i][j] == self.marker:
					pts+=1
			if pts == 3:
				print('YOU WON')
				return True

	def check_columns(self):
		"""
		Check the columns to see if current player has won
		"""
		i=0
		for i in range(len(self.board[i])):
			pts = 0
			for j in range(len(self.board)):
				if self.board[j][i] == self.marker:
					pts+=1
			if pts == 3:
				print('YOU WON')
				return True

	def interpret_board(self, board):
		"""
		Take single string representation of game state and represent as a single 2D 
		array once again
		"""
		new_board = []
		row = []
		for i, v in enumerate(str(board)):
			row.append(v)
			if (i+1)%3==0:
				new_board.append(row)
				row = []

		return new_board

	def uninterpret_board(self):
		"""
		Take game state and represent it as a single string rather than a 2D 
		array for messaginf purposes
		"""
		board_string = ''
		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				board_string+=self.board[i][j]

		return board_string

	def print_final_board(self, board):
		"""
		Take the string interpretation of the winning/losing board state and print to screen 
		for user to see
		"""
		interpreted = self.interpret_board(board)
		self.print_board(interpreted)

