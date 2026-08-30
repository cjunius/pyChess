"""Score conventions and transposition-table flags shared across the search.

Mate is scored by *remaining depth* (``-MATE - depth``), not distance-to-root,
so mate scores are not safe to reuse as bounds across different depths: the
transposition table keeps the stored move for ordering but never returns a
value with ``abs(score) >= MATE_GUARD`` as a cut-off.

``INF`` is the alpha-beta window sentinel; every real evaluation sits well
inside ``+/- MATE``.
"""

INF = 99999  # alpha-beta window sentinel
MATE = 9999  # abs(score) at or above this is mate-related
MATE_IN_MAX = 9899  # MATE - 100: mate within ~100 plies (worker win/loss flag)
MATE_GUARD = 9000  # the TT never returns abs(score) >= this as a bound

# Transposition-table entry bounds.
TT_EXACT = 0
TT_LOWER = 1  # value is a lower bound (fail-high / beta cut-off)
TT_UPPER = 2  # value is an upper bound (fail-low / all moves searched)
