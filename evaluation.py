import chess

mg_pawn_table = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

eg_pawn_table = [
      0,   0,   0,   0,   0,   0,   0,   0,
    178, 173, 158, 134, 147, 132, 165, 187,
     94, 100,  85,  67,  56,  53,  82,  84,
     32,  24,  13,   5,  -2,   4,  17,  17,
     13,   9,  -3,  -7,  -7,  -8,   3,  -1,
      4,   7,  -6,   1,   0,  -5,  -1,  -8,
     13,   8,   8,  10,  13,   0,   2,  -7,
      0,   0,   0,   0,   0,   0,   0,   0
]

mg_knight_table = [
    -55, -40, -30, -30, -30, -30, -40, -55,
    -40, -20, 0, 10, 10, 0, -20, -40,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 0, 20, 30, 30, 20, 0, -30,
    -30, 0, 20, 30, 30, 20, 0, -30,
    -30, 0, 10, 20, 20, 15, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -55, -40, -30, -30, -30, -30, -40, -55]

eg_knight_table = [
    -58, -38, -13, -28, -31, -27, -63, -99,
    -25,  -8, -25,  -2,  -9, -25, -24, -52,
    -24, -20,  10,   9,  -1,  -9, -19, -41,
    -17,   3,  22,  22,  22,  11,   8, -18,
    -18,  -6,  16,  25,  16,  17,   4, -18,
    -23,  -3,  -1,  15,  10,  -3, -20, -22,
    -42, -20, -10,  -5,  -2, -20, -23, -44,
    -29, -51, -23, -15, -22, -18, -50, -64
]

mg_bishop_table = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

eg_bishop_table = [
    -14, -21, -11,  -8, -7,  -9, -17, -24,
     -8,  -4,   7, -12, -3, -13,  -4, -14,
      2,  -8,   0,  -1, -2,   6,   0,   4,
     -3,   9,  12,   9, 14,  10,   3,   2,
     -6,   3,  13,  19,  7,  10,  -3,  -9,
    -12,  -3,   8,  10, 13,   3,  -7, -15,
    -14, -18,  -7,  -1,  4,  -9, -15, -27,
    -23,  -9, -23,  -5, -9, -16,  -5, -17
]

mg_rook_table = [
    0, 0, 0, 10, 10, 0, 0, 0,
    -5, 5, 10, 10, 10, 10, 5, -5,
    -5, 0, 5, 15, 15, 5, 0, -5,
    -5, 0, 5, 10, 10, 5, 0, -5,
    -5, 0, 5, 10, 10, 5, 0, -5,
    -5, 0, 5, 15, 15, 5, 0, -5,
    0, 10, 15, 15, 15, 15, 10, 0,
    0, 0, 0, 10, 10, 0, 0, 0]

eg_rook_table = [
    13, 10, 18, 15, 12,  12,   8,   5,
    11, 13, 13, 11, -3,   3,   8,   3,
     7,  7,  7,  5,  4,  -3,  -5,  -3,
     4,  3, 13,  1,  2,   1,  -1,   2,
     3,  5,  8,  4, -5,  -6,  -8, -11,
    -4,  0, -5, -1, -7, -12,  -8, -16,
    -6, -6,  0,  2, -9,  -9, -11,  -3,
    -9,  2,  3, -1, -5, -13,   4, -20
]

mg_queen_table = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

eg_queen_table = [
     -9,  22,  22,  27,  27,  19,  10,  20,
    -17,  20,  32,  41,  58,  25,  30,   0,
    -20,   6,   9,  49,  47,  35,  19,   9,
      3,  22,  24,  45,  57,  40,  57,  36,
    -18,  28,  19,  47,  31,  34,  39,  23,
    -16, -27,  15,   6,   9,  17,  10,   5,
    -22, -23, -30, -16, -16, -23, -36, -32,
    -33, -28, -22, -43,  -5, -32, -20, -41
]

mg_king_table = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]

eg_king_table = [
    -74, -35, -18, -18, -11,  15,   4, -17,
    -12,  17,  14,  17,  17,  38,  23,  11,
     10,  17,  23,  15,  20,  45,  44,  13,
     -8,  22,  24,  27,  26,  33,  26,   3,
    -18,  -4,  21,  24,  27,  23,   9, -11,
    -19,  -3,  11,  21,  23,  16,   7,  -9,
    -27, -11,   4,  13,  14,   4,  -5, -17,
    -53, -34, -21, -11, -28, -14, -24, -43
]

MG_PST = [
    (chess.PAWN, mg_pawn_table),
    (chess.KNIGHT, mg_knight_table),
    (chess.BISHOP, mg_bishop_table),
    (chess.ROOK, mg_rook_table),
    (chess.QUEEN, mg_queen_table),
    (chess.KING, mg_king_table)
]

class Evaluation:

    @staticmethod
    def game_over(board: chess.Board, depth_remaining: int) -> int:

        if board.is_checkmate():
            eval = 9999 + depth_remaining
            return -eval if board.turn else eval
        if board.is_stalemate():
            return 0
        if board.is_insufficient_material():
            return 0
        if board.is_fivefold_repetition():
            return 0
        if board.is_seventyfive_moves():
            return 0

    @staticmethod
    def material_balance(board) -> int:
        white = board.occupied_co[chess.WHITE]
        black = board.occupied_co[chess.BLACK]
        eval = ( 
            100 * (chess.popcount(white & board.pawns) - chess.popcount(black & board.pawns)) +
            300 * (chess.popcount(white & board.knights) - chess.popcount(black & board.knights)) +
            330 * (chess.popcount(white & board.bishops) - chess.popcount(black & board.bishops)) +
            550 * (chess.popcount(white & board.rooks) - chess.popcount(black & board.rooks)) +
            1000 * (chess.popcount(white & board.queens) - chess.popcount(black & board.queens))
        )
        return -eval if board.turn else eval
    
    @staticmethod
    def piece_square_table(board) -> int:
        eval = 0
        for piece, heatmap in MG_PST:
            eval += sum([heatmap[i] for i in board.pieces(piece, chess.WHITE)])*10
            eval += sum([-heatmap[chess.square_mirror(i)] for i in board.pieces(piece, chess.BLACK)])*10
        return -eval if board.turn else eval

    @staticmethod
    def board_control(board) -> int:
        eval = 0
        for square in chess.SquareSet(board.occupied_co[chess.WHITE]):
            eval += len(board.attacks(square))*10

        for square in chess.SquareSet(board.occupied_co[chess.BLACK]):
            eval -= len(board.attacks(square))*10

        return -eval if board.turn else eval
    
    @staticmethod
    def mobility(board) -> int:
        countA = len(list(board.legal_moves))
        board.turn = not board.turn
        countB = len(list(board.legal_moves))
        board.turn = not board.turn
        eval = countA - countB
        return eval
    
    @staticmethod
    def pawns(board) -> int:
        # D, S, I = doubled, blocked and isolated pawns
        # return -0.5(D-D' + S-S' + I-I')
        eval = 0
        return -eval if board.turn else eval
    
# ToDo:
# - Material Evaluation - COMPLETE
# - Piece Square Table Evaluation - Simplified - Expand usage to include to Midgame and endgame PST
# - Double, Isolated, Backwards, and Passed Pawn evaluation
# - Open and semi-open files for rooks and kings evaluation
# - Bishop pair evaluation
# - Tempo evaluation
# - Tampered evaluation between middlegame and endgame
