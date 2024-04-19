import chess
from bots import randomBot
from bots import firstLegalMoveBot
from bots import lastLegalMoveBot

def main():

    white_wins = 0
    black_wins = 0
    draws = 0

    white_bot = choose_bot("White")
    black_bot = choose_bot("Black")
    print(white_bot.getName() + " vs " + black_bot.getName())

    for _ in range(1, 100):

        board = chess.Board(chess.STARTING_BOARD_FEN)
        while not board.outcome():
            winner = validate_move(board, white_bot.findMove(board) )
            if not winner == None:
                if winner == "White":
                    white_wins += 1
                elif winner == "Black":
                    black_wins += 1
                else:
                    draws += 1
                break

            winner = validate_move(board, black_bot.findMove(board) )
            if not winner == None:
                if winner == "White":
                    white_wins += 1
                elif winner == "Black":
                    black_wins += 1
                else:
                    draws += 1
                break

    print("White wins: " + str(white_wins))
    print("Black wins: " + str(black_wins))
    print("Draws: " + str(draws))
    print("")

def choose_bot(color):
    choice = input("Choose a bot for " + color +":\n1: Random move bot \n2: First legal move bot \n3: Last legal move bot\nChoice: ")
    print("")
    if choice == "1":
        return randomBot
    elif choice == "2":
        return firstLegalMoveBot
    elif choice == "3":
        return lastLegalMoveBot
    else:
        print("Invalid choice")
        return choose_bot()
    
def validate_move(board, move):
    if move in board.legal_moves:
        board.push(move)
        outcome = board.outcome()
        if outcome:
            if chess.WHITE == outcome.winner:
                print("White won - " + str(board.outcome().termination))
                return "White"
            elif chess.BLACK == outcome.winner:
                print("Black won - " + str(board.outcome().termination))
                return "Black"
            else:
                print("Draw - " + str(board.outcome().termination))
                return "Draw"
    else:
        turn = board.turn()
        if chess.WHITE == turn:
            print("Black won - Illegal move detected: " + move)
            return "Black"
        else:
            print("White won - Illegal move detected: " + move)
            return "White"
    return None

if __name__ == "__main__":
    main()
