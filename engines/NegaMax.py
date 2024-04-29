import chess
import chess.polyglot
import time
import sys

from abc import abstractmethod
from move_ordering import Move_Ordering
from engines.Transposition_Table import TransTable, TransTableEntry, FLAG

class Engine():
    def __init__(self, 
        depth=3, 
        opening_book="bots/books/bookfish.bin", 
        debug=False, 
        useAlphaBetaPruning=True,
        useTranspositionTable=True
    ):
        self.depth = depth
        self.evaluations = 0
        self.opening_book = opening_book
        self.debug = debug
        self.useAlphaBetaPruning = useAlphaBetaPruning
        self.useTranspositionTable = useTranspositionTable
        if useTranspositionTable:
            self.useAlphaBetaPruning = True
            self.tt = TransTable()
        self.color = chess.WHITE

        print("Initializing Bot: " + self.getName())
        print("Features:")
        print(" - Using Depth: " + str(self.depth))
        print(" - Using Alpha Beta Pruning: " + str(self.useAlphaBetaPruning))
        print(" - Using Transposition Table: " + str(self.useTranspositionTable))
        print(" - Using Opening Book: " + str(self.opening_book))
        print(" - Output Debug info: " + str(self.debug))
        print("")

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
                if self.debug:
                    output += "Book move: " + str(board.san(move))
                    print(output)
                return move
        except:
            bestMove = chess.Move.null()
            bestValue = -sys.maxsize+500
            alpha = -sys.maxsize+500
            beta = sys.maxsize-500

            startTime = time.time()

            legal_moves = Move_Ordering.order_moves(board)
            for move in legal_moves:

                board.push(move)
                boardValue = -self.negamax(board, self.depth - 1, alpha, beta)
                board.pop()

                if boardValue > bestValue:
                    bestValue = boardValue
                    bestMove = move

                if self.useAlphaBetaPruning:
                    alpha = max(alpha, boardValue)

            endTime = time.time()
            diff = endTime - startTime
            
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
            self.total_moves = 0
            return bestMove
        
    # Negamax Search
    # https://en.wikipedia.org/wiki/Negamax
    def negamax(self, board: chess.Board, depth: int, alpha: int, beta: int):

        if self.useTranspositionTable:
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
            #return self.evaluate_board(board, depth)
            return self.quiesce(board, alpha, beta, depth)
        
        value = -sys.maxsize
        legal_moves = Move_Ordering.order_moves(board)
        for move in legal_moves:
            board.push(move)
            value = max(value, -self.negamax(board, depth - 1, -beta, -alpha))
            board.pop()

            if self.useAlphaBetaPruning:

                alpha = max(alpha, value)

                if alpha >= beta:
                    break
                
                if self.useTranspositionTable:
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

    # Quiescence Search
    # https://www.chessprogramming.org/Quiescence_Search
    def quiesce(self, board: chess.Board, alpha: int, beta: int, depth: int):
        self.evaluations += 1
        stand_pat = self.evaluate_board(board, depth)
        if stand_pat >= beta:
            return beta
        alpha = max(alpha, stand_pat)

        if board.is_checkmate():
            return stand_pat

        legal_moves = list(board.legal_moves)
        legal_moves.sort(reverse=True, key=lambda move: (board.is_irreversible(move)))
        for move in legal_moves: 
            board.push(move)
            if not board.is_irreversible(move): 
                board.pop()
                break
            score = -self.quiesce(board, -beta, -alpha, depth-1)
            board.pop()

            if score >= beta:
                return beta
            alpha = max(alpha, score)
        return alpha