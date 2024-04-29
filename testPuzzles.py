import chess
import time

from bots.BoardControlBot import BoardControlBot
from bots.cjBot import CJBot
from bots.randomBot import RandomBot
from bots.materialGirlBot import MaterialGirlBot
from bots.pieceSquareTableBot import PieceSquareTableBot
from bots.materialPSTBot import MaterialPSTBot
from bots.mobilityBot import MobilityBot
from bots.NegaScoutBot import NegaScoutBot
from bots.NegaMaxBot import NegaMaxBot
from bots.NegaMaxABBot import NegaMaxABBot
from bots.NegaMaxABTTBot import NegaMaxABTTBot
from bots.MTDfBot import MTDfBot

mate_in_1 = [    
    # https://chessfox.com/checkmate-patterns/
    ("8/4N1pk/8/8/8/4R3/8/6K1 w - - 0 1","Rh3#"),                               # Anastasia's Mate
    ("6k1/6P1/5K2/8/8/8/7R/8 w - - 0 1", "Rh8#"),                               # Anderssen's Mate
    ("7k/1R6/5N2/8/8/8/8/6K1 w - - 0 1", "Rh7#"),                               # Arabian Mate
    ("6k1/5ppp/8/8/8/8/5PPP/3R2K1 w - - 0 1", "Rd8#"),                          # Back Rank Mate
    ("4k3/8/5Q2/8/8/5B2/8/6K1 w - - 0 1", "Bc6#"),                              # Balestra Mate
    ("5rk1/8/8/6N1/8/3B4/1B6/6K1 w - - 0 1", "Bh7#"),                           # Blackburne's Mate
    ("5rk1/1R5R/8/8/8/8/8/6K1 w - - 0 1", "Rbg7#"),                             # Blind Swine Mate
    ("2kr4/3p4/8/8/5B2/3B4/8/2K5 w - - 0 1", "Ba6#"),                           # Boden's Mate
    ("7k/7p/8/4N3/8/8/8/2K3R1 w - - 0 1", "Nf7#"),                              # Corner Mate
    ("8/2k5/8/8/7Q/8/8/1R1R2K1 w - - 0 1", "Qc4#"),                             # Corridor Mate
    ("6bk/7p/8/8/8/6B1/8/6K1 w - - 0 1", "Be5#"),                               # Diagonal Corridor Mate
    ("8/8/8/6p1/5qk1/2Q5/6K1/8 w - - 0 1", "Qh3#"),                             # Cozio's Mate (Dovetail Mate)
    ("5rk1/6p1/6P1/8/8/7Q/8/6K1 w - - 0 1", "Qh7#"),                            # Damiano's Mate
    ("8/8/1R6/5pkp/8/5KPP/8/8 w - - 0 1", "h4#"),                               # David and Goliath Mate
    ("3rkr2/8/8/8/2Q5/8/8/6K1 w - - 0 1", "Qe6#"),                              # Epaulette Mate
    ("rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 1", "Qh4#"),  # Fool's Mate
    ("7k/6p1/8/8/2B5/8/8/2KR4 w - - 0 1", "Rh1#"),                              # Graco's Mate
    ("6k1/6P1/5K2/8/8/8/8/7R w - - 0 1", "Rh8#"),                               # H-file Mate
    ("2R5/6pk/6N1/5P2/8/8/8/6K1 w - - 0 1", "Rh8#"),                            # Hook Mate
    ("2k5/8/1Q1R4/8/8/8/8/6K1 w - - 0 1", "Rd8#"),                              # Kill Box Mate
    ("7k/1R6/R7/8/8/8/8/6K1 w - - 0 1", "Ra8#"),                                # Lawnmower Mate
    ("6k1/5p1p/5PpQ/8/8/8/8/6K1 w - - 0 1", "Qg7#"),                            # Lolli's Mate
    ("4Q3/5Bpk/7p/8/8/8/8/6K1 w - - 0 1", "Qg8#"),                              # Max Lange's Mate
    ("4k3/4pp2/8/B7/8/8/8/3R2K1 w - - 0 1", "Rd8#"),                            # Mayet's Mate
    ("7k/7p/8/8/8/4B3/8/2K3R1 w - - 0 1", "Bd4#"),                              # Morphy's Mate
    ("1n2kb1r/p4ppp/4q3/4p1B1/4P3/8/PPP2PPP/2KR4 w k - 0 1", "Rd8#"),           # Opera Mate
    ("5rk1/p4p1p/8/8/8/2B5/8/2KR4 w - - 0 1", "Rg1#"),                          # Pillsbury's Mate
    ("rnb5/ppk5/2p5/6B1/8/8/5PPP/3R2K1 w - - 0 1", "Bd8#"),                     # Reti's Mate
    ("r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 0 1", "Qxf7#"), # Scholar's Mate
    ("6rk/6pp/8/6N1/8/8/8/6K1 w - - 0 1", "Nf7#"),                              # Smothered MAte
    ("5rk1/5p1p/8/3N4/8/8/1B6/6K1 w - - 0 1", "Ne7#"),                          # Suffocation Mate
    ("8/5p1p/6k1/8/6K1/4Q3/8/8 w - - 0 1", "Qg5#"),                             # Swallow's Tail Mate (Gueridon Mate)
    ("8/6p1/6kR/8/5Q2/8/8/6K1 w - - 0 1", "Qf6#"),                              # Triangle Mate
    ("5k2/2R5/4PN2/8/8/8/8/6K1 w - - 0 1", "Rf7#"),                             # Vukovic Mate
]

