"""Tests for the UCI protocol layer (``pychess.__main__``)."""

import builtins

import chess
import pytest

from pychess import __main__ as cli
from pychess.__main__ import UCI, main
from pychess.constants import MATE
from pychess.engine import RandomEngine
from pychess.lazy_smp import SearchResult
from pychess.types import GoLimits


class DeadEngine:
    """Always returns an empty PV, to exercise the ``bestmove 0000`` path."""

    def search(self, board: chess.Board, limits: GoLimits | None = None) -> SearchResult:
        return SearchResult(0, [], 0, 0, 0.0)


@pytest.fixture
def uci(monkeypatch):
    """A UCI session with the opening book disabled and a fast random engine."""
    monkeypatch.setattr(cli, "BOOK_PATH", "/nonexistent/book.bin")
    session = UCI()
    session.engine = RandomEngine()
    return session


class TestParseGo:
    def test_integer_params(self):
        limits = UCI().parse_go(["go", "depth", "8", "movetime", "1500", "wtime", "60000"])
        assert limits == {"depth": 8, "movetime": 1500, "wtime": 60000}

    def test_infinite_flag(self):
        assert UCI().parse_go(["go", "infinite"]) == {"infinite": True}

    def test_bad_value_is_ignored(self):
        assert UCI().parse_go(["go", "depth", "xyz"]) == {}

    def test_bare_go(self):
        assert UCI().parse_go(["go"]) == {}


class TestProcessCommand:
    def test_uci_handshake(self, uci, capsys):
        uci.process_command("uci")
        out = capsys.readouterr().out
        assert "id name pychess" in out
        assert "uciok" in out

    def test_isready(self, uci, capsys):
        uci.process_command("isready")
        assert capsys.readouterr().out.strip() == "readyok"

    def test_unknown_command(self, uci, capsys):
        uci.process_command("frobnicate")
        assert "Unknown command" in capsys.readouterr().out

    def test_ignored_commands_do_not_raise(self, uci):
        for cmd in ("debug on", "setoption name X", "register", "stop", "ponderhit"):
            uci.process_command(cmd)

    def test_quit_exits(self, uci):
        with pytest.raises(SystemExit):
            uci.process_command("quit")

    def test_ucinewgame_resets_state(self, uci):
        uci.board.push_uci("e2e4")
        uci.process_command("ucinewgame")
        assert uci.board.fen() == chess.STARTING_FEN

    def test_position_startpos_with_moves(self, uci):
        uci.process_command("position startpos moves e2e4 e7e5")
        assert [m.uci() for m in uci.board.move_stack] == ["e2e4", "e7e5"]

    def test_position_fen(self, uci):
        fen = "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1"
        uci.process_command(f"position fen {fen}")
        assert uci.board.fen() == fen

    def test_print_commands(self, uci, capsys):
        uci.process_command("position startpos moves d2d4")
        uci.process_command("printBoard")
        uci.process_command("printLegalMoves")
        uci.process_command("printMoveStack")
        out = capsys.readouterr().out
        assert "d4" in out  # move stack / legal moves rendered as SAN

    def test_perft(self, uci, capsys):
        uci.process_command("position startpos")
        uci.process_command("perft 2")
        assert "nodes 400" in capsys.readouterr().out

    def test_go_uses_the_engine_when_off_book(self, uci, capsys):
        uci.process_command("position startpos moves e2e4 e7e5")
        uci.process_command("go depth 1")
        out = capsys.readouterr().out
        assert out.startswith("info starting search")
        assert "bestmove " in out

    def test_go_falls_back_to_a_legal_move(self, uci, capsys):
        uci.engine = DeadEngine()
        uci.process_command("go depth 1")
        assert "bestmove 0000" in capsys.readouterr().out

    def test_self_play_stops_on_a_finished_game(self, uci, capsys):
        uci.board = chess.Board("7k/5Q2/6K1/8/8/8/8/8 b - - 0 1")  # stalemate
        uci.process_command("selfPlay")
        assert capsys.readouterr().out.strip().endswith("1/2-1/2")

    def test_self_play_loops_then_stops_on_empty_pv(self, uci, capsys):
        uci.engine = DeadEngine()
        uci.process_command("selfPlay")
        out = capsys.readouterr().out
        assert "info depth" not in out  # DeadEngine's empty PV breaks the loop
        assert out.strip().endswith("*")  # game still in progress

    def test_self_play_plays_book_moves(self, monkeypatch, capsys):
        # Re-enable the book so the book branch of the loop runs, then stop it.
        session = UCI()
        session.engine = DeadEngine()
        calls = iter([chess.Move.from_uci("e2e4"), None])
        monkeypatch.setattr(session, "book_move", lambda: next(calls))
        session.process_command("selfPlay")
        assert session.board.move_stack[0].uci() == "e2e4"


class _FixedEngine:
    """Returns a preset SearchResult, to exercise ``info`` formatting."""

    def __init__(self, result: SearchResult) -> None:
        self._result = result

    def search(self, board: chess.Board, limits: GoLimits | None = None) -> SearchResult:
        return self._result


class TestScoreField:
    def test_centipawns(self):
        assert UCI._score_field(53) == "score cp 53"
        assert UCI._score_field(-120) == "score cp -120"

    def test_mate_in_moves_is_signed(self):
        assert UCI._score_field(MATE - 1) == "score mate 1"  # 1 ply -> mate in 1
        assert UCI._score_field(MATE - 3) == "score mate 2"  # 3 plies -> mate in 2
        assert UCI._score_field(-(MATE - 4)) == "score mate -2"  # getting mated

    def test_go_reports_mate_score(self, uci, capsys):
        uci.engine = _FixedEngine(SearchResult(MATE - 3, [chess.Move.from_uci("a1a2")], 5, 10, 0.0))
        uci.process_command("position fen 7k/8/5K2/8/8/8/8/R7 w - - 0 1")
        uci.process_command("go depth 5")
        assert "score mate 2" in capsys.readouterr().out


class TestBookMove:
    def test_missing_book_returns_none(self, uci):
        assert uci.book_move() is None  # fixture points BOOK_PATH at nothing

    def test_real_book_returns_a_legal_move(self):
        session = UCI()  # real BOOK_PATH
        move = session.book_move()
        if move is not None:  # book file is present in a source checkout
            assert move in session.board.legal_moves


def test_main_loop_processes_until_quit(monkeypatch, capsys):
    commands = iter(["isready", "uci", "quit"])
    monkeypatch.setattr(builtins, "input", lambda: next(commands))
    main()
    out = capsys.readouterr().out
    assert "readyok" in out
    assert "uciok" in out
