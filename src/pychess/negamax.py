from __future__ import annotations

from typing import TYPE_CHECKING

import chess

from .constants import INF, MATE, TT_EXACT, TT_LOWER, TT_UPPER

if TYPE_CHECKING:
    from .clock import Clock
    from .evaluation import PestoEvaluator
    from .move_ordering import MoveOrderer
    from .shared_tt import SharedTT
    from .transposition import TranspositionTable

# Upper bound on quiescence extension (plies past the normal horizon).
Q_MAX_DEPTH = 8
# Delta-pruning margin: a bit more than a queen.
Q_DELTA_MARGIN = 1100


class SearchAbortError(Exception):
    """Raised inside the search when the clock says stop; the caller discards
    the partial iteration and keeps the previous one."""


def is_drawn(board: chess.Board) -> bool:
    return (
        board.is_fivefold_repetition()
        or board.is_stalemate()
        or board.is_seventyfive_moves()
        or board.is_insufficient_material()
    )


class Negamax:
    """Fail-soft negamax with a quiescence leaf, over injected collaborators.

    ``evaluator``  - ``.evaluate(board) -> int`` from the side-to-move's view
    ``orderer``    - ``.order_moves`` / ``.mvvlva`` / ``.record_killer`` / ``.record_history``
    ``tt``         - ``.key`` / ``.probe`` / ``.store`` (in-process or shared)
    ``clock``      - ``.should_stop(nodes) -> bool``

    ``search`` and ``quiesce`` share ``self.nodes``; the clock is polled every
    4096 nodes and raises ``SearchAbortError`` once armed.
    """

    def __init__(
        self,
        evaluator: PestoEvaluator,
        orderer: MoveOrderer,
        tt: TranspositionTable | SharedTT,
        clock: Clock,
    ) -> None:
        self.evaluator = evaluator
        self.orderer = orderer
        self.tt = tt
        self.clock = clock
        self.nodes = 0

    def search(
        self, board: chess.Board, alpha: int, beta: int, depth: int, ply: int = 0
    ) -> tuple[int, list[chess.Move]]:
        self.nodes += 1
        if ply and not (self.nodes & 4095) and self.clock.should_stop(self.nodes):
            raise SearchAbortError

        if depth <= 0 or board.is_game_over():
            if board.is_checkmate():
                return -MATE - depth, []
            if is_drawn(board):
                return -depth, []
            return self.quiesce(board, alpha, beta, 0), []

        alpha_orig = alpha

        key = self.tt.key(board)
        tt_cutoff, tt_value, tt_move = self.tt.probe(key, depth, alpha, beta)
        if tt_cutoff and ply > 0:
            return tt_value, [tt_move] if tt_move else []

        best_score = -INF
        best_move = None
        pv = []
        for move in self.orderer.order_moves(board, tt_move=tt_move, ply=ply):
            board.push(move)
            try:
                child_score, child_pv = self.search(board, -beta, -alpha, depth - 1, ply + 1)
            except SearchAbortError:
                board.pop()
                raise
            child_score = -child_score
            board.pop()

            if child_score > best_score:
                best_score = child_score
                best_move = move
                pv = [move, *child_pv]

            if best_score > alpha:
                alpha = best_score

            if alpha >= beta:
                if not board.is_capture(move):
                    self.orderer.record_killer(ply, move)
                    self.orderer.record_history(board, move, depth)
                break

        if best_score <= alpha_orig:
            flag = TT_UPPER
        elif best_score >= beta:
            flag = TT_LOWER
        else:
            flag = TT_EXACT
        self.tt.store(key, depth, best_score, flag, best_move)

        return best_score, pv

    def quiesce(self, board: chess.Board, alpha: int, beta: int, qply: int) -> int:
        """Fail-soft quiescence search.

        - Depth-bounded: capture chains are cut off after ``Q_MAX_DEPTH`` plies.
        - Check-aware: while in check every legal evasion is searched and there
          is no stand-pat cut-off, so the side to move can never "pass" out of
          check.
        - Non-check nodes search captures and promotions only, MVV-LVA ordered,
          with stand-pat and delta pruning.
        """
        self.nodes += 1
        if not (self.nodes & 4095) and self.clock.should_stop(self.nodes):
            raise SearchAbortError

        if board.is_checkmate():
            return qply - MATE
        if is_drawn(board) or board.is_repetition(3):
            return 0

        if board.is_check():
            best = -INF
            if qply >= Q_MAX_DEPTH:
                return self.evaluator.evaluate(board)
            moves = list(board.legal_moves)
        else:
            best = self.evaluator.evaluate(board)
            if best >= beta or qply >= Q_MAX_DEPTH:
                return best
            if best > alpha:
                alpha = best
            if best < alpha - Q_DELTA_MARGIN:  # delta pruning
                return best
            moves = [m for m in board.legal_moves if board.is_capture(m) or m.promotion]
            moves.sort(key=lambda m: self.orderer.mvvlva(board, m), reverse=True)

        for move in moves:
            board.push(move)
            try:
                score = -self.quiesce(board, -beta, -alpha, qply + 1)
            except SearchAbortError:
                board.pop()
                raise
            board.pop()

            if score > best:
                best = score
            if best > alpha:
                alpha = best
            if alpha >= beta:
                break

        return best
