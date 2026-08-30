---
name: bench
description: >
  Run the search benchmarks and regenerate the tables in docs/performance.md
  with fresh, real numbers. Use when the user asks to "run the benchmarks",
  "update performance numbers", or after a change that should affect speed.
---

# bench

`docs/performance.md` must only ever contain **measured** numbers for the
current engine. This skill produces them; never hand-edit timings.

## 1. Environment

```bash
pip install -e ".[dev]"
python -c "import platform, os; print(platform.processor() or platform.machine(), os.cpu_count(), 'cores'); print(platform.python_version())"
```

Record the machine and Python version - the tables in `docs/performance.md`
are labelled with them and results are machine-specific.

## 2. Fixed-depth single-process search (start position)

Regenerates the "Single process, fixed-depth `search()`" table - the controlled
baseline, second in the file. A fresh `Negamax` per depth (cold TT), un-armed
clock so it never aborts. "Nodes" is `searcher.nodes` (main search +
quiescence). Stop adding rows once a search passes ~5 seconds.

```python
import time
from pychess.clock import Clock
from pychess.constants import INF
from pychess.eval_board import EvalBoard
from pychess.evaluation import PestoEvaluator
from pychess.move_ordering import MoveOrderer
from pychess.negamax import Negamax
from pychess.transposition import TranspositionTable

for depth in range(2, 12):
    s = Negamax(PestoEvaluator(), MoveOrderer(), TranspositionTable(), Clock())
    t = time.time()
    s.search(EvalBoard(), -INF, INF, depth)
    dt = time.time() - t
    print(f"| {depth} | {dt:.3f}s | {s.nodes:,} |")
    if dt > 5:
        break
```

## 3. Lazy SMP (start position)

Regenerates the "What `go` runs today: Lazy SMP" table - the real search path,
first in the file. Use a generous `movetime` so the run isn't deadline-capped.
Stop once a search passes ~5s. Node counts and times vary run to run; take one
clean run and note that in the file.

```python
import time
from pychess.eval_board import EvalBoard
from pychess.engine import Engine

for depth in range(6, 12):
    t = time.time()
    r = Engine().search(EvalBoard(), {"depth": depth, "movetime": 120000})
    dt = time.time() - t
    print(f"| {depth} | {dt:.2f}s | {r.nodes:,} |")
    if dt > 5:
        break
```

Run each script with `.venv/bin/python` (or the active env). Steps 2 and 3
together take roughly a minute.

## 4. Update `docs/performance.md`

- Replace the rows in both tables with the new numbers.
- The single-process table's `perft(depth)` column is the published start-position
  perft sequence (400 / 8,902 / 197,281 / 4,865,609 / 119,060,324 /
  3,195,901,860 / 84,998,978,956 for depths 2-8) - static, only extend it if you
  add deeper rows. Recompute the `pruned` column as `1 - nodes/perft` from the
  fresh node counts.
- Update the machine / Python-version sentence at the top of the file.
- Keep both tables trimmed to where the time is ~5s or less - drop or add rows
  as the numbers move.

## 5. Cross-check

If speed changed materially, check whether these still hold and flag (don't
silently rewrite) any that drifted:

- the `~45-50k nps` figure and the blitz / rapid depth notes in
  `docs/engine-strength.md`.

## 6. Report

Show the old vs new table rows and the environment they were measured on.
