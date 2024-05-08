import random
import chess
from chess import Board

class BaseSearch(object):
    def __init__(self, board: Board):
        if board is None:
            raise ValueError("Board must be specified")
        self.board = board

    def stop_signal(self):
        return False
    
    def is_drawn(self):
        return self.board.is_fivefold_repetition() \
            or self.board.is_stalemate() \
            or self.board.is_seventyfive_moves() \
            or self.board.is_insufficient_material()
    
    def order_moves(self):
        return self.board.legal_moves
    
class RandomMixin(BaseSearch):
    def search(self, alpha, beta, depth, ply=0):
        return 0, [random.choice(list(self.board.legal_moves))]
    

class NegamaxMixin(BaseSearch):
    def search(self, alpha, beta, depth, ply=0):

        if depth <= 0 or self.board.is_game_over():
            if self.board.is_checkmate():
                return -9999 - depth, []
            elif self.is_drawn():
                return 0 - depth, []
            else:
                return self.evaluate(), []
            
        if ply > 1 and self.stop_signal():
            return 0, []
        
        best_score = -99999
        pv = []
        moves = self.order_moves()
        for move in moves:
            self.board.push(move)
            child_score, child_pv = self.search(-beta, -alpha, depth-1, ply+1)
            child_score = -child_score
            self.board.pop()

            if ply > 0 and self.stop_signal():
                return 0, []
            
            if child_score >= beta:
                return beta, []
            
            if child_score > best_score:
                best_score = child_score
                
                if best_score > alpha:
                    alpha = best_score
                    pv = [move] + child_pv

        return alpha, pv