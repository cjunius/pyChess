import chess
import chess.polyglot
import time

pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]

evaluations = 0

def getName():
    return "CJ Bot"

def findMove(board: chess.Board):
    if board.ply() % 2 == 0:
        output = "White "
    else:
        output = "Black "
    
    try:
        with chess.polyglot.open_reader("bots/books/bookfish.bin") as reader:
            move = reader.weighted_choice(board).move
            output += "Book move: " + str(board.san(move))
            print(output)
            return move
    except:
            
        global evaluations
        evaluations = 0

        startTime = time.time()
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000

        numPieces = len(board.piece_map())

        depth = 3 #+ (16-wp-bp)//16 + (8-wn-bn-wb-bb)//8 + (4-wr-br)//4 + (2-wq-bq)//2

        num_legal_moves = 0
        for move in board.legal_moves:
            num_legal_moves += 1
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
        
        output += "{:2}. {:7} Eval: {:5} ".format(board.fullmove_number, board.san(bestMove), bestValue)
        output += "\tMoves: {}".format(num_legal_moves)
        output += "\tPieces: {}".format(numPieces)
        output += "\tDepth: {}".format(depth)
        output += "\tEvals: {:8}".format(evaluations)
        output += "\tTime: {:6.4f}s".format(diff)
        output += "\tEvals/Time: {:6.4f}".format(evaluations/diff)
        print(output)
        
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

def evaluate_board(board: chess.Board):

    global evaluations

    evaluations += 1 
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0
    
    if evaluations > 350000:
        return 0

    #eval = _eval_material(board)
    eval = _eval_attacks(board)
    #eval += _eval_piece_heatmap(board)
    
    #eval += _eval_attackers(board)

    # ToDo: Evaluate Mobility and Board Control??
    # ToDo: Evaluate Development??
    #eval += _eval_square_attacks(board)*3
    
    # ToDo: Evaludate King Safety
    #eval += _eval_king_safety(board)
    

    # ToDo: Evaluate Pawn Formations: doubled pawns, Opposing Pawns blocking each other, Passed Pawns, Isolated Pawns

    # ToDo: Evaluate # of Open Files and Control of Files    

    # ToDo: Balance evaluation time with depth

    if board.turn:
        return eval
    else:
        return -eval
    
def _eval_material(board):
    piece_values = [100, 280, 320, 379, 929, 0]
    eval = 0

    for piece, value in zip(chess.PIECE_TYPES, piece_values):
        eval += len(board.pieces(piece, chess.WHITE)) * value

    for piece, value in zip(chess.PIECE_TYPES, piece_values):
        eval -= len(board.pieces(piece, chess.BLACK)) * value
   
    return eval

def _eval_piece_heatmap(board):
    # Pawn Heatmap
    eval = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    eval -= sum([pawntable[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)])

    # Knight Heatmap
    eval += sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    eval -= sum([knightstable[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    
    # Bishop Heatmap
    eval += sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    eval -= sum([bishopstable[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK)])
    
    # Rook Heatmap
    eval += sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    eval -= sum([rookstable[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)])

    # Queen Heatmap
    eval += sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    eval -= sum([queenstable[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)])

    # King Heatmap
    eval += kingstable[board.king(chess.WHITE)]
    eval -= kingstable[board.king(chess.BLACK)]

    return eval

def _eval_square_attacks(board):
    eval = 0
    for square in chess.SQUARES:
        eval += len(board.attackers(chess.WHITE, square))
        eval -= len(board.attackers(chess.BLACK, square))
    return eval

def _eval_attacks(board):
    eval = 0
    piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]
    for color in chess.COLORS:
        color_eval = 0
        for piece_type in piece_types:
            for square in board.pieces(piece_type, color):
                color_eval += len(board.attacks(square))
        if color:
            eval += color_eval
        else:
            eval -= color_eval
    return eval*30

def _eval_attackers(board):
    eval = 0

    piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]
    for color in chess.COLORS:
        color_eval = 0
        for piece_type in piece_types:
            for square in board.pieces(piece_type, color):
                color_eval += len(board.attackers(not color, square))
        if color:
            eval -= color_eval
        else:
            eval += color_eval

    eval -= len(board.attackers(chess.BLACK, board.king(chess.WHITE)))
    eval += len(board.attackers(chess.WHITE, board.king(chess.BLACK)))

    return eval

def _eval_king_safety(board):
    eval = 0
    return eval

