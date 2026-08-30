from __future__ import annotations

from typing import TYPE_CHECKING

import chess

from .constants import CONTEMPT, INF, MATE, MATE_IN_MAX, TT_EXACT, TT_LOWER, TT_UPPER

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

# Null-move pruning: give the opponent a free move at reduced depth; if the
# position still fails high it is almost certainly a cut-off.
NULL_MIN_DEPTH = 3  # don't bother below this - the reduced search is too shallow
NULL_DEEP_DEPTH = 6  # above this the reduction grows from 2 to 3
NULL_VERIFY_DEPTH = 10  # at/above this, confirm the cut with a real reduced search

# Late move reductions: quiet, late, non-checking moves are searched shallower
# first; a result above alpha triggers a full-depth re-search.
LMR_MIN_DEPTH = 3  # nodes shallower than this search every move at full depth
LMR_FULL_MOVES = 3  # the first N moves at a node always get a full-depth search


class SearchAbortError(Exception):
    """Raised inside the search when the clock says stop; the caller discards
    the partial iteration and keeps the previous one."""


def is_drawn(board: chess.Board) -> bool:
    """Terminal draws - the game is over by rule, no claim needed."""
    return (
        board.is_fivefold_repetition()
        or board.is_stalemate()
        or board.is_seventyfive_moves()
        or board.is_insufficient_material()
    )


