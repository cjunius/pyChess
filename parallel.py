import multiprocessing
import time

from multiprocessing.pool import Pool

import chess
from chess import Move
from search import BaseSearch, SearchAbort, MATE_VALUE


class BaseParallel(BaseSearch):
    def __init__(self):
        self.board = None
        self.depth = 5

    def parallel_search(self, board, limits=None):
        raise NotImplementedError


def _lazy_smp_worker(payload):
    """One Lazy SMP helper: iterative deepening against the shared TT.

    Runs in its own process. Workers are seeded with different start depths so
    they populate the shared table along slightly different paths; the shared
    entries then speed up every other worker.
    """
    from engines import NegamaxEngine
    from eval_board import EvalBoard
    from shared_tt import SharedTT, SharedFlag

    (root_fen, moves, root_slice, max_depth, deadline,
     tt_name, tt_slots, worker_id, stop_name) = payload

    tt = SharedTT(slots=tt_slots, name=tt_name, create=False)
    stop = SharedFlag(name=stop_name, create=False)
    board = EvalBoard(root_fen)
    for uci in moves:
        board.push_uci(uci)

    engine = NegamaxEngine()
    engine._shared_tt = tt
    engine._stop_flag = stop
    engine._deadline = deadline
    engine._node_limit = None
    engine._nodes = 0
    engine._can_abort = False
    if root_slice is not None:
        engine._root_moves = {chess.Move.from_uci(u) for u in root_slice}

    best = (0, [], 0)
    try:
        for depth in range(1 + (worker_id % 3), max_depth + 1):
            try:
                score, pv = engine.search(board, -99999, 99999, depth)
            except SearchAbort:
                break
            engine._can_abort = True
            best = (score, [m.uci() for m in pv], depth)
            if stop.is_set() or time.time() >= deadline:
                break
            if score >= MATE_VALUE - 100:       # forced win found - everyone stops
                stop.set()
                break
            if score <= -(MATE_VALUE - 100):    # every move in this slice loses
                break
    finally:
        tt.close()
        stop.close()
    return best


def _smp_result_key(result):
    """Rank Lazy SMP worker results: a forced win beats everything (fastest
    first), then deepest search, then best score; a forced loss is ranked
    last (least bad, deepest)."""
    score, _pv, depth = result
    if score >= MATE_VALUE - 100:
        return (2, score, depth)
    if score <= -(MATE_VALUE - 100):
        return (0, depth, score)
    return (1, depth, score)


class LazySMPMixin(BaseParallel):
    """`Lazy SMP <https://www.chessprogramming.org/Lazy_SMP>`_.

    ``N`` worker processes each run their own iterative deepening on the root
    position while sharing one lock-free transposition table in shared memory.
    Divergent start depths plus TT contention make the workers explore
    different subtrees; the deepest completed result wins.

    Process start-up (spawn) costs a fair bit on macOS/Windows, so this only
    pays off for multi-second searches - short searches fall back to the
    single-process ``search_with_time``.
    """

    SMP_TT_SLOTS = 1 << 20   # 1M entries * 16 bytes = 16 MB

    def parallel_search(self, board, limits=None):
        from shared_tt import SharedTT, SharedFlag

        limits = limits or {}
        start = time.time()

        n_workers = max(1, multiprocessing.cpu_count() - 1)
        deadline = self._deadline_for(board, limits, start) \
            or (start + self.DEFAULT_MOVETIME)
        max_depth = min(int(limits.get("depth") or self.MAX_DEPTH), self.MAX_DEPTH)

        if n_workers < 2 or (deadline - start) < 0.75:
            return self.search_with_time(board, limits)

        root_fen = board.root().fen()
        moves = [m.uci() for m in board.move_stack]

        # Worker 0 searches every root move (authoritative PV); the rest split
        # the root moves so the expensive top-level subtrees are divided while
        # still sharing everything below the root through the TT.
        legal = [m.uci() for m in board.legal_moves]
        splitters = max(1, n_workers - 1)
        slices = [None]
        for i in range(1, n_workers):
            slices.append(legal[(i - 1) % splitters::splitters] or None)

        tt = SharedTT(slots=self.SMP_TT_SLOTS, create=True)
        stop = SharedFlag(create=True)
        payloads = [(root_fen, moves, slices[i], max_depth, deadline,
                     tt.name, tt.slots, i, stop.name)
                    for i in range(n_workers)]
        try:
            with Pool(n_workers) as pool:
                async_res = pool.map_async(_lazy_smp_worker, payloads)
                while not async_res.ready() and time.time() < deadline:
                    time.sleep(0.02)
                stop.set()
                results = async_res.get()
        finally:
            stop.close()
            stop.unlink()
            tt.close()
            tt.unlink()

        results = [r for r in results if r and r[1]]
        if not results:
            return self.search_with_time(board, limits)

        score, pv_uci, depth = max(results, key=_smp_result_key)
        pv = [chess.Move.from_uci(u) for u in pv_uci]
        print("info depth {} score cp {} time {} pv {}".format(
            depth, int(score), round(time.time() - start, 3), " ".join(pv_uci)))
        return score, pv


