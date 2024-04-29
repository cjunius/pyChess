import chess
from engines.NegaMax import Engine
from evaluation import Evaluation

class MaterialPSTBot(Engine):

    def getName(self):
        return "Material & Piece-Square Table Bot"

    def evaluate_board(self, board: chess.Board, depth: int):
        
        if board.is_game_over():
            return Evaluation.game_over(board, depth)
        
        if board.is_repetition():
            return 0
        
        eval = 0
        eval += Evaluation.material_balance(board)
        eval += Evaluation.piece_square_table(board)

        return eval 