mate_in_2 = [
    ("1k6/6R1/7P/8/8/8/8/6K1 w - - 0 1", "h7"),                                     # Mate in 2, p1, pawn push
    ("2k5/6RP/8/8/8/8/8/6K1 w - - 1 2", "h8=Q#"),                                   # Mate in 2, p2 , continuation

    ("r2qkbnr/ppp2ppp/2np4/4N3/2B1P3/2N4P/PPPP1PP1/R1BbK2R w KQkq - 0 1", "Bxf7+"), # Legal's Mate - part1
    ("r2q1bnr/ppp1kBpp/2np4/4N3/4P3/2N4P/PPPP1PP1/R1BbK2R w KQ - 0 1", "Nd5#"),     # Legal's Mate - part 2

    ("8/6k1/8/5Q1R/8/8/8/6K1 w - - 0 1", "Rh7+"),                                   # Railroad Mate - Part 1
    ("6k1/7R/8/5Q2/8/8/8/6K1 w - - 0 1", "Qf7#"),                                   # Railroad Mate - part 2
]

mate_in_3_as_black = [
    ("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1", "Qd1+"),               # Mate in 3 - Part 1 - Qd1+ (Sacrifice), Kxd1, 
    ("1k1r4/pp1b1R2/6pp/4p3/2B5/4Q3/PPP2B2/3K4 b - - 0 2", "Bg4+"),                 # Mate in 3 - Part 2 - Bg4+, Kc1 or Ke1
    ("1k1r4/pp3R2/6pp/4p3/2B3b1/4Q3/PPP2B2/2K5 b - - 2 3", "Rd1#"),                 # Mate in 3 - Part 3 - Rd1#
    ("1k1r4/pp3R2/6pp/4p3/2B3b1/4Q3/PPP2B2/4K3 b - - 2 3", "Rd1#"),                 # Mate in 3 - Part 3 alt - Rd1#
]

mate_in_3_as_white = [
    ("5k2/2b2ppp/3q4/5b2/3P4/PP2Q3/2r1B1PP/4R1K1 w - - 0 1", "Qe8+"),                # Same as above with pieces flipped color
    ("4k3/2b2ppp/3q4/5b2/3P4/PP6/2r1B1PP/4R1K1 w - - 0 2", "Bb5+"),
    ("5k2/2b2ppp/3q4/1B3b2/3P4/PP6/2r3PP/4R1K1 w - - 2 3", "Re8#"),
    ("3k4/2b2ppp/3q4/1B3b2/3P4/PP6/2r3PP/4R1K1 w - - 2 3", "Re8#")
]

