"""Unit tests for ``negamax`` - a ``Negamax`` assembled from real collaborators
plus the ``is_drawn`` helper."""

import chess
import pytest

from pychess.clock import Clock
from pychess.constants import INF, MATE
from pychess.evaluation import PestoEvaluator
from pychess.move_ordering import MoveOrderer
from pychess.negamax import Negamax, SearchAbortError, claims_draw, is_drawn
from pychess.transposition import TranspositionTable

MATE_IN_1 = chess.Board("4k3/8/4K3/8/8/8/8/7R w - - 0 1")  # Rh8#


def make_negamax(clock: Clock | None = None, tt: TranspositionTable | None = None) -> Negamax:
    return Negamax(PestoEvaluator(), MoveOrderer(), tt or TranspositionTable(), clock or Clock())


def test_finds_mate_in_one():
    score, pv = make_negamax().search(MATE_IN_1.copy(), -INF, INF, 3)
    assert score >= MATE - 100
    assert pv[0] == chess.Move.from_uci("h1h8")


def test_avoids_getting_mated():
    board = chess.Board("6k1/5ppp/8/8/8/8/5PPP/R5K1 b - - 0 1")
    score, _pv = make_negamax().search(board, -INF, INF, 4)
    assert score > -(MATE - 100)  # not getting mated


def test_wins_the_hanging_rook():
    # Rooks share the 4th rank; black's is undefended and the king is far.
    board = chess.Board("4k3/8/8/8/r6R/8/8/4K3 w - - 0 1")
    score, pv = make_negamax().search(board, -INF, INF, 4)
    assert pv[0] == chess.Move.from_uci("h4a4")
    assert score > 300


def test_depth_one_still_returns_a_move():
    _score, pv = make_negamax().search(chess.Board(), -INF, INF, 1)
    assert pv and pv[0] in set(chess.Board().legal_moves)


def test_shares_node_count_between_search_and_quiescence():
    engine = make_negamax()
    engine.search(chess.Board(), -INF, INF, 3)
    assert engine.nodes > 0


def test_abort_is_raised_once_the_clock_is_armed():
    clock = Clock(deadline=0.0)
    clock.arm()
    engine = make_negamax(clock=clock)
    with pytest.raises(SearchAbortError):
        engine.search(chess.Board(), -INF, INF, 6, ply=1)


def test_is_drawn_stalemate():
    assert is_drawn(chess.Board("7k/5Q2/6K1/8/8/8/8/8 b - - 0 1"))


def test_is_drawn_insufficient_material():
    assert is_drawn(chess.Board("4k3/8/8/8/8/8/8/4K3 w - - 0 1"))


def test_is_drawn_normal_position_is_not_drawn():
    assert not is_drawn(chess.Board())


# -- null-move pruning ------------------------------------------------------


def test_null_ok_guards():
    # Normal middlegame position, deep enough: null move is allowed.
    assert Negamax._null_ok(chess.Board(), depth=4, can_null=True, ply=1)
    # Already tried a null move on the way here.
    assert not Negamax._null_ok(chess.Board(), depth=4, can_null=False, ply=1)
    # Root node: keep the PV honest.
    assert not Negamax._null_ok(chess.Board(), depth=4, can_null=True, ply=0)
    # Too shallow.
    assert not Negamax._null_ok(chess.Board(), depth=2, can_null=True, ply=1)
    # In check: passing is not an option.
    in_check = chess.Board("4k3/8/8/8/7b/8/5P2/4K3 w - - 0 1")
    assert not Negamax._null_ok(in_check, depth=4, can_null=True, ply=1)
    # King + pawns only: likely zugzwang, the null search would lie.
    kp = chess.Board("4k3/pppppppp/8/8/8/8/PPPPPPPP/4K3 w - - 0 1")
    assert not Negamax._null_ok(kp, depth=4, can_null=True, ply=1)


# A quiet middlegame where a free move plainly still loses for the side that
# took it, so null-move cut-offs land.
QUIET_MIDGAME = "r2q1rk1/ppp2ppp/2np1n2/2b1p3/2B1P3/2NP1N2/PPP2PPP/R1BQ1RK1 w - - 0 8"


def test_null_move_prunes_nodes_without_changing_the_move(monkeypatch):
    board = chess.Board(QUIET_MIDGAME)

    with_null = make_negamax()
    score_a, pv_a = with_null.search(board.copy(), -INF, INF, 5)

    without_null = make_negamax()
    monkeypatch.setattr(Negamax, "_null_ok", staticmethod(lambda *a, **k: False))
    score_b, pv_b = without_null.search(board.copy(), -INF, INF, 5)

    assert with_null.nodes < without_null.nodes
    assert pv_a[0] == pv_b[0]
    assert abs(score_a - score_b) <= 40


def test_null_move_still_finds_mate_in_one():
    score, pv = make_negamax().search(MATE_IN_1.copy(), -INF, INF, 4)
    assert score >= MATE - 100
    assert pv[0] == chess.Move.from_uci("h1h8")


# -- late move reductions -------------------------------------------------


