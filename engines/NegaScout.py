from abc import abstractmethod
import chess
import chess.polyglot
import time
import sys

from move_ordering import Move_Ordering

# Todo: Figure out why it fails Mate in 2 and Mate in 3 tests

class Engine():
    def __init__(self, depth=3, opening_book="bots/books/bookfish.bin", debug=False):
        self.depth = depth
        self.opening_book = opening_book
        self.myTurn = chess.WHITE
        self.evaluations = 0 
        self.debug = debug

    @abstractmethod
    def getName(self):
        pass
        
    @abstractmethod
    def evaluate_board(self, board: chess.Board):
        pass

    def findMove(self, board: chess.Board):
        self.myTurn = board.turn
        output = "White " if board.turn else "Black "
        try:
            with chess.polyglot.open_reader(self.opening_book) as reader:
                move = reader.weighted_choice(board).move
                output += "Book move: " + str(board.san(move))
                print(output)
                return move
        except:
            bestMove = chess.Move.null()
            bestValue = -10000
            alpha = -99999
            beta = 99999

            startTime = time.time()
            legal_moves = Move_Ordering.order_moves(board)
            for move in legal_moves:
                
                board.push(move)
                if board.is_checkmate(): 
                    board.pop()
                    bestMove = move
                    bestValue = 99999
                    break # No sense in searching if move is checkmate
                boardValue = -self.negascout(board, self.depth - 1, alpha, beta)
                board.pop()

                if boardValue > bestValue:
                    bestValue = boardValue
                    bestMove = move

                alpha = max(boardValue, alpha)

            endTime = time.time()
            diff = round(endTime - startTime, 3)
            
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
        
    def negascout(self, board, depth, alpha, beta):
        
        if depth == 0 or board.is_game_over():
            return -self.quiesce(board, alpha, beta)

        legal_moves = Move_Ordering.order_moves(board)
        for move in legal_moves:
            board.push(move)
            if move == legal_moves[0]:
                score = -self.negascout(board, depth-1, -beta, -alpha)
            else:
                score = -self.negascout(board, depth-1, -alpha - 1, -alpha) #null window search
                if alpha < score < beta:
                    score = -self.negascout(board, depth-1, -beta, -alpha) #if fail, do a full re-search
                    
            board.pop()

            alpha = max(alpha, score)

            if alpha >= beta:
                break # beta-cutoff

        return alpha

    # Quiescence Search
    # https://www.chessprogramming.org/Quiescence_Search
    def quiesce(self, board, alpha, beta):
        self.evaluations += 1
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