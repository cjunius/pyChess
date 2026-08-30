"""Score conventions and transposition-table flags shared across the search.

Mate is scored as *distance from the root*: a forced mate delivered ``m`` plies
from the root scores ``MATE - m`` for the mating side (so a faster mate always
outranks a slower one). ``abs(score) >= MATE_IN_MAX`` marks a mate score.

Because that distance is measured from the root, a mate score is only meaningful
at the ply it was found. Before a score goes into the transposition table it is
rebased to be relative to the storing node (:func:`tt_store_score`); on the way
out it is rebased back to the root (:func:`tt_probe_score`). With that in place
the TT can return mate bounds like any other score.

``INF`` is the alpha-beta window sentinel; every real evaluation sits well
inside ``+/- MATE``.
"""

INF = 99999  # alpha-beta window sentinel
MATE = 9999  # abs(score) at or above MATE_IN_MAX is mate-related
MATE_IN_MAX = 9899  # MATE - 100: abs(score) >= this is a mate (max tree ply << 100)

CONTEMPT = 0  # a draw scores -CONTEMPT for the side to move; > 0 == play on

# Transposition-table entry bounds.
TT_EXACT = 0
TT_LOWER = 1  # value is a lower bound (fail-high / beta cut-off)
TT_UPPER = 2  # value is an upper bound (fail-low / all moves searched)


def tt_store_score(value: int, ply: int) -> int:
    """Rebase a root-relative score to the storing node at ``ply``.

    Only mate scores move; everything else is returned unchanged.
    """
    if value >= MATE_IN_MAX:
        return value + ply
    if value <= -MATE_IN_MAX:
        return value - ply
    return value


def tt_probe_score(value: int, ply: int) -> int:
    """Inverse of :func:`tt_store_score`: rebase a stored score back to the root."""
    if value >= MATE_IN_MAX:
        return value - ply
    if value <= -MATE_IN_MAX:
        return value + ply
    return value
