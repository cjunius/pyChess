from enum import Enum

class FLAG(Enum):
    LOWER_BOUND = -1
    EXACT = 0
    UPPER_BOUND = 1

class TransTableEntry():
    def __init__(self, hash):
        self.z_key = hash
        self.value: int = 0
        self.depth: int = 0
        self.flag: FLAG = FLAG.EXACT

class TransTable():
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

    def getEntry(self, hash):
        return self.table.get(hash)  
        