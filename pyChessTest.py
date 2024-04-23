import chess
import time
from evaluation import Evaluation

# FEN: r3kb1r/pp1bpppp/2n2nN1/2ppq3/2P5/6PP/PPNPPP2/R1BQKBR1 b Qkq - 5 9
# Eval Time: 30.28s

board = chess.Board("r1bqkb1r/p1pppp1p/np6/5nB1/3PQ3/2N5/PPP1PPPP/R3KBNR w KQkq - 2 6")
eval = 0
num_runs = 1000

start = time.time()
for i in range(0,num_runs):
    eval = Evaluation.material_balance(board)
end = time.time()
print("Time: {:1.8f}  Eval: {}  - Material Balance".format(end-start, eval))

start = time.time()
for i in range(0,num_runs):
    eval = Evaluation.piece_square_table(board)
end = time.time()
print("Time: {:1.8f}  Eval: {}  - Piece Square Table".format(end-start, eval))

start = time.time()
for i in range(0,num_runs):
    eval = Evaluation.mobility(board)
end = time.time()
print("Time: {:1.8f}  Eval: {}  - Mobility".format(end-start, eval))

start = time.time()
for i in range(0,num_runs):
    eval = Evaluation.board_control(board)
end = time.time()
print("Time: {:1.8f}  Eval: {}  - Board Control".format(end-start, eval))

start = time.time()
for i in range(0,num_runs):
    eval = Evaluation.board_control_slow(board)
end = time.time()
print("Time: {:1.8f}  Eval: {}  - Board Control Slow".format(end-start, eval))