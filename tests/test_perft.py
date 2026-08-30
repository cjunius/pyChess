"""Perft (performance test / move-path enumeration) regression tests.

Reference node counts are the well-known published values from the Chess
Programming Wiki (https://www.chessprogramming.org/Perft_Results).
"""

import multiprocessing

import chess
import pytest

from pychess.perft import count_nodes, parallel_perft

STARTPOS = chess.STARTING_FEN
KIWIPETE = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
POSITION_3 = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1"
POSITION_4 = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"
POSITION_5 = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8"
POSITION_6 = "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10"

CASES = [
    (STARTPOS, 1, 20),
    (STARTPOS, 2, 400),
    (STARTPOS, 3, 8902),
    (STARTPOS, 4, 197281),
    (KIWIPETE, 1, 48),
    (KIWIPETE, 2, 2039),
    (KIWIPETE, 3, 97862),
    (POSITION_3, 1, 14),
    (POSITION_3, 2, 191),
    (POSITION_3, 3, 2812),
    (POSITION_3, 4, 43238),
    (POSITION_4, 1, 6),
    (POSITION_4, 2, 264),
    (POSITION_4, 3, 9467),
    (POSITION_5, 1, 44),
    (POSITION_5, 2, 1486),
    (POSITION_5, 3, 62379),
    (POSITION_6, 1, 46),
    (POSITION_6, 2, 2079),
    (POSITION_6, 3, 89890),
]


@pytest.mark.parametrize("fen,depth,expected", CASES)
def test_count_nodes(fen, depth, expected):
    assert count_nodes(depth, chess.Board(fen)) == expected


def test_count_nodes_depth_zero():
    assert count_nodes(0, chess.Board()) == 1


def test_parallel_perft_matches_serial():
    board = chess.Board(KIWIPETE)
    with multiprocessing.Pool(2) as pool:
        assert parallel_perft(pool, 3, board) == count_nodes(3, board)
