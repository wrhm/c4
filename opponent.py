""" opponent.py

Module for a Connect-4 computer opponent

Developed at: https://github.com/wrhm/c4
  Date begun: 07 Jul 2018
 Last edited: 07 Jul 2018

To-do:
* flake8
* functions and variables: style like_this, not likeThis
* create a subclass/inherited class per AI?
* Add more AIs

Helpful links:
* https://docs.python.org/3/tutorial/classes.html
"""

from random import randint as ri


class Opponent:
    """ A representation of a general Connect-4 AI """

    def __init__(self):
        self.mode = 'random'
        # self.name = None

    def attempt_move(self, board, column, piece):
        """ Make a move for <piece> in <column>, if possible.
        Return True iff it was possible.
        """

        (success, r) = board.column_has_vacancy(column)
        if success:
            board.board[r][column] = piece
        return success

    def choose_next_move(self, board):
        """Proof-of-concept: choose left-most available column

        look_ahead_1: if find winning move, take it. otherwise random
        """

        if self.mode == 'lefty':
            c = 0
            while not board.column_has_vacancy(c)[0]:
                c += 1
            return c
        elif self.mode == 'random':
            open_cols = [i for i in range(board.board_width) if
                         board.column_has_vacancy(i)[0]]
            return open_cols[ri(0, len(open_cols) - 1)]
        elif self.mode == 'look_ahead_1':
            pass
