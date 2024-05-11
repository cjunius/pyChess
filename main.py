
from multiprocessing.pool import Pool
import concurrent.futures
from operator import itemgetter
import time
import sys
import signal

from chess import Board
from evaluation import PieceValueMixin, PieceSquareTableMixin
from move_ordering import ChecksCapturesOrderMixin
from perft import perft
from sys import stdout
from search import NegamaxMixin, QuiescenceSearchMixin, RandomMixin


def catchKeyboardInterrupt(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, catchKeyboardInterrupt)


class NegamaxEngine(NegamaxMixin, QuiescenceSearchMixin, PieceValueMixin, PieceSquareTableMixin, ChecksCapturesOrderMixin):
    pass

class UCI:
    def __init__(self) -> None:
        self.board = Board()
        self.engine = NegamaxEngine()
        self.depth = 6

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
                self.board = Board()
                return ""
            case "position":
                return self.position_handler(args)
            case "go":
                return self.go_handler(False)
            case "go_parallel":
                return self.go_handler(True)
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
                san_stack = [replay.san_and_push(m) for m in self.engine.board.move_stack]
                return str(san_stack) + "\n"
            case "perft":
                return self.perft_handler(args)
            case "selfPlay":
                return self.selfPlay_handler(args)
            case _:
                return "Unknown command\n"
            


    def uci_handler(self):
        value = "id name CJBot\n"
        value += "id author cjunius\n"
        value += "\n"
        value += "uciok\n"
        return value


    def position_handler(self, args):
        
        board = Board()

        if args[1] == "fen":
            fen_string = args[2]
            for i in range(3, 8):
                fen_string += " " + args[i]

            board = Board(fen_string)            

        moves_found = False
        for i in range(1, len(args)):

            if moves_found:
                board.push_uci(args[i])
            else:
                if args[i] == "moves": 
                    moves_found = True
        
        self.board = board

        return ""
            

    def go_handler(self, parallel: bool):

        # try:
        #     move = polyglot.MemoryMappedReader("opening_book/bookfish.bin").weighted_choice(self.board).move
        #     stdout.write("info using book move\n")
        #     stdout.flush()
        #     return "bestmove " + str(move) + "\n"
        # except:
            start = time.time()
            if parallel:
                best_score, pv = self.parallel_go() 
            else:
                best_score, pv = self.engine.search(self.board, -99999, 99999, self.depth)
            end = time.time()
            stdout.write("info score " + str(best_score) + " pv " + str(pv) + "\n")
            stdout.write("info time " + str(end - start) + "\n")
            stdout.flush()
            return "bestmove " + str(pv[0]) + "\n"
        

    def parallel_go(self):
        best_score = -99999
        pv = []
        count = 0
        start = time.time()
        results = Pool().imap(self.call_search, range(1, self.depth+1))
        for t, x in results:
            end = time.time()
            print('info score {} pv {} time {}'.format(str(t), str(x), str(end-start)))
            if len(x) > count:
                count = len(x)
                best_score = t
                pv = x
        return best_score, pv
        
    def call_search(self, depth):
        return self.engine.search(self.board, -99999, 99999, depth)

    def selfPlay_handler(self, args):
        pass


def main() -> None:
    uic = UCI()
    while True:
        command = input()
        value = uic.processCommand(command)
        stdout.write(value)
        stdout.flush()


if __name__ == "__main__":
    main()