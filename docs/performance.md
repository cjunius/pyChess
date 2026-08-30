# Performance

Fresh benchmark of the current engine (move ordering, TT, bounded quiescence,
null-move pruning, LMR, PVS, mate-distance pruning, hand-crafted eval terms) on
one machine: Apple Silicon, 10 cores, Python 3.14. Search is from the starting
position; rows stop once a search passes ~5 seconds. "Nodes" is the engine's
node counter (number of `Negamax.search` / `Negamax.quiesce` calls).

## What `go` / `go depth N` runs today: Lazy SMP from the start position

This is the real search path - `go` always runs Lazy SMP: 9 worker processes
each doing their own iterative deepening against one lock-free shared-memory TT.
A generous `movetime` so the run isn't deadline-capped.

| depth | time | nodes |
|------:|-----:|------:|
| 6 | 0.45s |  45,000 |
| 7 | 0.60s |  95,000 |
| 8 | 2.30s | 320,000 |

Depth 8 from the opening lands in ~2s on this 10-core machine, depth 9 in
~5–8s. These numbers vary run to run - the workers race and divide the tree
differently each time, and at shallow depths process startup dominates - so
they are rounded and representative, not exact.

## Single process, fixed-depth `search()` from the start position

A controlled baseline: one `Negamax`, a fresh (cold) TT per depth, clock never
armed. Deterministic, and it isolates search-tree efficiency from the Lazy SMP
speed-up, so this is the table to watch when judging whether a search change
helped. Not what the engine runs in a game.

The `perft(depth)` column is the size of the *full* legal game tree at that
depth from the start position (the published
[perft results](https://www.chessprogramming.org/Perft_Results) - leaf count at
exactly `depth` plies, no evaluation, no pruning). It is the branching the
search would face with no alpha-beta at all. `pruned` is `1 - nodes/perft`.

| depth | time | nodes | perft(depth) | pruned |
|------:|-----:|------:|-------------:|-------:|
| 2 | 0.003s |     182 |            400 |      55% |
| 3 | 0.008s |     463 |          8,902 |      95% |
| 4 | 0.034s |   1,840 |        197,281 |    99.1% |
| 5 | 0.132s |   6,943 |      4,865,609 |   99.86% |
| 6 | 0.344s |  17,728 |    119,060,324 |  99.985% |
| 7 | 1.462s |  67,810 |  3,195,901,860 | 99.998% |
| 8 | 3.690s | 178,647 | 84,998,978,956 | 99.9998% |

The `pruned` column is an *estimate*: the two counts aren't the same unit.
"nodes" is every `board.push` in the pruned tree (internal nodes and quiescence
included, and quiescence looks past `depth` in forcing lines); `perft` is only
the leaves at exactly `depth`. So it overstates pruning a little at shallow
depths and understates it once quiescence dominates - but the trend is real:
move ordering, the TT, and the reductions (null-move, LMR, PVS) take the tree
from "search half of it" to "search one node in ~475,000" by depth 8.

Consecutive `nodes` rows zigzag rather than growing smoothly: PVS makes odd
plies (side-to-move gets the last word) cheap relative to even ones.
