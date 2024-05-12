import random
from typing import List
from chess import Move

class BaseSearch(object):
    def stop_signal(self):
        return False
    
    def is_drawn(self, board):
        return board.is_fivefold_repetition() \
            or board.is_stalemate() \
            or board.is_seventyfive_moves() \
            or board.is_insufficient_material()
    
    def order_moves(self, board):
        return board.legal_moves
    
    def evaluate_leaf_node(self, board, alpha, beta, depth):
        return self.evaluate(), []
    
class RandomMixin(BaseSearch):
    def search(self, board, alpha=0, beta=0, depth=0, ply=0):
        return 0, [random.choice(list(board.legal_moves))]


class NegamaxMixin(BaseSearch):
    def search(self, board, alpha, beta, depth, ply=0):

        if depth <= 0 or board.is_game_over():
            if board.is_checkmate():
                return -9999 - depth, []
            elif self.is_drawn(board):
                return 0 - depth, []
            else:
                return self.evaluate_leaf_node(board, alpha, beta, depth), []
            
        if ply > 1 and self.stop_signal():
            return 0, []
        
        best_score = -99999
        pv = []
        moves = self.order_moves(board)
        for move in moves:
            board.push(move)
            child_score, child_pv = self.search(board, -beta, -alpha, depth-1, ply+1)
            child_score = -child_score
            board.pop()

            if ply > 0 and self.stop_signal():
                return 0, []
            
            if child_score >= beta:
                return beta, []
            
            if child_score > best_score:
                best_score = child_score
                
            # Removing Indentation
            if best_score > alpha:
                alpha = best_score
                pv = [move] + child_pv

            # Adding
            if alpha >= beta:
                break

        return alpha, pv
    
class QuiescenceSearchMixin(BaseSearch):

    def evaluate_leaf_node(self, board, alpha: int, beta: int, depth: int) -> int:
        if board.is_game_over():
            if board.is_checkmate():
                return -9999 - depth
            if self.is_drawn(board):
                return 0 - depth
            
        if board.is_repetition():
            return 0

        stand_pat = self.evaluate(board)
        if stand_pat >= beta:
            return beta
        alpha = max(alpha, stand_pat)

        def order_moves_quiescence() -> List[Move]:
            captures = []
            for move in board.legal_moves:
                if board.gives_check(move):
                    captures.append(move)
                elif board.is_capture(move):
                    captures.append(move)
                elif not move.promotion == None:
                    captures.append(move)

            return captures

        moves = order_moves_quiescence()
        for move in moves:

            #ToDo: Delta Pruning

            board.push(move)
            score = -self.evaluate_leaf_node(board, -beta, -alpha, depth-1)
            board.pop()
            
            if score >= beta:
                return beta
            alpha = max(alpha, score)

        return alpha
    
    