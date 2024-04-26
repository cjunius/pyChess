from abc import abstractmethod
import chess
import chess.polyglot
import time
import sys

from move_ordering import Move_Ordering

class Engine():
    def __init__(self, depth=3, opening_book="bots/books/bookfish.bin", debug=False):
        self.depth = depth
        self.evaluations = 0
        self.opening_book = opening_book
        self.myTurn = chess.WHITE
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
                boardValue = -self.negamaxab(board, self.depth - 1, alpha, beta)
                board.pop()
                
                if boardValue > bestValue:
                    bestValue = boardValue
                    bestMove = move

                alpha = max(alpha, boardValue)

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
        
    def negamaxab(self, board, depth, alpha, beta):

        if depth == 0 or board.is_game_over():
            self.evaluations += 1
            return -self.quiesce(board, alpha, beta)
        
        best_score = -sys.maxsize

        legal_moves = Move_Ordering.order_moves(board)
        for move in legal_moves:

            board.push(move)
            best_score = max(best_score, -self.negamaxab(board, depth-1, -beta, -alpha))
            board.pop()

            if best_score >= beta:
                return best_score #fail-soft beta-cutoff

            alpha = max(alpha, best_score)

        return best_score

    # Quiescence Search
    # https://www.chessprogramming.org/Quiescence_Search
    def quiesce(self, board, alpha, beta):
        self.evaluations += 1
        stand_pat = -self.evaluate_board(board, self.myTurn)
        if stand_pat >= beta:
            return beta
        alpha = max(alpha, stand_pat)

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