others = [
    # Forcing a draw/stalemate

    # Other
    ("3r1k2/4npp1/1ppr3p/p6P/P2PPPP1/1NR5/5K2/2R5 w - - 0 1", "d5"),
    ("2q1rr1k/3bbnnp/p2p1pp1/2pPp3/PpP1P1P1/1P2BNNP/2BQ1PRK/7R b - - 0 1", "f5"),
    ("rnbqkb1r/p3pppp/1p6/2ppP3/3N4/2P5/PPP1QPPP/R1B1KB1R w KQkq - 0 1", "e6"),
    ("r1b2rk1/2q1b1pp/p2ppn2/1p6/3QP3/1BN1B3/PPP3PP/R4RK1 w - - 0 1", "a4"),
    ("2r3k1/pppR1pp1/4p3/4P1P1/5P2/1P4K1/P1P5/8 w - - 0 1", "g6"),
    ("1nk1r1r1/pp2n1pp/4p3/q2pPp1N/b1pP1P2/B1P2R2/2P1B1PP/R2Q2K1 w - - 0 1", "Nf6"),
    ("4b3/p3kp2/6p1/3pP2p/2pP1P2/4K1P1/P3N2P/8 w - - 0 1", "f5"),
    ("2kr1bnr/pbpq4/2n1pp2/3p3p/3P1P1B/2N2N1Q/PPP3PP/2KR1B1R w - - 0 1", "f5"),
    ("3rr1k1/pp3pp1/1qn2np1/8/3p4/PP1R1P2/2P1NQPP/R1B3K1 b - - 0 1", "Ne5"),
    ("2r1nrk1/p2q1ppp/bp1p4/n1pPp3/P1P1P3/2PBB1N1/4QPPP/R4RK1 w - - 0 1", "f4"),
    ("r3r1k1/ppqb1ppp/8/4p1NQ/8/2P5/PP3PPP/R3R1K1 b - - 0 1", "Bf5"),
    ("r2q1rk1/4bppp/p2p4/2pP4/3pP3/3Q4/PP1B1PPP/R3R1K1 w - - 0 1", "b4"),
    #("rnb2r1k/pp2p2p/2pp2p1/q2P1p2/8/1Pb2NP1/PB2PPBP/R2Q1RK1 w - - 0 1", "Qd2 Qe1"),
    ("2r3k1/1p2q1pp/2b1pr2/p1pp4/6Q1/1P1PP1R1/P1PN2PP/5RK1 w - - 0 1", "Qxg7+"),
    ("r1bqkb1r/4npp1/p1p4p/1p1pP1B1/8/1B6/PPPN1PPP/R2Q1RK1 w kq - 0 1", "Ne4"),
    ("r2q1rk1/1ppnbppp/p2p1nb1/3Pp3/2P1P1P1/2N2N1P/PPB1QP2/R1B2RK1 b - - 0 1", "h5"),
    ("r1bq1rk1/pp2ppbp/2np2p1/2n5/P3PP2/N1P2N2/1PB3PP/R1B1QRK1 b - - 0 1", "Nb3"),
    ("3rr3/2pq2pk/p2p1pnp/8/2QBPP2/1P6/P5PP/4RRK1 b - - 0 1", "Rxe4"),
    ("r4k2/pb2bp1r/1p1qp2p/3pNp2/3P1P2/2N3P1/PPP1Q2P/2KRR3 w - - 0 1", "g4"),
    ("3rn2k/ppb2rpp/2ppqp2/5N2/2P1P3/1P5Q/PB3PPP/3RR1K1 w - - 0 1", "Nh6"),
    ("2r2rk1/1bqnbpp1/1p1ppn1p/pP6/N1P1P3/P2B1N1P/1B2QPP1/R2R2K1 b - - 0 1", "Bxe4"),
    ("r1bqk2r/pp2bppp/2p5/3pP3/P2Q1P2/2N1B3/1PP3PP/R4RK1 b kq - 0 1", "f6"),
    ("r2qnrnk/p2b2b1/1p1p2pp/2pPpp2/1PP1P3/PRNBB3/3QNPPP/5RK1 w - - 0 1", "f4")
]

failing = [
    ("1k6/6R1/7P/8/8/8/8/6K1 w - - 0 1", "h7")                                     # Mate in 2, p1, pawn push
    #,("2k5/6RP/8/8/8/8/8/6K1 w - - 1 2", "h8=Q#")                                   # Mate in 2, p2 , continuation
    #,("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1", "Qd1+")              # Mate in 3 - Part 1 - Qd1+ (Sacrifice), Kxd1, 
    #,("1k1r4/pp1b1R2/6pp/4p3/2B5/4Q3/PPP2B2/3K4 b - - 0 2", "Bg4+")                 # Mate in 3 - Part 2 - Bg4+, Kc1 or Ke1
]