def claims_draw(board: chess.Board) -> bool:
    """Claimable draws - threefold repetition and the fifty-move rule. Not
    ``is_game_over`` in python-chess, but the search must still score them 0:
    inside the tree either side can force the claim."""
    return board.halfmove_clock >= 100 or board.is_repetition(3)


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

    @staticmethod
    def _draw_score() -> int:
        """A draw, from the side-to-move's point of view. ``CONTEMPT`` > 0 makes
        the engine treat a draw as slightly bad for itself and play on."""
        return -CONTEMPT

    @staticmethod
    def _null_ok(board: chess.Board, depth: int, can_null: bool, ply: int) -> bool:
        """Whether a null move is safe to try at this node.

        Skip it at the root, when it was already tried on the way here, at very
        low depth, while in check, and in likely zugzwang - when the side to
        move has only king and pawns a free move is worth more than any real
        one, so the null search lies.
        """
        if not can_null or ply == 0 or depth < NULL_MIN_DEPTH or board.is_check():
            return False
        us = board.occupied_co[board.turn]
        return bool((board.knights | board.bishops | board.rooks | board.queens) & us)

    @staticmethod
    def _lmr_reduction(move_index: int, depth: int, *, favoured: bool) -> int:
        """Plies to shave off a late quiet move's first search.

        Grows with how late the move is ordered and how deep the node;
        ``favoured`` - a killer or a move with positive history - shrinks it by
        one. Clamped so the reduced search keeps at least one ply.
        """
        r = 1 + (move_index >= 6) + (depth >= 8)
        if favoured:
            r -= 1
        return max(0, min(r, depth - 2))

    def search(
        self,
        board: chess.Board,
        alpha: int,
        beta: int,
        depth: int,
        ply: int = 0,
        *,
        can_null: bool = True,
    ) -> tuple[int, list[chess.Move]]:
        self.nodes += 1
        if ply and not (self.nodes & 4095) and self.clock.should_stop(self.nodes):
            raise SearchAbortError

        if depth <= 0 or board.is_game_over():
            if board.is_checkmate():
                return -(MATE - ply), []
            if is_drawn(board):
                return self._draw_score(), []
            return self.quiesce(board, alpha, beta, 0, ply), []

        if ply and claims_draw(board):
            return self._draw_score(), []

        if ply:
            # Mate-distance pruning: this node can do no better than mating now
            # and no worse than being mated now, so clamp the window and bail
            # if it collapses - the search then never chases a slower mate.
            alpha = max(alpha, -(MATE - ply))
            beta = min(beta, MATE - ply)
            if alpha >= beta:
                return alpha, []

        alpha_orig = alpha

        key = self.tt.key(board)
        tt_cutoff, tt_value, tt_move = self.tt.probe(key, depth, alpha, beta, ply)
        if tt_cutoff and ply > 0:
            return tt_value, [tt_move] if tt_move else []

        # --- Null-move pruning ------------------------------------------------
        if (
            self._null_ok(board, depth, can_null, ply)
            and beta < MATE_IN_MAX
            and self.evaluator.evaluate(board) >= beta
        ):
            r = 2 + (depth > NULL_DEEP_DEPTH)
            board.push(chess.Move.null())
            try:
                null_score, _ = self.search(
                    board, -beta, -beta + 1, depth - 1 - r, ply + 1, can_null=False
                )
            except SearchAbortError:
                board.pop()
                raise
            null_score = -null_score
            board.pop()

            if null_score >= beta:
                if depth < NULL_VERIFY_DEPTH:
                    return beta, []
                # Verification search: a real (non-null) reduced search from the
                # same position guards against zugzwang, where the null result
                # is a mirage.
                verify, _ = self.search(board, beta - 1, beta, depth - r, ply, can_null=False)
                if verify >= beta:
                    return beta, []

        in_check = board.is_check()

        best_score = -INF
        best_move = None
        pv = []
        for move_index, move in enumerate(
            self.orderer.order_moves(board, tt_move=tt_move, ply=ply)
        ):
            is_capture = board.is_capture(move)

            reduction = 0
            if (
                depth >= LMR_MIN_DEPTH
                and move_index >= LMR_FULL_MOVES
                and not in_check
                and not is_capture
                and not move.promotion
                and move != tt_move
                and not board.gives_check(move)
            ):
                favoured = self.orderer.is_killer(ply, move) or (
                    self.orderer.history_score(board, move) > 0
                )
                reduction = self._lmr_reduction(move_index, depth, favoured=favoured)

            board.push(move)
            try:
                if move_index == 0:
                    # The (well-ordered) first move gets the full window.
                    child_score, child_pv = self.search(board, -beta, -alpha, depth - 1, ply + 1)
                    child_score = -child_score
                else:
                    # Later moves: a null-window scout, reduced if LMR applies.
                    # It only asks "is this move better than alpha?".
                    child_score, child_pv = self.search(
                        board, -alpha - 1, -alpha, depth - 1 - reduction, ply + 1
                    )
                    child_score = -child_score
                    # Scout failed high: re-search at full depth and, unless the
                    # cut-off is already certain, the full window.
                    if child_score > alpha and (child_score < beta or reduction):
                        child_score, child_pv = self.search(
                            board, -beta, -alpha, depth - 1, ply + 1
                        )
                        child_score = -child_score
            except SearchAbortError:
                board.pop()
                raise
            board.pop()

            if child_score > best_score:
                best_score = child_score
                best_move = move
                pv = [move, *child_pv]

            if best_score > alpha:
                alpha = best_score

            if alpha >= beta:
                if not is_capture:
                    self.orderer.record_killer(ply, move)
                    self.orderer.record_history(board, move, depth)
                break

        if best_score <= alpha_orig:
            flag = TT_UPPER
        elif best_score >= beta:
            flag = TT_LOWER
        else:
            flag = TT_EXACT
        self.tt.store(key, depth, best_score, flag, best_move, ply)

        return best_score, pv

    def quiesce(self, board: chess.Board, alpha: int, beta: int, qply: int, ply: int = 0) -> int:
        """Fail-soft quiescence search.

        - Depth-bounded: capture chains are cut off after ``Q_MAX_DEPTH`` plies.
        - Check-aware: while in check every legal evasion is searched and there
          is no stand-pat cut-off, so the side to move can never "pass" out of
          check.
        - Non-check nodes search captures and promotions only, MVV-LVA ordered,
          with stand-pat and delta pruning.

        ``ply`` is the distance from the search root, used only to score mates
        relative to the root like ``search`` does.
        """
        self.nodes += 1
        if not (self.nodes & 4095) and self.clock.should_stop(self.nodes):
            raise SearchAbortError

        if board.is_checkmate():
            return -(MATE - ply - qply)
        if is_drawn(board) or claims_draw(board):
            return self._draw_score()

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
                score = -self.quiesce(board, -beta, -alpha, qply + 1, ply)
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
