"""Positional evaluation terms layered on top of the PeSTO piece-square tables.

``positional(board)`` returns a ``(mg, eg)`` pair from White's point of view, to
be added to the tapered PeSTO score before the side-to-move flip. Everything
here is recomputed from scratch per call; the pure-pawn terms (passed /
isolated / doubled) are the expensive part and are memoised by
``PestoEvaluator`` on the pawn bitboards.

Weights are deliberately modest - a mistuned term should nudge, not dominate.
"""

from __future__ import annotations

import chess

# --- weights (centipawns) ------------------------------------------------

PASSED_MG = (0, 5, 10, 20, 35, 60, 100, 0)  # by the pawn's own rank (White view)
PASSED_EG = (0, 15, 25, 40, 65, 105, 160, 0)
ISOLATED_MG, ISOLATED_EG = 12, 8
DOUBLED_MG, DOUBLED_EG = 8, 18

BISHOP_PAIR_MG, BISHOP_PAIR_EG = 22, 42
ROOK_OPEN_FILE, ROOK_HALF_OPEN_FILE = 24, 11
KNIGHT_OUTPOST = 20
TEMPO = 12

SHIELD_MISSING = 12  # a file next to the king with no friendly pawn
KING_OPEN_FILE = 14  # ... and no pawn of either colour on it

# --- precomputed masks -------------------------------------------------

_ADJACENT_FILES = tuple(
    (chess.BB_FILES[f - 1] if f > 0 else 0) | (chess.BB_FILES[f + 1] if f < 7 else 0)
    for f in range(8)
)


def _ahead(rank: int, *, white: bool) -> int:
    ranks = range(rank + 1, 8) if white else range(rank)
    mask = 0
    for r in ranks:
        mask |= chess.BB_RANKS[r]
    return mask


_WHITE_PASSED_BLOCK = []  # enemy pawns here stop a White passer
_BLACK_PASSED_BLOCK = []
_WHITE_FILE_AHEAD = []  # own file, strictly ahead (doubled / passer-in-front)
_BLACK_FILE_AHEAD = []
_WHITE_OUTPOST_BLOCK = []  # enemy pawns here can chase a White knight off
_BLACK_OUTPOST_BLOCK = []
for _sq in range(64):
    _f, _r = chess.square_file(_sq), chess.square_rank(_sq)
    _own_adj = chess.BB_FILES[_f] | _ADJACENT_FILES[_f]
    _WHITE_PASSED_BLOCK.append(_own_adj & _ahead(_r, white=True))
    _BLACK_PASSED_BLOCK.append(_own_adj & _ahead(_r, white=False))
    _WHITE_FILE_AHEAD.append(chess.BB_FILES[_f] & _ahead(_r, white=True))
    _BLACK_FILE_AHEAD.append(chess.BB_FILES[_f] & _ahead(_r, white=False))
    _WHITE_OUTPOST_BLOCK.append(_ADJACENT_FILES[_f] & _ahead(_r, white=True))
    _BLACK_OUTPOST_BLOCK.append(_ADJACENT_FILES[_f] & _ahead(_r, white=False))

_OUTPOST_RANKS_WHITE = chess.BB_RANK_4 | chess.BB_RANK_5 | chess.BB_RANK_6
_OUTPOST_RANKS_BLACK = chess.BB_RANK_5 | chess.BB_RANK_4 | chess.BB_RANK_3


# --- pawn structure (memoisable: depends only on pawn placement) --------


