import io
import os
import chess
import chess.svg
from chessboard import display

game_board = None

def main():

    bot1_wins = 0
    bot2_wins = 0
    draws = 0

    white_bot = choose_bot("White")
    black_bot = choose_bot("Black")
    print("\n" + white_bot.getName() + " vs " + black_bot.getName())
    game_board = display.start()

    for i in range(0, 9):

        board = chess.Board()
        display.update(board.fen(), game_board)

        while not board.outcome():

            if i%2 == 0:
                winner = validate_move(board, white_bot.findMove(board.copy(stack=False)) )
                display.update(board.fen(), game_board)
                if not winner == None:
                    if winner == "White":
                        bot1_wins += 1
                    elif winner == "Black":
                        bot2_wins += 1
                    else:
                        draws += 1
                    break

            winner = validate_move(board, black_bot.findMove(board.copy(stack=False)) )
            display.update(board.fen(), game_board)
            if not winner == None:
                if winner == "White":
                    if i%2 == 0:
                        bot1_wins += 1
                    else:
                        bot2_wins += 1
                elif winner == "Black":
                    if i%2 == 0:
                        bot2_wins += 1
                    else:
                        bot1_wins += 1
                else:
                    draws += 1
                break

            if i%2 == 1:
                winner = validate_move(board, white_bot.findMove(board.copy(stack=False)) )
                display.update(board.fen(), game_board)
                if not winner == None:
                    if winner == "White":
                        bot2_wins += 1
                    elif winner == "Black":
                        bot1_wins += 1
                    else:
                        draws += 1
                    break

        board.clear()
        board.reset()
        1
    bot1_score = bot1_wins + draws * 0.5
    bot2_score = bot2_wins + draws * 0.5
    print("\n" + white_bot.getName() + " vs " + black_bot.getName())
    print("Final: " + str(bot1_score) + " - " + str(bot2_score))
    print("")
    display.terminate()

def choose_bot(color: str):
    files = os.listdir('./bots')
    filtered_files = [file[: -3] for file in files if file.endswith(".py")]
    bots = [__import__( "bots." + file , {}, {}, ['bots']) for file in filtered_files]
    bots.sort(key=lambda x: x.getName())

    count = 0

    print("")
    for bot in bots:
        print('{num}: {name}'.format(num=count+1,name=bot.getName()))
        count += 1

    x = input('choose a bot for ' + color + ': ')
    bot = bots[int(x)-1]
    return bot
    
def validate_move(board: chess.Board, move: chess.Move):
    if move in board.legal_moves:
        board.push(move)
        outcome = board.outcome()
        if outcome:
            if chess.WHITE == outcome.winner:
                print("White won - " + str(board.outcome().termination) + "\n")
                return "White"
            elif chess.BLACK == outcome.winner:
                print("Black won - " + str(board.outcome().termination) + "\n")
                return "Black"
            else:
                print("Draw - " + str(board.outcome().termination) + "\n")
                return "Draw"
    else:
        if chess.WHITE == board.turn:
            print("Black won - Illegal move detected\n")
            return "Black"
        else:
            print("White won - Illegal move detected\n")
            return "White"
    return None

if __name__ == "__main__":
    main()
