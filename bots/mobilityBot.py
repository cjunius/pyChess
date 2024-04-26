import chess
from engines.NegaMaxABTT import Engine
from evaluation import Evaluation

class MobilityBot(Engine):

    def getName(self):
        return "Mobility Bot"

    def evaluate_board(self, board: chess.Board, turn: bool):
        
        quick_eval = Evaluation.quick_check(board, turn)
        if quick_eval is not None:
            return quick_eval
        
        eval = 0
        eval += Evaluation.mobility(board)

        return eval
