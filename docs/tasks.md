# Tasks

The next five changes, roughly in priority order (Elo per unit of effort, and
how much each compounds with the rest). Each is a self-contained addition to
`Negamax` / `lazy_smp` / the evaluator unless noted. Elo figures are rough
community numbers for an engine already at this level - measure, don't trust.

## 1. Aspiration windows

Iterative deepening currently re-searches every depth with the full
`(-INF, INF)` window. Instead, open depth `d` with a narrow window around the
previous iteration's score (`score ± 25`, say); on a fail-high or fail-low
widen that side (double the delta, or jump to `±INF`) and re-search. Most
iterations land inside the window and search far fewer nodes. Lives in
`lazy_smp._worker`'s deepening loop, per worker. Pairs naturally with PVS.
~15-30 Elo, a small change.

## 2. Shallow-depth pruning (reverse futility, futility, late move pruning)

At low depth, near the leaves, prune aggressively on the static eval:

- **Reverse futility / static null move**: if `eval - margin*depth >= beta` at
  `depth <= ~6` and not in check, return `eval`.
- **Futility**: at `depth <= ~2`, if `eval + margin < alpha`, skip quiet moves
  that can't raise alpha.
- **Late move pruning**: past a depth-dependent move count at low depth, skip
  the remaining quiet non-checking moves entirely.

Never when in check, for captures/promotions, or near mate scores. Big node
reduction; the effective branching factor drops again. ~40-70 Elo combined, but
tune the margins carefully - too greedy and tactics start getting missed
(guard with the existing mate tests plus a WAC/ECM tactical suite).

## 3. Static Exchange Evaluation (SEE)

A `see(board, move) -> int` that plays out the capture sequence on one square
with the cheapest attacker each time. Two uses:

- **Move ordering**: order captures with `SEE < 0` *after* the quiet killers
  instead of just behind winning captures - `MoveOrderer` currently trusts
  MVV-LVA, which mis-ranks a queen grabbing a defended pawn.
- **Quiescence pruning**: in `Negamax.quiesce`, skip captures with `SEE < 0`
  entirely instead of searching every capture.

python-chess gives `board.attackers(color, square)` to build the attacker
lists. ~25-50 Elo, and it makes quiescence much cheaper.

## 4. Search extensions

Spend an extra ply where the tree is forcing so tactics are not missed at the
horizon:

- **Check extension**: `depth += 1` when the move gives check (cap total
  extensions per line so it can't blow up).
- **One-reply extension**: extend when the side to move has a single legal
  move.
- Later: **singular extensions** (re-search to prove the TT move is the only
  good one) - higher effort, do it after PVS/LMR are stable.

~15-25 Elo for the cheap two; more with singular.

## 5. Evaluation tuning harness (Texel's method)

The PeSTO tables and the new `eval_terms` weights are untuned for this engine.
Add `tools/tune.py`: label a few hundred thousand quiet positions with the game
result (from self-play PGNs or a public dataset), then fit every weight by
minimising the logistic error between `sigmoid(eval)` and the result. Keep the
weights in one place so the tuner can rewrite them. Unlocks the eval terms
already added and makes every future term measurable. ~30-100 Elo depending on
how untuned things currently are; the highest-ceiling item on this list.

### Also worth doing

- **Syzygy tablebases** (`chess.syzygy`): probe WDL/DTZ for <= 6 pieces at the
  root and in the search for perfect endgame play. Needs a `SyzygyPath` and the
  tablebase files (~150 GB for 6-man), so gate it on config and no-op when the
  files are absent.
- **UCI `setoption`**: `Hash`, `Threads`, `Contempt`, `SyzygyPath`,
  `MultiPV` - currently parsed and ignored.
- **2-fold repetition as a draw inside the search** (not just 3-fold): a
  position seen twice within the tree is almost always a forced draw; detecting
  it a repetition earlier saves nodes.

## Housekeeping

### GitHub repo settings (do these in the repo UI - not tracked in files)

- [ ] Rename the repo `pyChess` -> `pychess` so it matches the package name;
      update the local remote afterwards.

### Opening book (`opening_book/bookfish.bin`)

An ~18 MB binary lives in git history (see [opening_book/README.md](../opening_book/README.md)).
It works fine as-is, but for a cleaner repo consider one of: migrate it to Git
LFS, fetch it on first run instead of vendoring it, or document it as an
optional external download. Any of these needs a history rewrite to actually
shrink the pack, so it is a deliberate call, not a drive-by fix.
