import contextlib
import multiprocessing
import os
import signal
import sys
from pathlib import Path
from typing import cast

import chess
from chess import polyglot

from . import __version__
from .engine import Engine, SupportsSearch
from .eval_board import EvalBoard
from .lazy_smp import SearchResult
from .perft import perft
from .types import GoLimits

# UCI "go" parameters that take a single integer argument.
GO_INT_PARAMS = {"depth", "nodes", "movetime", "wtime", "btime", "winc", "binc", "movestogo"}

# Polyglot opening book. Defaults to the copy in the source checkout; override
# with PYCHESS_BOOK when the package is installed elsewhere. A missing book is
# not an error - the engine just searches from move one.
BOOK_PATH = os.environ.get(
    "PYCHESS_BOOK",
    str(Path(__file__).resolve().parents[2] / "opening_book" / "bookfish.bin"),
)


class UCI:
    def __init__(self) -> None:
        self.board = EvalBoard()
        self.engine: SupportsSearch = Engine()
        self.depth = 4

    def process_command(self, line: str) -> None:
        args = line.split(" ")
        match args[0]:
            case "uci":
                print(f"id name pychess {__version__}")
                print("id author cjunius")
                print("uciok")
            case "debug":
                pass
            case "isready":
                print("readyok")
            case "setoption":
                pass
            case "register":
                pass
            case "ucinewgame":
                self.board = EvalBoard()
                self.engine = Engine()
            case "position":
                self.position_handler(args)
            case "go":
                self.go_handler(args)
            case "stop":
                pass
            case "quit":
                sys.exit(0)
            case "ponderhit":
                pass
            case "printBoard":
                print(str(self.board))
            case "printLegalMoves":
                print(str([self.board.san(m) for m in self.board.legal_moves]))
            case "printMoveStack":
                replay = self.board.root()
                print(str([replay.san_and_push(m) for m in self.board.move_stack]))
            case "perft":
                self.perft_handler(args)
            case "selfPlay":
                self.self_play_handler(args)
            case _:
                print("Unknown command")

    def position_handler(self, args: list[str]) -> None:
        if len(args) > 1 and args[1] == "fen":
            try:
                moves_idx = args.index("moves")
                fen_string = " ".join(args[2:moves_idx])
            except ValueError:
                fen_string = " ".join(args[2:])
            self.board = EvalBoard(fen_string)
        else:
            self.board = EvalBoard()

        moves_found = False
        for arg in args[1:]:
            if moves_found:
                self.board.push_uci(arg)
            elif arg == "moves":
                moves_found = True

    def parse_go(self, args: list[str]) -> GoLimits:
        limits: dict[str, int | bool] = {}
        i = 1
        while i < len(args):
            token = args[i]
            if token in GO_INT_PARAMS and i + 1 < len(args):
                with contextlib.suppress(ValueError):
                    limits[token] = int(args[i + 1])
                i += 2
            elif token == "infinite":
                limits["infinite"] = True
                i += 1
            else:
                i += 1
        return cast(GoLimits, limits)

    def book_move(self) -> chess.Move | None:
        """Return a Polyglot book move for the current position, or None."""
        try:
            with polyglot.MemoryMappedReader(BOOK_PATH) as reader:
                return reader.weighted_choice(self.board).move
        except (IndexError, FileNotFoundError, OSError):
            return None

    def print_info(self, result: SearchResult) -> None:
        """Format one UCI ``info`` line from a SearchResult."""
        pv = " ".join(m.uci() for m in result.pv)
        print(
            f"info depth {result.depth} score cp {result.score} "
            f"nodes {result.nodes} time {round(result.elapsed, 3)} pv {pv}"
        )

    def perft_handler(self, args: list[str]) -> None:
        depth = int(args[1]) if len(args) > 1 else 4
        nodes, elapsed = perft(self.board, depth)
        print(f"info depth {depth} nodes {nodes} time {elapsed}")

    def go_handler(self, args: list[str]) -> None:
        print("info starting search")

        move = self.book_move()
        if move is not None:
            print("info using book move")
            print("bestmove " + move.uci())
            return

        result = self.engine.search(self.board, self.parse_go(args))
        self.print_info(result)
        print("bestmove " + (result.pv[0].uci() if result.pv else "0000"))

    def self_play_handler(self, args: list[str]) -> None:
        while not self.board.is_game_over():
            move = self.book_move()
            if move is not None:
                print("info using book move")
                print("bestmove " + move.uci())
                self.board.push(move)
                continue

            result = self.engine.search(self.board, {"depth": self.depth})
            if not result.pv:
                break
            self.print_info(result)
            print("bestmove " + result.pv[0].uci())
            self.board.push(result.pv[0])

        print(str(self.board.result()))


def main() -> None:
    """Run the UCI protocol loop on stdin/stdout."""
    signal.signal(signal.SIGINT, lambda *_: sys.exit(0))
    uci = UCI()
    while True:
        command = input()
        if command == "quit":
            break
        uci.process_command(command)


if __name__ == "__main__":
    # Harmless normally; needed only if the app is ever frozen (PyInstaller etc).
    multiprocessing.freeze_support()
    main()
