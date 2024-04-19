import random

def getName():
    return "First Legal Move Bot"

def findMove(board):
    legal_moves = list(board.legal_moves)
    move = legal_moves[0]
    return move
