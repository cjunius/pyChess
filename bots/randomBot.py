import random

def findMove(legal_moves):
    numLegalMoves = legal_moves.count()
    idx = random.randint(0, numLegalMoves)
    legal_moves = list(legal_moves)
    move = legal_moves[idx-1]
    return move
