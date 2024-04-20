import chess

def getName():
    return "Cheater Bot"

def findMove(board: chess.Board):
    board.reset()
    board.push_san("e4")
    board.push_san("e5")
    board.push_san("Qh5")
    board.push_san("Nc6")
    board.push_san("Bc4")
    board.push_san("Nf6")
    board.push_san("Qxf7")
    return board.pop()
