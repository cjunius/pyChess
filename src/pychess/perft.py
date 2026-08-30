import functools
import multiprocessing
import time
from collections.abc import Iterator
from multiprocessing.pool import Pool

from chess import Board


def perft(board: Board, depth: int) -> tuple[int, float]:
    start = time.time()
    nodes = count_nodes(depth, board)
    return nodes, time.time() - start


def count_nodes(depth: int, board: Board) -> int:
    """Number of leaf nodes at exactly ``depth`` plies from ``board``."""
    if depth <= 0:
        return 1
    if depth == 1:
        return board.legal_moves.count()

    nodes = 0
    for move in board.legal_moves:
        board.push(move)
        nodes += count_nodes(depth - 1, board)
        board.pop()
    return nodes


def parallel_perft(pool: Pool, depth: int, board: Board) -> int:
    def successors(board: Board) -> Iterator[Board]:
        for move in board.legal_moves:
            board_after = board.copy(stack=False)
            board_after.push(move)
            yield board_after

    if depth <= 0:
        return 1
    perft_f = functools.partial(count_nodes, depth - 1)
    return sum(pool.imap_unordered(perft_f, successors(board)))


def main() -> None:  # pragma: no cover - depth-6 benchmark, run manually
    depth = 6
    cpu_count = multiprocessing.cpu_count()
    board = Board()

    start = time.time()
    with Pool(cpu_count) as pool:
        nodes = parallel_perft(pool, depth=depth, board=board)
    print(f"info CPUs {cpu_count} nodes {nodes} time {time.time() - start}")

    start = time.time()
    nodes = count_nodes(depth, board)
    print(f"info CPUs 1 nodes {nodes} time {time.time() - start}")


if __name__ == "__main__":
    main()
