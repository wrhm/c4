# c4.py
# Connect-4 implementation
# Date created: 20 Oct 2017
#  Last edited: 26 Oct 2017

from random import randint as ri

board = []
board_height = 6
board_width = 7

human_piece = '@'
computer_piece = '#'
open_space = '_'
pieces = human_piece + computer_piece

for nrow in xrange(board_height):
	board.append([open_space for i in xrange(board_width)])

def display(b):
	print(' 0 1 2 3 4 5 6')
	print('+%s+'%('-'*13))
	for i in xrange(len(board)):
		print('|%s|'%('|'.join(board[i])))
	print('+%s+'%('-'*13))
	print(' 0 1 2 3 4 5 6')

def checkForWinner():
	if (''.join([''.join(row) for row in board])).count(open_space) == 0:
		return 'Draw'

	lines = set()

	# rows
	for e in [''.join(r) for r in board]:
		lines.add(e)

	# columns
	for c in xrange(board_width):
		# lines.append(''.join([board[r][c] for r in xrange(board_height)]))
		lines.add(''.join([board[r][c] for r in xrange(board_height)]))

	# diagonals NE
	for c in xrange(board_width):
		for r in xrange(board_height):
			s_NE = ''
			i,j = 0,0
			while c+i<board_width and r+j>=0:
				s_NE += board[r+j][c+i]
				i += 1
				j -= 1
			s_SE = ''
			i,j = 0,0
			while c+i<board_width and r+j<board_height:
				s_SE += board[r+j][c+i]
				i += 1
				j += 1
			# lines += [s_NE,s_SE]
			lines.add(s_NE)
			lines.add(s_SE)

	human_str = human_piece*4
	computer_str = computer_piece*4
	for e in lines:
		if human_str in e:
			# Human wins
			return 'Human'
		if computer_str in e:
			# Computer wins
			return 'Computer'

	# Game hasn't ended yet
	return 'Ongoing'

def testMove(column):
	r = board_height - 1
	while r >= 0:
		if board[r][column] == open_space:
			return True
		r -= 1
	return False

def move(column, piece):
	r = board_height - 1
	while r >= 0:
		if board[r][column] == open_space:
			board[r][column] = piece
			return True
		r -= 1
	return False

# lookAhead1: if find winning move, take it. otherwise random
def chooseNextMove(mode='random'):
	'''Proof-of-concept: choose left-most available column'''
	if mode == 'lefty':
		c = 0
		while not testMove(c):
			c += 1
		return c
	elif mode == 'random':
		open_cols = [i for i in xrange(board_width) if testMove(i)]
		return open_cols[ri(0,len(open_cols)-1)]
	elif mode == 'lookAhead1':
		pass

# Game loop
AI_mode = 'random'
status = 'Ongoing'
display(board)
player_index = 0
players = ['Human','Computer']
while status == 'Ongoing':
	piece = pieces[player_index]
	print('%s\'s turn (%s)'%(players[player_index],piece))
	if piece == human_piece:
		c = int(raw_input('Column (0-6)\n>> '))
		isValidMove = move(c,piece)
		while not isValidMove:
			print('Move invalid.')
			isValidMove = move(c,piece)
	else:
		# AI chooses move
		c = chooseNextMove(AI_mode)
		move(c,piece)
	display(board)
	status = checkForWinner()
	print('status: %s'%status)
	player_index = 1 - player_index
print('Winner: %s'%status)