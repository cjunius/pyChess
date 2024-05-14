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

## Performance Results on a Macbook Pro M1

### Single Process from starting position

- info score 0 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6')] time 0.008128881454467773
- info score 50 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6'), Move.from_uci('b1c3')] time 0.03927803039550781
- info score 0 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6'), Move.from_uci('b1c3'), Move.from_uci('b8c6')] time 0.14339184761047363
- info score 40 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6'), Move.from_uci('b1c3'), Move.from_uci('b8c6'), Move.from_uci('e2e4')] time 1.422001838684082
- info score 0 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6'), Move.from_uci('b1c3'), Move.from_uci('b8c6'), Move.from_uci('e2e4'), Move.from_uci('e7e5')] time 10.046779870986938
- info score 35 pv [Move.from_uci('e2e4'), Move.from_uci('b8c6'), Move.from_uci('g1f3'), Move.from_uci('g8f6'), Move.from_uci('e4e5'), Move.from_uci('f6d5'), Move.from_uci('b1c3')] time 214.95130610466003

### Parallel Processes from starting position

- info score 0 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6')] time 0.13646221160888672
- info score 50 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6'), Move.from_uci('b1c3')] time 0.15276002883911133
- info score 0 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6'), Move.from_uci('b1c3'), Move.from_uci('b8c6')] time 0.2571988105773926
- info score 40 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6'), Move.from_uci('b1c3'), Move.from_uci('b8c6'), Move.from_uci('e2e4')] time 2.9780540466308594
- info score 0 pv [Move.from_uci('g1f3'), Move.from_uci('g8f6'), Move.from_uci('b1c3'), Move.from_uci('b8c6'), Move.from_uci('e2e4'), Move.from_uci('e7e5')] time 10.565109968185425
- info score 35 pv [Move.from_uci('e2e4'), Move.from_uci('b8c6'), Move.from_uci('g1f3'), Move.from_uci('g8f6'), Move.from_uci('e4e5'), Move.from_uci('f6d5'), Move.from_uci('b1c3')] time 429.6187961101532