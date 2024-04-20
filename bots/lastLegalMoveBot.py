import random
import chess

def getName():
    return "Last Legal Move Bot"

def findMove(board: chess.Board):
    numLegalMoves = board.legal_moves.count()
    legal_moves = list(board.legal_moves)
    move = legal_moves[numLegalMoves-1]
    return move