def test_lmr_reduction_grows_with_lateness_and_depth():
    # First few moves, shallow node: no reduction.
    assert Negamax._lmr_reduction(3, 4, favoured=False) == 1
    # Later move, deep node: bigger reduction.
    assert Negamax._lmr_reduction(8, 10, favoured=False) == 3
    # A killer / good-history move is reduced one ply less.
    assert Negamax._lmr_reduction(8, 10, favoured=True) == 2
    # Never reduces the reduced search below one ply.
    assert Negamax._lmr_reduction(20, 3, favoured=False) == 1
    assert Negamax._lmr_reduction(3, 3, favoured=True) == 0


def test_lmr_prunes_nodes_without_blundering(monkeypatch):
    board = chess.Board("r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/2N2N2/PPPP1PPP/R1BQK2R w KQkq - 4 4")

    with_lmr = make_negamax()
    score_a, pv_a = with_lmr.search(board.copy(), -INF, INF, 4)

    without_lmr = make_negamax()
    monkeypatch.setattr(Negamax, "_lmr_reduction", staticmethod(lambda *a, **k: 0))
    score_b, _pv_b = without_lmr.search(board.copy(), -INF, INF, 4)

    assert with_lmr.nodes < without_lmr.nodes  # the reductions save work
    assert pv_a[0] in set(board.legal_moves)
    assert abs(score_a - score_b) <= 40  # and don't cost more than a fraction of a pawn


def test_lmr_still_wins_the_hanging_rook():
    board = chess.Board("4k3/8/8/8/r6R/8/8/4K3 w - - 0 1")
    _score, pv = make_negamax().search(board, -INF, INF, 5)
    assert pv[0] == chess.Move.from_uci("h4a4")


# -- principal variation search -----------------------------------------


def test_pvs_returns_a_legal_consistent_pv():
    # Walk the reported PV from the start position; every move must be legal in
    # turn - a broken scout / re-search would splice in a stale line.
    board = chess.Board()
    _score, pv = make_negamax().search(board.copy(), -INF, INF, 6)
    assert pv
    for move in pv:
        assert move in board.legal_moves
        board.push(move)


def test_pvs_finds_a_quiet_best_move_ordered_after_captures():
    # 1.Nxe5?? Qa5+ wins the knight; the quiet 1.d3 (ordered well after the
    # capture) holds everything. PVS must re-search past the scout to see it.
    board = chess.Board("r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4")
    score, pv = make_negamax().search(board, -INF, INF, 5)
    assert pv[0] != chess.Move.from_uci("f3e5")
    assert score > -50  # not down a piece


# -- draw, repetition and mate scoring ---------------------------------

# White mates in two (Kf7, Kh7, Rh1#) - checkmate lands 3 plies from the root.
MATE_IN_2 = chess.Board("7k/8/5K2/8/8/8/8/R7 w - - 0 1")

# White is up a rook but the position has already repeated three times.
REPETITION = chess.Board("4k3/8/8/8/8/8/8/R3K3 w - - 0 1")
for _uci in ["a1a2", "e8d8", "a2a1", "d8e8"] * 2:
    REPETITION.push_uci(_uci)


def test_claims_draw_spots_repetition_and_the_fifty_move_rule():
    assert claims_draw(REPETITION)
    assert not claims_draw(chess.Board())
    fifty = chess.Board("4k3/8/8/8/8/8/8/R3K3 w - - 0 1")
    fifty.halfmove_clock = 100
    assert claims_draw(fifty)


def test_mate_in_two_is_scored_by_distance_from_the_root():
    score, pv = make_negamax().search(MATE_IN_2.copy(), -INF, INF, 5)
    assert score == MATE - 3  # checkmate 3 plies away
    board = MATE_IN_2.copy()
    for move in pv:
        board.push(move)
    assert board.is_checkmate()
    assert len(pv) == 3


def test_mate_score_is_stable_across_depths():
    # The TT stores mate scores relative to the storing node; if the ply rebase
    # were wrong, a hit from a different depth would shift the reported mate.
    scores = {d: make_negamax().search(MATE_IN_2.copy(), -INF, INF, d)[0] for d in (4, 5, 6, 7)}
    assert set(scores.values()) == {MATE - 3}


def test_search_scores_a_repetition_as_a_draw_despite_material():
    # ply=1 so the in-tree draw guard fires; White is a whole rook up.
    score, _pv = make_negamax().search(REPETITION.copy(), -INF, INF, 4, ply=1)
    assert score == 0


def test_search_scores_the_fifty_move_rule_as_a_draw():
    board = chess.Board("4k3/8/8/8/8/8/8/R3K3 w - - 0 1")
    board.halfmove_clock = 100
    score, _pv = make_negamax().search(board, -INF, INF, 4, ply=1)
    assert score == 0


def test_root_still_returns_a_move_in_an_already_drawn_position():
    # At the root (ply 0) the guard is skipped - the engine must still move.
    _score, pv = make_negamax().search(REPETITION.copy(), -INF, INF, 4)
    assert pv and pv[0] in set(REPETITION.legal_moves)


def test_quiesce_scores_a_repetition_as_a_draw():
    assert make_negamax().quiesce(REPETITION.copy(), -INF, INF, 0, 1) == 0
