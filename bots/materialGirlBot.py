import chess
import chess.polyglot
import time

DEPTH = 3

evaluations = 0

def getName():
    return "Material Girl Bot"

def findMove(board: chess.Board):
    
    try:
        with chess.polyglot.open_reader("bots/books/bookfish.bin") as reader:
            move = reader.weighted_choice(board).move
            output += "Book move: " + str(board.san(move))
            print(output)
            return move
    except:
            
        global evaluations
        evaluations = 0
        num_legal_moves = 0
        numPieces = len(board.piece_map())

        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000

        startTime = time.time()
        for move in board.legal_moves:
            num_legal_moves += 1
            board.push(move)
            boardValue = -alphabeta(-beta, -alpha, DEPTH - 1, board)
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            if boardValue > alpha:
                alpha = boardValue
            board.pop()
        endTime = time.time()
        diff = endTime - startTime
        
        output = "White " if board.ply() % 2 == 0 else "Black "
        output += "{:2}. {:7} Eval: {:5} ".format(board.fullmove_number, board.san(bestMove), bestValue)
        output += "\tMoves: {}".format(num_legal_moves)
        output += "\tPieces: {}".format(numPieces)
        output += "\tDepth: {}".format(DEPTH)
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
        return -9999 if board.turn else 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    eval = _eval_material(board)

    return eval if board.turn else -eval
    
def _eval_material(board):
    eval = 0

    PIECE_VALUES = {(chess.PAWN, 100), (chess.KNIGHT, 280), (chess.BISHOP, 320), (chess.ROOK, 379), (chess.QUEEN, 929), (chess.KING, 0)}
    for piece, value in PIECE_VALUES:
        eval += len(board.pieces(piece, chess.WHITE)) * value
        eval -= len(board.pieces(piece, chess.BLACK)) * value
   
    return eval