import chess
from dataclasses import dataclass

@dataclass
class Config:
    depth: int = 4
    nodes: int = 0
    opening_book: str = "opening_book/cerebellum.bin"
    threads: int = 1
    log_file: str = ""
    ttsize: int = 10**7

    # PESTO CONSTANTS

    MG_PIECE_VALUES = [ 
        (chess.PAWN, 82), 
        (chess.KNIGHT, 337), 
        (chess.BISHOP, 365), 
        (chess.ROOK, 477),
        (chess.QUEEN, 1025),
        (chess.KING, 0)
    ]
    
    EG_PIECE_VALUES = [ 
        (chess.PAWN, 94), 
        (chess.KNIGHT, 281), 
        (chess.BISHOP, 297), 
        (chess.ROOK, 512),
        (chess.QUEEN, 936),
        (chess.KING, 0)
    ]