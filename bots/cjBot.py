import chess
from engines.NegaMaxABTT import Engine
from evaluation import Evaluation

class CJBot(Engine):

    def getName(self):
        return "CJ Bot"
    
    def evaluate_board(self, board: chess.Board, turn: bool):

        quick_eval = Evaluation.quick_check(board, turn)
        if quick_eval is not None:
            return quick_eval
        
        eval = 0
        eval += Evaluation.material_balance(board, turn)
        eval += Evaluation.board_control(board, turn)
        eval += Evaluation.mobility(board)

        return eval

