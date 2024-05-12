import random
import time
from chess import Move
from enum import Enum

class FLAG(Enum):
    LOWER_BOUND = -1
    EXACT = 0
    UPPER_BOUND = 1

class TransTableEntry():
    __slots__ = ['z_key', 'best_move', 'depth', 'value', 'flag', 'age']

    def __init__(self, hash: int):
        self.z_key: int = hash
        self.best_move: Move = Move.null()
        self.depth: int = 0
        self.value: int = 0
        self.flag: FLAG = FLAG.EXACT
        self.age: float = time.time()

class TransTable():
    __slots__ = ['table', 'size', 'maxSize']

    def __init__(self, init_size = 0, max_size = 10 ** 7):
        self.table = {}
        self.size: int = init_size
        self.maxSize: int = max_size

    def update_ttable(self, entry: TransTableEntry):
        if self.size == self.maxSize:
            self.table.pop(random.choice(self.table.keys()))
            self.size -= 1
    
        self.table[entry.z_key] = entry
        self.size += 1

    def getEntry(self, hash: int):
        return self.table.get(hash)
        