# Tasks

The next five changes, in the order most likely to gain the most playing
strength. Each is a self-contained addition to `Negamax.search` /
`Negamax.quiesce` unless noted.

## 1. Null-move pruning

If giving the opponent a free move (a "null move") still fails high at reduced
depth (`R = 2..3`), the position is almost certainly a cut-off - return `beta`
without searching the real moves. Skip it when side-to-move is in check, in a
likely zugzwang (king + pawns only), or when depth is very low. Add a
verification search at high depth to avoid zugzwang blunders. Needs a
`board.push(chess.Move.null())` path and a `_null_ok` guard in the search.
Typically the single largest Elo jump available (~50-100).

## 2. Principal Variation Search (NegaScout)

Search the first (best-ordered) move with the full `(-beta, -alpha)` window,
then every later move with a null window `(-alpha-1, -alpha)`; only re-search
with the full window on the rare fail-high. With the move ordering already in
place (TT move, MVV-LVA, killers, history) the first move is usually best, so
most nodes get the cheaper scout search. ~20-40 Elo and it compounds with
everything below.

## 3. Late Move Reductions (LMR)

Once past the first few moves at a node, search quiet, non-checking, non-TT
moves at `depth - 1 - reduction` (reduction grows with move index and depth,
shrink it for killers / good history). Re-search at full depth if the reduced
search beats `alpha`. Combined with PVS this is usually the biggest tree
reduction after null-move - effective branching factor drops sharply, so
iterative deepening reaches 2-4 plies deeper in the same time.

## 4. Correct draw, repetition and mate scoring

- Detect threefold repetition and the 50-move rule *inside* the search tree
  (`board.is_repetition(3)`, `board.halfmove_clock`), not just the automatic
  five-fold / seventy-five-move draws in `is_drawn`.
- Score every draw a flat `0` (currently negamax returns `0 - depth`), with an
  optional small contempt value.
- Store mate scores in the TT as distance-to-mate relative to the current ply
  (`score +/- ply` on store/probe) so `MATE_GUARD` can be removed and mate
  cut-offs actually propagate. This fixes real half-point losses and lets the
  engine convert forced mates faster.

## 5. Evaluation upgrade

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

## Recently completed

From the previous review passes: move ordering, transposition table, iterative
deepening + UCI time management, perft fix + tests, quiescence rewrite (bounded,
check-aware, fail-soft), tapered PeSTO evaluation with an incremental
accumulator, standard `info` output, resource-leak fixes, Lazy SMP with a
lock-free shared-memory TT (now the only search path - `go` always runs it), and
a rebuild of the search as composed collaborators (`Negamax` holds an evaluator
/ move orderer / TT / clock) instead of a mixin stack, with unit tests for each
piece.

Packaging & tooling: `src/pychess/` package layout, `pyproject.toml` (replacing
`requirements.txt` / `pytest.ini`), a `pychess` console entry point, Apache-2.0
license, `py.typed`, and Ruff (lint + format) + Mypy + pytest-cov (85% gate) in
CI, with `pre-commit` mirroring it locally.

## Housekeeping

### GitHub repo settings (do these in the repo UI - not tracked in files)

- [ ] Rename the repo `pyChess` -> `pychess` so it matches the package name;
      update the local remote afterwards.
- [ ] Tag `v0.1.0` and cut a **GitHub Release** from the `CHANGELOG.md` entry.

### Opening book (`opening_book/bookfish.bin`)

An ~18 MB binary lives in git history (see [opening_book/README.md](../opening_book/README.md)).
It works fine as-is, but for a cleaner repo consider one of: migrate it to Git
LFS, fetch it on first run instead of vendoring it, or document it as an
optional external download. Any of these needs a history rewrite to actually
shrink the pack, so it is a deliberate call, not a drive-by fix.
