import chess
import chess.polyglot
import time

depth = 4

pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    78, 83, 86, 73, 102, 82, 85, 90,
    7, 29, 21, 44, 40, -31, 44, 7,
    -17, 16, -2, 15, 14, 0, 15, -13,
    -26, 3, 10, 9, 6, 1, 0, -23,
    -22, 9, 5, -11, -10, -2, 3, -19,
    -31, 8, -7, -37, -36, -14, 3, -31,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -66, -53, -75, -75, -10, -55, -58, -70,
    -3,  -6, 100, -36,   4,  62,  -4, -14,
    10,  67,   1,  74,  73,  27,  62,  -2,
    24,  24,  45,  37,  33,  41,  25,  17,
    -1,   5,  31,  21,  22,  35,   2,   0,
    -18,  10,  13,  22,  18,  15,  11, -14,
    -23, -15,   2,   0,   2,   0, -23, -20,
    -74, -23, -26, -24, -19, -35, -22, -69]

bishopstable = [
    -59, -78, -82, -76, -23,-107, -37, -50,
    -11,  20,  35, -42, -39,  31,   2, -22,
    -9,  39, -32,  41,  52, -10,  28, -14,
    25,  17,  20,  34,  26,  25,  15,  10,
    13,  10,  17,  23,  17,  16,   0,   7,
    14,  25,  24,  15,   8,  25,  20,  15,
    19,  20,  11,   6,   7,   6,  20,  16,
    -7,   2, -15, -12, -14, -15, -10, -10]

rookstable = [
    35,  29,  33,   4,  37,  33,  56,  50,
    55,  29,  56,  67,  55,  62,  34,  60,
    19,  35,  28,  33,  45,  27,  25,  15,
     0,   5,  16,  13,  18,  -4,  -9,  -6,
    -28, -35, -16, -21, -13, -29, -46, -30,
    -42, -28, -42, -25, -25, -35, -26, -46,
    -53, -38, -31, -26, -29, -43, -44, -53,
    -30, -24, -18,   5,  -2, -18, -31, -32]

queenstable = [
    6,   1,  -8,-104,  69,  24,  88,  26,
    14,  32,  60, -10,  20,  76,  57,  24,
    -2,  43,  32,  60,  72,  63,  43,   2,
    1, -16,  22,  17,  25,  20, -13,  -6,
    -14, -15,  -2,  -5,  -1, -10, -20, -22,
    -30,  -6, -13, -11, -16, -11, -16, -27,
    -36, -18,   0, -19, -15, -15, -21, -38,
    -39, -30, -31, -13, -31, -36, -34, -42]

kingstable = [
    4,  54,  47, -99, -99,  60,  83, -62,
    -32,  10,  55,  56,  56,  55,  10,   3,
    -62,  12, -57,  44, -67,  28,  37, -31,
    -55,  50,  11,  -4, -19,  13,   0, -49,
    -55, -43, -52, -28, -51, -47,  -8, -50,
    -47, -42, -43, -79, -64, -32, -29, -32,
    -4,   3, -14, -50, -57, -18,  13,   4,
    17,  30,  -3, -14,   6,  -1,  40,  18]

def getName():
    return "CJ Bot v0.3 - Depth 3"

def findMove(board: chess.Board):
    try:
        with chess.polyglot.open_reader("bots/books/bookfish.bin") as reader:
            move = reader.weighted_choice(board).move
            print("Book move: " + str(board.san(move)))
            return move
    except Exception as e:
        startTime = time.time()
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000

        legal_moves = list(board.legal_moves)
        legal_moves.sort(key=lambda x: (board.is_capture(x), board.gives_check(x) ) )

        for move in legal_moves:
            board.push(move)
            boardValue = -alphabeta(-beta, -alpha, depth - 1, board)
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            if boardValue > alpha:
                alpha = boardValue
            board.pop()
        endTime = time.time()
        diff = endTime - startTime
        print("Move: " + str(board.san(bestMove)) + "\tEvaluation: " + str(bestValue) + "\tTime: " + str(diff))
        return bestMove

def alphabeta(alpha, beta, depthleft, board):
    bestscore = -9999
    if (depthleft == 0):
        return quiesce(alpha, beta, board)
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(-beta, -alpha, depthleft - 1, board)
        board.pop()
        if (score >= beta):
            return score
        if (score > bestscore):
            bestscore = score
        if (score > alpha):
            alpha = score
    return bestscore

def quiesce(alpha, beta, board):
    stand_pat = evaluate_board(board)
    if (stand_pat >= beta):
        return beta
    if (alpha < stand_pat):
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce(-beta, -alpha, board)
            board.pop()

            if (score >= beta):
                return beta
            if (score > alpha):
                alpha = score
    return alpha

def evaluate_board(board):
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    material = 100 * (wp - bp) + 280 * (wn - bn) + 320 * (wb - bb) + 479 * (wr - br) + 929 * (wq - bq)

    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)]
                           for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
                           for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
                             for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
                           for i in board.pieces(chess.KING, chess.BLACK)])

    eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    if board.turn:
        return eval
    else:
        return -eval