def pawn_structure(white_pawns: int, black_pawns: int) -> tuple[int, int]:
    """``(mg, eg)`` White-POV score for passed / isolated / doubled pawns."""
    mg = eg = 0

    for sq in chess.scan_forward(white_pawns):
        f = chess.square_file(sq)
        if not (white_pawns & _WHITE_FILE_AHEAD[sq]):
            if not (black_pawns & _WHITE_PASSED_BLOCK[sq]):
                r = chess.square_rank(sq)
                mg += PASSED_MG[r]
                eg += PASSED_EG[r]
        else:
            mg -= DOUBLED_MG
            eg -= DOUBLED_EG
        if not (white_pawns & _ADJACENT_FILES[f]):
            mg -= ISOLATED_MG
            eg -= ISOLATED_EG

    for sq in chess.scan_forward(black_pawns):
        f = chess.square_file(sq)
        if not (black_pawns & _BLACK_FILE_AHEAD[sq]):
            if not (white_pawns & _BLACK_PASSED_BLOCK[sq]):
                r = 7 - chess.square_rank(sq)
                mg -= PASSED_MG[r]
                eg -= PASSED_EG[r]
        else:
            mg += DOUBLED_MG
            eg += DOUBLED_EG
        if not (black_pawns & _ADJACENT_FILES[f]):
            mg += ISOLATED_MG
            eg += ISOLATED_EG

    return mg, eg


# --- everything else (piece placement relative to pawns / king) --------


def _king_safety_mg(board: chess.Board, color: chess.Color, all_pawns: int, own_pawns: int) -> int:
    king = board.king(color)
    if king is None:  # pragma: no cover - a legal board always has both kings
        return 0
    kf = chess.square_file(king)
    penalty = 0
    for f in range(max(0, kf - 1), min(7, kf + 1) + 1):
        file_bb = chess.BB_FILES[f]
        if not (own_pawns & file_bb):
            penalty += SHIELD_MISSING
            if not (all_pawns & file_bb):
                penalty += KING_OPEN_FILE
    return -penalty


def positional(board: chess.Board, pawn_mg: int, pawn_eg: int) -> tuple[int, int]:
    """``(mg, eg)`` White-POV positional score. ``pawn_mg`` / ``pawn_eg`` are the
    (possibly cached) :func:`pawn_structure` result for this position."""
    white = board.occupied_co[chess.WHITE]
    black = board.occupied_co[chess.BLACK]
    white_pawns = board.pawns & white
    black_pawns = board.pawns & black
    all_pawns = board.pawns

    mg, eg = pawn_mg, pawn_eg

    # Bishop pair.
    if chess.popcount(board.bishops & white) >= 2:
        mg += BISHOP_PAIR_MG
        eg += BISHOP_PAIR_EG
    if chess.popcount(board.bishops & black) >= 2:
        mg -= BISHOP_PAIR_MG
        eg -= BISHOP_PAIR_EG

    # Rooks on open / half-open files.
    for sq in chess.scan_forward(board.rooks & white):
        file_bb = chess.BB_FILES[chess.square_file(sq)]
        if not (all_pawns & file_bb):
            mg += ROOK_OPEN_FILE
        elif not (white_pawns & file_bb):
            mg += ROOK_HALF_OPEN_FILE
    for sq in chess.scan_forward(board.rooks & black):
        file_bb = chess.BB_FILES[chess.square_file(sq)]
        if not (all_pawns & file_bb):
            mg -= ROOK_OPEN_FILE
        elif not (black_pawns & file_bb):
            mg -= ROOK_HALF_OPEN_FILE

    # Knight outposts: on an advanced square, pawn-defended, unchallengeable by
    # an enemy pawn.
    for sq in chess.scan_forward(board.knights & white & _OUTPOST_RANKS_WHITE):
        if (white_pawns & chess.BB_PAWN_ATTACKS[chess.BLACK][sq]) and not (
            black_pawns & _WHITE_OUTPOST_BLOCK[sq]
        ):
            mg += KNIGHT_OUTPOST
            eg += KNIGHT_OUTPOST // 2
    for sq in chess.scan_forward(board.knights & black & _OUTPOST_RANKS_BLACK):
        if (black_pawns & chess.BB_PAWN_ATTACKS[chess.WHITE][sq]) and not (
            white_pawns & _BLACK_OUTPOST_BLOCK[sq]
        ):
            mg -= KNIGHT_OUTPOST
            eg -= KNIGHT_OUTPOST // 2

    # King safety (mid-game only; tapers out through ``taper``).
    mg += _king_safety_mg(board, chess.WHITE, all_pawns, white_pawns)
    mg -= _king_safety_mg(board, chess.BLACK, all_pawns, black_pawns)

    return mg, eg
