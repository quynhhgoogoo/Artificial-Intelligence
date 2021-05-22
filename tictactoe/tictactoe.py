"""
Tic Tac Toe Player
"""

import math
import copy

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
    num_of_O = 0
    num_of_empty = 0

    # Calculate number of Xs and Os on board
    for row in range (0,3):
        for col in range (0,3):
            if board[row][col] == X:
                num_of_X = num_of_X + 1
            elif board[row][col] == O:
                num_of_O = num_of_O + 1
            else:
                num_of_empty = num_of_empty + 1

    # Decide which player will go on next move            
    if num_of_empty == 0:
        return None
    elif num_of_X > num_of_O:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = []
    
    for row in range (0,3):
        for col in range (0,3):
            if board[row][col] == EMPTY:
                possible_moves.append((row,col))

    return possible_moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result_board = copy.deepcopy(board)
    possible_moves = actions(board)

    # If player made an invalid move
    if action not in possible_moves:
        raise NameError("Invalid action")
    else:
        (row,col) = action
        result_board[row][col] = player(board)
    return result_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check winner in row
    for row in range(0,3):
        if board[row][0] == board[row][1] == board [row][2] != None:
            if board[row][0] == X:
                return X
            else:
                return O
    
    # Check winner in column
    for col in range (0,3):
        if board[0][col] == board[1][col] == board [2][col] != None:
            if board[row][0] == X:
                return X
            else:
                return O

    # Check winner diagonally
    if board[0][0] == board[1][1] == board [2][2] != None:
        if board[0][0] == X:
            return X
        else:
            return O
    
    if board[0][2] == board[1][1] == board [2][0] != None:
        if board[0][0] == X:
            return X
        else:
            return O

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if player(board) == None:
        return True
    elif winner(board) != None:
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def min_ultility(board):
    """
    Returns the minimum ultility of the game
    """
    if terminal(board):
        return utility(board)

    # As opponent is max player, they attempt to gain higher score    
    player_min = math.inf
    possible_moves = actions(board)

    for move in possible_moves:
        result_board = result(board, move)
        player_min = min(player_min, max_ultility(result_board))

    return player_min

def max_ultility(board):
    """
    Returns the maximum ultility of the game
    """
    if terminal(board):
        return utility(board)

    # As opponent is min player, they attempt to gain lower score    
    player_max = -math.inf
    possible_moves = actions(board)

    for move in possible_moves:
        result_board = result(board, move)
        player_max = max(player_max, min_ultility(result_board))

    return player_max

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return utility(board)
    
    current_player = player(board)
    possible_moves = actions(board)
    optimal_move = []

    if current_player == X:
        optimal_ultility = -math.inf
        for move in possible_moves:
            # If there is a move for higher ultility
            max_move = min_ultility(result(board, move))
            if max_move > optimal_ultility:
                optimal_ultility = max_move
                optimal_move = move

    elif current_player == O:
        optimal_ultility = math.inf
        for move in possible_moves:
            min_move = max_ultility(result(board, move))
            if min_move < optimal_ultility:
                optimal_ultility = min_move
                optimal_move = move
    
    return optimal_move
