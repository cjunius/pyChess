import multiprocessing

from multiprocessing.pool import Pool
from operator import itemgetter
import time
from search import BaseSearch

class BaseParallel(BaseSearch):
    def __init__(self):
        self.board = None
        self.depth = 5

    def parallel_search(self, board, depth):
        self.depth = depth
        self.board = board


class ParallelSearchMixin(BaseParallel):
    def parallel_search(self, board, depth):
        super(ParallelSearchMixin, self).parallel_search(board, depth)
        results = Pool(multiprocessing.cpu_count()//2).imap(self.call_search_move, self.board.legal_moves)
        best_score, pv = max(results, key = itemgetter(0))
        return best_score, pv
    
    def call_search_move(self, move):
            self.board.push(move)
            score, pv = self.search(self.board, -99999, 99999, self.depth-1)
            self.board.pop()
            score = -score
            pv.insert(0, move)
            return score, pv


class IterativeDeepeningMixin(BaseParallel):
    def iterative_deepening(self, board, depth):
        super(IterativeDeepeningMixin, self).parallel_search(board, depth)
        best_score = -99999
        pv = []
        start = time.time()
        results = Pool(multiprocessing.cpu_count()//2).imap(self.call_search_depth, range(2, self.depth+1))
        for t, x in results:
            end = time.time()
            print('info score {} pv {} time {}'.format(str(t), str(x), str(end-start)))
            if len(x) > len(pv):
                best_score = t
                pv = x
        return best_score, pv
    
    def call_search_depth(self, depth):
        return self.search(self.board, -99999, 99999, depth)