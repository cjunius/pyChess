from abc import abstractmethod
import chess
import chess.polyglot
import time
import sys

class Engine():
    def __init__(self, depth=3, opening_book="bots/books/bookfish.bin"):
        self.depth = depth
        self.evaluations = 0
        self.total_moves = 0
        self.opening_book = opening_book
        self.prev_evals = {}

    @abstractmethod
    def getName(self):
        pass
        
    @abstractmethod
    def evaluate_board(self, board: chess.Board):
        pass

    def findMove(self, board: chess.Board):
        output = "White " if board.ply() % 2 == 0 else "Black "
        try:
            with chess.polyglot.open_reader(self.opening_book) as reader:
                move = reader.weighted_choice(board).move
                output += "Book move: " + str(board.san(move))
                print(output)
                return move
        except:
            bestMove = chess.Move.null()
            bestValue = -sys.maxsize

            startTime = time.time()

            legal_moves = self._order_moves(board)
            self.total_moves += len(legal_moves)
            for move in legal_moves:

                board.push(move)
                boardValue = -self.negamax(self.depth - 1, board)
                
                if boardValue > bestValue:
                    bestValue = boardValue
                    bestMove = move
                
                board.pop()

            endTime = time.time()
            diff = endTime - startTime
            
            output += "{:2}. {:7} Eval: {:6}  ".format(board.fullmove_number, board.san(bestMove), bestValue)
            output += "Depth: {:2}  ".format(self.depth)
            output += "Nodes: {:8}  ".format(self.total_moves)
            output += "Evals: {:7}  ".format(self.evaluations)
            output += "Prune: {:.2%}  ".format((self.evaluations/self.total_moves))
            output += "Time: {:>6}  ".format("{:.2f}".format(diff))
            nps = self.evaluations/diff if diff>0 else 0.00
            output += "Evals/s: {:5.2f}  ".format(nps)
            output += "FEN: " + str(board.fen())
            print(output)
            
            self.evaluations = 0
            self.total_moves = 0
            return bestMove
        
    def negamax(self, depth, board):
        if depth == 0 or board.is_game_over():
            return self.quiesce(-sys.maxsize, sys.maxsize, board)
        
        best_score = -sys.maxsize
        legal_moves = self._order_moves(board)
        self.total_moves += len(legal_moves)
        for move in legal_moves:
            board.push(move)
            score = -self.negamax(depth - 1, board)
            best_score = max(score, best_score)
            board.pop()
        return best_score

    # Quiescence Search
    # https://www.chessprogramming.org/Quiescence_Search
    def quiesce(self, alpha, beta, board):
        self.evaluations += 1
        stand_pat = self.evaluate_board(board)
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        legal_moves = list(board.legal_moves)
        legal_moves.sort(reverse=True, key=lambda move: board.is_capture(move))
        for move in legal_moves:
            self.total_moves += 1
            if not board.is_capture(move): break
            board.push(move)
            score = -self.quiesce(-beta, -alpha, board)
            board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        return alpha

    def _order_moves(self, board):
        legal_moves = list(board.legal_moves)
        legal_moves.sort(reverse=True, key=lambda move: (
            board.gives_check(move), 
            board.is_castling(move),
            self._rank_captures(board, move),
        ))
        return legal_moves
    
    def _rank_captures(self, board, move):
        PIECE_VALUES = {
            'P': 100, 'p': 100,
            'N': 280, 'n': 280, 
            'B': 320, 'b': 320,
            'R': 379, 'r': 379,
            'Q': 929, 'q': 929,
            'K': 20000, 'k': 20000,
            None: 0
        }
        if board.is_capture(move): 
            return 1 + PIECE_VALUES[move.drop] - PIECE_VALUES[board.piece_at(move.from_square).symbol()]
        else: 
            return 0