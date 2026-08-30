import chess

from evaluation import MG_VALUE, EG_VALUE, MG_PST, EG_PST, PHASE_INC


class EvalBoard(chess.Board):
    """``chess.Board`` that maintains a running PeSTO evaluation accumulator.

    ``_mg`` / ``_eg`` are mid-/end-game scores from White's point of view and
    ``_phase`` is the summed game phase (0..24). They are updated incrementally
    on ``push``/``pop`` for ordinary moves and recomputed from scratch for the
    rarer promotion / castling / en-passant / null moves.
    """

    def __init__(self, fen=chess.STARTING_FEN, *, chess960=False):
        super().__init__(fen, chess960=chess960)
        self._eval_stack = []
        self._recompute_eval()

    # -- accumulator ---------------------------------------------------------

    def _recompute_eval(self):
        mg = eg = phase = 0
        for square, piece in self.piece_map().items():
            i = piece.piece_type - 1
            s = square if piece.color else square ^ 56
            sign = 1 if piece.color else -1
            mg += sign * (MG_VALUE[i] + MG_PST[i][s])
            eg += sign * (EG_VALUE[i] + EG_PST[i][s])
            phase += PHASE_INC[i]
        self._mg, self._eg, self._phase = mg, eg, phase

    def _acc(self, piece_type, color, square, sign):
        i = piece_type - 1
        s = square if color else square ^ 56
        csign = sign if color else -sign
        self._mg += csign * (MG_VALUE[i] + MG_PST[i][s])
        self._eg += csign * (EG_VALUE[i] + EG_PST[i][s])
        self._phase += sign * PHASE_INC[i]

    # -- move making -------------------------------------------------------

    def push(self, move):
        self._eval_stack.append((self._mg, self._eg, self._phase))

        mover = self.piece_at(move.from_square)
        if (not move or mover is None or move.promotion
                or self.is_castling(move) or self.is_en_passant(move)):
            super().push(move)
            self._recompute_eval()
            return

        self._acc(mover.piece_type, mover.color, move.from_square, -1)
        victim = self.piece_at(move.to_square)
        if victim is not None:
            self._acc(victim.piece_type, victim.color, move.to_square, -1)
        self._acc(mover.piece_type, mover.color, move.to_square, +1)
        super().push(move)

    def pop(self):
        move = super().pop()
        self._mg, self._eg, self._phase = self._eval_stack.pop()
        return move

    # -- copying ----------------------------------------------------------

    def copy(self, *, stack=True):
        board = super().copy(stack=stack)
        board._mg, board._eg, board._phase = self._mg, self._eg, self._phase
        board._eval_stack = list(self._eval_stack) if stack else []
        return board
