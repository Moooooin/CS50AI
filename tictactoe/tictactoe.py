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
    if terminal(board):
        return None
    
    cx = 0
    co = 0
    
    for i in board:
        for j in i:
            if j == X:
                cx += 1
            elif j == O:
                co += 1

    if cx > co:
        return O
    elif co == cx:
        return X
    else:
        raise Exception("Something weird went wrong")



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    if terminal(board):
        return set()
    
    aktionen = set()

    for i in [0, 1, 2]:
        for j in [0, 1, 2]:
            if board[i][j] == EMPTY:
                aktionen.add((i, j))

    return aktionen
    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    if action not in actions(board):
        raise Exception("Not a valid Action")
    
    neues = copy.deepcopy(board)
    neues[action[0]][action[1]] = player(board)

    return neues


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    siege = [[(0, 0), (0, 1), (0, 2)],
             [(1, 0), (1, 1), (1, 2)],
             [(2, 0), (2, 1), (2, 2)],
             [(0, 0), (1, 0), (2, 0)],
             [(0, 1), (1, 1), (2, 1)],
             [(0, 2), (1, 2), (2, 2)],
             [(0, 0), (1, 1), (2, 2)],
             [(0, 2), (1, 1), (2, 0)]]
    
    
    for sieg in siege:

        xp = 0
        op = 0

        for zelle in sieg:
            if board[zelle[0]][zelle[1]] == X:
                xp += 1
            elif board[zelle[0]][zelle[1]] == O:
                op += 1

        if xp == 3 and op == 0:
            return X
        elif op == 3 and xp == 0:
            return O
            
            
    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) is not None:
        return True
    
    for i in board:
        for j in i:
            if j == EMPTY:
                return False
            
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    sieger = winner(board)

    if sieger == X:
        return 1
    elif sieger == O:
        return -1
    else:
        return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    spieler = player(board)
    wert = None
    beste = None

    if terminal(board):
        return None
    
    if spieler == X:
        wert = -(math.inf)
    elif spieler == O:
        wert = math.inf

    if board == initial_state():
        return (1, 1)
    
    aktionen = actions(board)

    if len(aktionen) >= 7 and (1, 1) in aktionen:
        return (1, 1)
    
    for a in aktionen:
        
        if spieler == X:
            neuwert = minwert(result(board, a), 0)

            if neuwert >= wert:
                wert = neuwert
                beste = a
            
        
        elif spieler == O:
            neuwert = maxwert(result(board, a), 0)

            if neuwert <= wert:
                wert = neuwert
                beste = a

    return beste



def maxwert(board, c):
    """
    Returns the maximimum utility value
    """

    if terminal(board):
        return utility(board)
    
    c += 1
    if c > 7:
        return 0
    
    v = -(math.inf)
    for a in actions(board):
        v = max(v, minwert(result(board, a), c))

    return v



def minwert(board, c):
    """
    Returns the minimum utility value
    """

    if terminal(board):
        return utility(board)
    
    c += 1
    if c > 7:
        return 0
    
    v = math.inf
    for a in actions(board):
        v = min(v, maxwert(result(board, a), c))

    return v