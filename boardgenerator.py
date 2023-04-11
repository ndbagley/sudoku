"""
boardgenerator.py
This file creates a sudoku board

- The generator will create a solvable sudoku board
- The generator will take a difficulty value of 'Easy', 'Medium', or 'Hard' that will determine the number of zeroes

"""

import numpy as np
import sudoku
from random import sample, randrange
from copy import copy


class BoardGenerator:

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.board = self.make_board()

    def __str__(self):
        BoardGenerator._print_board(self.board)
        return ''

    @staticmethod
    def _print_board(board):
        """ Prints the board in a readable format """

        # check that board is 9x9 numpy array
        assert board.shape == (9, 9)
        assert type(board) == np.ndarray

        # convert elements to strings
        str_board = board.astype(str)

        # string seperator for rows
        row_sep = '-' * 25

        # looping through all 9 rows
        for i in range(9):
            # print row_sep every third row
            if i % 3 == 0:
                print(row_sep)

            # get row data
            row = str_board[i]

            # format row with vertical separators
            print('| ' + ' '.join(row[0:3]) + ' | ' + ' '.join(row[3:6]) + ' | ' + ' '.join(row[6:]) + ' |')

        # print final row_sep
        print(row_sep)


    @staticmethod
    def _pattern(row, col):
        """ Creates the pattern for a baseline valid solution """

        return (3 * (row % 3) + row // 3 + col) % 9

    @staticmethod
    def _shuffle(s):
        """ Shuffles the numbers in the row """

        return sample(s, len(s))

    @staticmethod
    def _make_solved():
        """ Creates a solved 9x9 sudoku puzzle """

        rg = range(3)
        rows = [g * 3 + r for g in BoardGenerator._shuffle(rg) for r in BoardGenerator._shuffle(rg)]
        cols = [g * 3 + c for g in BoardGenerator._shuffle(rg) for c in BoardGenerator._shuffle(rg)]
        nums = BoardGenerator._shuffle(range(1, 10))

        board = [[nums[BoardGenerator._pattern(r, c)] for c in cols] for r in rows]

        return board

    def make_board(self):
        """ Removes numbers from a solved board to make the puzzle """

        if self.difficulty == 'Hard':
            empties = randrange(50, 60)
        elif self.difficulty == 'Medium':
            empties = randrange(34, 44)
        else:
            empties = randrange(24, 34)

        board = BoardGenerator._make_solved()
        for p in sample(range(81), empties):
            board[p // 9][p % 9] = 0

        board = np.array(board)

        bot = sudoku.SudokuBot(copy(board))
        if bot.is_solvable():
            return board
        else:
            return self.make_board()


















