import functools, multiprocessing, time

from chess import Board
from multiprocessing.pool import Pool
from typing import Iterator, Tuple


def perft(board: Board, depth: float) -> Tuple[float, float]:
    start=time.time()
    nodes = count_nodes(depth, board)
    end=time.time()
    return nodes, end-start

def count_nodes(depth: int, board: Board) -> float:  
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
    
def parallel_perft(pool: Pool, depth: float, board: Board) -> float:
    def successors(board: Board) -> Iterator[Board]:
        for move in board.legal_moves:
            board_after = board.copy(stack=False)
            board_after.push(move)
            yield board_after

    perft_f = functools.partial(count_nodes, depth-1)
    return sum(pool.imap_unordered(perft_f, successors(board) ))


def main():
    depth: float = 6
    cpu_count = (multiprocessing.cpu_count())
    board = Board()
    start = time.time()
    nodes = parallel_perft(Pool(cpu_count), depth=depth, board=board)
    end=time.time()
    print("info CPUs " + str(cpu_count) + " Nodes searched " + str(nodes) + " time " + str(end-start))

    if depth <= 6:
        start=time.time()
        nodes = count_nodes(depth, board)
        end=time.time()
        print("info CPUs 1 Nodes searched " + str(nodes) + " time " + str(end-start))


if __name__ == "__main__":
    main()
    