# Consistency gate

`check.py` is the repository's self-consistency gate. It enforces that the
single source of truth (`src/operating_point.py`) and the rest of the repo
agree, so a parameter migration can't silently reach some files and not others.

```
python3 audit/check.py          # fast: SSOT + engine constants + stale-value scan
python3 audit/check.py --slow   # additionally runs the full tagged_solver self-test
```

**HARD checks** (non-zero exit on failure): SSOT internal consistency; the
engine's constants match the SSOT (read by import, or by regex if qutip is
absent); no superseded operating point (Δ=55/OmR=0.10) in code presets; no
stale floors in the master doc; the README headlines the all-in floor.

**SOFT checks** (reported, non-fatal): the remaining prose reconciliation
sweep — docs still stating the old operating point, and the δ₂ sign convention.

CI runs the fast gate on every push (`.github/workflows/consistency.yml`).
