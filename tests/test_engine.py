"""Tests for the assembled engines and the Lazy SMP coordinator."""

import time

import chess

from pychess import lazy_smp
from pychess.engine import Engine, RandomEngine
from pychess.lazy_smp import SearchResult, _Payload, _result_rank, _worker
from pychess.shared_tt import SharedFlag, SharedTT


def test_random_engine_returns_a_legal_move():
    board = chess.Board()
    result = RandomEngine().search(board)
    assert isinstance(result, SearchResult)
    assert result.pv[0] in set(board.legal_moves)
    assert result.score == 0


def test_result_rank_orders_win_over_depth_over_loss():
    win = lazy_smp._WorkerResult(9999, ["a1a8"], 3, 10)
    deep = lazy_smp._WorkerResult(20, ["e2e4"], 8, 10)
    shallow = lazy_smp._WorkerResult(50, ["d2d4"], 4, 10)
    loss = lazy_smp._WorkerResult(-9999, ["h2h3"], 5, 10)
    assert max([deep, shallow, win, loss], key=_result_rank) is win
    assert max([deep, shallow, loss], key=_result_rank) is deep
    assert min([deep, shallow, loss], key=_result_rank) is loss


def test_worker_runs_a_search_in_process():
    tt = SharedTT(slots=1 << 12, create=True)
    stop = SharedFlag(create=True)
    try:
        payload: _Payload = (
            chess.STARTING_FEN,
            [],
            None,
            3,
            time.time() + 5.0,
            tt.name,
            tt.slots,
            0,
            stop.name,
        )
        result = _worker(payload)
        assert result.depth >= 1
        assert result.pv and chess.Move.from_uci(result.pv[0]) in chess.Board().legal_moves
        assert result.nodes > 0
    finally:
        stop.close()
        stop.unlink()
        tt.close()
        tt.unlink()


def test_engine_search_end_to_end():
    result = Engine().search(chess.Board(), {"movetime": 300})
    assert result.pv
    assert result.pv[0] in set(chess.Board().legal_moves)
    assert result.nodes > 0
