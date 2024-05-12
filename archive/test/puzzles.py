MATE_IN_1 = [    
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
    ("rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 1", "Qh4#"),  # Fool's Mate
]

MATE_IN_2 = [
    ("1k6/6R1/7P/8/8/8/8/6K1 w - - 0 1", "h7"),                                     # Mate in 2, p1, pawn push
    ("2k5/6RP/8/8/8/8/8/6K1 w - - 1 2", "h8=Q#"),                                   # Mate in 2, p2 , continuation

    ("r2qkbnr/ppp2ppp/2np4/4N3/2B1P3/2N4P/PPPP1PP1/R1BbK2R w KQkq - 0 1", "Bxf7+"), # Legal's Mate - part 1
    ("r2q1bnr/ppp1kBpp/2np4/4N3/4P3/2N4P/PPPP1PP1/R1BbK2R w KQ - 0 1", "Nd5#"),     # Legal's Mate - part 2

    ("8/6k1/8/5Q1R/8/8/8/6K1 w - - 0 1", "Rh7+"),                                   # Railroad Mate - Part 1
    ("6k1/7R/8/5Q2/8/8/8/6K1 w - - 0 1", "Qf7#"),                                   # Railroad Mate - part 2

    ("1k6/8/8/8/8/p7/1r6/6K1 b - - 0 1", "a2"),                                     # Mate in 2, p1, pawn push
    ("1k6/8/8/8/8/8/pr6/5K2 b - - 1 2", "a1=Q#"),                                   # Mate in 2, p2 , continuation

    ("1k6/8/8/2q5/8/r7/1K6/8 b - - 0 1", "Qc3+"),                                   # Railroad Mate - Part 1
    ("1k6/8/8/8/8/r1q5/8/1K6 b - - 2 2", "Ra1#"),                                   # Railroad Mate - part 2
]

MATE_IN_3 = [
    ("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1", "Qd1+"),               # Mate in 3 - Part 1 - Qd1+ (Sacrifice), Kxd1, 
    ("1k1r4/pp1b1R2/6pp/4p3/2B5/4Q3/PPP2B2/3K4 b - - 0 2", "Bg4+"),                 # Mate in 3 - Part 2 - Bg4+, Kc1 or Ke1
    ("1k1r4/pp3R2/6pp/4p3/2B3b1/4Q3/PPP2B2/2K5 b - - 2 3", "Rd1#"),                 # Mate in 3 - Part 3 - Rd1#
    ("1k1r4/pp3R2/6pp/4p3/2B3b1/4Q3/PPP2B2/4K3 b - - 2 3", "Rd1#"),                 # Mate in 3 - Part 3 alt - Rd1#

    ("5k2/2b2ppp/3q4/5b2/3P4/PP2Q3/2r1B1PP/4R1K1 w - - 0 1", "Qe8+"),                # Same as above with pieces flipped color
    ("4k3/2b2ppp/3q4/5b2/3P4/PP6/2r1B1PP/4R1K1 w - - 0 2", "Bb5+"),
    ("5k2/2b2ppp/3q4/1B3b2/3P4/PP6/2r3PP/4R1K1 w - - 2 3", "Re8#"),
    ("3k4/2b2ppp/3q4/1B3b2/3P4/PP6/2r3PP/4R1K1 w - - 2 3", "Re8#")
]

