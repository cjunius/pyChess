from evaluation import PeSTOEvaluationMixin
from move_ordering import MoveOrderingMixin
from transposition import TranspositionTableMixin
from parallel import IterativeDeepeningMixin, LazySMPMixin
from search import NegamaxMixin, QuiescenceSearchMixin, RandomMixin

class NegamaxEngine(
    LazySMPMixin,
    IterativeDeepeningMixin,
    MoveOrderingMixin,
    TranspositionTableMixin,
    NegamaxMixin,
    QuiescenceSearchMixin,
    PeSTOEvaluationMixin,
):
    pass

class RandomEngine(RandomMixin):
    pass
