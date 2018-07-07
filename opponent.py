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
** look_ahead_1: if find winning move, take it. otherwise random

Helpful links:
* https://docs.python.org/3/tutorial/classes.html
"""

from random import randint as ri


class Opponent:
    """ A representation of a general Connect-4 AI """

    def __init__(self, mode='random'):
        modes = 'random lefty'.split()
        if mode in modes:
            self.mode = mode
        # self.name = None

    def choose_next_move(self, board):
        """ Choose next move, according to mode. """

        if self.mode == 'lefty':
            # Choose the left-most non-full column
            nfcs = board.get_nonFull_columns()
            return nfcs[0]
        elif self.mode == 'random':
            # Choose a random non-full column
            nfcs = board.get_nonFull_columns()
            return nfcs[ri(0, len(nfcs) - 1)]
        elif self.mode == 'look_ahead_1':
            pass
