# Reproducing the bridge's computations

Every bridge result (falsification/V*/FINDINGS.md) states the environment it ran in. This folder pins that
environment.

- **`bridge_env.json`:** interpreter, platform, package versions, BLAS/LAPACK backend and git commit. Generate it with
  `python tools/envstamp.py ENVIRONMENT/bridge_env.json`.
- **`bridge_requirements.lock`:** `pip freeze` of the interpreter used for all bridge runs (V8–V12).
- **Machine:** Apple M-series (arm64), macOS 26.5 (25F71). numpy links Apple Accelerate; scipy links its bundled
  OpenBLAS (see the json).

## Interpreter
`/Users/sumit/Github/conjecture_machine/.venv` is CPython 3.14.5 (Homebrew build, clang 21). To recreate it elsewhere:
```
python3.14 -m venv .venv && .venv/bin/pip install -r ENVIRONMENT/bridge_requirements.lock
```

## Policy (fleet-wide, from 2026-10-11)
- Each repo commits a lock file plus an env stamp.
- Each FINDINGS or RESULTS entry carries one line: `Environment: Python X.Y.Z, numpy …, scipy …, sympy …, BLAS …,
  commit …`.
- Results produced before this policy are back-filled with the environment as it stands now, and marked "back-filled".
- For paper claims, the two independent implementations should run on different interpreters or library stacks where
  possible. This is a cheap extra layer of independence: the Python 3.12 tokenizer and heap issue found on 2026-10-11
  affected only one interpreter.
