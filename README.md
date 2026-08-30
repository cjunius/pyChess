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

- perft <%depth> - returns the number of leaf nodes at the given depth (default=4)
- printBoard
  - prints an ascii version of the board
- printLegalMoves
  - returns the list of legal moves for the current position
- printMoveStack
  - returns the list of moves in the board's move stack
- go_parallel [same args as `go`]
  - returns the next move using Lazy SMP (multiple processes sharing a transposition table)

## To Do

The next five changes, in the order most likely to gain the most playing
strength. Each is a self-contained addition to `NegamaxMixin.search` /
`QuiescenceSearchMixin` unless noted.

### 1. Null-move pruning

If giving the opponent a free move (a "null move") still fails high at reduced
depth (`R = 2..3`), the position is almost certainly a cut-off - return `beta`
without searching the real moves. Skip it when side-to-move is in check, in a
likely zugzwang (king + pawns only), or when depth is very low. Add a
verification search at high depth to avoid zugzwang blunders. Needs a
`board.push(chess.Move.null())` path and a `_null_ok` guard in the search.
Typically the single largest Elo jump available (~50-100).

### 2. Principal Variation Search (NegaScout)

Search the first (best-ordered) move with the full `(-beta, -alpha)` window,
then every later move with a null window `(-alpha-1, -alpha)`; only re-search
with the full window on the rare fail-high. With the move ordering already in
place (TT move, MVV-LVA, killers, history) the first move is usually best, so
most nodes get the cheaper scout search. ~20-40 Elo and it compounds with
everything below.

### 3. Late Move Reductions (LMR)

Once past the first few moves at a node, search quiet, non-checking, non-TT
moves at `depth - 1 - reduction` (reduction grows with move index and depth,
shrink it for killers / good history). Re-search at full depth if the reduced
search beats `alpha`. Combined with PVS this is usually the biggest tree
reduction after null-move - effective branching factor drops sharply, so
iterative deepening reaches 2-4 plies deeper in the same time.

### 4. Correct draw, repetition and mate scoring

- Detect threefold repetition and the 50-move rule *inside* the search tree
  (`board.is_repetition(3)`, `board.halfmove_clock`), not just the automatic
  five-fold / seventy-five-move draws in `is_drawn`.
- Score every draw a flat `0` (currently negamax returns `0 - depth`), with an
  optional small contempt value.
- Store mate scores in the TT as distance-to-mate relative to the current ply
  (`score +/- ply` on store/probe) so `MATE_GUARD` can be removed and mate
  cut-offs actually propagate. This fixes real half-point losses and lets the
  engine convert forced mates faster.

### 5. Evaluation upgrade

PeSTO piece-square tables capture a lot of positional understanding but miss
king safety and pawn structure, which is where a mid-level engine gains most.
Add, keeping the incremental accumulator where possible and a pawn-hash cache
for the rest:

- King safety: attacker count / attack weight on the squares around the king,
  pawn-shield intactness, open files next to the king.
- Passed pawns (bonus scaled by rank and king distance), isolated / doubled /
  backward pawns.
- Bishop pair, rook on open / half-open file, knight outposts.
- Tempo bonus.

