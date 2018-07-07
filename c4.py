''' c4.py

Connect-4 implementation (python3)

Developed at: https://github.com/wrhm/c4
  Date begun: 20 Oct 2017
 Last edited: 07 Jul 2018

To-do:
* flake8
* Allow compatibility with both python2 and python3?
* functions and variables: style like_this, not likeThis
* Allow parameters in Board.__init__: dictionary?
* Abstract AI into separate class
* Allow choice of AI behavior
* Add more AIs
* DONE: sort Board functions by dependency
* DONE: Make Board.display handle more arbitrary number of columns
* DONE: Input validation
* DONE: Create a board class
'''

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
    while board.status == 'Ongoing':
        piece = board.pieces[board.player_index]
        print('\n%s\'s turn (%s)' % (board.players[board.player_index],
                                     piece))
        if piece == board.human_piece:
            board.request_human_move()
        else:
            # AI chooses move
            c = board.choose_next_move(board.AI_mode)
            board.attempt_move(c, piece)

        board.display()
        board.status = board.check_for_winner()
        dprint('status: %s' % board.status)

        board.switch_player()

    print('Winner: %s' % board.status)
