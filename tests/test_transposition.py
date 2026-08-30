"""Unit tests for ``transposition.TranspositionTable``."""

import chess

from pychess.constants import INF, MATE_GUARD, TT_EXACT, TT_LOWER, TT_UPPER
from pychess.transposition import TranspositionTable

STARTPOS = chess.Board()


def test_probe_miss_on_empty():
    tt = TranspositionTable()
    assert tt.probe(tt.key(STARTPOS), 1, -INF, INF) == (False, 0, None)


def test_exact_roundtrips():
    tt = TranspositionTable()
    key = tt.key(STARTPOS)
    move = chess.Move.from_uci("e2e4")
    tt.store(key, 4, 25, TT_EXACT, move)
    assert tt.probe(key, 4, -INF, INF) == (True, 25, move)


def test_shallower_entry_is_not_a_cutoff_but_still_gives_the_move():
    tt = TranspositionTable()
    key = tt.key(STARTPOS)
    move = chess.Move.from_uci("e2e4")
    tt.store(key, 2, 25, TT_EXACT, move)
    assert tt.probe(key, 5, -INF, INF) == (False, 0, move)


def test_lower_bound_only_cuts_when_it_beats_beta():
    tt = TranspositionTable()
    key = tt.key(STARTPOS)
    tt.store(key, 4, 50, TT_LOWER, None)
    assert tt.probe(key, 4, -INF, 40) == (True, 50, None)
    assert tt.probe(key, 4, -INF, 60) == (False, 0, None)


def test_upper_bound_only_cuts_when_it_is_below_alpha():
    tt = TranspositionTable()
    key = tt.key(STARTPOS)
    tt.store(key, 4, 50, TT_UPPER, None)
    assert tt.probe(key, 4, 60, INF) == (True, 50, None)
    assert tt.probe(key, 4, 40, INF) == (False, 0, None)


def test_deeper_entry_is_kept_on_store():
    tt = TranspositionTable()
    key = tt.key(STARTPOS)
    tt.store(key, 6, 10, TT_EXACT, None)
    tt.store(key, 3, 999, TT_EXACT, None)
    assert tt.probe(key, 3, -INF, INF) == (True, 10, None)


def test_mate_scores_are_never_returned_as_a_bound():
    tt = TranspositionTable()
    key = tt.key(STARTPOS)
    move = chess.Move.from_uci("e2e4")
    tt.store(key, 5, MATE_GUARD + 1, TT_EXACT, move)
    cutoff, value, got = tt.probe(key, 3, -INF, INF)
    assert cutoff is False and value == 0 and got == move
