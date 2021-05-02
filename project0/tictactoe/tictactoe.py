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
    num_of_X = 0
    num_of_Y = 0
    num_of_empty = 0

    # Calculate number of Xs and Os on board
    for col in range (0,3):
        for row in range (0,3):
            if board[row][col] == "X":
                num_of_X = num_of_X + 1
            elif board[row][col] == "Y":
                num_of_Y = num_of_Y + 1
            else:
                num_of_empty = num_of_empty + 1

    # Decide which player will go on next move            
    if num_of_empty == 0:
        return None
    elif num_of_O > num_of_X:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = []
    
    for col in range (0,3):
        for row in range (0,3):
            if board[row][col] == EMPTY:
                possible_moves.append(board[row][col])

    return possible_moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    pass


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    pass


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    i
    pass


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    pass


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    pass
