""" board.py

Module for a Connect-4 board representation

Developed at: https://github.com/wrhm/c4
  Date begun: 05 Jul 2018
 Last edited: 07 Jul 2018

To-do:
* flake8
* functions and variables: style like_this, not likeThis
* remove "board" from names of board variables
* Allow parameters in Board.__init__: dictionary?
** size, AI choice, first player
* Optimize win-checking: only check neighborhood of new piece
* DONE: Abstract AI into separate class

Helpful links:
* https://docs.python.org/3/tutorial/classes.html
"""

import constants
from constants import States
from opponent import Opponent


class Board:
    """ A representation of a Connect-4 board """

    def __init__(self):
        """ Initialize board-specific variables. """

        self.board = []
        self.board_height = constants.BOARD_HEIGHT
        self.board_width = constants.BOARD_WIDTH

        self.human_piece = constants.HUMAN_PIECE
        self.computer_piece = constants.COMPUTER_PIECE
        self.open_space = constants.OPEN_SPACE
        self.pieces = constants.PIECES

        # Maybe query the user for desired opponent type
        self.AI_type = 'random'
        self.AI = Opponent(self.AI_type)

        self.players = ['Human', 'Computer']
        self.state = States.ongoing

        # who goes first. (0 is human). maybe parameterize this
        self.player_index = 0

        # Initialize the board as a grid of blank cells
        for nrow in range(self.board_height):
            self.board.append([self.open_space for i in
                               range(self.board_width)])

    def switch_player(self):
        self.player_index = 1 - self.player_index

    def display(self):
        """ Display the game state to the terminal. """

        header = ' ' + ' '.join([str(i) for i in range(self.board_width)])
        num_dashes = 2 * self.board_width - 1

        print(header)
        print('+%s+' % ('-' * num_dashes))

        for i in range(len(self.board)):
            print('|%s|' % ('|'.join(self.board[i])))

        print('+%s+' % ('-' * num_dashes))
        print(header)

    def column_has_vacancy(self, column):
        """ If board has an opening in <column>, return (True,r), where r
        is the row where a new piece in that column would fall.

        Otherwise, return (False,-1)
        """

        r = self.board_height - 1
        while r >= 0:
            if self.board[r][column] == self.open_space:
                return (True, r)
            r -= 1
        return (False, -1)

    def attempt_move(self, column, piece):
        """ Make a move for <piece> in <column>, if possible.
        Return True iff it was possible.
        """

        (success, r) = self.column_has_vacancy(column)
        if success:
            self.board[r][column] = piece
        return success

    def get_nonFull_columns(self):
        """ Return an ordered list of indices of columns which have at least
            one vacancy.
        """

        return [c for c in range(self.board_width) if
                self.column_has_vacancy(c)[0]]

    def request_human_move(self):
        """ Request a column selection from the user, which is both:
            - an integer 0 <= c <= [board_width - 1]
            - the index of a non-full column
        """

        def is_nonempty_numeric_str(s):
            digits = '0123456789'
            if len(s) == 0:
                return False
            for c in s:
                if c not in digits:
                    return False
            return True

        def is_bounded_by(b, a, c):
            """ Assumes a,b,c are ints """
            return ((a <= b) and (b <= c))

        got_valid_request = False
        while not got_valid_request:
            in_str = input('Column (0-%d)\n>> ' % (self.board_width - 1))

            while not (is_nonempty_numeric_str(in_str) and
                       is_bounded_by(int(in_str), 0, self.board_width - 1)):
                print('Please enter an integer 0 <= c <= %d' %
                      (self.board_width - 1))
                in_str = input('Column (0-%d)\n>> ' % (self.board_width - 1))

            got_valid_request = self.attempt_move(int(in_str),
                                                  self.human_piece)

            if got_valid_request:
                return
            else:
                print('Column %s is full. Please pick another one.' % in_str)

    def check_for_winner(self):
        """ Check the board for a draw or victory/loss.
            - draw imaginary lines across all rows/columns/diagonals
            - if any of these lines has 4 non-empty cells in a row, it is a
              win for that player
            - otherwise, if no such line exists, but the board is full: Draw
            - otherwise, the game is still ongoing
        """

        human_str = self.human_piece * 4
        computer_str = self.computer_piece * 4

        def contains_win(s):
            return human_str in s or computer_str in s

        lines = set()

        # rows
        for e in [''.join(r) for r in self.board]:
            lines.add(e)

        # columns
        for c in range(self.board_width):
            this_col = ''.join([self.board[r][c] for
                                r in range(self.board_height)])
            lines.add(this_col)

        # diagonals - northeast and southeast
        for c in range(self.board_width):
            for r in range(self.board_height):
                s_NE = ''
                i, j = 0, 0
                while (c + i < self.board_width) and (r + j >= 0):
                    s_NE += self.board[r + j][c + i]
                    i += 1
                    j -= 1
                s_SE = ''
                i, j = 0, 0
                while (c + i < self.board_width and
                       r + j < self.board_height):
                    s_SE += self.board[r + j][c + i]
                    i += 1
                    j += 1
                lines.add(s_NE)
                lines.add(s_SE)

        # Check for a winner
        for e in lines:
            if human_str in e:
                self.state = States.human_wins
                return
            if computer_str in e:
                self.state = States.computer_wins
                return

        # If the board is full and has no winner, it's a draw
        if len(self.get_nonFull_columns()) == 0:
            self.state = States.draw
            return
