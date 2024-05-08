import random
from chess import Board, Move

from evaluation import PIECE_VALUES

class BaseMoveOrdering(object):
    def __init__(self, board: Board):
        if board is None:
            raise ValueError("Board must be specified")
        self.board = board

class ChecksCapturesOrderMixin(BaseMoveOrdering):
    def order_moves(self):
        checks = []
        captures = []
        non_captures = []

        for move in self.board.legal_moves:
            if self.board.gives_check(move):
                self.board.push(move)
                if self.board.is_checkmate():
                    self.board.pop()
                    return [move] #no point in searching other moves if checkmate exists
                self.board.pop()
                checks.append(move)
            elif self.board.is_capture(move):
                captures.append(move)
            else:
                non_captures.append(move)

        random.shuffle(checks)
        captures.sort(reverse=True, key=lambda x: self.mvvlva(x))
        random.shuffle(non_captures)

        return checks + captures + non_captures
    
    def mvvlva(self, m: Move):
        attacker = self.board.piece_at(m.from_square)
        victim = self.board.piece_at(m.to_square)
        if victim:
           return 8*PIECE_VALUES[victim.piece_type] - attacker.piece_type
        return 0