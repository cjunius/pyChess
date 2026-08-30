import chess
from chess.polyglot import zobrist_hash

from .constants import TT_EXACT, TT_LOWER, TT_UPPER, tt_probe_score, tt_store_score

# (depth, value, flag, move)
_Entry = tuple[int, int, int, "chess.Move | None"]


class TranspositionTable:
    """An always-replace-if-deeper table keyed by Zobrist hash.

    Entries are ``(depth, value, flag, move)`` tuples. This is the in-process
    table used for single-threaded search and tests; Lazy SMP uses
    ``shared_tt.SharedTT``, which exposes the same
    ``key`` / ``probe`` / ``store`` interface over shared memory.

    ``probe`` / ``store`` take the current ``ply`` so mate scores can be
    rebased between the root and the storing node (see ``constants``).
    """

    def __init__(self) -> None:
        self._table: dict[int, _Entry] = {}

    def clear(self) -> None:
        self._table.clear()

    def key(self, board: chess.Board) -> int:
        return zobrist_hash(board)

    def probe(
        self, key: int, depth: int, alpha: int, beta: int, ply: int = 0
    ) -> tuple[bool, int, chess.Move | None]:
        """Return ``(cutoff, value, move)``.

        ``cutoff`` is True when the stored value can be returned directly.
        ``move`` is the stored best move (possibly None) and is always returned
        for move ordering even when no cut-off is possible.
        """
        entry = self._table.get(key)
        if entry is None:
            return False, 0, None

        e_depth, e_value, e_flag, e_move = entry
        if e_depth >= depth:
            value = tt_probe_score(e_value, ply)
            if e_flag == TT_EXACT:
                return True, value, e_move
            if e_flag == TT_LOWER and value >= beta:
                return True, value, e_move
            if e_flag == TT_UPPER and value <= alpha:
                return True, value, e_move
        return False, 0, e_move

    def store(
        self,
        key: int,
        depth: int,
        value: int,
        flag: int,
        move: chess.Move | None,
        ply: int = 0,
    ) -> None:
        existing = self._table.get(key)
        if existing is not None and existing[0] > depth:
            return  # keep the deeper analysis
        self._table[key] = (depth, tt_store_score(value, ply), flag, move)
