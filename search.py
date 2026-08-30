import random
from typing import List
from chess import Move, polyglot

from transposition import TT_EXACT, TT_LOWER, TT_UPPER

# Upper bound on quiescence extension (plies past the normal horizon).
Q_MAX_DEPTH = 8
# Delta-pruning margin: a bit more than a queen.
Q_DELTA_MARGIN = 1100
# Score magnitude at/above which a value is mate-related.
MATE_VALUE = 9999


class SearchAbort(Exception):
    """Raised inside the search when a time or node limit is hit; the caller
    discards the partial iteration and keeps the previous one."""


class BaseSearch(object):

    _nodes = 0

    def stop_signal(self):
        return False

    def mvvlva(self, board, move):
        return 0

    def is_drawn(self, board):
        return board.is_fivefold_repetition() \
            or board.is_stalemate() \
            or board.is_seventyfive_moves() \
            or board.is_insufficient_material()
    
    def order_moves(self, board, tt_move=None, ply=0):
        return board.legal_moves

    def evaluate_leaf_node(self, board, alpha, beta, depth):
        return self.evaluate(), []

    # --- transposition-table / heuristic hooks -------------------------
    # Overridden by TranspositionTableMixin / MoveOrderingMixin. The no-op
    # defaults let NegamaxMixin run without those mixins mixed in.

    def tt_key(self, board):
        return None

    def tt_probe(self, key, depth, alpha, beta):
        return False, 0, None

    def tt_store(self, key, depth, value, flag, move):
        pass

    def record_killer(self, ply, move):
        pass

    def record_history(self, board, move, depth):
        pass
    
class RandomMixin(BaseSearch):
    def search(self, board, alpha=0, beta=0, depth=0, ply=0):
        return 0, [random.choice(list(board.legal_moves))]


class NegamaxMixin(BaseSearch):

    def search(self, board, alpha: float, beta: float, depth: float, ply: float=0) -> tuple[float, list[Move]]:

        self._nodes += 1
        if ply and not (self._nodes & 4095) and self.stop_signal():
            raise SearchAbort

        if depth <= 0 or board.is_game_over():
            if board.is_checkmate():
                return -9999 - depth, []
            elif self.is_drawn(board):
                return 0 - depth, []
            else:
                return self.evaluate_leaf_node(board, alpha, beta, depth), []

        alpha_orig = alpha

        tt_key = self.tt_key(board)
        tt_cutoff, tt_value, tt_move = self.tt_probe(tt_key, depth, alpha, beta)
        if tt_cutoff and ply > 0:
            return tt_value, [tt_move] if tt_move else []

        best_score = -99999
        best_move = None
        pv = []
        moves = self.order_moves(board, tt_move=tt_move, ply=ply)
        for move in moves:
            board.push(move)
            try:
                child_score, child_pv = self.search(board, -beta, -alpha, depth-1, ply+1)
            except SearchAbort:
                board.pop()
                raise
            child_score = -child_score
            board.pop()

            if child_score > best_score:
                best_score = child_score
                best_move = move
                pv = [move] + child_pv

            if best_score > alpha:
                alpha = best_score

            if alpha >= beta:
                if not board.is_capture(move):
                    self.record_killer(ply, move)
                    self.record_history(board, move, depth)
                break

        if best_score <= alpha_orig:
            flag = TT_UPPER
        elif best_score >= beta:
            flag = TT_LOWER
        else:
            flag = TT_EXACT
        self.tt_store(tt_key, depth, best_score, flag, best_move)

        return best_score, pv
    
class QuiescenceSearchMixin(BaseSearch):
    """Fail-soft quiescence search.

    - Depth-bounded: capture chains are cut off after ``Q_MAX_DEPTH`` plies.
    - Check-aware: while in check every legal evasion is searched and there is
      no stand-pat cut-off, so the side to move can never "pass" out of check.
    - Non-check nodes search captures and promotions only, MVV-LVA ordered,
      with stand-pat and delta pruning.
    """

    def evaluate_leaf_node(self, board, alpha, beta, depth):
        return self.quiesce(board, alpha, beta, 0)

    def quiesce(self, board, alpha, beta, qply):
        self._nodes += 1
        if not (self._nodes & 4095) and self.stop_signal():
            raise SearchAbort

        if board.is_checkmate():
            return qply - MATE_VALUE
        if self.is_drawn(board) or board.is_repetition(3):
            return 0

        in_check = board.is_check()

        if in_check:
            best = -99999
            if qply >= Q_MAX_DEPTH:
                return self.evaluate(board)
            moves = list(board.legal_moves)
        else:
            best = self.evaluate(board)
            if best >= beta or qply >= Q_MAX_DEPTH:
                return best
            if best > alpha:
                alpha = best
            if best < alpha - Q_DELTA_MARGIN:      # delta pruning
                return best
            moves = [m for m in board.legal_moves
                     if board.is_capture(m) or m.promotion]
            moves.sort(key=lambda m: self.mvvlva(board, m), reverse=True)

        for move in moves:
            board.push(move)
            try:
                score = -self.quiesce(board, -beta, -alpha, qply + 1)
            except SearchAbort:
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
