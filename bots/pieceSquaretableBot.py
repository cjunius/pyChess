import chess
import chess.polyglot
from engines.NegaMaxAB import Engine
from evaluation import Evaluation

class PieceSquareTableBot(Engine):

    def getName(self):
        return "Piece-Square Table Bot"

    def evaluate_board(self, board: chess.Board):

        if board.is_game_over():
            if board.is_checkmate():
                return -9999 if board.turn else 9999
            if board.is_stalemate():
                return -10
            if board.is_insufficient_material():
                return -10
            if board.is_fivefold_repetition():
                return -10
            if board.is_seventyfive_moves():
                return -10
        
        eval = Evaluation.piece_square_table(board)
        
        return eval if board.turn else -eval
