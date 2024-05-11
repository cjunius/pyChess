import random
from typing import List
from chess import Board, Move
import engines.evaluation as evaluation
import engines.move_ordering as move_ordering

# Quiescence Search
# https://www.chessprogramming.org/Quiescence_Search
def quiescence_search(board: Board, alpha: int, beta: int, depth: int) -> int:
    if board.is_game_over():
        if board.is_checkmate():
            return -9999 - depth
        if board.is_stalemate():
            return 0
        if board.is_insufficient_material():
            return 0
        if board.is_fivefold_repetition():
            return 0
        if board.is_seventyfive_moves():
            return 0
        
    if board.is_repetition():
        return 0

    stand_pat = evaluation.evaluate_board(board)
    if stand_pat >= beta:
        return beta
    alpha = max(alpha, stand_pat)

    def order_moves_quiescence() -> List[Move]:
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

    moves = order_moves_quiescence(board)
    for move in moves:

        #ToDo: Delta Pruning

        board.push(move)
        score = -quiescence_search(-beta, -alpha, depth-1)
        board.pop()
        
        if score >= beta:
            return beta
        alpha = max(alpha, score)

    return alpha