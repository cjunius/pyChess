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

# ---------------------------------------------------------------------------
# PeSTO tapered evaluation (Piece-Square Tables Only, Ronald Friederich)
#
# Separate mid-game and end-game piece values and tables; the final score is a
# linear interpolation between the two based on the amount of material left on
# the board ("game phase"). Tables below are written rank-8-first (as published
# on the Chess Programming Wiki) and flipped to python-chess square order
# (a1 = 0) at import time.
# ---------------------------------------------------------------------------

MG_VALUE = [82, 337, 365, 477, 1025, 0]      # P N B R Q K
EG_VALUE = [94, 281, 297, 512, 936, 0]
PHASE_INC = [0, 1, 1, 2, 4, 0]               # summed over all pieces, max 24

_MG_PAWN = [
      0,   0,   0,   0,   0,   0,   0,   0,
     98, 134,  61,  95,  68, 126,  34, -11,
     -6,   7,  26,  31,  65,  56,  25, -20,
    -14,  13,   6,  21,  23,  12,  17, -23,
    -27,  -2,  -5,  12,  17,   6,  10, -25,
    -26,  -4,  -4, -10,   3,   3,  33, -12,
    -35,  -1, -20, -23, -15,  24,  38, -22,
      0,   0,   0,   0,   0,   0,   0,   0,
]
_EG_PAWN = [
      0,   0,   0,   0,   0,   0,   0,   0,
    178, 173, 158, 134, 147, 132, 165, 187,
     94, 100,  85,  67,  56,  53,  82,  84,
     32,  24,  13,   5,  -2,   4,  17,  17,
     13,   9,  -3,  -7,  -7,  -8,   3,  -1,
      4,   7,  -6,   1,   0,  -5,  -1,  -8,
     13,   8,   8,  10,  13,   0,   2,  -7,
      0,   0,   0,   0,   0,   0,   0,   0,
]
_MG_KNIGHT = [
   -167, -89, -34, -49,  61, -97, -15, -107,
    -73, -41,  72,  36,  23,  62,   7,  -17,
    -47,  60,  37,  65,  84, 129,  73,   44,
     -9,  17,  19,  53,  37,  69,  18,   22,
    -13,   4,  16,  13,  28,  19,  21,   -8,
    -23,  -9,  12,  10,  19,  17,  25,  -16,
    -29, -53, -12,  -3,  -1,  18, -14,  -19,
   -105, -21, -58, -33, -17, -28, -19,  -23,
]
_EG_KNIGHT = [
    -58, -38, -13, -28, -31, -27, -63, -99,
    -25,  -8, -25,  -2,  -9, -25, -24, -52,
    -24, -20,  10,   9,  -1,  -9, -19, -41,
    -17,   3,  22,  22,  22,  11,   8, -18,
    -18,  -6,  16,  25,  16,  17,   4, -18,
    -23,  -3,  -1,  15,  10,  -3, -20, -22,
    -42, -20, -10,  -5,  -2, -20, -23, -44,
    -29, -51, -23, -15, -22, -18, -50, -64,
]
_MG_BISHOP = [
    -29,   4, -82, -37, -25, -42,   7,  -8,
    -26,  16, -18, -13,  30,  59,  18, -47,
    -16,  37,  43,  40,  35,  50,  37,  -2,
     -4,   5,  19,  50,  37,  37,   7,  -2,
     -6,  13,  13,  26,  34,  12,  10,   4,
      0,  15,  15,  15,  14,  27,  18,  10,
      4,  15,  16,   0,   7,  21,  33,   1,
    -33,  -3, -14, -21, -13, -12, -39, -21,
]
_EG_BISHOP = [
    -14, -21, -11,  -8,  -7,  -9, -17, -24,
     -8,  -4,   7, -12,  -3, -13,  -4, -14,
      2,  -8,   0,  -1,  -2,   6,   0,   4,
     -3,   9,  12,   9,  14,  10,   3,   2,
     -6,   3,  13,  19,   7,  10,  -3,  -9,
    -12,  -3,   8,  10,  13,   3,  -7, -15,
    -14, -18,  -7,  -1,   4,  -9, -15, -27,
    -23,  -9, -23,  -5,  -9, -16,  -5, -17,
]
_MG_ROOK = [
     32,  42,  32,  51,  63,   9,  31,  43,
     27,  32,  58,  62,  80,  67,  26,  44,
     -5,  19,  26,  36,  17,  45,  61,  16,
    -24, -11,   7,  26,  24,  35,  -8, -20,
    -36, -26, -12,  -1,   9,  -7,   6, -23,
    -45, -25, -16, -17,   3,   0,  -5, -33,
    -44, -16, -20,  -9,  -1,  11,  -6, -71,
    -19, -13,   1,  17,  16,   7, -37, -26,
]
_EG_ROOK = [
     13,  10,  18,  15,  12,  12,   8,   5,
     11,  13,  13,  11,  -3,   3,   8,   3,
      7,   7,   7,   5,   4,  -3,  -5,  -3,
      4,   3,  13,   1,   2,   1,  -1,   2,
      3,   5,   8,   4,  -5,  -6,  -8, -11,
     -4,   0,  -5,  -1,  -7, -12,  -8, -16,
     -6,  -6,   0,   2,  -9,  -9, -11,  -3,
     -9,   2,   3,  -1,  -5, -13,   4, -20,
]
_MG_QUEEN = [
    -28,   0,  29,  12,  59,  44,  43,  45,
    -24, -39,  -5,   1, -16,  57,  28,  54,
    -13, -17,   7,   8,  29,  56,  47,  57,
    -27, -27, -16, -16,  -1,  17,  -2,   1,
     -9, -26,  -9, -10,  -2,  -4,   3,  -3,
    -14,   2, -11,  -2,  -5,   2,  14,   5,
    -35,  -8,  11,   2,   8,  15,  -3,   1,
     -1, -18,  -9,  10, -15, -25, -31, -50,
]
_EG_QUEEN = [
     -9,  22,  22,  27,  27,  19,  10,  20,
    -17,  20,  32,  41,  58,  25,  30,   0,
    -20,   6,   9,  49,  47,  35,  19,   9,
      3,  22,  24,  45,  57,  40,  57,  36,
    -18,  28,  19,  47,  31,  34,  39,  23,
    -16, -27,  15,   6,   9,  17,  10,   5,
    -22, -23, -30, -16, -16, -23, -36, -32,
    -33, -28, -22, -43,  -5, -32, -20, -41,
]
_MG_KING = [
    -65,  23,  16, -15, -56, -34,   2,  13,
     29,  -1, -20,  -7,  -8,  -4, -38, -29,
     -9,  24,   2, -16, -20,   6,  22, -22,
    -17, -20, -12, -27, -30, -25, -14, -36,
    -49,  -1, -27, -39, -46, -44, -33, -51,
    -14, -14, -22, -46, -44, -30, -15, -27,
      1,   7,  -8, -64, -43, -16,   9,   8,
    -15,  36,  12, -54,   8, -28,  24,  14,
]
_EG_KING = [
    -74, -35, -18, -18, -11,  15,   4, -17,
    -12,  17,  14,  17,  17,  38,  23,  11,
     10,  17,  23,  15,  20,  45,  44,  13,
     -8,  22,  24,  27,  26,  33,  26,   3,
    -18,  -4,  21,  24,  27,  23,   9, -11,
    -19,  -3,  11,  21,  23,  16,   7,  -9,
    -27, -11,   4,  13,  14,   4,  -5, -17,
    -53, -34, -21, -11, -28, -14, -24, -43,
]


