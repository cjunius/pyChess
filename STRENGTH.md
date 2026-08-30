# Playing Strength Estimate

**Estimated rating: ~1800–2000 Elo** (FIDE / CCRL-ish scale) at blitz, most
likely around **1900**, with wide error bars (±150).

This is a reasoned estimate from the feature set and search speed, **not a
measured result** — no games against rated opposition or a reference engine
have been run yet. See [Measuring it properly](#measuring-it-properly) below.

## How the estimate is derived

### What pulls it up

| Component | Contribution |
|---|---|
| PeSTO tapered evaluation | The biggest single factor. PeSTO is a genuinely strong minimal eval — a fast engine with *only* PeSTO plays ~2000+. It understands piece activity, king centralization in endgames, and pawn advancement. |
| Alpha-beta + transposition table + iterative deepening + move ordering (TT move, MVV-LVA, killers, history) | A solid, modern search core. Move ordering is good enough that the search tree is near-optimally shaped. |
| Check-aware, depth-bounded quiescence | Won't hang pieces or miss short forcing tactics / mates inside the horizon. |
| Opening book (Stockfish-derived Polyglot) | Avoids early disasters. Worth roughly +50–150. |

### What holds it down

- **No null-move pruning, LMR, PVS, or search extensions.** Engines with these
  search ~2–4 plies deeper for the same time. This alone is worth an estimated
  250–400 Elo and is the main gap between this bot and a "strong hobby engine".
- **Evaluation has no king-safety or pawn-structure terms.** An opponent who
  keeps the position closed, avoids tactics, and slowly builds a kingside
  attack can exploit this — the bot won't see the attack coming until material
  is already falling.
- **Pure Python, ~45–50k nps** — roughly 1000x slower than a compiled engine.
  In a blitz middlegame it reaches depth ~6–8 in quiet positions, ~4–6 in
  sharp ones.
- Incomplete draw / repetition handling can cost the occasional half-point.

## Calibration against known engines

- **TSCP 1.81** (C; alpha-beta, quiescence, hash, history, iterative deepening,
  *no* null-move) is ~1700–1750 CCRL blitz. This bot has a clearly better
  evaluation and move ordering, but is much slower and searches no deeper
  structurally → roughly a wash, maybe slightly above.
- **Sungorus / CT800 / Claudia** class (null-move + LMR) sit ~2000–2200. This
  bot is a notch below them.

## Time-control sensitivity

| Time control | Estimate | Why |
|---|---|---|
| Bullet (1+0) | ~1600–1750 | Python per-move overhead dominates. |
| Blitz (3+2 / 5+3) | ~1850–2000 | Reaches depth 6–8. |
| Rapid / Classical | ~2000–2150 | Reaches depth 9–10+; PeSTO scales well with depth. |
| Lichess bot pool | ~1950–2200 blitz | Bot ratings there tend to run higher than CCRL. |

## Where the number would move

Completing the [README To Do list](README.md#to-do):

- Null-move pruning + LMR + PVS + aspiration windows: historically **+250–400 Elo**.
- King-safety + pawn-structure evaluation terms: another **+100–200**.

That would put an engine of this design in the **2300–2500** range, bounded
mainly by nps (a Cython/bitboard rewrite or PyPy would lift the ceiling).

## Measuring it properly

To turn this into a measured rating (±50 or so):

1. Install Stockfish and cap it to fixed skill levels or a fixed node count.
2. Run a few hundred fast games as a gauntlet (e.g. via `cutechess-cli` or a
   small `python-chess` match harness) from a balanced set of opening
   positions.
3. Anchor the result to the opponent's known rating.
