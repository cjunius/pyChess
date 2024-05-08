import chess

from chess import Board, polyglot
from config import Config
import pygame
from copy import copy
from engines.transposition_table import TransTable, TransTableEntry, FLAG
import engines.move_ordering as move_ordering
import engines.quiescence_search as quiescence_search
import multiprocessing
import multiprocessing.pool

class NegamaxEngine:

    def __init__(self, config: Config = Config()):
        self.config = config
        self.tt = TransTable()
        self.move_stack = []

    def get_name(self):
        return "Negamax Engine"

    def find_move(self, board: Board):
        try:
            return polyglot.MemoryMappedReader(self.config.opening_book).weighted_choice(board).move
        except:
            best_move = chess.Move.null()
            #best_move, best_score = self.negamaxRoot(board, self.config.depth, -999999, 999999)

            for i in range(1, self.config.depth + 1):
                best_move, best_score = self.negamaxRoot(board, i, -999999, 999999)
                if board.gives_check(best_move):
                    board.push(best_move)
                    if board.is_checkmate():
                        board.pop()
                        break
                    board.pop()
            return best_move       
    
    def negamaxRoot(self, board, depth, alpha, beta):
        best_move: chess.Move = chess.Move.null()
        best_score = -999999
        
        moves = move_ordering.order_moves(board)
        for move in moves:
            board.push(move)
            score = -self.negamax(board, depth-1, -beta, -alpha)
            board.pop()

            if score > best_score:
                best_score = score
                best_move = move
                print("info bestmove {}".format(board.san(best_move)))
            alpha = max(alpha, score)
            
        return best_move, best_score


    def negamax(self, board: Board, depth: int, alpha: int, beta: int) -> int:
        
        alpha_prime = alpha

        hash = polyglot.zobrist_hash(board=board)
        ttEntry = self.tt.getEntry(hash)
        if ttEntry and ttEntry.depth >= depth:
            if ttEntry.flag == FLAG.EXACT:
                return ttEntry.value
            elif ttEntry.flag == FLAG.LOWER_BOUND:
                alpha = max(alpha, ttEntry.value)
            elif ttEntry.flag == FLAG.UPPER_BOUND:
                beta = min(beta, ttEntry.value)
            
            if alpha >= beta:
                return ttEntry.value

        if depth <= 0 or board.is_game_over():
            return quiescence_search.quiescence_search(board=board, alpha=alpha, beta=beta, depth=depth)
        
        # ToDo: Null Move pruning here

        best_score = -999999
        moves = move_ordering.order_moves(board)
        pygame.event.pump() #Prevent OS from thinking pygame has gone unresponsive
        for move in moves:
            self.move_stack.append(board.san(move))
            board.push(move)
            score = -self.negamax(board, depth-1, -beta, -alpha)
            
            hash = polyglot.zobrist_hash(board=board)
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
            board.pop()
            self.move_stack.remove(board.san(move))

            if score >= beta:
                return score
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            if alpha >= beta:
                break

        return best_score
