import chess
from chess import Move

from evaluation import PIECE_VALUES


class MoveOrderingMixin(object):
    """Orders moves to maximise alpha-beta cut-offs.

    Priority (high to low):
      1. Transposition-table / hash move
      2. Captures, sorted by MVV-LVA
      3. Non-capture promotions
      4. Killer moves for this ply
      5. Quiet moves, sorted by the history heuristic

    Killer and history state is kept per engine instance and is reset by
    building a fresh engine on ``ucinewgame``.
    """

    # ---- lazily-created per-instance state -------------------------------

    @property
    def killers(self):
        try:
            return self._killers
        except AttributeError:
            self._killers = {}
            return self._killers

    @property
    def history(self):
        try:
            return self._history
        except AttributeError:
            self._history = {}
            return self._history

    # ---- ordering -------------------------------------------------------

    # Restricts the moves considered at the root; set by Lazy SMP workers so
    # each process owns a slice of the root moves. ``None`` means "all".
    _root_moves = None

    def order_moves(self, board, tt_move=None, ply=0):
        killers = self.killers.get(ply, ())
        history = self.history
        color = board.turn
        root_moves = self._root_moves if ply == 0 else None

        scored = []
        for move in board.legal_moves:
            if root_moves is not None and move not in root_moves:
                continue
            if tt_move is not None and move == tt_move:
                score = 1_000_000
            elif board.is_capture(move):
                score = 100_000 + self.mvvlva(board, move)
            elif move.promotion:
                score = 90_000 + PIECE_VALUES[move.promotion]
            elif move in killers:
                score = 80_000 - killers.index(move)
            else:
                score = history.get((color, move.from_square, move.to_square), 0)
            scored.append((score, move))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [move for _, move in scored]

    def mvvlva(self, board, move: Move) -> int:
        """Most Valuable Victim / Least Valuable Attacker score."""
        if board.is_en_passant(move):
            return PIECE_VALUES[chess.PAWN] * 10 - PIECE_VALUES[chess.PAWN] // 100

        victim = board.piece_type_at(move.to_square)
        if victim is None:
            return 0
        attacker = board.piece_type_at(move.from_square)
        return PIECE_VALUES[victim] * 10 - PIECE_VALUES[attacker] // 100

    # ---- cut-off bookkeeping ------------------------------------------

    def record_killer(self, ply, move):
        slot = self.killers.setdefault(ply, [])
        if move in slot:
            return
        slot.insert(0, move)
        del slot[2:]

    def record_history(self, board, move, depth):
        key = (board.turn, move.from_square, move.to_square)
        self.history[key] = self.history.get(key, 0) + depth * depth


# Backwards-compatible alias for the old name referenced elsewhere.
ChecksCapturesOrderMixin = MoveOrderingMixin
