import time, sys, signal, multiprocessing

from chess import Board, polyglot
from eval_board import EvalBoard
from engines import NegamaxEngine
from multiprocessing.pool import Pool
from operator import itemgetter
from perft import perft

def catchKeyboardInterrupt(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, catchKeyboardInterrupt)

# UCI "go" parameters that take a single integer argument.
GO_INT_PARAMS = {"depth", "nodes", "movetime",
                 "wtime", "btime", "winc", "binc", "movestogo"}

BOOK_PATH = "opening_book/bookfish.bin"


class UCI:
    def __init__(self) -> None:
        self.board = EvalBoard()
        self.engine = NegamaxEngine()
        self.depth = 4


    def processCommand(self, input: str) -> str:
        args = input.split(" ")
        match args[0]:
            case "uci":
                print("id name CJBot")
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
                self.engine = NegamaxEngine()
            case "position":
                self.position_handler(args)
            case "go":
                self.go_handler(False, args)
            case "go_parallel":
                self.go_handler(True, args)
            case "stop":
                pass
            case "quit":
                quit(0)
            case "ponderhit":
                pass
            case "printBoard":
                print(str(self.board))
            case "printLegalMoves":
                moves = [self.board.san(m) for m in self.board.legal_moves]
                print(str(moves))
            case "printMoveStack":
                replay = self.board.root()
                moves = [replay.san_and_push(m) for m in self.board.move_stack]
                print(str(moves))
            case "perft":
                self.perft_handler(args)
            case "selfPlay":
                self.selfPlay_handler(args)
            case "selfPlay_parallel":
                self.selfPlay_parallel_handler(args)
            case _:
                print("Unknown command")

    
    def position_handler(self, args):

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
        for i in range(1, len(args)):

            if moves_found:
                self.board.push_uci(args[i])
            else:
                if args[i] == "moves":
                    moves_found = True


    def parse_go(self, args) -> dict:
        limits = {}
        i = 1
        while i < len(args):
            token = args[i]
            if token in GO_INT_PARAMS and i + 1 < len(args):
                try:
                    limits[token] = int(args[i + 1])
                except ValueError:
                    pass
                i += 2
            elif token == "infinite":
                limits["infinite"] = True
                i += 1
            else:
                i += 1
        return limits


    def book_move(self):
        """Return a Polyglot book move for the current position, or None."""
        try:
            with polyglot.MemoryMappedReader(BOOK_PATH) as reader:
                return reader.weighted_choice(self.board).move
        except (IndexError, FileNotFoundError, OSError):
            return None


    def perft_handler(self, args):
        depth = int(args[1]) if len(args) > 1 else 4
        nodes, elapsed = perft(self.board, depth)
        print("info depth {} nodes {} time {}".format(depth, nodes, elapsed))


    def go_handler(self, parallel: bool, args):
        print("info starting search")

        move = self.book_move()
        if move is not None:
            print("info using book move")
            print("bestmove " + move.uci())
            return

        limits = self.parse_go(args)
        start = time.time()
        if parallel:
            best_score, pv = self.engine.parallel_search(self.board, limits)
        else:
            best_score, pv = self.engine.search_with_time(self.board, limits)
        end = time.time()
        pv_uci = " ".join(m.uci() for m in pv)
        print('info score {} pv {} time {}'.format(best_score, pv_uci, end - start))
        print("bestmove " + (pv[0].uci() if pv else "0000"))


    def selfPlay_handler(self, args):
        while not self.board.is_game_over():
            move = self.book_move()
            if move is not None:
                print("info using book move")
                print("bestmove " + move.uci())
                self.board.push(move)
                continue

            start = time.time()
            best_score, pv = self.engine.search_with_time(self.board, {"depth": self.depth})
            end = time.time()
            if not pv:
                break
            print('info score {} pv {} time {}'.format(
                best_score, " ".join(m.uci() for m in pv), end - start))
            print("bestmove " + pv[0].uci())
            self.board.push(pv[0])

        print(str(self.board.result()))


    def selfPlay_parallel_handler(self, args):
        while not self.board.is_game_over():
            move = self.book_move()
            if move is not None:
                print("info using book move")
                print("bestmove " + move.uci())
                self.board.push(move)
                continue

            best_score, pv = self.engine.parallel_search(self.board, {"depth": self.depth})
            if not pv:
                break
            print('bestmove ' + pv[0].uci())
            self.board.push(pv[0])

        print(str(self.board.result()))


def main() -> None:
    uic = UCI()
    while True:
        command = input()
        if not command == "quit":
            uic.processCommand(command)
        else:
            break


if __name__ == "__main__":
    # On Windows calling this function is necessary.
    multiprocessing.freeze_support()

    main()