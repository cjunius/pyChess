import chess
import pytest

from archive.config import Config
import archive.helper as helper
from .puzzles import MATE_IN_1, MATE_IN_2, MATE_IN_3, SIMPLE_CAPTURES, SIMPLE_FORKS, COMPLEX_FORKS

class TestPuzzles:
    @pytest.mark.parametrize("fen,expected_move", MATE_IN_1)
    def test_negamax_mateIn1(self, fen, expected_move):
        board = chess.Board(fen)
        negamaxEngine = helper.get_negamax_engine(config=Config(depth=1))
        actual_move = negamaxEngine.find_move(board)
        print("{}: expected {} actual {} - {}".format(negamaxEngine.get_name(), expected_move, board.san(actual_move), fen))
        assert board.san(actual_move) == expected_move

    @pytest.mark.parametrize("fen,expected_move", MATE_IN_2)
    def test_negamax_mateIn2(self, fen, expected_move):
        board = chess.Board(fen)
        negamaxEngine = helper.get_negamax_engine(config=Config(depth=3))
        actual_move = negamaxEngine.find_move(board)
        print("{}: expected {} actual {} - {}".format(negamaxEngine.get_name(), expected_move, board.san(actual_move), fen))
        assert board.san(actual_move) == expected_move

    @pytest.mark.parametrize("fen,expected_move", MATE_IN_3)
    def test_negamax_mateIn3(self, fen, expected_move):
        board = chess.Board(fen)
        negamaxEngine = helper.get_negamax_engine(config=Config(depth=5))
        actual_move = negamaxEngine.find_move(board)
        print("{}: expected {} actual {} - {}".format(negamaxEngine.get_name(), expected_move, board.san(actual_move), fen))
        assert board.san(actual_move) == expected_move

    @pytest.mark.parametrize("fen,expected_move", SIMPLE_CAPTURES)
    def test_negamax_simple_captures(self, fen, expected_move):
        board = chess.Board(fen)
        negamaxEngine = helper.get_negamax_engine(config=Config(depth=3))
        actual_move = negamaxEngine.find_move(board)
        print("{}: expected {} actual {} - {}".format(negamaxEngine.get_name(), expected_move, board.san(actual_move), fen))
        assert board.san(actual_move) == expected_move

    @pytest.mark.parametrize("fen,expected_move", SIMPLE_FORKS)
    def test_negamax_simple_forks(self, fen, expected_move):
        board = chess.Board(fen)
        negamaxEngine = helper.get_negamax_engine(config=Config(depth=3))
        actual_move = negamaxEngine.find_move(board)
        print("{}: expected {} actual {} - {}".format(negamaxEngine.get_name(), expected_move, board.san(actual_move), fen))
        assert board.san(actual_move) == expected_move

    @pytest.mark.parametrize("fen,expected_move", COMPLEX_FORKS)
    def test_negamax_complex_forks(self, fen, expected_move):
        board = chess.Board(fen)
        negamaxEngine = helper.get_negamax_engine(config=Config(depth=5))
        actual_move = negamaxEngine.find_move(board)
        print("{}: expected {} actual {} - {}".format(negamaxEngine.get_name(), expected_move, board.san(actual_move), fen))
        assert board.san(actual_move) == expected_move
