import random
import chess
from engines.NegaMaxAB import Engine

class RandomBot(Engine):
    def getName(self):
        return "Random Bot"

    def findMove(self, board: chess.Board):
        legal_moves = list(board.legal_moves)
        return random.choice(legal_moves)
    
    def evaluate_board(self, board: chess.Board):
        return 0
