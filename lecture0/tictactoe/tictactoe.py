"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    x_count = 0
    o_count = 0

    for row in board:
        for col in row:
            if col == X:
                x_count +=1
            elif col == O:
                o_count +=1

    if x_count == o_count:
        return X
    
    else:
        return O


def actions(board):

    """
    Returns set of all possible actions (i, j) available on the board.
    """

    moves =  set()

    for i in range(3):
        for j in range(3):

            if board[i][j] == None:
                moves.add((i,j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    turn = player(board)

    new_board = [row[:] for row in board]

    pot_move = new_board[action[0]][action[1]] 

    if pot_move == None:
        new_board[action[0]][action[1]] = turn

    else:
        raise Exception
    
    return new_board



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    winner_x = ['X','X','X']
    winner_o = ['O','O','O']
    left_col = []
    mid_col = []
    right_col = []
    left_diag = []
    right_diag = []


    for row in board:

        if row == winner_x:
            return X
        
        if row == winner_o:
            return O
        
        left_col.append(row[0])
        mid_col.append(row[1])
        right_col.append(row[2])
    
    left_diag.extend([left_col[0],mid_col[1],right_col[2]])
    right_diag.extend([left_col[2],mid_col[1],right_col[0]])

    if left_col == winner_x or mid_col == winner_x or right_col == winner_x or left_diag == winner_x or right_diag == winner_x:
        return X
    
    if left_col == winner_o or mid_col == winner_o or right_col == winner_o or left_diag == winner_o or right_diag == winner_o:
        return O


    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) != None:
        return True

    for row in board:

        if None in row:
            return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """


    if winner(board) == X:
        return 1
    
    if winner(board) == O:
        return -1
    
    return 0

    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError


def main():

    board = [
        ["O", None, "O"],
        ["X", None, "X"],
        ["O", "X", "X"]
    ]

    # print(actions(board))
                  
    # print(result(board,action=(0,0)))
    print(winner(board))
    print(terminal(board))


if __name__ == '__main__':
    main()

    