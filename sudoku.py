"""
sudoku.py
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

        if self.num_blank > 44:
            self.difficulty = 'Hard'
        elif self.num_blank > 34:
            self.difficulty = 'Medium'
        else:
            self.difficulty = 'Easy'

    def __str__(self):
        SudokuBot._print_board(self.solved_board)
        return ''

    @staticmethod
    def _print_board(board):

        """ Prints the sudoku board in a readable format """

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
    def _round_thirds(index):
        """ Rounds the grid into 3x3 subsection """

        round_float = np.ceil((index + 1) / 3) * 3
        round_int = np.int(round_float)

        return round_int

    def check_unique(self, row, col):
        """ Finds the unique values that a cell could be """

        # get distinct values from row and column
        row_vals = np.unique(self.solved_board[row, :])
        col_vals = np.unique(self.solved_board[:, col])

        # find the 3x3 subgrid that the cell is in
        row_end = SudokuBot._round_thirds(row)
        col_end = SudokuBot._round_thirds(col)

        # get distinct values from subgrid
        sub_vals = np.unique(self.solved_board[row_end - 3 : row_end, col_end - 3 : col_end])

        # combine all values from row, col, subgrid
        vals = np.concatenate((row_vals, col_vals, sub_vals), axis=None)

        # find unique values across row, col, subgrid
        existing = np.unique(vals)

        return existing

    def fill_forced(self, row, col, potentials):
        """ Finds if the value is forced through ruling out """

        # gather list of potential values for the row
        row_vals = []
        for i in range(9):
            if i == col:
                continue
            else:
                if potentials[(row, i)]:
                    row_vals += potentials[(row, i)]
        filled_row = list(np.unique(self.solved_board[row, :]))
        row_vals += filled_row
        row_vals = np.unique(row_vals)
        # fill given cell if it is deduced that a number can only go there from rows
        for i in range(1, 10):
            if i not in row_vals:
                self.solved_board[row, col] = i
                print('Row: ', str(row + 1), 'Col: ', str(col + 1), ' resolved to ', str(i))
                return

        # gather list of potential values for the column
        col_vals = []
        for i in range(9):
            if i == row:
                continue
            else:
                if potentials[(i, col)]:
                    col_vals += potentials[(i, col)]
        filled_col = list(np.unique(self.solved_board[:, col]))
        col_vals += filled_col
        col_vals = np.unique(col_vals)
        # fill given cell if it is deduced that a number can only go there from columns
        for i in range(1, 10):
            if i not in col_vals:
                self.solved_board[row, col] = i
                print('Row: ', str(row + 1), 'Col: ', str(col + 1), ' resolved to ', str(i))
                return

        # gather list of potential values for the 3x3 grid
        grid_vals = []
        row_end = SudokuBot._round_thirds(row)
        col_end = SudokuBot._round_thirds(col)
        for i in range(row_end - 3, row_end):
            for n in range(col_end - 3, col_end):
                if i == row and n == col:
                    continue
                else:
                    if potentials[(i, n)]:
                        grid_vals += potentials[(i, n)]
        filled_sub = list(np.unique(self.solved_board[row_end - 3: row_end, col_end - 3: col_end]))
        grid_vals += filled_sub
        grid_vals = np.unique(grid_vals)
        # fill given cell if it is deduced that a number can only go there from the subgrid
        print(row, col, grid_vals)
        for i in range(1, 10):
            if i not in grid_vals:
                self.solved_board[row, col] = i
                print('Row: ', str(row + 1), 'Col: ', str(col + 1), ' resolved to ', str(i))
                return

    def fill_values(self, row, col):
        """ Fills a cell if it is solvable """

        # check if a value is empty
        if self.solved_board[row, col] == 0:
            existing = self.check_unique(row, col)
            potential = [val for val in range(1, 10) if val not in existing]

            # fill in the cell if there is only one potential number
            if len(potential) == 1:
                self.solved_board[row, col] = potential[0]
                print('Row: ', str(row + 1), 'Col: ', str(col + 1), ' resolved to ', str(potential[0]))

            return potential

    def solver(self):
        """ Solves the sudoku board if it is solvable """

        # max at 50 iterations of the board
        prev_zeroes_left = np.count_nonzero(self.solved_board)
        iters = 0
        goodtogo = True
        while goodtogo:

            cell_vals = {}

            # loop through rows and cols to find initial solutions as well as store potential values
            for row in range(9):
                for col in range(9):
                    potential = self.fill_values(row, col)
                    cell_vals[(row, col)] = potential

            for row in range(9):
                for col in range(9):
                    self.fill_forced(row, col, cell_vals)

            self.iters += 1
            print('\n Loop number ', str(iters + 1), ' complete \n')
            iters += 1

            # if the solver makes no progress then the puzzle is unsolvable
            zeroes_left = np.count_nonzero(self.solved_board == 0)
            if zeroes_left == prev_zeroes_left:
                goodtogo = False
            #if iters == 50:
                #goodtogo = False

            prev_zeroes_left = copy(zeroes_left)

            # checks board to see if it is solved
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

        print('Could not resolve board after {} iterations\n'.format(iters))
        str(self)
        return False

    def is_solvable(self):
        """ Determines if a board is solvable """

        # run the solver to see if the board is solvable
        if self.solver():
            self.solved_board = copy(self.initial_board)
            self.iters = 0
            return True
        else:
            return False

    def puzzle_difficulty(self):
        """ Returns the difficulty level of the puzzle """

        print(self.difficulty)










