import chess
from engines.NegaMaxABTT import Engine
from evaluation import Evaluation

class PieceSquareTableBot(Engine):

    def getName(self):
        return "Piece-Square Table Bot"

    def evaluate_board(self, board: chess.Board, turn: bool):
        
        quick_eval = Evaluation.quick_check(board, turn)
        if quick_eval is not None:
            return quick_eval
        
        eval = Evaluation.piece_square_table(board, turn)

        return eval
