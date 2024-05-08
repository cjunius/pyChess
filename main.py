
import time
import chess
import sys
import signal

from evaluation import PieceValueMixin, PieceSquareTableMixin
from move_ordering import ChecksCapturesOrderMixin
from perft import perft
from sys import stdout
from search import NegamaxMixin, RandomMixin


def catchKeyboardInterrupt(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, catchKeyboardInterrupt)


class NegamaxEngine(NegamaxMixin, PieceValueMixin, PieceSquareTableMixin, ChecksCapturesOrderMixin):
    pass

class RandomEngine(RandomMixin):
    pass

class UCI:
    def __init__(self) -> None:
        self.board = chess.Board()
        self.engine = RandomEngine(self.board)


    def processCommand(self, input: str) -> str:
        args = input.split(" ")
        match args[0]:
            case "uci":
                return self.uci_handler()
            case "debug":
                return "Not implemented yet\n"
            case "isready":
                return "readyok\n"
            case "setoption":
                return "Not implemented yet\n"
            case "register":
                return "Not implemented yet\n"
            case "ucinewgame":
                self.board = chess.Board()
                self.engine = RandomEngine(self.board)
                return ""
            case "position":
                return self.position_handler(args)
            case "go":
                return self.go_handler()
            case "stop":
                return "Not implemented yet\n"
            case "ponderhit":
                return "Not implemented yet\n"
            case "quit":
                quit()
            case "printBoard":
                return str(self.board) + "\n"
            case "printLegalMoves":
                return str(list(self.board.legal_moves)) + "\n"
            case "printMoveStack":
                replay = self.board.root()
                san_stack = [replay.san_and_push(m) for m in self.board.move_stack]
                return str(san_stack) + "\n"
            case "perft":
                return self.perft_handler(args)
            case _:
                return "Unknown command\n"


    def uci_handler(self):
        value = "id name CJBot\n"
        value += "id author cjunius\n"
        value += "\n"
        value += "uciok\n"
        return value


    def position_handler(self, args):

        if args[1] == "startpos":
            self.board = chess.Board()
        
        if args[1] == "fen":
            fen_string = args[2]
            for i in range(3, 8):
                fen_string += " " + args[i]

            self.board = chess.Board(fen_string)

        moves_found = False
        for i in range(1, len(args)):

            if moves_found:
                self.board.push_uci(args[i])
            else:
                if args[i] == "moves": 
                    moves_found = True

        self.engine = RandomEngine(self.board)
        
        return ""
            

    def go_handler(self):
        start = time.time()
        best_score, pv = self.engine.search(-99999, 99999, 5)
        end = time.time()
        stdout.write("info score " + str(best_score) + " pv " + str(pv) + "\n")
        stdout.write("info time " + str(end - start) + "\n")
        stdout.flush()
        return "bestmove " + str(pv[0]) + "\n"

        # Can respond with info statements
        # info depth <x>
        # info time <x> (in ms)
        # info nodes <x>
        # info pv <move1> ... <moveN>
        # info score cp <x> (in centipawns)
        # info score mate <y> (mate in y moves, NOT plies)
        # info score lowerbound <x>
        # info score upperbound <x>
        # info currmove <move>
        # info nps <x>


    def perft_handler(self, args):
        depth = int(args[1])
        for i in range(2, depth+1):
            nodes, time = perft(self.board, i)
            stdout.write("info depth " + str(i) + " nodes " + str(nodes) + " time " + str(time) + "\n")
            stdout.flush()
        return ""


def main() -> None:
    uic = UCI()
    while True:
        command = input()
        value = uic.processCommand(command)
        stdout.write(value)
        stdout.flush()


if __name__ == "__main__":
    main()