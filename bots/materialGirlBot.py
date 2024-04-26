import chess
from engines.NegaMaxABTT import Engine
from evaluation import Evaluation

class MaterialGirlBot(Engine):

    def getName(self):
        return "Material Girl Bot"

    def evaluate_board(self, board: chess.Board, turn: bool):
        
        quick_eval = Evaluation.quick_check(board, turn)
        if quick_eval is not None:
            return quick_eval
        
        eval = Evaluation.material_balance(board, turn)

        return eval
