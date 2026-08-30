from chess.polyglot import zobrist_hash

# Entry flags
TT_EXACT = 0   # value is exact
TT_LOWER = 1   # value is a lower bound (fail-high / beta cut-off)
TT_UPPER = 2   # value is an upper bound (fail-low / all moves searched)

# Scores at or beyond this magnitude are mate-related. The engine currently
# scores mate by remaining depth rather than distance-to-root, so those values
# are not safe to reuse for cut-offs across different depths - we still keep the
# stored move for ordering, but never return the score as a bound.
MATE_GUARD = 9000


class TranspositionTableMixin(object):
    """A simple always-replace-if-deeper transposition table.

    Keyed by Zobrist hash (``chess.polyglot.zobrist_hash``). Entries are
    ``(depth, value, flag, move)`` tuples. The table lives on the engine
    instance and persists between ``go`` commands; ``ucinewgame`` builds a
    fresh engine which drops it.

    When ``self._shared_tt`` is set (Lazy SMP workers) probes and stores are
    delegated to that cross-process table instead of the per-instance dict.
    """

    _shared_tt = None

    @property
    def transposition_table(self):
        try:
            return self._transposition_table
        except AttributeError:
            self._transposition_table = {}
            return self._transposition_table

    def tt_clear(self):
        self.transposition_table.clear()

    def tt_key(self, board):
        return zobrist_hash(board)

    def tt_probe(self, key, depth, alpha, beta):
        """Return ``(cutoff, value, move)``.

        ``cutoff`` is True when the stored value can be returned directly.
        ``move`` is the stored best move (possibly None) and is always
        returned for move ordering even when no cut-off is possible.
        """
        if self._shared_tt is not None:
            return self._shared_tt.probe(key, depth, alpha, beta)

        entry = self.transposition_table.get(key)
        if entry is None:
            return False, 0, None

        e_depth, e_value, e_flag, e_move = entry
        if e_depth >= depth and abs(e_value) < MATE_GUARD:
            if e_flag == TT_EXACT:
                return True, e_value, e_move
            if e_flag == TT_LOWER and e_value >= beta:
                return True, e_value, e_move
            if e_flag == TT_UPPER and e_value <= alpha:
                return True, e_value, e_move
        return False, 0, e_move

    def tt_store(self, key, depth, value, flag, move):
        if self._shared_tt is not None:
            self._shared_tt.store(key, depth, value, flag, move)
            return
        existing = self.transposition_table.get(key)
        if existing is not None and existing[0] > depth:
            return  # keep the deeper analysis
        self.transposition_table[key] = (depth, value, flag, move)
