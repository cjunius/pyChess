from abc import abstractmethod
import chess
import chess.polyglot
import time
import sys

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

    @abstractmethod
    def getName(self):
        pass
        
    @abstractmethod
    def evaluate_board(self, board: chess.Board):
        pass

    def findMove(self, board: chess.Board):
        self.color = board.turn
        output = "White " if board.turn else "Black "
        try:
            with chess.polyglot.open_reader(self.opening_book) as reader:
                move = reader.weighted_choice(board).move
                output += "Book move: " + str(board.san(move))
                print(output)
                return move
        except:
            bestMove = chess.Move.null()
            bestValue = -sys.maxsize
            alpha = -sys.maxsize+500
            beta = sys.maxsize-500

            startTime = time.time()
            legal_moves = Move_Ordering.order_moves(board)
            for move in legal_moves:
                
                self.san_move_stack.append(board.san(move))
                board.push(move)
                value = self.negascout(board, self.depth - 1, alpha, beta)
                board.pop()
                self.san_move_stack.pop()

                if value > bestValue:
                    bestValue = value
                    bestMove = move

                alpha = max(value, alpha)
                if alpha >= beta:
                    break

                print("Evaluated move {}  Score:  {}  Alpha: {}  Beta: {}  - CurBestScore: {}  CurBestMove:  {}".format(board.san(move), value, alpha, beta, bestValue, board.san(bestMove)))

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
        
    #https://www.chessprogramming.org/NegaScout
    def negascout(self, board, depth, alpha, beta):
        
        if depth == 0 or board.is_game_over():                              # leaf node
            eval = self.evaluate_board(board, depth, self.color) #self.quiesce(board, alpha, beta, depth) 
            return eval

        legal_moves = Move_Ordering.order_moves(board)
        firstMove = legal_moves[0]
        for move in legal_moves:

            beta_prime = beta

            self.san_move_stack.append(board.san(move))
            board.push(move)
            score = self.negascout(board, depth-1, -beta_prime, -alpha)    # null window search
            if alpha < score < beta and not move == firstMove:
                score = self.negascout(board, depth-1, -beta, -alpha)      # null window search failed, so re-search

            if self.san_move_stack[0] == "Qd2+" or self.san_move_stack[0] == "Qd1+":
                print("Evaluated " + str(self.san_move_stack) + ": " + str(score) + "  Alpha: " + str(alpha) + "  Beta: " + str(beta))

            self.san_move_stack.pop()
            board.pop()
            alpha = max(alpha, score)

            if alpha >= beta:
                return alpha                                                # beta-cutoff

            beta_prime = alpha + 1                                          # set new null window

        return alpha

    # Quiescence Search
    # https://www.chessprogramming.org/Quiescence_Search
    def quiesce(self, board, alpha, beta, depth):
        self.evaluations += 1
        stand_pat = self.evaluate_board(board, depth, self.color)
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        for move in board.legal_moves: 
            if not board.is_capture(move):
                continue

            board.push(move)
            score = self.quiesce(board, -beta, -alpha, depth-1)
            board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        return alpha