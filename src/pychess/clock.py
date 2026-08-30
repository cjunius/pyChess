"""UCI time management and the search-abort predicate.

``deadline_from_limits`` turns the raw ``go`` limits into a wall-clock deadline;
``Clock`` is polled by the search (every few thousand nodes) and, once armed,
tells it to bail out via ``SearchAbortError``.
"""

import time

import chess

from .shared_tt import SharedFlag
from .types import GoLimits

MAX_DEPTH = 64
DEFAULT_MOVETIME = 4.0  # seconds, used for a bare "go"


def deadline_from_limits(board: chess.Board, limits: GoLimits, start: float) -> float | None:
    """Return the ``time.time()`` value the search must finish by, or ``None``
    when only ``depth`` / ``nodes`` bound it."""
    if limits.get("movetime") is not None:
        return start + limits["movetime"] / 1000.0

    my = limits.get("wtime") if board.turn == chess.WHITE else limits.get("btime")
    if my is not None:
        inc = (limits.get("winc") if board.turn == chess.WHITE else limits.get("binc")) or 0
        movestogo = limits.get("movestogo") or 30
        budget = my / (movestogo + 1) + 0.75 * inc
        budget = min(budget, 0.4 * my)
        return start + max(budget, 10) / 1000.0

    if limits.get("infinite"):
        return start + 60.0
    if limits.get("depth") is None and limits.get("nodes") is None:
        return start + DEFAULT_MOVETIME
    return None


class Clock:
    """Stop predicate for one search.

    ``should_stop`` returns ``False`` until ``arm()`` is called, so the first
    full iteration always completes and the search never returns without a
    move. Lazy SMP workers share one ``stop_flag`` so a forced mate found by
    any worker stops the rest.
    """

    def __init__(
        self,
        deadline: float | None = None,
        node_limit: int | None = None,
        stop_flag: SharedFlag | None = None,
    ) -> None:
        self.deadline = deadline
        self.node_limit = node_limit
        self.stop_flag = stop_flag
        self._armed = False

    def arm(self) -> None:
        self._armed = True

    def should_stop(self, nodes: int) -> bool:
        if not self._armed:
            return False
        if self.stop_flag is not None and self.stop_flag.is_set():
            return True
        if self.node_limit is not None and nodes >= self.node_limit:
            return True
        return self.deadline is not None and time.time() >= self.deadline
