"""Shared type aliases."""

from typing import TypedDict


class GoLimits(TypedDict, total=False):
    """Parsed ``go`` arguments. Every key is optional; missing means "no limit"."""

    depth: int
    nodes: int
    movetime: int  # milliseconds
    wtime: int
    btime: int
    winc: int
    binc: int
    movestogo: int
    infinite: bool
