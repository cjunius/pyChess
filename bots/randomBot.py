import random

def getName():
    return "Random Move Bot"

def findMove(board):
    numLegalMoves = board.legal_moves.count()
    idx = random.randint(0, numLegalMoves)
    legal_moves = list(board.legal_moves)
    move = legal_moves[idx-1]
    return move
