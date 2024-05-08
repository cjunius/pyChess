import random
from chess import Board, Move
from typing import List

PIECE_VALUES = {
        'P': 1, 'p': 1,
        'N': 2, 'n': 2, 
        'B': 3, 'b': 3,
        'R': 4, 'r': 4,
        'Q': 5, 'q': 5,
        'K': 6, 'k': 6,
        None: 0
    }

# Castling (King Safety)
# Mate
# Checks
# Captures (mvv-lva)
# Threats ??
# Non-Captures

# Typical Move Ordering from chessprogramming.org/Move_Ordering
# 1. PV-Node of the principal variation from the previous iteration
# 2. Hash move from hash tables
# 3. Winning Captures/Promotions
# 4. Equal Captures/Promotions
# 5. Killer moves (non capture), often with mate killers first
# 6. Non-captures sorted by history heuristic and that like
# 7. Losing captures

def order_moves(board: Board) -> List[Move]:

    checks = []
    captures = []
    threats = []
    promotions = []
    castling = []
    non_captures = []

    for move in board.legal_moves:
        if board.gives_check(move):
            board.push(move)
            if board.is_checkmate():
                board.pop()
                return [move] #no point in searching other moves if checkmate exists
            board.pop()
            checks.append(move)
        elif board.is_capture(move):
            captures.append(move)
        elif board.is_castling(move):
            castling.append(move)
        elif not move.promotion == None:
            promotions.append(move)
        else:
            non_captures.append(move)

    checks.sort(reverse=True, key=lambda move: _rank_checks(board, move))
    captures.sort(reverse=True, key=lambda move: _rank_captures(board, move))
    non_captures.sort(reverse=True, key=lambda move: _rank_non_captures(board, move))

    return castling + checks + captures + threats + promotions + non_captures
    

def _rank_checks(board: Board, move: Move) -> int:
    try:
        board.push(move)
        if board.is_checkmate():
            board.pop()
            return 2
        board.pop()

        return 1
    except:
        return 0


def _rank_captures(board: Board, move: Move) -> int:
    try:
        victim = board.piece_at(move.to_square).symbol()
        attacker = board.piece_at(move.from_square).symbol()
        return 10*PIECE_VALUES[victim] - PIECE_VALUES[attacker] # Most Valuable Victim - Least Valuable Attacker
    except:
        return 0
    
# ToDo: Rank by Piece Square Table value on move.to_square
def _rank_non_captures(board: Board, move: Move) -> int:
    try:
        return PIECE_VALUES[board.piece_at(move.from_square).symbol()]
    except:
        return 0
    
def order_moves_quiescence(board: Board) -> List[Move]:
    captures = []
    for move in board.legal_moves:
        if board.gives_check(move):
            captures.append(move)
        elif board.is_capture(move):
            captures.append(move)
        elif not move.promotion == None:
            captures.append(move)

    random.shuffle(captures)
    return captures