import chess
from chess import Board

PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KING_TABLE = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
]

PIECE_VALUE_SQUARE_TABLES = [
    (chess.PAWN,    100, PAWN_TABLE),
    (chess.KNIGHT,  350, KNIGHT_TABLE),
    (chess.BISHOP,  350, BISHOP_TABLE),
    (chess.ROOK,    525, ROOK_TABLE),
    (chess.QUEEN,   1000, QUEEN_TABLE),
    (chess.KING,    2000, KING_TABLE)
]

# ToDo:
# - Material Evaluation - COMPLETE
#   - Double, Isolated, and Backward Pawns
#   - Bishop Pair
#   - Open and Semi-Open Rooks
#   - King Safety
# - Piece Square Table Evaluation - COMPLETE
#   - Tapered evaluation between middlegame and endgame - PeSTO
# - Tempo evaluation  - COMPLETE

def evaluate_board(board: Board) -> int:
    eval = -50 if board.is_check() else 0
    #eval += evaluate_material_balance(board)
    eval += evaluate_piece_square_table(board)
    eval += 5*evaluate_mobility(board)
    return eval


def evaluate_material_balance(board: Board) -> int:
    eval = 0
    for piece, value, _ in PIECE_VALUE_SQUARE_TABLES:
        if piece == chess.KING: continue # Kings cancel each other
        eval += value * (len(board.pieces(piece, board.turn)) - len(board.pieces(piece, not board.turn)))
    return eval


def evaluate_piece_square_table(board: Board) -> int:
    eval = 0
    for piece, value, pst in PIECE_VALUE_SQUARE_TABLES:
        eval += sum([pst[i]+value for i in board.pieces(piece, chess.WHITE)])
        eval -= sum([pst[chess.square_mirror(i)]+value for i in board.pieces(piece, chess.BLACK)])
    return eval if board.turn else -eval

def board_control(board: Board) -> int:
    eval = 0
    for square in chess.SquareSet(board.occupied_co[board.turn]):
        eval += len(board.attacks(square))

    for square in chess.SquareSet(board.occupied_co[not board.turn]):
        eval -= len(board.attacks(square))

    return eval
    
def evaluate_mobility(board: Board) -> int:
        if len(list(board.move_stack)) == 0:
            return 0

        last_move = board.pop()
        countA = len(list(board.legal_moves))
        board.push(last_move)
        countB = len(list(board.legal_moves))
        return countA - countB

def evaluate_pawn_structure(board: Board) -> int:
    # D, S, I = doubled, blocked and isolated pawns
    # return -0.5(D-D' + S-S' + I-I')
    eval = 0
    return eval
    
