
from chess import Board
from config import Config

class LastMoveEngine:

    def __init__(self, config: Config = Config()):
        self.config = config

    def get_name(self):
        return "Last Move Engine"

    def find_move(self, board: Board):
        return list(board.legal_moves)[-1]