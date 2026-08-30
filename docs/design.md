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
- [Quiescence Search](https://www.chessprogramming.org/Quiescence_Search) - fail-soft, depth-bounded, check-aware
- [Transposition Table](https://www.chessprogramming.org/Transposition_Table) - Zobrist-keyed, EXACT / LOWER / UPPER bounds
- [Iterative Deepening](https://www.chessprogramming.org/Iterative_Deepening) - per worker, with UCI time management
- [Move Ordering](https://www.chessprogramming.org/Move_Ordering) - TT move, [MVV-LVA](https://www.chessprogramming.org/MVV-LVA) captures, promotions, [killers](https://www.chessprogramming.org/Killer_Heuristic), [history](https://www.chessprogramming.org/History_Heuristic)
- [Lazy SMP](https://www.chessprogramming.org/Lazy_SMP) - workers share a lock-free shared-memory TT
- Opening book (Stockfish-derived Polyglot)

### [Evaluation](https://www.chessprogramming.org/Evaluation)

- [PeSTO](https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function) - tapered mid-/end-game [piece-square tables](https://www.chessprogramming.org/Piece-Square_Tables), interpolated by game phase, [incrementally updated](https://www.chessprogramming.org/Incremental_Updates) on `EvalBoard.push` / `pop`

## Backlog

### Search

- [Static Exchange Evaluation](https://www.chessprogramming.org/Static_Exchange_Evaluation) for capture ordering
- [Relative History Heuristic](https://www.chessprogramming.org/Relative_History_Heuristic)
- [Aspiration Windows](https://www.chessprogramming.org/Aspiration_Windows)
- [Null Move Pruning](https://www.chessprogramming.org/Null_Move_Pruning)
- [Principal Variation Search](https://www.chessprogramming.org/Principal_Variation_Search)
- [Late Move Reductions](https://www.chessprogramming.org/Late_Move_Reductions)
- [Syzygy endgame tablebases](https://www.chessprogramming.org/Endgame_Tablebases)

### Evaluation

- [King safety](https://www.chessprogramming.org/King_Safety), [pawn structure](https://www.chessprogramming.org/Pawn_Structure) (doubled / isolated / passed), [mobility](https://www.chessprogramming.org/Mobility), [tempo](https://www.chessprogramming.org/Tempo)
- [Evaluation](https://www.chessprogramming.org/Evaluation_Hash_Table) / [material](https://www.chessprogramming.org/Material_Hash_Table) / [pawn](https://www.chessprogramming.org/Pawn_Hash_Table) hash tables

### Alternative search algorithms to evaluate

- [NegaScout](https://www.chessprogramming.org/NegaScout)
- [NegaC*](https://www.chessprogramming.org/NegaC*)
- [MTD(f)](https://www.chessprogramming.org/MTD\(f\))
