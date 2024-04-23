import chess
import chess.polyglot
from engine import Engine
from evaluation import Evaluation

class MaterialGirlBot(Engine):
    def getName(self):
        return "Material Girl Bot"

    def evaluate_board(self, board: chess.Board):
        if board.is_checkmate():
            return -9999 if board.turn else 9999
        if board.is_stalemate():
            return -1
        if board.is_insufficient_material():
            return -1
        if board.is_fivefold_repetition():
            return -1
        if board.is_seventyfive_moves():
            return -1
        
        eval = Evaluation.material_balance(board)

        return eval if board.turn else -eval
