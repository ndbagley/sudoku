"""

This file creates a bot designed to solve a 9x9 sudoku with standard rules.

- The bot cannot employ a 'guess and check' strategy. If it cannot be solved by human logic, the bot won't solve it.
- The bot will recognize if a puzzle is not solvable
- The bot will be able to determine the difficulty level of the given puzzle based on the steps it took to solve it

"""
import numpy as np
from copy import copy


class SudokuBot:

    def __init__(self, board):
        self.initial_board = copy(board)
        self.solved_board = board
        self.iters = 0
        self.num_blank = 27 - np.count_nonzero(board)

        if self.num_blank > 36:
            self.difficulty = 'Hard'
        elif 27 < num_zeroes < 36:
            self.difficulty = 'Medium'
        else:
            self.difficulty = 'Easy'

    def __str__(self):

        SudokuBot._print_board(self.solved_board)
        return ''

    @staticmethod
    def _print_board(board):

        """
        Prints the sudoku board in a readable format.
        """

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

        # print final ror_sep
        print(row_sep)

    @staticmethod
    def _round_thirds(index):
        round_float = np.ceil((index + 1) / 3) * 3
        round_int = np.int(round_float)

        return round_int

    def check_unique(self, row, col):
        # get distinct values from row and column
        row_vals = np.unique(self.solved_board[row, :])
        col_vals = np.unique(self.solved_board[:, col])

        # find the 3x3 subgrid that the cell is in
        row_end = SudokuBot._round_thirds(row)
        col_end = SudokuBot._round_thirds(col)

        # get distince values from subgrid
        sub_vals = np.unique(self.solved_board[row_end - 3 : row_end, col_end - 3 : col_end])

        # combine all values from row, col, subgrid
        vals = np.concatenate((row_vals, col_vals, sub_vals), axis=None)

        # find unique values across row, col, subgrid
        existing = np.unique(vals)

        return existing

    def fill_values(self, row, col):
        # check if a value is empty
        if self.solved_board[row, col] == 0:
            existing = self.check_unique(row, col)
            potential = [val for val in range(1, 10) if val not in existing]

            # fill in the cell if there is only one potential number
            if len(potential) == 1:
                self.solved_board[row, col] = potential[0]
                print('Row: ', str(row + 1), 'Col: ', str(col + 1), ' resolved to ', str(potential[0]))

    def solver(self):
        # max at 50 iterations of the board
        for i in range(50):

            # loop through rows and cols
            for row in range(9):
                for col in range(9):
                    self.fill_values(row, col)

            self.iters += 1
            print('\n Loop number ', str(i + 1), ' complete \n')

            # checks board to see if it is solved
            zeroes_left = np.count_nonzero(self.solved_board == 0)

            if zeroes_left == 0:
                print('Solved!\n')
                print('Initial Board')
                print('=' * 25)
                SudokuBot._print_board(self.initial_board)
                print('\nSolved Board')
                print('=' * 25)
                print(str(self))
                return True
                break
            else:
                print(' ', str(zeroes_left), ' zeroes left\n')

        print('Could not resolve board in 50 iterations')
        return False

    def is_solvable(self):
        # run the solver to see if the board is solvable
        if self.solver():
            self.solved_board = copy(self.initial_board)
            self.iters = 0
            return True
        else:
            return False

    def puzzle_difficulty(self):
        print(self.difficulty)
        









