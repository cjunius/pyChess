"""Unit tests for ``evaluation.PestoEvaluator``."""

import chess

from pychess.eval_board import EvalBoard
from pychess.evaluation import PestoEvaluator


def test_startpos_is_roughly_balanced():
    assert abs(PestoEvaluator().evaluate(chess.Board())) <= 60


def test_side_to_move_relative():
    ev = PestoEvaluator()
    w = chess.Board("4k3/8/8/8/8/8/8/R3K3 w - - 0 1")
    b = chess.Board("4k3/8/8/8/8/8/8/R3K3 b - - 0 1")
    assert ev.evaluate(w) > 0  # white to move, white is up a rook
    assert ev.evaluate(b) < 0  # black to move, still down a rook


def test_incremental_accumulator_matches_recompute():
    incremental = EvalBoard()
    for uci in ("e2e4", "e7e5", "g1f3", "b8c6", "f1b5", "a7a6"):
        incremental.push_uci(uci)
    plain = chess.Board(incremental.fen())
    assert PestoEvaluator().evaluate(incremental) == PestoEvaluator().evaluate(plain)
