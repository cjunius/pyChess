from chess import Move

from evaluation import PIECE_VALUES

class BaseMoveOrdering(object):
    def __init__(self):
        pass

class ChecksCapturesOrderMixin(BaseMoveOrdering):
    def order_moves(self, board):
        checks = []
        captures = []
        non_captures = []

        for move in board.legal_moves:
            if board.gives_check(move):
                board.push(move)
                if board.is_checkmate():
                    board.pop()
                    return [move] #no point in searching other moves if checkmate exists
                board.pop()
                checks.append(move)
            elif board.is_capture(move):
                captures.append(move)
            else:
                non_captures.append(move)

        captures.sort(reverse=True, key=lambda x: self.mvvlva(board, x))

        return checks + captures + non_captures
    
    def mvvlva(self, board, m: Move):
        attacker = board.piece_at(m.from_square)
        victim = board.piece_at(m.to_square)
        if victim:
            return 8*PIECE_VALUES[victim.piece_type] - attacker.piece_type
        return 0