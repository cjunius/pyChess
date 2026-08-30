# Design

How the engine is put together, what each technique buys, and the backlog of
ideas not yet implemented. For a *prioritised* list of next steps see
[tasks.md](tasks.md); for strength and speed numbers see
[engine-strength.md](engine-strength.md) and [performance.md](performance.md).

## Architecture

`Negamax` is the search core. It holds four collaborators, each a plain object
with a small interface, injected at construction:

| collaborator | responsibility |
|---|---|
| `PestoEvaluator` | static evaluation from the side-to-move's view |
| `MoveOrderer` | orders moves to maximise alpha-beta cut-offs; owns killer / history tables |
| `TranspositionTable` / `SharedTT` | Zobrist-keyed cache; same `key` / `probe` / `store` interface, one in-process, one in shared memory |
| `Clock` | turns `go` limits into a deadline / node budget and answers `should_stop` |

`lazy_smp.search` is the coordinator: it spawns worker processes, each running
its own iterative deepening `Negamax` against a shared `SharedTT`, and returns
the best completed result as a `SearchResult`. `__main__.py` is the UCI protocol
layer and the only place that prints `info` / `bestmove`.

## Implemented

### [Search](https://www.chessprogramming.org/Search)

- [Negamax](https://www.chessprogramming.org/Negamax) - fail-soft
- [Alpha-Beta Pruning](https://www.chessprogramming.org/Alpha-Beta)
- [Principal Variation Search](https://www.chessprogramming.org/Principal_Variation_Search) - full window on the first move, null-window scout + re-search on the rest
- [Null Move Pruning](https://www.chessprogramming.org/Null_Move_Pruning) - `R = 2..3`, skipped in check / zugzwang / at low depth, with a verification search at high depth
- [Late Move Reductions](https://www.chessprogramming.org/Late_Move_Reductions) - late quiet non-checking moves searched `1..3` plies shallower, full-depth re-search on a fail-high
- [Mate-distance pruning](https://www.chessprogramming.org/Mate_Distance_Pruning) - window clamped to the fastest mate still possible from the node
- [Quiescence Search](https://www.chessprogramming.org/Quiescence_Search) - fail-soft, depth-bounded, check-aware
- Draw detection - threefold repetition and the fifty-move rule scored `0` inside the tree (`CONTEMPT` hook for a non-zero draw score)
- [Transposition Table](https://www.chessprogramming.org/Transposition_Table) - Zobrist-keyed, EXACT / LOWER / UPPER bounds, mate scores rebased by ply on store/probe
- [Iterative Deepening](https://www.chessprogramming.org/Iterative_Deepening) - per worker, with UCI time management
- [Move Ordering](https://www.chessprogramming.org/Move_Ordering) - TT move, [MVV-LVA](https://www.chessprogramming.org/MVV-LVA) captures, promotions, [killers](https://www.chessprogramming.org/Killer_Heuristic), [history](https://www.chessprogramming.org/History_Heuristic)
- [Lazy SMP](https://www.chessprogramming.org/Lazy_SMP) - workers share a lock-free shared-memory TT
- Opening book (Stockfish-derived Polyglot)

### [Evaluation](https://www.chessprogramming.org/Evaluation)

- [PeSTO](https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function) - tapered mid-/end-game [piece-square tables](https://www.chessprogramming.org/Piece-Square_Tables), interpolated by game phase, [incrementally updated](https://www.chessprogramming.org/Incremental_Updates) on `EvalBoard.push` / `pop`
- Positional terms (`eval_terms`) - [passed](https://www.chessprogramming.org/Passed_Pawn) / [isolated](https://www.chessprogramming.org/Isolated_Pawn) / [doubled](https://www.chessprogramming.org/Doubled_Pawn) pawns, [bishop pair](https://www.chessprogramming.org/Bishop_Pair), [rook on open file](https://www.chessprogramming.org/Rook_on_Open_File), [knight outposts](https://www.chessprogramming.org/Outpost), [pawn-shield king safety](https://www.chessprogramming.org/King_Safety), [tempo](https://www.chessprogramming.org/Tempo); recomputed per call with the pawn terms cached on the pawn bitboards

## Backlog

### Search

- [Static Exchange Evaluation](https://www.chessprogramming.org/Static_Exchange_Evaluation) for capture ordering
- [Relative History Heuristic](https://www.chessprogramming.org/Relative_History_Heuristic)
- [Aspiration Windows](https://www.chessprogramming.org/Aspiration_Windows)
- [Syzygy endgame tablebases](https://www.chessprogramming.org/Endgame_Tablebases)

### Evaluation

- Stronger [king safety](https://www.chessprogramming.org/King_Safety) (attack-weight on the king zone, not just the pawn shield), [mobility](https://www.chessprogramming.org/Mobility), [backward pawns](https://www.chessprogramming.org/Backward_Pawn), king-distance scaling for passers
- [Evaluation](https://www.chessprogramming.org/Evaluation_Hash_Table) / [material](https://www.chessprogramming.org/Material_Hash_Table) hash tables; make the new positional terms incremental on `EvalBoard`

### Alternative search algorithms to evaluate

- [NegaC*](https://www.chessprogramming.org/NegaC*)
- [MTD(f)](https://www.chessprogramming.org/MTD\(f\))

(NegaScout / PVS is already implemented - see above.)