Then wire in [Syzygy endgame tablebases](https://python-chess.readthedocs.io/en/latest/syzygy.html)
(`chess.syzygy`) for perfect play with <= 6 pieces.

---

*Recently completed (from the previous review pass): move ordering, transposition
table, single-process iterative deepening + UCI time management, perft fix +
tests, quiescence rewrite (bounded, check-aware, fail-soft), tapered PeSTO
evaluation with an incremental accumulator, standard `info` output, resource-leak
fixes, and Lazy SMP (`go_parallel`) with a lock-free shared-memory TT.*

## Chess Engine

### [Search](https://www.chessprogramming.org/Search)

- [Negamax](https://www.chessprogramming.org/Negamax) - fail-soft
- [Move Ordering](https://www.chessprogramming.org/Move_Ordering) - TT move, captures, promotions, killers, history
  - [MVV-LVA Captures](https://www.chessprogramming.org/MVV-LVA)
  - [Killer Heuristic](https://www.chessprogramming.org/Killer_Heuristic)
  - [History Heuristic](https://www.chessprogramming.org/History_Heuristic)
- [Alpha-Beta Pruning](https://www.chessprogramming.org/Alpha-Beta)
  - [Quiescence Search](https://www.chessprogramming.org/Quiescence_Search) - fail-soft, depth-bounded, check-aware
  - [Transposition Table](https://www.chessprogramming.org/Transposition_Table) - Zobrist-keyed, EXACT/LOWER/UPPER bounds
  - [Iterative Deepening](https://www.chessprogramming.org/Iterative_Deepening) - single-process, with UCI time management
- [Lazy SMP](https://www.chessprogramming.org/Lazy_SMP) - `go_parallel`, workers share a lock-free shared-memory TT
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
  - [Principal Variation Search](https://www.chessprogramming.org/Principal_Variation_Search)
  - [Late Move Reductions](https://www.chessprogramming.org/Late_Move_Reductions)
- Endgame Tablebase  

#### Additional Engines to research

- [NegaScout](https://www.chessprogramming.org/NegaScout)
- [NegaC*](https://www.chessprogramming.org/NegaC*)
- [MTD(f)](https://www.chessprogramming.org/MTD\(f\))

### [Evaluation](https://www.chessprogramming.org/Evaluation)

- [PeSTO](https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function) - tapered mid-/end-game piece-square tables, interpolated by game phase
  - [Material Balance](https://www.chessprogramming.org/Material) / [Point Value](https://www.chessprogramming.org/Point_Value)
  - [Piece-Square Tables](https://www.chessprogramming.org/Piece-Square_Tables) - [incrementally updated](https://www.chessprogramming.org/Incremental_Updates) on `EvalBoard.push`/`pop`
- [Pawn Structure: Doubled, Blocked, and Isolated Pawns](https://www.chessprogramming.org/Pawn_Structure)
- [Mobility](https://www.chessprogramming.org/Mobility)
- [Center Control](https://www.chessprogramming.org/Center_Control)
- [Connectivity](https://www.chessprogramming.org/Connectivity)
- [Trapped Pieces](https://www.chessprogramming.org/Trapped_Pieces)
- [King Safety](https://www.chessprogramming.org/King_Safety)
- [Space](https://www.chessprogramming.org/Space)
- [Tempo](https://www.chessprogramming.org/Tempo)

#### Optimizations to Consider/Research

- [Evaluation Hash Table](https://www.chessprogramming.org/Evaluation_Hash_Table)
- [Material Hash Table](https://www.chessprogramming.org/Material_Hash_Table)
- [Pawn Hash Table](https://www.chessprogramming.org/Pawn_Hash_Table)

- Evaluate the board before making any moves
- Substract the value of the piece being moved in the from position
- Add the value of the piece being moved in the to position

### Tests

Run with `pytest` (config in `pytest.ini`, tests under `test/`).

- `test/test_perft.py` - move generation validated against published perft node counts
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

## Playing Strength

Estimated at **~1800–2000 Elo** (blitz, FIDE/CCRL-ish scale), most likely around
1900. This is a feature-based estimate, not a measured result - see
[STRENGTH.md](STRENGTH.md) for the reasoning, calibration against known engines,
time-control sensitivity, and how to measure it properly.

## Performance Results

All figures below are a fresh benchmark on one machine (Apple Silicon, 10
cores, Python 3.13), fixed-depth search from the starting position. "Before"
is the pre-review engine (plain negamax, no move ordering, no working TT,
unbounded quiescence, from-scratch material+PST eval); "After" is the current
engine. Both columns were run on the *same* machine, so this is a like-for-like
comparison rather than a comparison against the older M1 numbers.

For reference, the original M1 run recorded depth 5 = 1.42s, depth 6 = 10.0s,
depth 7 = 215s single-process (and the old "parallel" mode was *slower*: depth
7 = 430s).

### Single process, fixed-depth `search()` from the start position

| depth | Before (time / nodes) | After (time / nodes) | speed-up |
|------:|----------------------:|---------------------:|---------:|
| 2 |   0.002s /      87 | 0.002s /     79 |  ~1x |
| 3 |   0.015s /     802 | 0.012s /    657 |  1.3x |
| 4 |   0.091s /   3,991 | 0.064s /  2,387 |  1.4x |
| 5 |   1.157s /  46,875 | 0.321s / 15,139 |  3.6x |
| 6 |   8.169s / 317,377 | 1.770s / 72,048 |  4.6x |
| 7 | 152.4s / 5,451,009 | 9.565s / 453,119 | **16x** |

The gap widens every ply because move ordering (TT move, MVV-LVA, killers,
history) and the transposition table compound. "Nodes" is `board.push` calls
(main search + quiescence).

### Current engine, iterative deepening (what `go` / `go depth N` actually runs)

| target depth | time | nodes |
|-------------:|-----:|------:|
| 5 |  0.24s |  12k |
| 6 |  1.38s |  53k |
| 7 |  5.11s | 236k |
| 8 | 38.6s  | 2.1M |

Iterative deepening is roughly 2x faster than a cold fixed-depth search
(each iteration seeds the next through the TT and improves move ordering).

### Parallel from the start position (`go_parallel`)

| depth | Before ("parallel", root-split) | After (Lazy SMP, 9 workers, shared TT) |
|------:|--------------------------------:|--------------------------------------:|
| 6 |  10.6s | 0.84s |
| 7 | 430s   | 3.77s |
| 8 |  —     | 17.9s |

The old parallel mode lost to its own single-threaded search (full windows, no
shared table). Lazy SMP is ~1.5x faster than the current single-threaded
iterative deepening at depth 6-7 and ~2x by depth 8, on this 10-core machine.