"""`Lazy SMP <https://www.chessprogramming.org/Lazy_SMP>`_.

``N`` worker processes each run their own iterative deepening on the root
position while sharing one lock-free transposition table in shared memory.
Divergent start depths plus TT contention make the workers explore different
subtrees; the deepest completed result wins.
"""

import multiprocessing
import time
from dataclasses import dataclass
from multiprocessing.pool import Pool
from typing import NamedTuple

import chess

from .clock import DEFAULT_MOVETIME, MAX_DEPTH, Clock, deadline_from_limits
from .constants import INF, MATE_IN_MAX
from .eval_board import EvalBoard
from .evaluation import PestoEvaluator
from .move_ordering import MoveOrderer
from .negamax import Negamax, SearchAbortError
from .shared_tt import SharedFlag, SharedTT
from .types import GoLimits

SMP_TT_SLOTS = 1 << 20  # 1M entries * 16 bytes = 16 MB

# The pickled payload each worker process receives.
_Payload = tuple[str, list[str], list[str] | None, int, float, int | None, str, int, int, str]


class _WorkerResult(NamedTuple):
    """What a worker hands back: raw score, PV as uci strings, depth, nodes."""

    score: int
    pv: list[str]
    depth: int
    nodes: int


@dataclass
class SearchResult:
    score: int
    pv: list[chess.Move]
    depth: int
    nodes: int
    elapsed: float  # seconds


def _worker(payload: _Payload) -> _WorkerResult:
    """One Lazy SMP helper: iterative deepening against the shared TT.

    Runs in its own process. Workers are seeded with different start depths so
    they populate the shared table along slightly different paths; the shared
    entries then speed up every other worker.
    """
    (
        root_fen,
        moves,
        root_slice,
        max_depth,
        deadline,
        node_limit,
        tt_name,
        tt_slots,
        worker_id,
        stop_name,
    ) = payload

    tt = SharedTT(slots=tt_slots, name=tt_name, create=False)
    stop = SharedFlag(name=stop_name, create=False)

    board = EvalBoard(root_fen)
    for uci in moves:
        board.push_uci(uci)

    root_moves = None
    if root_slice is not None:
        root_moves = {chess.Move.from_uci(u) for u in root_slice}

    clock = Clock(deadline=deadline, node_limit=node_limit, stop_flag=stop)
    searcher = Negamax(PestoEvaluator(), MoveOrderer(root_moves=root_moves), tt, clock)

    best = _WorkerResult(0, [], 0, 0)
    try:
        for depth in range(1 + (worker_id % 3), max_depth + 1):
            try:
                score, pv = searcher.search(board, -INF, INF, depth)
            except SearchAbortError:
                break
            clock.arm()
            best = _WorkerResult(score, [m.uci() for m in pv], depth, searcher.nodes)
            if stop.is_set() or time.time() >= deadline:
                break
            if score >= MATE_IN_MAX:  # forced win found - everyone stops
                stop.set()
                break
            if score <= -MATE_IN_MAX:  # every move in this slice loses
                break
    finally:
        tt.close()
        stop.close()
    return best


def _result_rank(r: _WorkerResult) -> tuple[int, int, int]:
    """Rank worker results: a forced win beats everything (fastest first), then
    deepest search, then best score; a forced loss ranks last (least bad,
    deepest)."""
    if r.score >= MATE_IN_MAX:
        return (2, r.score, r.depth)
    if r.score <= -MATE_IN_MAX:
        return (0, r.depth, r.score)
    return (1, r.depth, r.score)


def search(
    board: chess.Board, limits: GoLimits | None = None, *, tt_slots: int = SMP_TT_SLOTS
) -> SearchResult:
    """Search ``board`` under UCI ``limits`` and return a ``SearchResult``."""
    limits = limits or {}
    start = time.time()

    n_workers = max(1, multiprocessing.cpu_count() - 1)
    deadline = deadline_from_limits(board, limits, start)
    deadline = deadline if deadline is not None else float("inf")
    max_depth = min(int(limits.get("depth") or MAX_DEPTH), MAX_DEPTH)

    root_fen = board.root().fen()
    moves = [m.uci() for m in board.move_stack]

    # Worker 0 searches every root move (authoritative PV); the rest split the
    # root moves so the expensive top-level subtrees are divided while still
    # sharing everything below the root through the TT.
    legal = [m.uci() for m in board.legal_moves]
    splitters = max(1, n_workers - 1)
    slices: list[list[str] | None] = [None]
    for i in range(1, n_workers):
        slices.append(legal[(i - 1) % splitters :: splitters] or None)

    tt = SharedTT(slots=tt_slots, create=True)
    stop = SharedFlag(create=True)
    node_limit = limits.get("nodes")
    payloads: list[_Payload] = [
        (
            root_fen,
            moves,
            slices[i],
            max_depth,
            deadline,
            node_limit,
            tt.name,
            tt.slots,
            i,
            stop.name,
        )
        for i in range(n_workers)
    ]
    try:
        with Pool(n_workers) as pool:
            async_res = pool.map_async(_worker, payloads)
            while not async_res.ready() and time.time() < deadline:
                time.sleep(0.02)
            stop.set()
            results = async_res.get()
    finally:
        stop.close()
        stop.unlink()
        tt.close()
        tt.unlink()

    elapsed = time.time() - start
    total_nodes = sum(r.nodes for r in results if r)

    usable = [r for r in results if r and r.pv]
    if not usable:
        # Every worker crashed or died before completing a single ply; fall
        # back to any legal move so the engine still replies.
        legal_moves = list(board.legal_moves)
        return SearchResult(0, legal_moves[:1], 0, total_nodes, elapsed)

    best = max(usable, key=_result_rank)
    pv = [chess.Move.from_uci(u) for u in best.pv]
    return SearchResult(int(best.score), pv, best.depth, total_nodes, elapsed)
