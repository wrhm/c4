""" c4.py

Connect-4 implementation (python3)

Developed at: https://github.com/wrhm/c4
  Date begun: 20 Oct 2017
 Last edited: 07 Jul 2018

To-do:
* I added this line just for you, IanQS :)
* flake8
* Allow compatibility with both python2 and python3?
* functions and variables: style like_this, not likeThis
* Allow parameters in Board.__init__: dictionary?
* Allow choice of AI behavior
"""

from constants import States
from board import Board

DEBUG = False


def dprint(s):
    if DEBUG:
        print(s)


if __name__ == '__main__':

    # Initialize a new board and display it
    board = Board()
    board.display()

    # Main game loop
    while board.state == States.ongoing:
        piece = board.pieces[board.player_index]
        print('\n%s\'s turn (%s)' % (board.players[board.player_index],
                                     piece))
        if piece == board.human_piece:
            board.request_human_move()
        else:
            # AI chooses move
            c = board.AI.choose_next_move(board)
            board.attempt_move(c, piece)

        board.display()
        board.check_for_winner()

        board.switch_player()

    if board.state == States.computer_wins:
        print('Winner: Computer')
    elif board.state == States.human_wins:
        print('Winner: Human')
    else:
        print('It\'s a draw!')