def _to_a1_first(table):
    """Flip a rank-8-first table to python-chess square order (a1 = 0)."""
    return [table[(7 - (i // 8)) * 8 + (i % 8)] for i in range(64)]


MG_PST = [_to_a1_first(t) for t in
          (_MG_PAWN, _MG_KNIGHT, _MG_BISHOP, _MG_ROOK, _MG_QUEEN, _MG_KING)]
EG_PST = [_to_a1_first(t) for t in
          (_EG_PAWN, _EG_KNIGHT, _EG_BISHOP, _EG_ROOK, _EG_QUEEN, _EG_KING)]


def pesto_terms(board):
    """Return ``(mg, eg, phase)`` from White's point of view, computed from
    scratch over the current position."""
    mg = eg = phase = 0
    for square, piece in board.piece_map().items():
        i = piece.piece_type - 1
        s = square if piece.color else square ^ 56
        sign = 1 if piece.color else -1
        mg += sign * (MG_VALUE[i] + MG_PST[i][s])
        eg += sign * (EG_VALUE[i] + EG_PST[i][s])
        phase += PHASE_INC[i]
    return mg, eg, phase


def taper(mg, eg, phase):
    """Interpolate between mid- and end-game scores (White's point of view)."""
    mg_phase = phase if phase < 24 else 24
    return (mg * mg_phase + eg * (24 - mg_phase)) // 24


class PeSTOEvaluationMixin(object):
    """Tapered PeSTO evaluation returned from the side-to-move's perspective.

    Uses the incrementally-maintained accumulator on ``EvalBoard`` when the
    board provides one, otherwise falls back to a full recompute.
    """

    def evaluate(self, board) -> int:
        mg = getattr(board, "_mg", None)
        if mg is None:
            mg, eg, phase = pesto_terms(board)
        else:
            eg, phase = board._eg, board._phase
        score = taper(mg, eg, phase)
        return score if board.turn else -score


class BaseEvaluation(object):
    def __init__(self):
        pass

    def evaluate(self, board) -> int:
        return 0


class PieceValueMixin(BaseEvaluation):
    def evaluate(self, board) -> int:
        score: int = super(PieceValueMixin, self).evaluate(board)
        for piece in chess.PIECE_TYPES:
            pieces_mask_turn = board.pieces_mask(piece, board.turn)
            score += chess.popcount(pieces_mask_turn) * PIECE_VALUES[piece]

            pieces_mask_not_turn = board.pieces_mask(piece, board.turn ^ 1)
            score -= chess.popcount(pieces_mask_not_turn) * PIECE_VALUES[piece]

        return score
    

class PieceSquareTableMixin(BaseEvaluation):
    def evaluate(self, board) -> int:
        parent_score: int = super(PieceSquareTableMixin, self).evaluate(board)
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
        parent_score: int = super(PieceValueSquareTableMixin, self).evaluate(board)
        score = 0
        for piece in chess.PIECE_TYPES:
            for square in board.pieces(piece, chess.WHITE):
                score += PIECE_SQUARE_TABLES[piece][square] + PIECE_VALUES[piece]
            for square in board.pieces(piece, chess.BLACK):
                score -= PIECE_SQUARE_TABLES[piece][square ^ 56] + PIECE_VALUES[piece]
        if board.turn ^ 1: #Black to Move
            score = -score
        return score + parent_score

class MobilityMixin(BaseEvaluation):
    def evaluate(self, board) -> int:
        parent_score: int = super(MobilityMixin, self).evaluate(board)
        if len(list(board.move_stack)) == 0:
            return 0

        last_move = board.pop()
        countA = len(list(board.legal_moves))
        board.push(last_move)
        countB = len(list(board.legal_moves))
        return countA - countB + parent_score
    

class BoardControlEvaluationMixin(BaseEvaluation):
    def evaluate(self, board) -> int:
        eval: int = super(BoardControlEvaluationMixin, self).evaluate(board)
        for square in chess.SquareSet(board.occupied_co[board.turn]):
            eval += len(board.attacks(square))

        for square in chess.SquareSet(board.occupied_co[board.turn ^ 1]):
            eval -= len(board.attacks(square))

        return eval