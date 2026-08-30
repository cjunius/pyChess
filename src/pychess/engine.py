import random
from typing import Protocol

import chess

from . import lazy_smp
from .lazy_smp import SearchResult
from .types import GoLimits


class SupportsSearch(Protocol):
    """The interface the UCI layer needs from an engine."""

    def search(self, board: chess.Board, limits: GoLimits | None = None) -> SearchResult: ...


class Engine:
    """The default engine: Lazy SMP over a fail-soft negamax / PeSTO search.

    Stateless today - each ``search`` spins up its own shared transposition
    table. Rebuilt on ``ucinewgame`` so any future per-game state is dropped.
    """

    def search(self, board: chess.Board, limits: GoLimits | None = None) -> SearchResult:
        return lazy_smp.search(board, limits or {})


class RandomEngine:
    """Plays a uniformly random legal move. A baseline for testing."""

    def search(self, board: chess.Board, limits: GoLimits | None = None) -> SearchResult:
        move = random.choice(list(board.legal_moves))
        return SearchResult(score=0, pv=[move], depth=0, nodes=1, elapsed=0.0)
