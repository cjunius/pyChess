import functools
import multiprocessing

from multiprocessing.pool import Pool
import time

from chess import Move
from search import BaseSearch

class BaseParallel(BaseSearch):
    def __init__(self):
        self.board = None
        self.depth = 5

    def parallel_search(self, board, depth):
        self.depth: float = depth
        self.board = board


class ParallelSearchMixin(BaseParallel):
    def parallel_search(self, board, depth) -> tuple[float, list[Move]]:
        super(ParallelSearchMixin, self).parallel_search(board, depth)

        best_score: float = -99999
        pv = []

        start = time.time()
        results = Pool(multiprocessing.cpu_count()-1).imap(self.call_search_move, self.board.legal_moves)
        for result in results:
            if result[0] > best_score:
                best_score = result[0]
                pv = result[1]
                end = time.time()
                print("info score {} pv {} time {}".format(result[0], result[1], end-start))
                
        return best_score, pv
    
    
    def call_search_move(self, move) -> tuple[float, list[Move]]:
            self.board.push(move)
            score, pv = self.search(self.board, -99999, 99999, self.depth-1)
            self.board.pop()
            score = -score
            pv.insert(0, move)
            return score, pv


class IterativeDeepeningMixin(BaseParallel):
    def iterative_deepening(self, board, depth) -> tuple[float, list[Move]]:
        super(IterativeDeepeningMixin, self).parallel_search(board, depth)
        best_score: float = -99999
        pv = []
        start = time.time()
        part_f = functools.partial(self.search, self.board, -99999, 99999)
        results = Pool(multiprocessing.cpu_count()//2).imap(part_f, range(2, self.depth+1))
        for t, x in results:
            end = time.time()
            print('info score {} pv {} time {}'.format(str(t), str(x), str(end-start)))
            if len(x) > len(pv):
                best_score = t
                pv = x
        return best_score, pv