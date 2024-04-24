import sys
import signal
import chess
import time
from evaluation import Evaluation

from bots.BoardControlBot import BoardControlBot
from bots.cjBot import CJBot
from bots.randomBot import RandomBot
from bots.materialGirlBot import MaterialGirlBot
from bots.pieceSquareTableBot import PieceSquareTableBot
from bots.NegaScoutBot import NegaScoutBot
from bots.NegaMaxBot import NegaMaxBot
from bots.NegaMaxABBot import NegaMaxABBot

# Catch KeyboardInterrupt and quit
def catchthesignal(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, catchthesignal)


methods = ['material_balance', 'piece_square_table', 'board_control', 'mobility', 'board_control_slow']
args = [chess.Board("r1bqkb1r/p1pppp1p/np6/5nB1/3PQ3/2N5/PPP1PPPP/R3KBNR w KQkq - 2 6")]
for method in methods:
    start = time.time()
    for i in range(0,1000):
        eval = getattr(Evaluation, method)(*args)
    end = time.time()
    print("Time: {:1.8f}  Eval: {} - {}".format(end-start, eval, method))
    # Time: 0.00100088  Eval: 100 - material_balance
    # Time: 0.02301335  Eval: 166 - piece_square_table
    # Time: 0.03904319  Eval: 19 - board_control
    # Time: 0.13712454  Eval: 22 - mobility
    # Time: 0.25723362  Eval: 19 - board_control_slow


## BOTS
BOTS = [NegaScoutBot(), NegaMaxABBot()]
# BOTS = [BoardControlBot(), CJBot(), MaterialGirlBot(), PieceSquareTableBot(), RandomBot()]
# board = chess.Board("r3kb1r/pp1bpppp/2n2nN1/2ppq3/2P5/6PP/PPNPPP2/R1BQKBR1 b Qkq - 5 9")
# board = chess.Board("r1bqkb1r/p1pppp1p/np6/5nB1/3PQ3/2N5/PPP1PPPP/R3KBNR w KQkq - 2 6")
board = chess.Board("1r4k1/1r2ppbp/3n2p1/q1pP4/5BP1/2N2Q1P/PP2RPK1/R7 b - - 2 20")

for bot in BOTS:
    print("# " + bot.getName() + " - using board_control evaluation")
    start = time.time()
    move = bot.findMove(board)
    end = time.time()
    print("")

# FEN: r1bqkb1r/p1pppp1p/np6/5nB1/3PQ3/2N5/PPP1PPPP/R3KBNR w KQkq - 2 6
# Stockfish says move is Qxf5
# Time: 3.49618459 - Qxf5 - Board Control Bot 
# Time: 8.09434819 - Qxa8 - CJ Bot
# Time: 6.36178160 - Qxa8 - Material Girl Bot
# Time: 0.31128287 - Qxe7+ - Piece-Square Table Bot
# Time: 0.00000000 - b4 - Random Bot

# FEN: r1bqkb1r/p1pppp1p/np6/5nB1/3PQ3/2N5/PPP1PPPP/R3KBNR w KQkq - 2 6
# NegaScout Bot - using board_control evaluation
# White  6. Qxe7+   Eval:     -2  Depth:  3  Nodes:  1359096  Evals:  126444  Prune: 9.30%  Time:  11.10  Evals/s: 11389.22  FEN: r1bqkb1r/p1pppp1p/np6/5nB1/3PQ3/2N5/PPP1PPPP/R3KBNR w KQkq - 2 6
# NegaMax Alpha-Beta Bot - using board_control evaluation
# White  6. Qxe7+   Eval:     -7  Depth:  3  Nodes:  1359096  Evals:    6031  Prune: 0.44%  Time:   0.58  Evals/s: 10370.94  FEN: r1bqkb1r/p1pppp1p/np6/5nB1/3PQ3/2N5/PPP1PPPP/R3KBNR w KQkq - 2 6

# FEN: 1r4k1/1r2ppbp/3n2p1/q1pP4/5BP1/2N2Q1P/PP2RPK1/R7 b - - 2 20
# Stockfish says move is Bd5
# NegaScout Bot - using board_control evaluation
# Black 20. Qa6     Eval:      6  Depth:  3  Nodes:  4389902  Evals: 1826217  Prune: 41.60%  Time: 176.85  Evals/s: 10326.58  FEN: 1r4k1/1r2ppbp/3n2p1/q1pP4/5BP1/2N2Q1P/PP2RPK1/R7 b - - 2 20
# NegaMax Alpha-Beta Bot - using board_control evaluation
# Black 20. Bxc3    Eval:      3  Depth:  3  Nodes:  4389902  Evals:  419824  Prune: 9.56%  Time:  41.55  Evals/s: 10105.10  FEN: 1r4k1/1r2ppbp/3n2p1/q1pP4/5BP1/2N2Q1P/PP2RPK1/R7 b - - 2 20