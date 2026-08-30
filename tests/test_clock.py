"""Unit tests for ``clock`` - the stop predicate and time management."""

import chess
import pytest

from pychess.clock import Clock, deadline_from_limits


def test_never_stops_until_armed():
    clock = Clock(deadline=0.0)  # already in the past
    assert clock.should_stop(10**9) is False
    clock.arm()
    assert clock.should_stop(0) is True


def test_node_limit():
    clock = Clock(node_limit=1000)
    clock.arm()
    assert clock.should_stop(999) is False
    assert clock.should_stop(1000) is True


def test_deadline_from_limits_movetime():
    assert deadline_from_limits(chess.Board(), {"movetime": 2000}, 100.0) == 102.0


def test_deadline_from_limits_depth_only_is_open_ended():
    assert deadline_from_limits(chess.Board(), {"depth": 8}, 0.0) is None


def test_deadline_from_limits_bare_go_uses_default():
    assert deadline_from_limits(chess.Board(), {}, 0.0) == pytest.approx(4.0)


def test_deadline_from_limits_infinite():
    assert deadline_from_limits(chess.Board(), {"infinite": True}, 0.0) == 60.0


def test_deadline_from_limits_clock_budget():
    # 60s left, 2s increment, 30 moves to go: 60000/31 + 0.75*2000 ms,
    # below the 0.4*wtime cap.
    board = chess.Board()
    got = deadline_from_limits(board, {"wtime": 60000, "winc": 2000, "movestogo": 30}, 0.0)
    assert got == pytest.approx(60000 / 31 / 1000 + 1.5)


def test_deadline_from_limits_uses_side_to_move_clock():
    board = chess.Board()
    board.push_uci("e2e4")  # black to move -> btime applies, wtime ignored
    got = deadline_from_limits(board, {"wtime": 1, "btime": 60000}, 0.0)
    assert got == pytest.approx(60000 / 31 / 1000)
