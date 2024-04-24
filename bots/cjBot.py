import chess
from engines.NegaMaxAB import Engine
from evaluation import Evaluation

class CJBot(Engine):
    def getName(self):
        return "CJ Bot"
    
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
        
        eval = Evaluation.material_balance(board)
        eval += Evaluation.piece_square_table(board)
        eval += Evaluation.board_control(board)

        return eval if board.turn else -eval
    
# ToDo:
# - Material Evaluation - COMPLETE
# - Piece Square Table Evaluation - Simplified - Expand usage to include to Midgame and endgame PST
# - Double, Isolated, Backwards, and Passed Pawn evaluation
# - Open and semi-open files for rooks and kings evaluation
# - Bishop pair evaluation
# - Tempo evaluation
# - Tampered evaluation between middlegame and endgame

