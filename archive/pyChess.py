import signal
import sys
import chess
import chess.svg
from chessboard import display



import archive.helper as helper

# Catch KeyboardInterrupt and quit
def catchthesignal(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, catchthesignal)

game_board = None

def main():

    bot1_wins = 0
    bot2_wins = 0
    draws = 0

    engine1 = choose_engine("Player 1")
    engine2 = choose_engine("Player 2")
    print("\n" + engine1.get_name() + " vs " + engine2.get_name())
    game_board = display.start()

    for i in range(0, 9):

        board = chess.Board()
        display.update(board.fen(), game_board)

        winner = None
        while not board.outcome():

            if i%2 == 0:
                winner = validate_move(board, engine1.find_move(board.copy(stack=False)) )
                display.update(board.fen(), game_board)
                if not winner == None:
                    break

            winner = validate_move(board, engine2.find_move(board.copy(stack=False)) )
            display.update(board.fen(), game_board)
            if not winner == None:
                break

            if i%2 == 1:
                winner = validate_move(board, engine1.find_move(board.copy(stack=False)) )
                display.update(board.fen(), game_board)
                if not winner == None:
                    break

        if (winner == "White" and i%2 == 0) or (winner == "Black" and i%2 == 1):
            bot1_wins += 1
        elif (winner == "Black" and i%2 == 0) or (winner == "White" and i%2 == 1):
            bot2_wins += 1
        else:
            draws += 1

        bot1_score = bot1_wins + draws * 0.5
        bot2_score = bot2_wins + draws * 0.5
        print(engine1.get_name() + " " + str(bot1_score) + " - " + str(bot2_score) + " " + engine2.get_name())

        board.clear()
        board.reset()
        
    display.terminate()

def choose_engine(player: str):
    ENGINES = helper.get_engines()
    print("")
    for idx, engine in enumerate(ENGINES):
        print('{num}: {name}'.format(num=idx+1,name=engine.get_name()))

    x = input('Choose ' + player + ': ')
    engine = ENGINES[int(x)-1]
    return engine
    
def validate_move(board: chess.Board, move: chess.Move):
    if move in board.legal_moves:
        board.push(move)
        outcome = board.outcome()
        if outcome:
            if chess.WHITE == outcome.winner:
                return "White"
            elif chess.BLACK == outcome.winner:
                return "Black"
            else:
                return "Draw"
    else:
        if chess.WHITE == board.turn:
            print("Illegal move detected\n")
            return "Black"
        else:
            print("Illegal move detected\n")
            return "White"
    return None

if __name__ == "__main__":
    main()
