import time, sys, signal, multiprocessing

from chess import Board, polyglot
from engines import NegamaxEngine
from multiprocessing.pool import Pool
from operator import itemgetter
from perft import perft

def catchKeyboardInterrupt(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, catchKeyboardInterrupt)


class UCI:
    def __init__(self) -> None:
        self.board = Board()
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
                self.board = Board()
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
                #return self.perft_handler(args)
                pass
            case "selfPlay":
                self.selfPlay_handler(args)
            case "selfPlay_parallel":
                self.selfPlay_parallel_handler(args)
            case _:
                print("Unknown command")

    
    def position_handler(self, args):
        
        if args[1] == "fen":
            fen_string = args[2]
            for i in range(3, 8):
                fen_string += " " + args[i]

            self.board = Board(fen_string)  
        else:
            self.board = Board()

        moves_found = False
        for i in range(1, len(args)):

            if moves_found:
                self.board.push_uci(args[i])
            else:
                if args[i] == "moves": 
                    moves_found = True


    def go_handler(self, parallel: bool, args):
        print("info starting search")
        

        # try:
        #     move = polyglot.MemoryMappedReader("opening_book/bookfish.bin").weighted_choice(self.board).move
        #     print("info using book move")
        #     print("bestmove " + str(move))
        #     return
        
        # except:
        #     pass

        if len(args) > 1 and args[1] == "depth":
            self.depth = int(args[2])
        start = time.time()
        if parallel:
            best_score, pv = self.engine.parallel_search(self.board, self.depth)
        else:
            #best_score, pv = self.engine.iterative_deepening(self.board, self.depth)
            best_score, pv = self.engine.search(self.board, -99999, 99999, self.depth)
        end = time.time()
        print('info score {} pv {} time {}'.format(str(best_score), str(pv), str(end-start)))
        print("bestmove " + str(pv[0]))


    def selfPlay_handler(self, args):
        while not self.board.is_game_over():
            start = time.time()
            best_score, pv = self.engine.search(self.board, -99999, 99999, self.depth)
            end = time.time()
            print('info score {} pv {} time {}'.format(str(best_score), str(pv), str(end-start)))
            self.board.push(pv[0])

    
    def selfPlay_parallel_handler(self, args):
        while not self.board.is_game_over():
            try:
                move = polyglot.MemoryMappedReader("opening_book/bookfish.bin").weighted_choice(self.board).move
                print("info using book move")
                print("bestmove " + str(move))
                self.board.push(move)

            except:
                best_score, pv = self.engine.parallel_search(self.board, self.depth)
                print('bestmove ' + str(pv[0]))
                self.board.push(pv[0])

        print(str(self.board.result()))


def main() -> None:
    uic = UCI()
    while True:
        command = input()
        if not command == "quit":
            uic.processCommand(command)
        else:


if __name__ == "__main__":
    # On Windows calling this function is necessary.
    multiprocessing.freeze_support()

    main()