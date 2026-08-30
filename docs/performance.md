# Performance

All figures below are a fresh benchmark on one machine (Apple Silicon, 10
cores, Python 3.13), fixed-depth search from the starting position. "Before"
is the pre-review engine (plain negamax, no move ordering, no working TT,
unbounded quiescence, from-scratch material+PST eval); "After" is the current
engine. Both columns were run on the *same* machine, so this is a like-for-like
comparison rather than a comparison against the older M1 numbers.

For reference, the original M1 run recorded depth 5 = 1.42s, depth 6 = 10.0s,
depth 7 = 215s single-process (and the old "parallel" mode was *slower*: depth
7 = 430s).

## Single process, fixed-depth `search()` from the start position

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

## Single-process iterative deepening (removed - kept here for reference)

| target depth | time | nodes |
|-------------:|-----:|------:|
| 5 |  0.24s |  12k |
| 6 |  1.38s |  53k |
| 7 |  5.11s | 236k |
| 8 | 38.6s  | 2.1M |

This was the old `go` path (roughly 2x faster than a cold fixed-depth search,
since each iteration seeds the next through the TT). Lazy SMP beat it at every
depth on this machine, so it was dropped - `go` now always runs Lazy SMP.

## What `go` / `go depth N` runs today: Lazy SMP from the start position

| depth | Before ("parallel", root-split) | After (Lazy SMP, 9 workers, shared TT) |
|------:|--------------------------------:|--------------------------------------:|
| 6 |  10.6s | 0.84s |
| 7 | 430s   | 3.77s |
| 8 |  —     | 17.9s |

The old root-split parallel mode lost to its own single-threaded search (full
windows, no shared table). Lazy SMP is ~1.5x faster than the old single-process
iterative deepening at depth 6-7 and ~2x by depth 8, on this 10-core machine.
