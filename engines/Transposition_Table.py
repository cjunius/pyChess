import chess
import chess.polyglot
from enum import Enum

class FLAG(Enum):
    LOWER_BOUND = -1
    EXACT = 0
    UPPER_BOUND = 1

class TransTableEntry():
    __slots__ = ['z_key', 'value', 'depth', 'flag']

    def __init__(self, hash):
        self.z_key = hash
        self.value: int = 0
        self.depth: int = 0
        self.flag: FLAG = FLAG.EXACT

class TransTable():
    __slots__ = ['table', 'size', 'maxSize']

    def __init__(self, init_size = 0, max_size = 10 ** 7):
        self.table = {}
        self.size: int = init_size
        self.maxSize: int = max_size

    def update_ttable(self, entry: TransTableEntry):
        if self.size == self.maxSize:
            self.table.popitem()
            self.size -= 1
    
        self.table[entry.z_key] = entry
        self.size += 1

    def getEntry(self, hash: int):
        return self.table.get(hash)
    
    def getEntry(self, board: chess.Board):
        z_hash = chess.polyglot.zobrist_hash(board)
        return self.table.get(z_hash)
        