# Engine Strength

**Estimated rating: ~1950–2150 Elo** (FIDE / CCRL-ish scale) at blitz, most
likely around **2050**, with wide error bars (±150).

This is a reasoned estimate from the feature set and search speed, **not a
measured result** — no games against rated opposition or a reference engine
have been run yet. See [Measuring it properly](#measuring-it-properly) below.

This estimate was re-derived after the search rebuild (null-move pruning, LMR,
PVS, mate-distance pruning, correct draw / mate scoring) and the first pass of
hand-crafted evaluation terms landed — see `CHANGELOG.md`. The previous figure
(~1900) predated all of that.

## How the estimate is derived

### What pulls it up

| Component | Contribution |
|---|---|
| PeSTO tapered evaluation | A genuinely strong minimal eval — a fast engine with *only* PeSTO plays ~2000+. Understands piece activity, king centralisation in endgames, pawn advancement. |
| Hand-crafted eval terms on top (passed / isolated / doubled pawns, bishop pair, rook on open file, knight outposts, pawn-shield king safety, tempo) | Fills the biggest PeSTO blind spots. Basic king safety removes a class of "walked into an attack" losses. Untuned, so conservatively worth +30–100 over bare PeSTO. |
| Modern search: alpha-beta + PVS + null-move pruning + LMR + mate-distance pruning, over a Zobrist TT with iterative deepening | The standard reduction stack. Reaches 2–4 plies deeper than plain alpha-beta for the same time — the single biggest strength factor after the eval. |
| Move ordering: TT move, MVV-LVA, promotions, killers, history | Good enough that the tree is near-optimally shaped and the reductions above pay off. |
| Check-aware, depth-bounded quiescence with delta pruning | Won't hang pieces or miss short forcing tactics / mates inside the horizon. |
| Correct mate & draw scoring | Distance-to-mate scores propagate through the TT; threefold / fifty-move draws are seen inside the tree. Removes a class of half-point losses and slow conversions. |
| Lazy SMP over ~9 cores | ~2–3x effective speed-up, so a ply or two deeper again in real games. |
| Opening book (Stockfish-derived Polyglot) | Avoids early disasters. Worth roughly +50–150. |

### What holds it down

- **Pure Python, ~45–50k nps per core** — roughly 1000x slower than a compiled
  engine. With Lazy SMP and the reductions it reaches depth ~8–9 from the
  opening in a few seconds ([performance.md](performance.md)); a blitz
  middlegame runs ~7–9 plies in quiet positions, ~5–7 in sharp ones. This is
  now the dominant ceiling.
- **Eval weights are untuned.** PeSTO's tables plus the new terms have never
  been fit to this engine's own games, so some terms may be pulling against
  each other. A Texel-style tuning pass is the highest-ceiling item left.
- **No shallow-depth pruning or aspiration windows.** Reverse-futility /
  futility / late-move pruning and a narrowed root window would each buy more
  depth; SEE would sharpen capture ordering and quiescence.
- **King safety is only a pawn-shield term** — no attacker-count / attack-weight
  model, so a slow piece build-up against the king is under-valued until it is
  nearly a threat.
- **No search extensions** (check / one-reply / singular), so some tactics are
  still missed right at the horizon.
- **Endgame technique is thin** — no tablebases, and a PST-based eval converts
  won endings slowly.

## Calibration against known engines

- **TSCP 1.81** (C; alpha-beta, quiescence, hash, history, iterative deepening,
  *no* null-move) is ~1700–1750 CCRL blitz. This bot has a clearly better
  search and eval but runs ~20x slower — net clearly ahead, ~2000–2150.
- **Sungorus 1.4** (C; null-move, LMR, PST eval, ~1M nps) is ~2330 CCRL. This
  bot has a comparable search stack and a comparable-or-better hand-crafted
  eval, but ~20x fewer nps costs ~150–250 → ~2050–2200.
- **CT800 / Claudia** class (~2300–2400) sit above this bot, mostly on speed
  and eval tuning.

## Time-control sensitivity

| Time control | Estimate | Why |
|---|---|---|
| Bullet (1+0) | ~1750–1900 | Python per-move and Lazy SMP process-spawn overhead dominate. |
| Blitz (3+2 / 5+3) | ~1950–2150 | Reaches depth 8–10. |
| Rapid / Classical | ~2150–2300 | Reaches depth 11–13+; a PST-based eval scales well with depth. |
| Lichess bot pool | ~2050–2300 blitz | Bot ratings there tend to run higher than CCRL. |

## Where the number would move

Completing the [roadmap](tasks.md):

- Aspiration windows + shallow-depth pruning + SEE + extensions: historically
  **+80–180 Elo** combined at this level, and they compound with the reductions
  already in place.
- Texel-tuned eval weights: **+30–100**, possibly more given how untuned things
  are now.
- Deeper king safety, mobility, Syzygy tablebases: another **+50–150**.

That would put an engine of this design in the **2300–2500** range, bounded
mainly by nps (a Cython / bitboard rewrite or PyPy would lift the ceiling).

## Measuring it properly

To turn this into a measured rating (±50 or so):

1. Install Stockfish and cap it to fixed skill levels or a fixed node count.
2. Run a few hundred fast games as a gauntlet (e.g. via `cutechess-cli` or a
   small `python-chess` match harness) from a balanced set of opening
   positions.
3. Anchor the result to the opponent's known rating.
