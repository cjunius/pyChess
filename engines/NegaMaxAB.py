from abc import abstractmethod
import chess
import chess.polyglot
import time
import sys

class Engine():
    def __init__(self, depth=3, opening_book="bots/books/bookfish.bin"):
        self.depth = depth
        self.evaluations = 0
        self.nodes = 0
        self.opening_book = opening_book
        self.prev_evals = {}

    @abstractmethod
    def getName(self):
        pass
        
    @abstractmethod
    def evaluate_board(self, board: chess.Board):
        pass

    def node_count(self, board, depth):
                nodes = len(list(board.legal_moves))
                if depth == 0:
                    return nodes
                for move in board.legal_moves:
                    board.push(move)
                    nodes += self.node_count(board, depth-1)
                    board.pop()
                return nodes

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
            alpha = -sys.maxsize
            beta = sys.maxsize

            self.nodes = self.node_count(board, self.depth)

            startTime = time.time()
            legal_moves = self._order_moves(board)
            for move in legal_moves:

                board.push(move)
                boardValue = -self.negamaxab(-beta, -alpha, self.depth - 1, board)
                board.pop()
                
                if boardValue > bestValue:
                    bestValue = boardValue
                    bestMove = move

                if boardValue > alpha:
                    alpha = boardValue

            endTime = time.time()
            diff = endTime - startTime
            
            output += "{:2}. {:7} Eval: {:6}  ".format(board.fullmove_number, board.san(bestMove), bestValue)
            output += "Depth: {:2}  ".format(self.depth)
            output += "Nodes: {:8}  ".format(self.nodes)
            output += "Evals: {:7}  ".format(self.evaluations)
            output += "Prune: {:.2%}  ".format((self.evaluations/self.nodes))
            output += "Time: {:>6}  ".format("{:.2f}".format(diff))
            nps = self.evaluations/diff if diff>0 else 0.00
            output += "Evals/s: {:5.2f}  ".format(nps)
            output += "FEN: " + str(board.fen())
            print(output)
            
            self.evaluations = 0
            self.total_moves = 0
            return bestMove
        
    def negamaxab(self, alpha, beta, depth, board):

        if depth == 0 or board.is_game_over():
            return self.quiesce(alpha, beta, board)
        
        best_score = -sys.maxsize

        legal_moves = self._order_moves(board)
        for move in legal_moves:
            board.push(move)
            score = -self.negamaxab(-beta, -alpha, depth - 1, board)
            board.pop()

            if score >= beta:
                return score #fail-soft beta-cutoff

            if score > best_score:
                best_score = score

                if score > alpha:
                    alpha = score

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