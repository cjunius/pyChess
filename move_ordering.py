import chess

class Move_Ordering:

    @staticmethod   
    def order_moves(board: chess.Board):
        legal_moves = list(board.legal_moves)
        legal_moves.sort(reverse=True, key=lambda move: (
            Move_Ordering._rank_checks(board, move), 
            Move_Ordering._rank_captures(board, move),
            board.is_castling(move),
            
        ))
        return legal_moves
    
    @staticmethod
    def _rank_checks(board: chess.Board, move: chess.Move):
        if board.gives_check(move):
            value = 1
            board.push(move)
            if board.is_checkmate():
                value = 2
            board.pop()
            return value
        else:
            return 0

    @staticmethod
    def _rank_captures(board: chess.Board, move: chess.Move):
        PIECE_VALUES = {
            'P': 1, 'p': 1,
            'N': 2, 'n': 2, 
            'B': 3, 'b': 3,
            'R': 4, 'r': 4,
            'Q': 5, 'q': 5,
            'K': 6, 'k': 6,
            None: 0
        }
        if board.is_capture(move): 
            return 64*PIECE_VALUES[move.drop] - PIECE_VALUES[board.piece_at(move.from_square).symbol()]
        else: 
            return 0