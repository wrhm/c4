""" constants.py

Constants used by the scripts.

Developed at: https://github.com/wrhm/c4
  Date begun: 07 Jul 2018
 Last edited: 07 Jul 2018
"""

from enum import Enum

BOARD_HEIGHT = 6
BOARD_WIDTH = 7  # should not exceed 10, due to Board.display
HUMAN_PIECE = '@'
COMPUTER_PIECE = 'O'
OPEN_SPACE = '_'
PIECES = HUMAN_PIECE + COMPUTER_PIECE


class States(Enum):
    computer_wins = 0
    human_wins = 1
    draw = 2
    ongoing = 3
