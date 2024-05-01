import chess
from engines.NegaScout import Engine
from evaluation import Evaluation

class NegaScoutBot(Engine):

    def __init__(self, depth=3, debug=False):
        super().__init__(depth=depth, debug=debug)

    def getName(self):
        return "NegaScout Bot"

    def evaluate_board(self, board: chess.Board, depth: int, color: bool):
        
        if board.is_game_over():
            eval = Evaluation.game_over(board, depth)
            return eval if color else -eval

        if board.is_repetition():
            return 0
        
        eval = 0
        eval += Evaluation.material_balance(board)
        #eval += Evaluation.board_control(board)
        #eval += Evaluation.mobility(board)

        return eval
