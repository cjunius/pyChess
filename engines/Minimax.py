from abc import abstractmethod
import chess
import chess.polyglot
import time
import sys

from engines.Transposition_Table import FLAG, TransTable, TransTableEntry
from move_ordering import Move_Ordering

class Engine():
    def __init__(self, depth=3, opening_book="bots/books/bookfish.bin", debug=False):
        self.depth = depth
        self.opening_book = opening_book
        self.evaluations = 0 
        self.debug = debug
        self.color = chess.WHITE
        self.san_move_stack = []
        self.once = True
        self.tt = TransTable()

    @abstractmethod
    def getName(self):
        pass
        
    @abstractmethod
    def evaluate_board(self, board: chess.Board):
        pass

    def findMove(self, board: chess.Board):
        
        try:
            return chess.polyglot.MemoryMappedReader(self.opening_book).weighted_choice(board).move
        
        except Exception:
            
            bestValue = -999999
            bestMove = chess.Move.null()

            moves = Move_Ordering.order_moves(board)
            for move in moves:
                board.push(move)
                if board.is_checkmate():
                    board.pop()
                    return move
                score = self.alphaBeta(board, -99999, 99999, self.depth)
                board.pop()
                if score > bestValue:
                    bestValue = score
                    bestMove = move

            return bestMove

    def alphaBetaMax(self, board: chess.Board, alpha: int, beta: int, depth: int) -> int:
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board, depth)
        
        moves = Move_Ordering.order_moves(board)
        for move in moves:
            board.push(move)
            score = self.alphaBetaMin(board, alpha, beta, depth-1)
            board.pop()
            if score >= beta:
                return beta # fail hard beta-cutoff
            alpha = max(alpha, score) # alpha acts like max in Minimax
        return alpha
    
    def alphaBetaMin(self, board: chess.Board, alpha: int, beta: int, depth) -> int:
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board, depth)
        
        moves = Move_Ordering.order_moves(board)
        for move in moves:
            board.push(move)
            score = self.alphaBetaMax(board, alpha, beta, depth-1)
            board.pop()
            if score <= alpha:
                return alpha # fail hard alpha-cutoff
            beta = min(beta, score) # alpha acts like max in Minimax
        return beta
    
    def alphaBeta(self, board: chess.Board, alpha: int, beta: int, depth: int) -> int:

        alpha_prime = alpha
        bestScore = -999999

        ttEntry = self.tt.getEntry(board)
        if ttEntry and ttEntry.depth >= depth:
            if ttEntry.flag == FLAG.EXACT:
                return ttEntry.value
            elif ttEntry.flag == FLAG.LOWER_BOUND:
                alpha = max(alpha, ttEntry.value)
            elif ttEntry.flag == FLAG.UPPER_BOUND:
                beta = min(beta, ttEntry.value)
            
            if alpha >= beta:
                return ttEntry.value

        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board, depth)
        
        moves = Move_Ordering.order_moves(board)
        for move in moves:
            board.push(move)
            score = -self.alphaBeta(board, -beta, -alpha, depth-1)
            board.pop()

            self._updateTranspositionTableEntry(ttEntry, score, depth, alpha_prime, beta)

            if score >= beta:
                return beta # fail-soft beta-cutoff
            
            if score > bestScore:
                bestScore = score
                alpha = max(alpha, score)

        return bestScore
    
    def _updateTranspositionTableEntry(self, ttEntry, score, depth, alpha_prime, beta):
        if ttEntry is None:
            ttEntry = TransTableEntry(hash=hash)
        ttEntry.value = score
        ttEntry.depth = depth

        if score <= alpha_prime:
            ttEntry.flag = FLAG.LOWER_BOUND
        elif score >= beta:
            ttEntry.flag = FLAG.UPPER_BOUND
        else:
            ttEntry.flag = FLAG.EXACT
        
        self.tt.update_ttable(ttEntry)