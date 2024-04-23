import chess
import chess.svg

from bots.attackerBot import AttackerBot
from bots.cjBot import CJBot
from bots.randomBot import RandomBot
from bots.materialGirlBot import MaterialGirlBot

BOTS = [AttackerBot(), MaterialGirlBot(), CJBot(), RandomBot()]
BOTS.sort(key=lambda x: x.getName())

def main():

    bot1_wins = 0
    bot2_wins = 0
    draws = 0

    white_bot = choose_bot("White")
    black_bot = choose_bot("Black")
    print("\n" + white_bot.getName() + " vs " + black_bot.getName())

    for i in range(0, 9):

        board = chess.Board()

        winner = None
        while not board.outcome():

            if i%2 == 0:
                winner = validate_move(board, white_bot.findMove(board.copy(stack=False)) )
                if not winner == None:
                    break

            winner = validate_move(board, black_bot.findMove(board.copy(stack=False)) )
            if not winner == None:
                break

            if i%2 == 1:
                winner = validate_move(board, white_bot.findMove(board.copy(stack=False)) )
                if not winner == None:
                    break

        if (winner == "White" and i%2 == 0) or (winner == "Black" and i%2 == 1):
            bot1_wins += 1
        elif (winner == "Black" and i%2 == 0) or (winner == "White" and i%2 == 1):
            bot2_wins += 2
        else:
            draws += 1

        board.clear()
        board.reset()
        
    bot1_score = bot1_wins + draws * 0.5
    bot2_score = bot2_wins + draws * 0.5
    print("\n" + white_bot.getName() + " vs " + black_bot.getName())
    print("Final: " + str(bot1_score) + " - " + str(bot2_score))
    print("")
    

def choose_bot(color: str):
    print("")
    count = 1
    for bot in BOTS:
        print('{num}: {name}'.format(num=count,name=bot.getName()))
        count += 1

    x = input('choose a bot for ' + color + ': ')
    bot = BOTS[int(x)-1]
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
