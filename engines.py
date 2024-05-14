from evaluation import PieceSquareTableMixin, PieceValueMixin
from parallel import IterativeDeepeningMixin, ParallelSearchMixin
from search import NegamaxMixin, QuiescenceSearchMixin, RandomMixin

class NegamaxEngine(ParallelSearchMixin, NegamaxMixin, QuiescenceSearchMixin, PieceValueMixin, PieceSquareTableMixin, IterativeDeepeningMixin): #ChecksCapturesOrderMixin slows the engine down
    pass

class RandomEngine(RandomMixin):
    pass