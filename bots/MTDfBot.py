import chess
from engines.MTDf import Engine
from evaluation import Evaluation

class MTDfBot(Engine):

    def getName(self):
        return "MTDf Bot"

    def evaluate_board(self, board: chess.Board, depth: int):
        
        if board.is_game_over():
            return Evaluation.game_over(board, depth)
        
        if board.is_repetition():
            return 0
        
        eval = 0
        #eval += Evaluation.material_balance(board)
        eval += Evaluation.board_control(board)
        #eval += Evaluation.mobility(board)

        return eval 
