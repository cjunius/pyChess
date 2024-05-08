from random import choice
from chess import Board
from config import Config

class RandomEngine:

    def __init__(self, config: Config = Config()):
        self.config = config

    def get_name(self):
        return "Random Engine"

    def find_move(self, board: Board):
        return choice([move for move in board.legal_moves])