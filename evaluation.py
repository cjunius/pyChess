import chess

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
    def __init__(self):
        pass

    def evaluate(self, board) -> int:
        return 0


class PieceValueMixin(BaseEvaluation):
    def evaluate(self, board) -> int:
        score = super(PieceValueMixin, self).evaluate(board)
        for piece in chess.PIECE_TYPES:
            pieces_mask = board.pieces_mask(piece, board.turn)
            score += chess.popcount(pieces_mask) * PIECE_VALUES[piece]

            pieces_mask = board.pieces_mask(piece, not board.turn)
            score -= chess.popcount(pieces_mask) * PIECE_VALUES[piece]

        return score
    

class PieceSquareTableMixin(BaseEvaluation):
    def evaluate(self, board) -> int:
        parent_score = super(PieceSquareTableMixin, self).evaluate(board)
        score = 0
        for piece in chess.PIECE_TYPES:
            for square in board.pieces(piece, chess.WHITE):
                score += PIECE_SQUARE_TABLES[piece][square]
            for square in board.pieces(piece, chess.BLACK):
                score -= PIECE_SQUARE_TABLES[piece][square ^ 56]
        if not board.turn: #Black to Move
            score = -score
        return parent_score + score
    

class PieceValueSquareTableMixin(BaseEvaluation):
    def evaluate(self, board) -> int:
        parent_score = super(PieceValueSquareTableMixin, self).evaluate(board)
        score = 0
        for piece in chess.PIECE_TYPES:
            for square in board.pieces(piece, chess.WHITE):
                score += PIECE_SQUARE_TABLES[piece][square] + PIECE_VALUES[piece]
            for square in board.pieces(piece, chess.BLACK):
                score -= PIECE_SQUARE_TABLES[piece][square ^ 56] + PIECE_VALUES[piece]
        if not board.turn: #Black to Move
            score = -score
        return parent_score + score


class MobilityMixin(BaseEvaluation):
    def evaluate(self, board) -> int:
        parent_score = super(MobilityMixin, self).evaluate(board)
        if len(list(board.move_stack)) == 0:
            return 0

        last_move = board.pop()
        countA = len(list(board.legal_moves))
        board.push(last_move)
        countB = len(list(board.legal_moves))
        return countA - countB + parent_score
    

class BoardControlEvaluationMixin(BaseEvaluation):
    def evaluate(self, board) -> int:
        eval = super(BoardControlEvaluationMixin, self).evaluate(board)
        for square in chess.SquareSet(board.occupied_co[board.turn]):
            eval += len(board.attacks(square))

        for square in chess.SquareSet(board.occupied_co[not board.turn]):
            eval -= len(board.attacks(square))

        return eval