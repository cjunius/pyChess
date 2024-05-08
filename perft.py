import functools
import multiprocessing
from multiprocessing.pool import Pool
import time
from typing import Iterator, Tuple
from chess import Board

captures = 0
end_positions = 0
castles = 0
promotions = 0
checks = 0
discovered_checks = 0
double_checks = 0
checkmates = 0

def perft(board: Board, depth: int) -> Tuple[int, float]:
    start=time.time()
    nodes = count_nodes(depth, board)
    end=time.time()
    return nodes, end-start

def count_nodes(depth: int, board: Board) -> int:  
    global captures, checks, checkmates 
    if depth == 0:
        return 1
    elif depth > 1:
        nodes = 0
        for move in board.legal_moves:
            board.push(move)
            nodes += count_nodes(depth-1, board)
            board.pop()
        return nodes
    else:
        return 1
    
def parallel_perft(pool: Pool, depth: int, board: Board) -> int:
    def successors(board: Board) -> Iterator[Board]:
        for move in board.legal_moves:
            board_after = board.copy(stack=False)
            board_after.push(move)
            yield board_after

    perft_f = functools.partial(count_nodes, depth-1)
    return sum(pool.imap_unordered(perft_f, successors(board) ))

def main():
    global captures, checks, checkmates 
    cpu_count = (multiprocessing.cpu_count())
    board = Board()
    totalNodes = 0
    moveNodes = []
    start=time.time()
    for move in board.legal_moves:
        board.push(move)
        nodes = parallel_perft(Pool(cpu_count), depth=5, board=board)
        board.pop()
        totalNodes += nodes
        moveNodes.append( (board.uci(move), nodes))
    end=time.time()

    moveNodes.sort(key=lambda x: x)
    for move, nodes in moveNodes:
        print(str(move) + " " + str(nodes))
    print("info CPUs " + str(cpu_count) + " Nodes searched " + str(totalNodes) + " time " + str(end-start))
    print("Captures: " + str(captures))
    print("Checks: " + str(checks))
    print("Checkmates: " + str(checkmates))

if __name__ == "__main__":
    main()
    