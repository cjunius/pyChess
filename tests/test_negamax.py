"""Unit tests for ``negamax`` - a ``Negamax`` assembled from real collaborators
plus the ``is_drawn`` helper."""

import chess
import pytest

from pychess.clock import Clock
from pychess.constants import INF, MATE
from pychess.evaluation import PestoEvaluator
from pychess.move_ordering import MoveOrderer
from pychess.negamax import Negamax, SearchAbortError, is_drawn
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
