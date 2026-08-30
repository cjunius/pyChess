"""Unit tests for ``eval_terms`` - the positional layer over PeSTO."""

import chess

from pychess import eval_terms
from pychess.eval_board import EvalBoard
from pychess.evaluation import PestoEvaluator


def _pawns(fen: str) -> tuple[int, int]:
    b = chess.Board(fen)
    return b.pawns & b.occupied_co[chess.WHITE], b.pawns & b.occupied_co[chess.BLACK]


def test_pawn_structure_is_zero_at_the_start():
    assert eval_terms.pawn_structure(*_pawns(chess.STARTING_FEN)) == (0, 0)


def test_passed_pawn_scores_more_the_further_it_is_advanced():
    near = eval_terms.pawn_structure(*_pawns("4k3/8/8/8/4P3/8/8/4K3 w - - 0 1"))
    far = eval_terms.pawn_structure(*_pawns("4k3/8/4P3/8/8/8/8/4K3 w - - 0 1"))
    assert 0 < near[0] < far[0]
    assert 0 < near[1] < far[1]


def test_isolated_and_doubled_pawns_are_penalised():
    # White: doubled + isolated a-pawns. Black: healthy trio.
    mg, eg = eval_terms.pawn_structure(*_pawns("4k3/5ppp/8/8/P7/P7/8/4K3 w - - 0 1"))
    assert mg < 0 and eg < 0


def test_pawn_structure_is_colour_symmetric():
    fen = "2r3k1/1p3ppp/p7/3p4/3P4/P7/1P3PPP/2R3K1 w - - 0 1"
    mg, eg = eval_terms.pawn_structure(*_pawns(fen))
    m_mg, m_eg = eval_terms.pawn_structure(*_pawns(chess.Board(fen).mirror().fen()))
    assert (mg, eg) == (-m_mg, -m_eg)


def test_positional_is_colour_symmetric():
    # A position exercising every term for both colours: bishop pairs, rooks on
    # open / half-open files, a knight outpost, ragged pawns, exposed kings.
    fen = "2r3k1/1b3p1p/1np5/pP1p4/P2P4/1NP5/1B3P1P/2R3K1 w - - 0 1"
    board = chess.Board(fen)
    mirror = board.mirror()
    for prior in ((0, 0), (17, -9)):
        a = eval_terms.positional(board, *prior)
        b = eval_terms.positional(mirror, -prior[0], -prior[1])
        assert a == (-b[0], -b[1])


def test_bishop_pair_favours_the_side_that_has_it():
    # White two bishops, Black two knights, otherwise identical.
    board = chess.Board("1n1nk3/8/8/8/8/8/8/1B1BK3 w - - 0 1")
    mg, eg = eval_terms.positional(board, 0, 0)
    assert mg >= eval_terms.BISHOP_PAIR_MG
    assert eg >= eval_terms.BISHOP_PAIR_EG


def test_rook_on_an_open_file_beats_a_rook_on_a_closed_one():
    open_file = eval_terms.positional(chess.Board("4k3/8/8/8/8/8/5PPP/R3K3 w - - 0 1"), 0, 0)
    closed = eval_terms.positional(chess.Board("4k3/8/8/8/8/8/P4PPP/R3K3 w - - 0 1"), 0, 0)
    assert open_file[0] > closed[0]


def test_knight_outpost_is_rewarded():
    # White knight on d6, defended by the c5 pawn, no black b/d pawn to evict it.
    board = chess.Board("4k3/8/3N4/2P5/8/8/8/4K3 w - - 0 1")
    mg, _eg = eval_terms.positional(board, 0, 0)
    assert mg >= eval_terms.KNIGHT_OUTPOST


def test_king_safety_penalises_a_missing_pawn_shield():
    safe = eval_terms.positional(chess.Board("4k3/8/8/8/8/8/5PPP/6K1 w - - 0 1"), 0, 0)
    exposed = eval_terms.positional(chess.Board("4k3/8/8/8/8/8/8/6K1 w - - 0 1"), 0, 0)
    assert exposed[0] < safe[0]


def test_evaluator_pawn_cache_matches_the_uncached_result():
    ev = PestoEvaluator()
    board = EvalBoard("2r3k1/1p3ppp/p7/3p4/3P4/P7/1P3PPP/2R3K1 w - - 0 1")
    first = ev.evaluate(board)
    assert ev._pawn_cache  # populated
    assert ev.evaluate(board) == first  # cache hit is consistent


def test_tempo_bonus_goes_to_the_side_to_move():
    white = PestoEvaluator().evaluate(chess.Board("4k3/8/8/8/8/8/8/4K3 w - - 0 1"))
    black = PestoEvaluator().evaluate(chess.Board("4k3/8/8/8/8/8/8/4K3 b - - 0 1"))
    assert white == eval_terms.TEMPO
    assert black == eval_terms.TEMPO
