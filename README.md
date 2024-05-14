# pyChess

UCI Python Chess Engine

## Quick Start

Requires Python 3.12

```bash
git clone https://github.com/cjunius/pyChess.git
cd pyChess
pip install -r requirements.txt
python main.py
```

### UCI Commands

- uci
  - returns the ngine name, author, and "uciok"
- ucinewgame
  - resets the chess board
- position [fen <%fen> | startpos] moves <%move1> ... <%moveN>
  - sets the position of the chess board from a known fen or starting position
- isready
  - returns "readyok"
- go [depth <depth>]
  - returns the next move with an optional search depth (default=5)
- quit
  - exits the program

#### Custom UCI Commands

- perft <%depth> - Accidentally removed needs to be re-added
  - returns the total number of nodes for a given depth
- printBoard
  - prints an ascii version of the board
- printLegalMoves
  - returns the list of legal moves for the current position
- printMoveStack
  - returns the list of moves in the board's move stack
- go_parallel [depth <depth>]
  - returns the next move using parallel processing with an optional search depth (default=5)

## Chess Engine

### [Search](https://www.chessprogramming.org/Search)

- [Negamax](https://www.chessprogramming.org/Negamax)
- [Move Ordering](https://www.chessprogramming.org/Move_Ordering) - Checks, Captures, Threats
  - [MVV-LVA Captures](https://www.chessprogramming.org/MVV-LVA)
- [Alpha-Beta Pruning](https://www.chessprogramming.org/Alpha-Beta)
  - [Quiescence Search](https://www.chessprogramming.org/Quiescence_Search)
  - [Transposition Table](https://www.chessprogramming.org/Transposition_Table) - WIP
  - [Iterative Deepening](https://www.chessprogramming.org/Iterative_Deepening) - WIP
- Opening Book

#### Optimizations still to be researched and implemented

- Move Ordering
  - Captures
    - [Dedicated Piece-Square Table](https://www.chessprogramming.org/Piece-Square_Tables)
    - [Static Exchange Evaluation](https://www.chessprogramming.org/Static_Exchange_Evaluation)
  - Non-Captures
    - [Killer Heuristic](https://www.chessprogramming.org/Killer_Heuristic)
    - [History Heuristic](https://www.chessprogramming.org/History_Heuristic)
    - [Relative History Heuristic](https://www.chessprogramming.org/Relative_History_Heuristic)
- Alpha Beta Optimizations
  - [Aspiration Windows](https://www.chessprogramming.org/Aspiration_Windows)
  - [Null Move Pruning](https://www.chessprogramming.org/Null_Move_Pruning)
  - [Aspiration Windows](https://www.chessprogramming.org/Aspiration_Windows)
  - [Lazy SMP](https://www.chessprogramming.org/Lazy_SMP)
    - Requires the python [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) module
- Endgame Tablebase  

#### Additional Engines to research

- [NegaScout](https://www.chessprogramming.org/NegaScout)
- [NegaC*](https://www.chessprogramming.org/NegaC*)
- [MTD(f)](https://www.chessprogramming.org/MTD\(f\))

### [Evaluation](https://www.chessprogramming.org/Evaluation)

- [Simplified Evaluation Function](https://www.chessprogramming.org/Simplified_Evaluation_Function)
  - [Material Balance](https://www.chessprogramming.org/Material)
    - [Point Value](https://www.chessprogramming.org/Point_Value)
  - [Piece-Square Tables](https://www.chessprogramming.org/Piece-Square_Tables)
- [Pawn Structure: Doubled, Blocked, and Isolated Pawns](https://www.chessprogramming.org/Pawn_Structure)
- [Mobility](https://www.chessprogramming.org/Mobility)
- [Center Control](https://www.chessprogramming.org/Center_Control)
- [Connectivity](https://www.chessprogramming.org/Connectivity)
- [Trapped Pieces](https://www.chessprogramming.org/Trapped_Pieces)
- [King Safety](https://www.chessprogramming.org/King_Safety)
- [Space](https://www.chessprogramming.org/Space)
- [Tempo](https://www.chessprogramming.org/Tempo)

#### Optimizations to Consider/Research

- [PeSTO](https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function)
- [Evaluation Hash Table](https://www.chessprogramming.org/Evaluation_Hash_Table)
- [Material Hash Table](https://www.chessprogramming.org/Material_Hash_Table)
- [Pawn Hash Table](https://www.chessprogramming.org/Pawn_Hash_Table)

- Evaluate the board before making any moves
- Substract the value of the piece being moved in the from position
- Add the value of the piece being moved in the to position

### Tests

- Mate in 1, 2, 3, 4 & 5 (given depth = 2n-1)
- Captures
  - Counting Attackers vs Defenders
- Tactics
  - Discovered Attacks
  - Forks
  - Pins
  - Removing the Defender
  - Skewers
- Classic Games

## Performance Results

### Single Process for depth 2 to 6 from starting position

- info score 0 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6')] time 0.21019816398620605
- info score 50 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6'), Move.from_uci('b1c3')] time 0.31528592109680176
- info score 0 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6'), Move.from_uci('b1c3'), Move.from_uci('b8c6')] time 1.162055492401123
- info score 40 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6'), Move.from_uci('b1c3'), Move.from_uci('b8c6'), Move.from_uci('e2e4')] time 9.679795265197754
- info score 0 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6'), Move.from_uci('b1c3'), Move.from_uci('b8c6'), Move.from_uci('e2e4'), Move.from_uci('e7e5')] time 60.78723621368408

### Parallel Processes for depth 2 to 6 from starting position (Processes = 11)

- info score 0 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6')] time 0.2942671775817871
- info score 50 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6'), Move.from_uci('b1c3')] time 0.3848557472229004
- info score 0 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6'), Move.from_uci('b1c3'), Move.from_uci('b8c6')] time 0.7356688976287842
- info score 40 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6'), Move.from_uci('b1c3'), Move.from_uci('b8c6'), Move.from_uci('e2e4')] time 12.785161256790161
- info score 0 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6'), Move.from_uci('b1c3'), Move.from_uci('b8c6'), Move.from_uci('e2e4'), Move.from_uci('e7e5')] time 32.21928000450134