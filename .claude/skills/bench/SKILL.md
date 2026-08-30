---
name: bench
description: >
  Run the search benchmarks and regenerate the tables in docs/performance.md
  with fresh, real numbers. Use when the user asks to "run the benchmarks",
  "update performance numbers", or after a change that should affect speed.
---

# bench

`docs/performance.md` must only ever contain **measured** numbers. This skill
produces them; never hand-edit timings.

## 1. Environment

```bash
pip install -e ".[dev]"
python -c "import platform, os; print(platform.processor() or platform.machine(), os.cpu_count(), 'cores'); print(platform.python_version())"
```

Record the machine and Python version - the tables in `docs/performance.md`
are labelled with them and results are machine-specific.

## 2. Fixed-depth single-process search (start position)

Regenerates the "After" column of the "Single process, fixed-depth `search()`"
table. A fresh `Negamax` per depth (cold TT), un-armed clock so it never aborts.
"Nodes" is `searcher.nodes` (main search + quiescence).

```python
import time
from pychess.clock import Clock
from pychess.constants import INF
from pychess.eval_board import EvalBoard
from pychess.evaluation import PestoEvaluator
from pychess.move_ordering import MoveOrderer
from pychess.negamax import Negamax
from pychess.transposition import TranspositionTable

for depth in range(2, 8):
    s = Negamax(PestoEvaluator(), MoveOrderer(), TranspositionTable(), Clock())
    t = time.time()
    s.search(EvalBoard(), -INF, INF, depth)
    print(f"| {depth} | {time.time() - t:.3f}s / {s.nodes:,} |")
```

## 3. Lazy SMP (start position)

Regenerates the "After" column of the "What `go` runs today: Lazy SMP" table.
Use a generous `movetime` so the run isn't deadline-capped.

```python
import time
from pychess.eval_board import EvalBoard
from pychess.engine import Engine

for depth in (6, 7, 8):
    t = time.time()
    r = Engine().search(EvalBoard(), {"depth": depth, "movetime": 120000})
    print(f"| {depth} | reached d{r.depth} | {time.time() - t:.2f}s | {r.nodes:,} nodes |")
```

Run each script with `.venv/bin/python` (or the active env). Steps 2 and 3
together take roughly a minute.

## 4. Update `docs/performance.md`

- Replace the "After (time / nodes)" cells in the fixed-depth table and the
  Lazy SMP table with the new numbers.
- Update the machine / Python-version sentence at the top of the file.
- **Leave alone:** the "Before" columns (pre-review engine, not reproducible),
  the M1 reference paragraph, and the "Single-process iterative deepening
  (removed)" table.
- Recompute the "speed-up" column from the new numbers.

## 5. Cross-check

If speed changed materially, check whether these still hold and flag (don't
silently rewrite) any that drifted:

- the `~45-50k nps` figure and the "depth ~6-8 in blitz" notes in
  `docs/engine-strength.md`.

## 6. Report

Show the old vs new table rows and the environment they were measured on.