SIMPLE_CAPTURES = [
    ("6k1/2q2pp1/7p/8/8/7P/2Q2PP1/6K1 w - - 0 1", "Qxc7"), # White Queen takes Queen
    ("6k1/2r2pp1/7p/8/8/7P/2Q2PP1/6K1 w - - 0 1", "Qxc7"), # White Queen takes Rook
    ("6k1/2b2pp1/7p/8/8/7P/2Q2PP1/6K1 w - - 0 1", "Qxc7"), # White Queen takes Bishop
    ("6k1/2n2pp1/7p/8/8/7P/2Q2PP1/6K1 w - - 0 1", "Qxc7"), # White Queen takes Knight
    ("6k1/2p2pp1/7p/8/8/7P/2Q2PP1/6K1 w - - 0 1", "Qxc7"), # White Queen takes Pawn
    ("6k1/2q2pp1/7p/8/8/7P/2R2PP1/6K1 w - - 0 1", "Rxc7"), # White Rook takes Queen
    ("6k1/2r2pp1/7p/8/8/7P/2R2PP1/6K1 w - - 0 1", "Rxc7"), # White Rook takes Rook
    ("6k1/2b2pp1/7p/8/8/7P/2R2PP1/6K1 w - - 0 1", "Rxc7"), # White Rook takes Bishop
    ("6k1/2n2pp1/7p/8/8/7P/2R2PP1/6K1 w - - 0 1", "Rxc7"), # White Rook takes Knight
    ("6k1/2p2pp1/7p/8/8/7P/2R2PP1/6K1 w - - 0 1", "Rxc7"), # White Rook takes Pawn
    ("6k1/2q2ppp/8/8/8/6B1/5PPP/6K1 w - - 0 1", "Bxc7"), # White Bishop takes Queen
    ("6k1/2r2ppp/8/8/8/6B1/5PPP/6K1 w - - 0 1", "Bxc7"), # White Bishop takes Rook
    ("6k1/2b2ppp/8/8/8/6B1/5PPP/6K1 w - - 0 1", "Bxc7"), # White Bishop takes Bishop
    ("6k1/2n2ppp/8/8/8/6B1/5PPP/6K1 w - - 0 1", "Bxc7"), # White Bishop takes Knight
    ("6k1/2p2ppp/8/8/8/6B1/5PPP/6K1 w - - 0 1", "Bxc7"), # White Bishop takes Pawn
    ("6k1/2q2ppp/8/3N4/8/8/5PPP/6K1 w - - 0 1", "Nxc7"), # White Knight takes Queen
    ("6k1/2r2ppp/8/3N4/8/8/5PPP/6K1 w - - 0 1", "Nxc7"), # White Knight takes Rook
    ("6k1/2b2ppp/8/3N4/8/8/5PPP/6K1 w - - 0 1", "Nxc7"), # White Knight takes Bishop
    ("6k1/2n2ppp/8/3N4/8/8/5PPP/6K1 w - - 0 1", "Nxc7"), # White Knight takes Knight
    ("6k1/2p2ppp/8/3N4/8/8/5PPP/6K1 w - - 0 1", "Nxc7"), # White Knight takes Pawn
    ("5k2/2q5/3P4/8/8/8/8/5K2 w - - 0 1", "dxc7"), # White Pawn takes Queen
    ("5k2/2r5/3P4/8/8/8/8/5K2 w - - 0 1", "dxc7"), # White Pawn takes Rook
    ("5k2/2b5/3P4/8/8/8/8/5K2 w - - 0 1", "dxc7"), # White Pawn takes Bishop
    ("5k2/2k5/3P4/8/8/8/8/5K2 w - - 0 1", "dxc7"), # White Pawn takes Knight
    ("5k2/2p5/3P4/8/8/8/8/5K2 w - - 0 1", "dxc7"), # White Pawn takes Pawn

    ("6k1/2q2pp1/7p/8/8/7P/2Q2PP1/6K1 b - - 0 1", "Qxc2"), # Black Queen takes Queen
    ("6k1/2q2pp1/7p/8/8/7P/2R2PP1/6K1 b - - 0 1", "Qxc2"), # Black Queen takes Rook
    ("6k1/2q2pp1/7p/8/8/7P/2B2PP1/6K1 b - - 0 1", "Qxc2"), # Black Queen takes Bishop
    ("6k1/2q2pp1/7p/8/8/7P/2N2PP1/6K1 b - - 0 1", "Qxc2"), # Black Queen takes Knight
    ("6k1/2q2pp1/7p/8/8/7P/2P2PP1/6K1 b - - 0 1", "Qxc2"), # Black Queen takes Pawn
]

SIMPLE_FORKS = [
    ("6k1/5pp1/1b1n3p/8/2PP4/7P/5PP1/6K1 w - - 0 1", "c5"), # Pawn Fork
    ("r3k1nr/ppp2ppp/2np4/2bNp3/2B1P1b1/3P1N2/PPP2PPP/R1B1K2R w KQkq - 0 1", "Nxc7+"), # White Knight forks King and Rook
    ("8/8/4K3/7n/6k1/3Q4/8/8 b - - 0 1", "Nf4+"), # Black Knight forks King and Queen
    ("4r3/k7/4r3/8/2K3N1/8/8/8 b - - 0 1", "Re4+"), # Black Rook forks King and Knight
    ("1k1b4/8/7R/8/8/8/8/2K5 b - - 0 1", "Bg5+"), # Black Bishop forks King and Rook
    ("8/8/3K4/7k/3nb3/8/8/8 w - - 0 1", "Ke5"), # White King forks Bishop and Knight
]

COMPLEX_FORKS = [
    ("r5k1/p2n1p1p/1pb1pp2/7N/2P5/P7/5PPP/3RK2R w - - 0 1", "Rxd7"), # Part 1: White Rook takes Knight to Setup Knight Fork if Bishop Takes
    ("r5k1/p2b1p1p/1p2pp2/7N/2P5/P7/5PPP/4K2R w - - 0 2", "Nxf6+"), # Part 2: White Knight forks King and Bishop
    ("r7/p2b1pkp/1p2pN2/8/2P5/P7/5PPP/4K2R w - - 1 3", "Nxd7"), # Part 3: White Knight takes Bishop and is up a Knight)

    ("r5k1/p2qn2p/1r4p1/3bBp2/1Qp2PP1/2P2B2/7P/1R1R2K1 w - - 0 1", "Qxe7"), # Part 1: White Queen takes Knight, Black Queen takes Queen
    ("r5k1/p3q2p/1r4p1/3bBp2/2p2PP1/2P2B2/7P/1R1R2K1 w - - 0 2", "Bxd5+"), # Part 2: White Bishop takes Bishop, forking King and Rook
    #("r4k2/p3q2p/1r4p1/3BBp2/2p2PP1/2P5/7P/1R1R2K1 w - - 1 3", "Bxa8"), # Part 3: White Bishop takes Rook, Black Rook takes Rook #ToDo: Alternative Rxb6 leads to similar position (2nd best stockfish move +0.6) Stockfish +1.9 for Rxa8
    ("B4k2/p3q2p/6p1/4Bp2/2p2PP1/2P5/7P/1r1R2K1 w - - 0 4", "Rxb1"), # Part 4: White Rook takes Rook, White is up 2 Bishops and a Rook to Blacks Queen and Pawn
]

# Pins
# - Relative Pin
# - Absolute Pin
# - Double Pin

# Discovered Checks
# - Discovered Double Check

# Mates 
# - Mate in 4
# - Mate in 5
# - Smothered Mate with a Pin
# - Two Pawn Checkmate

# Endgames
# - K+Q vs K
# - R+R+K vs K
# - Q+R+K vs K

# Cross Check
# Classical Games

OTHER = [
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