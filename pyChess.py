import signal
import sys
import chess
import chess.svg
from chessboard import display

from bots.BoardControlBot import BoardControlBot
from bots.cjBot import CJBot
from bots.randomBot import RandomBot
from bots.materialGirlBot import MaterialGirlBot
from bots.pieceSquareTableBot import PieceSquareTableBot
from bots.MTDfBot import MTDfBot

# Catch KeyboardInterrupt and quit
def catchthesignal(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, catchthesignal)

game_board = None

def main():

    bot1_wins = 0
    bot2_wins = 0
    draws = 0

    bot1 = choose_bot("Bot 1")
    bot2 = choose_bot("Bot 2")
    print("\n" + bot1.getName() + " vs " + bot2.getName())
    game_board = display.start()

    for i in range(0, 9):

        board = chess.Board()
        display.update(board.fen(), game_board)

        winner = None
        while not board.outcome():

            if i%2 == 0:
                winner = validate_move(board, bot1.findMove(board.copy(stack=False)) )
                display.update(board.fen(), game_board)
                if not winner == None:
                    break

            winner = validate_move(board, bot2.findMove(board.copy(stack=False)) )
            display.update(board.fen(), game_board)
            if not winner == None:
                break

            if i%2 == 1:
                winner = validate_move(board, bot1.findMove(board.copy(stack=False)) )
                display.update(board.fen(), game_board)
                if not winner == None:
                    break

        if (winner == "White" and i%2 == 0) or (winner == "Black" and i%2 == 1):
            bot1_wins += 1
        elif (winner == "Black" and i%2 == 0) or (winner == "White" and i%2 == 1):
            bot2_wins += 2
        else:
            draws += 1

        bot1_score = bot1_wins + draws * 0.5
        bot2_score = bot2_wins + draws * 0.5
        print(bot1.getName() + " " + str(bot1_score) + " - " + str(bot2_score) + " " + bot2.getName())
        print("")

        board.clear()
        board.reset()
        
    display.terminate()

def choose_bot(player: str):
    BOTS = [BoardControlBot(), CJBot(), MaterialGirlBot(), MTDfBot(depth=5), PieceSquareTableBot(), RandomBot()]
    print("")
    count = 1
    for bot in BOTS:
        print('{num}: {name}'.format(num=count,name=bot.getName()))
        count += 1

    x = input('choose ' + player + ': ')
    bot = BOTS[int(x)-1]
    return bot
    
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
