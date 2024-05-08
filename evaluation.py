import chess
from chess import Board

PIECE_VALUES = [None, 100, 320, 330, 500, 900, 0]

PIECE_SQUARE_TABLES = [
    None,
    [   # Pawn
         0,   0,   0,   0,   0,   0,  0,  0,
         5,  10,  10, -20, -20,  10, 10,  5,
         5,  -5, -10,   0,   0, -10, -5,  5,
         0,   0,   0,  20,  20,   0,  0,  0,
         5,   5,  10,  25,  25,  10,  5,  5,
        10,  10,  20,  30,  30,  20, 10, 10,
        50,  50,  50,  50,  50,  50, 50, 50,
         0,   0,   0,   0,   0,   0,  0,  0
    ],
    [   # Knight
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20,   0,   0,   0,   0, -20, -40,
        -30,   5,  10,  15,  15,  10,   5, -30,
        -30,   0,  15,  20,  20,  15,   0, -30,
        -30,   0,  10,  15,  15,  10,   0, -30,
        -30,   5,  15,  20,  20,  15,   5, -30,
        -40, -20,   0,   5,   5,   0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50
    ],
    [   # Bishop
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10,   5,   0,   0,   0,   0,   5, -10,
        -10,  10,  10,  10,  10,  10,  10, -10,
        -10,   0,  10,  10,  10,  10,   0, -10,
        -10,   5,   5,  10,  10,   5,   5, -10,
        -10,   0,   5,  10,  10,   5,   0, -10,
        -10,   0,   0,   0,   0,   0,   0, -10,
        -20, -10, -10, -10, -10, -10, -10, -20
    ],
    [   # Rook
         0,  0,  0,  5,  5,  0,  0,  0,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
         5, 10, 10, 10, 10, 10, 10,  5,
         0,  0,  0,  0,  0,  0,  0,  0
    ],
    [   # Queen
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10,   0,   5,  0,  0,   0,   0, -10,
        -10,   5,   5,  5,  5,   5,   0, -10,
          0,   0,   5,  5,  5,   5,   0,  -5,
         -5,   0,   5,  5,  5,   5,   0,  -5,
        -10,   0,   5,  5,  5,   5,   0, -10,
        -10,   0,   0,  0,  0,   0,   0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20
    ],
    [   # King mid-game
         20,  30,  10,   0,   0,  10,  30,  20,
         20,  20,   0,   0,   0,   0,  20,  20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
    ]
]

class BaseEvaluation(object):
    def __init__(self, board: Board):
        if board is None:
            raise ValueError("Board must be specified")
        self.board = board

    def evaluate(self) -> int:
        return 0


class PieceValueMixin(BaseEvaluation):
    def evaluate(self) -> int:
        score = super(PieceValueMixin, self).evaluate()
        for piece in chess.PIECE_TYPES:
            pieces_mask = self.board.pieces_mask(piece, self.board.turn)
            score += chess.popcount(pieces_mask) * PIECE_VALUES[piece]

            pieces_mask = self.board.pieces_mask(piece, not self.board.turn)
            score -= chess.popcount(pieces_mask) * PIECE_VALUES[piece]

        return score
    

class PieceSquareTableMixin(BaseEvaluation):
    def evaluate(self) -> int:
        parent_score = super(PieceSquareTableMixin, self).evaluate()
        score = 0
        for piece in chess.PIECE_TYPES:
            for square in self.board.pieces(piece, chess.WHITE):
                score += PIECE_SQUARE_TABLES[piece][square]
            for square in self.board.pieces(piece, chess.BLACK):
                score -= PIECE_SQUARE_TABLES[piece][square ^ 56]
        if not self.board.turn: #Black to Move
            score = -score
        return parent_score + score