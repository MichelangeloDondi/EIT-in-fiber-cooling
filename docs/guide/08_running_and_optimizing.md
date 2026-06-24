# 08 · Running & optimising the model

*The two simulations that make this program runnable — how to reproduce every number, then turn the
knobs yourself.*
[← Thermometry](07_thermometry_and_analysis.md) · [Guide cover (README) →](../../README.md)

---

## The two PI tools

The whole program reduces to two self-contained Python scripts. Run #1 to pick the operating point,
run #2 to see what a real cloud does at that point.

| tool | question it answers | output |
|---|---|---|
| **`src/engines/eit_cooling_tool.py`** | the **axial** floor — how close to the ground state one atom on the axis gets, for a given operating point and delivery | steady-state ⟨n_z⟩ + the exact optical spectrum at the atoms |
| **`src/engines/cloud_cooling_tool.py`** | the **radial/cloud** floor — what a cloud at temperature T_r reaches, and how much a flat-top or a second tone helps | cloud ⟨n_z⟩ vs profile, coverage, T_r, tone count |

```bash
pip install -r requirements.txt               # numpy(<2) scipy qutip(5.x) sympy matplotlib

python src/engines/eit_cooling_tool.py           # spectrum tables + 14 fast self-checks (<1 s) — the smoke test
python src/engines/eit_cooling_tool.py --report  # full annotated operating-point report (~30 s)
python src/engines/eit_cooling_tool.py --regression   # reproduce the audited axial floors (the trust gate)
python src/engines/cloud_cooling_tool.py --regression # reproduce the box-collapse + two-tone crossover (~3 min)
```

The `--regression` modes are the **trust gates**: they re-derive the numbers the guide quotes, so you
confirm the tools reproduce the audited results *before* trusting any knob you turn. Run the smoke test
after any edit to the axial tool.

## The knob → tool table

Everything is a `Config(...)` field; any field can be swept (the axial tool has `sweep1d`/`sweep2d`,
the cloud tool caches the slow part and re-runs in seconds).

| to explore… | tool | turn this | start from |
|---|---|---|---|
| floor vs detuning Δ | axial | `Delta` | `preset("dual_end_optimal")` |
| the weaker-probe lever (the main one) | axial | `OmR` | dual_end_optimal |
| dual-end vs retro delivery | axial | `configuration` | both presets |
| the retro tag-AOM choice | axial | `tag_2fA`, `eta_dp` | single_end_tagged |
| repumper detunings | axial | `Drep1`, `Drep2` | dual_end_optimal |
| **flat-top vs Gaussian trap** | cloud | `profile` (`gaussian`/`box`) | `preset("box_flat_top")` |
| **how flat the trap must be** | cloud | `r_flat_um` | box_flat_top |
| **hot vs cold cloud** | cloud | `T_radial_uK` (100 cold, 556 hot) | gaussian_cooled / _uncooled |
| **one cooling tone vs two** | cloud | `n_tones`, `Delta2` | two_tone_hot |

```python
# run from the repo root; sys.path is set automatically when running the script directly
from eit_cooling_tool import Config, run, report
cfg = Config(configuration="dual_end", Delta=50, OmR=0.11, B_field=1.5)
nbar, delta2 = run(cfg)     # steady-state axial floor + the servoed two-photon detuning
report(cfg)                 # full spectrum + floor + cooling time + regime check
```

To make a new point permanent, add a branch to `preset(name)`. The top of each file lists every knob
with a one-line explanation and marks the fixed atomic constants you must **not** change.

## Two traps a successor will hit

- **Fock truncation `Nf`.** A floor is only trustworthy once `Nf` is large enough. The `--regression`
  gate uses Nf=6 for speed and prints dual ≈ 0.0048; a converged `run()` prints ≈ 0.0059 at OmR=0.12 —
  same physics, different truncation. If a floor looks suspiciously low (or, for a hot cloud,
  suspiciously *settled*), raise Nf and re-check. This exact failure produced — and retracted — a cloud
  number (Chapter 06).
- **numpy 2 on macOS is correct but slow.** `requirements.txt` pins `numpy<2` for a reason: numpy 2 +
  macOS Accelerate gives *identical* numbers but makes the multilevel solves ~10× slower (tens of
  minutes per solve). The smoke test and the cloud gate are fine on numpy 2; for the full axial gate use
  numpy<2 or an OpenBLAS build. Do **not** relax the pin on a "numbers match" test — that misses the
  point (it is a reproduce-in-reasonable-time bar).

---

**Go deeper →** the full run/tune walkthrough, the extending-the-tools patterns, and the two headline
results to reproduce are [`START_HERE_simulations.md`](../../START_HERE_simulations.md); the validated
engine list with gate values is [INDEX §5](../../INDEX.md); the audited number→script ledger is
[`CLAIMS.md`](../../CLAIMS.md).
