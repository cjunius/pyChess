import chess
import chess.polyglot
from engines.NegaScout import Engine
from evaluation import Evaluation

PIECE_VALUES = [(chess.PAWN, 100), (chess.KNIGHT, 280), (chess.BISHOP, 320), (chess.ROOK, 379), (chess.QUEEN, 929), (chess.KING, 0)]

class NegaScoutBot(Engine):

    def getName(self):
        return "NegaScout Bot"

    def evaluate_board(self, board: chess.Board):
        if board.is_game_over():
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

        return Evaluation.board_control(board)