puzzles = [
    #("Mate in 1", mate_in_1) 
    ("Mate in 2", mate_in_2)
    ,("Mate in 3 - Playing as White", mate_in_3_as_white)
    ,("Mate in 3 - Playing as Black", mate_in_3_as_black)
    #,("Others", others)
    #("Failing", failing)
]

depth = 5
# bots = [NegaScoutBot(depth=depth)]
bots = [NegaMaxABBot(depth=depth)]
# bots = [NegaMaxABBot(depth=depth), NegaScoutBot(depth=depth)]
# bots = [MaterialGirlBot(depth=depth), PieceSquareTableBot(depth=depth), BoardControlBot(depth=depth), MobilityBot(depth=depth), MaterialPSTBot(depth=depth), CJBot(depth=depth)]

results = []
for name, puzzle in puzzles:
    results.append("")
    results.append(name)
    print(name)
    for bot in bots:
        correct = 0
        incorrect = 0
        start = time.time()
        for fen, solution in puzzle:
            board = chess.Board(fen)
            move = bot.findMove(board)
            print("Expected: {:6}  Got: {:6}  - Correct: {:5} - {} depth {}".format(solution, board.san(move), str(solution == board.san(move)), bot.getName(), depth))
            if board.san(move) == solution:
                correct += 1
            else:
                incorrect += 1        
        end = time.time()
        diff = round(end-start, 2)
        results.append("{:60}  Result: {} - {}  Time: {:6.2f}".format(bot.getName(), correct, incorrect, diff))
    print("")
    
for result in results:
    print(result)


# Mate in 1 - Depth 4
# NegaMax Alpha-Beta Bot                            Result: 34 - 0  Time:   0.06
# NegaMax Alpha-Beta with Transposition Table Bot   Result: 34 - 0  Time:   0.07
# NegaScout Bot                                     Result: 34 - 0  Time:   0.06

# Mate in 2 - Depth 4
# NegaMax Alpha-Beta Bot                            Result: 6 - 0  Time:   3.13
# NegaMax Alpha-Beta with Transposition Table Bot   Result: 6 - 0  Time:   3.52
# NegaScout Bot                                     Result: 5 - 1  Time:  13.08

# Mate in 3 - Depth 4
# NegaMax Alpha-Beta Bot                            Result: 4 - 0  Time:  16.13
# NegaMax Alpha-Beta with Transposition Table Bot   Result: 4 - 0  Time:  18.00
# NegaScout Bot                                     Result: 2 - 2  Time:  13.56



# Mate in 1 - Depth 4
# Material Girl Bot                                             Result: 34 - 0  Time:   0.05
# Piece-Square Table Bot                                        Result: 34 - 0  Time:   0.05
# Board Control Bot                                             Result: 34 - 0  Time:   0.06
# Mobility Bot                                                  Result: 34 - 0  Time:   0.10
# Material & Piece-Square Table Bot                             Result: 34 - 0  Time:   0.05
# CJ Bot                                                        Result: 34 - 0  Time:   0.05

# Mate in 2 - Depth 4
# Material Girl Bot                                             Result: 6 - 0  Time:   1.77
# Piece-Square Table Bot                                        Result: 6 - 0  Time:   2.00
# Board Control Bot                                             Result: 4 - 2  Time:   3.56
# Mobility Bot                                                  Result: 6 - 0  Time:   2.95
# Material & Piece-Square Table Bot                             Result: 6 - 0  Time:   1.98
# CJ Bot                                                        Result: 6 - 0  Time:   3.33

# Mate in 3 - Depth 4
# Material Girl Bot                                             Result: 3 - 1  Time:   7.15
# Piece-Square Table Bot                                        Result: 3 - 1  Time:   7.57
# Board Control Bot                                             Result: 3 - 1  Time:  14.63
# Mobility Bot                                                  Result: 3 - 1  Time:   8.30
# Material & Piece-Square Table Bot                             Result: 3 - 1  Time:  16.13
# CJ Bot                                                        Result: 4 - 0  Time:  18.76

