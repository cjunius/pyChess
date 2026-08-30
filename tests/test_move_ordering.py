"""Unit tests for ``move_ordering.MoveOrderer``."""

import chess

from pychess.move_ordering import MoveOrderer


def test_tt_move_comes_first():
    board = chess.Board()
    tt_move = chess.Move.from_uci("g1f3")
    ordered = MoveOrderer().order_moves(board, tt_move=tt_move, ply=0)
    assert ordered[0] == tt_move


def test_captures_precede_quiets():
    # White pawn on e4 can take on d5; lots of quiet moves available.
    board = chess.Board("rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
    ordered = MoveOrderer().order_moves(board)
    assert board.is_capture(ordered[0])
    assert ordered[0] == chess.Move.from_uci("e4d5")


def test_root_moves_restricts_the_root_only():
    board = chess.Board()
    keep = {chess.Move.from_uci("e2e4"), chess.Move.from_uci("d2d4")}
    orderer = MoveOrderer(root_moves=keep)
    assert set(orderer.order_moves(board, ply=0)) == keep
    # deeper plies are unrestricted
    assert len(orderer.order_moves(board, ply=1)) == 20


def test_killer_move_beats_other_quiets():
    board = chess.Board()
    orderer = MoveOrderer()
    killer = chess.Move.from_uci("h2h3")
    orderer.record_killer(0, killer)
    ordered = list(orderer.order_moves(board, ply=0))
    quiets = [m for m in ordered if not board.is_capture(m)]
    assert quiets[0] == killer


def test_is_killer_tracks_recorded_killers():
    orderer = MoveOrderer()
    killer = chess.Move.from_uci("h2h3")
    assert not orderer.is_killer(0, killer)
    orderer.record_killer(0, killer)
    assert orderer.is_killer(0, killer)
    assert not orderer.is_killer(1, killer)


def test_history_score_reflects_recorded_cutoffs():
    board = chess.Board()
    orderer = MoveOrderer()
    move = chess.Move.from_uci("g1f3")
    assert orderer.history_score(board, move) == 0
    orderer.record_history(board, move, depth=4)
    assert orderer.history_score(board, move) == 16


def test_mvvlva_prefers_taking_the_bigger_piece():
    # White pawn on d4 could take either rook on c5 / e5.
    board = chess.Board("3qk3/8/8/2r1r3/3P4/8/8/3QK3 w - - 0 1")
    pxr = chess.Move.from_uci("d4c5")
    pxr2 = chess.Move.from_uci("d4e5")
    assert MoveOrderer().mvvlva(board, pxr) == MoveOrderer().mvvlva(board, pxr2) > 0
