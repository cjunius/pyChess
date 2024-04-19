import chess
from bots import randomBot

def main():
    board = chess.Board()
    round = 1
    while True:
        print(str(round) + ". ", end="")
        make_white_move(board, randomBot)
        make_black_move(board, randomBot)
        round += 1

def make_white_move(board, bot):
    move = bot.findMove(board.legal_moves)
    print(board.san(move) + " ", end="")
    board.push(move)
    check_board_status(board)

def make_black_move(board, bot):
    move = bot.findMove(board.legal_moves)
    print(board.san(move))
    board.push(move)
    check_board_status(board)
    

def check_board_status(board):
    outcome = board.outcome()
    if outcome:

        if 1 == len(board.move_stack) % 2:
            print("")

        if chess.WHITE == outcome.winner:
            print("White won")
        elif chess.BLACK == outcome.winner:
            print("Black won")
        else:
            print("Draw")

        print(str(board.outcome().termination))
        
        exit()

if __name__ == "__main__":
    main()
