from evaluation import PieceValueSquareTableMixin
from move_ordering import ChecksCapturesOrderMixin
from parallel import IterativeDeepeningMixin, ParallelSearchMixin
from search import NegamaxMixin, QuiescenceSearchMixin, RandomMixin

class NegamaxEngine(ParallelSearchMixin, NegamaxMixin, QuiescenceSearchMixin, PieceValueSquareTableMixin, ChecksCapturesOrderMixin, IterativeDeepeningMixin):
    pass

class RandomEngine(RandomMixin):
    pass