class IterativeDeepeningMixin(BaseParallel):
    """Single-process iterative deepening with UCI time management.

    Each iteration reuses the previous one through the transposition table
    (both for cut-offs and for move ordering via the stored best move), so
    deepening is nearly free when the position is stable. Iterations are
    aborted cleanly via ``SearchAbort`` once a limit is hit; the last fully
    completed iteration is returned.
    """

    MAX_DEPTH = 64
    DEFAULT_MOVETIME = 4.0            # seconds, used for a bare "go"
    BRANCHING_ESTIMATE = 2.5         # predict next iteration cost

    _can_abort = False
    _deadline = None
    _node_limit = None
    _stop_flag = None

    def stop_signal(self):
        if not self._can_abort:
            return False
        if self._stop_flag is not None and self._stop_flag.is_set():
            return True
        if self._node_limit is not None and self._nodes >= self._node_limit:
            return True
        if self._deadline is not None and time.time() >= self._deadline:
            return True
        return False

    def _deadline_for(self, board, limits, start):
        if limits.get("movetime") is not None:
            return start + limits["movetime"] / 1000.0
        my = limits.get("wtime") if board.turn == chess.WHITE else limits.get("btime")
        if my is not None:
            inc = (limits.get("winc") if board.turn == chess.WHITE
                   else limits.get("binc")) or 0
            movestogo = limits.get("movestogo") or 30
            budget = my / (movestogo + 1) + 0.75 * inc
            budget = min(budget, 0.4 * my)
            return start + max(budget, 10) / 1000.0
        if limits.get("infinite"):
            return start + 60.0
        if limits.get("depth") is None and limits.get("nodes") is None:
            return start + self.DEFAULT_MOVETIME
        return None

    def search_with_time(self, board, limits=None):
        limits = limits or {}
        start = time.time()

        self._deadline = self._deadline_for(board, limits, start)
        self._node_limit = limits.get("nodes")
        self._nodes = 0
        self._can_abort = False

        max_depth = limits.get("depth")
        if max_depth is None:
            max_depth = self.MAX_DEPTH
        max_depth = min(int(max_depth), self.MAX_DEPTH)

        root_len = len(board.move_stack)
        best_score, best_pv = 0, []

        for depth in range(1, max_depth + 1):
            iter_start = time.time()
            try:
                score, pv = self.search(board, -99999, 99999, depth)
            except SearchAbort:
                while len(board.move_stack) > root_len:
                    board.pop()
                break

            best_score, best_pv = score, pv
            self._can_abort = True
            elapsed = time.time() - start
            print("info depth {} score cp {} nodes {} time {} pv {}".format(
                depth, int(score), self._nodes, round(elapsed, 3),
                " ".join(m.uci() for m in pv)))

            if abs(score) >= MATE_VALUE - 100:
                break
            if self._node_limit is not None and self._nodes >= self._node_limit:
                break
            iter_time = time.time() - iter_start
            if self._deadline is not None and \
                    time.time() + iter_time * self.BRANCHING_ESTIMATE > self._deadline:
                break

        return best_score, best_pv