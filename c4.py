''' c4.py

Connect-4 implementation (python3)

Developed at: https://github.com/wrhm/c4
  Date begun: 20 Oct 2017
 Last edited: 06 Jul 2018

To-do:
* I added this line just for you, IanQS :)
* flake8
* Allow compatibility with both python2 and python3?
* pick casing styles for functions and variables, likeThis or like_this
* make a board module?
* Allow parameters in Board.__init__: dictionary?
* Abstract AI into separate class
* Allow choice of AI behavior
* Add more AIs
* DONE: sort Board functions by dependency
* DONE: Make Board.display handle more arbitrary number of columns
* DONE: Input validation
* DONE: Create a board class

Helpful links:
* https://docs.python.org/3/tutorial/classes.html
* https://www.python.org/dev/peps/pep-0008/?#naming-conventions
'''

from random import randint as ri

DEBUG = False


def dprint(s):
    if DEBUG:
        print(s)


class Board:
    """A representation of a Connect-4 board"""

    def __init__(self):
        """ Initialize board-specific variables. """
        self.board = []
        self.board_height = 6
        self.board_width = 7  # should not exceed 10, due to self.display
        self.human_piece = '@'
        self.computer_piece = 'O'
        self.open_space = '_'
        self.pieces = self.human_piece + self.computer_piece
        self.AI_mode = 'random'  # maybe parameterize this
        self.status = 'Ongoing'
        self.players = ['Human', 'Computer']

        # who goes first. (0 is human)
        self.player_index = 0  # maybe parameterize this

        # Initialize the board as a grid of blank cells
        for nrow in range(self.board_height):
            self.board.append([self.open_space for i in
                               range(self.board_width)])

    def switchPlayer(self):
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
        ''' Make a move for <piece> in <column>, if possible.
        Return True iff it was possible.
        '''
        (success, r) = self.column_has_vacancy(column)
        if success:
            self.board[r][column] = piece
        return success

    def requestHumanMove(self):
        """ Request a column selection from the user, which is both:
            - an integer 0 <= c <= [board_width - 1]
            - the index of a non-full column
        """

        def isNonemptyNumericStr(s):
            digits = '0123456789'
            if len(s) == 0:
                return False
            for c in s:
                if c not in digits:
                    return False
            return True

        got_valid_request = False
        while not got_valid_request:
            in_str = input('Column (0-%d)\n>> ' % (self.board_width - 1))
            while not (isNonemptyNumericStr(in_str) and 0 <= int(in_str) and
                       int(in_str) <= self.board_width - 1):
                print('Please enter an integer 0 <= c <= %d' %
                      (self.board_width - 1))
                in_str = input('Column (0-%d)\n>> ' % (self.board_width - 1))

            dprint('Validated column #: %s' % in_str)

            got_valid_request = self.attempt_move(int(in_str),
                                                  self.human_piece)
            if got_valid_request:
                return
            else:
                print('Column %s is full. Please pick another one.' % in_str)

    def checkForWinner(self):
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

        # diagonals - NE and SE
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

        for e in lines:
            if human_str in e:
                # Human wins
                return 'Human'

            if computer_str in e:
                # Computer wins
                return 'Computer'

        # Assuming the previous state was not a win, full means draw
        if (''.join([''.join(row) for
                    row in self.board])).count(self.open_space) == 0:
            return 'Draw'

        # Game hasn't ended yet
        return 'Ongoing'

    def chooseNextMove(self, mode='random'):
        '''Proof-of-concept: choose left-most available column

        lookAhead1: if find winning move, take it. otherwise random
        '''
        if mode == 'lefty':
            c = 0
            while not self.column_has_vacancy(c)[0]:
                c += 1
            return c
        elif mode == 'random':
            open_cols = [i for i in range(self.board_width) if
                         self.column_has_vacancy(i)[0]]
            return open_cols[ri(0, len(open_cols) - 1)]
        elif mode == 'lookAhead1':
            pass


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
            board.requestHumanMove()
        else:
            # AI chooses move
            c = board.chooseNextMove(board.AI_mode)
            board.attempt_move(c, piece)

        board.display()
        board.status = board.checkForWinner()
        dprint('status: %s' % board.status)

        board.switchPlayer()

    print('Winner: %s' % board.status)
