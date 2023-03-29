import numpy as np
import sudoku

zero_board = np.zeros(shape=(9, 9), dtype=int)
board_init = zero_board.copy()

board_init[0,:] = [0,0,0,0,0,0,5,7,3]
board_init[1,:] = [8,0,0,0,2,0,0,0,0]
board_init[2,:] = [7,0,0,9,0,0,8,1,0]
board_init[3,:] = [5,8,0,7,0,6,0,0,0]
board_init[4,:] = [0,0,1,8,0,0,0,6,0]
board_init[5,:] = [2,3,0,0,4,0,0,0,9]
board_init[6,:] = [9,1,5,0,0,0,0,0,0]
board_init[7,:] = [0,0,0,0,8,0,6,0,1]
board_init[8,:] = [0,0,0,0,0,0,0,4,0]

def nice_board(board):

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

bot = sudoku.SudokuBot(board_init)
bot.puzzle_difficulty()