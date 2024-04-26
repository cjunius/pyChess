from abc import abstractmethod
import chess
import chess.polyglot
import sys
import time

from abc import abstractmethod

from move_ordering import Move_Ordering
from engines.Transposition_Table import TransTable, TransTableEntry, FLAG

class Engine():
    def __init__(self, depth=3, opening_book="bots/books/bookfish.bin", debug=False):
        self.depth = depth
        self.evaluations = 0
        self.opening_book = opening_book
        self.myTurn = chess.WHITE
        self.tt = TransTable()
        self.debug = debug

    @abstractmethod
    def getName(self):
        pass
        
    @abstractmethod
    def evaluate_board(self, board: chess.Board):
        pass

    def findMove(self, board: chess.Board):
        self.myTurn = board.turn
        output = "White " if board.turn == 0 else "Black "
        try:
            with chess.polyglot.open_reader(self.opening_book) as reader:
                move = reader.weighted_choice(board).move
                output += "Book move: " + str(board.san(move))
                print(output)
                return move
        except:
            bestMove = chess.Move.null()
            bestValue = -sys.maxsize
            alpha = -sys.maxsize
            beta = sys.maxsize

            startTime = time.time()
            legal_moves = Move_Ordering.order_moves(board)
            for move in legal_moves:

                board.push(move)
                if board.is_checkmate(): 
                    board.pop()
                    bestMove = move
                    bestValue = sys.maxsize
                    break # No sense in searching if move is checkmate
                boardValue = -self.negamax_abtt(board, self.depth - 1, alpha, beta)
                board.pop()
                
                if boardValue > bestValue:
                    bestValue = boardValue
                    bestMove = move

                alpha = max(alpha, boardValue)

            endTime = time.time()
            diff = round(endTime - startTime, 2)

            if self.debug: 
                output += "{:2}. {:7} Eval: {:6}  ".format(board.fullmove_number, board.san(bestMove), bestValue)
                output += "Depth: {:2}  ".format(self.depth)
                output += "Evals: {:7}  ".format(self.evaluations)
                output += "Time: {:7.3f}  ".format(diff)
                eps = round(self.evaluations/diff, 2) if diff>0 else 0.00
                output += "Evals/s: {:8.2f}  ".format(eps)
                output += "FEN: " + str(board.fen())
                print(output)

            self.evaluations = 0

            return bestMove
        
    # https://en.wikipedia.org/wiki/Negamax
    def negamax_abtt(self, board, depth, alpha, beta):
        alpha_prime = alpha

        hash = chess.polyglot.zobrist_hash(board=board)
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
        
        if depth == 0 or board.is_game_over():
            return -self.quiesce(board, alpha, beta)
            
        value = -sys.maxsize
        legal_moves = Move_Ordering.order_moves(board)
        for move in legal_moves:
            board.push(move)
            value = max(value, -self.negamax_abtt(board, depth-1, -beta, -alpha))
            alpha = max(alpha, value)
            board.pop()

            if alpha >= beta:
                #break
                return alpha # fail-soft beta-cutoff

        if ttEntry is None:
            ttEntry = TransTableEntry(hash)
        ttEntry.value = value
        ttEntry.depth = depth

        if value <= alpha_prime:
            ttEntry.flag = FLAG.LOWER_BOUND
        elif value >= beta:
            ttEntry.flag = FLAG.UPPER_BOUND
        else:
            ttEntry.flag = FLAG.EXACT
        
        self.tt.update_ttable(ttEntry)
        
        return value

    # https://www.chessprogramming.org/Quiescence_Search
    def quiesce(self, board, alpha, beta):
        1
        stand_pat = -self.evaluate_board(board, self.myTurn)
        if stand_pat >= beta:
            return beta
        alpha = max(alpha, stand_pat)

        if board.is_game_over():
            return stand_pat

        legal_moves = list(board.legal_moves)
        legal_moves.sort(reverse=True, key=lambda move: board.is_capture(move))
        for move in legal_moves:
            if not board.is_capture(move): break
            board.push(move)
            score = -self.quiesce(board, -beta, -alpha)
            board.pop()

            if score >= beta:
                return beta
            alpha = max(alpha, score)
        return alpha