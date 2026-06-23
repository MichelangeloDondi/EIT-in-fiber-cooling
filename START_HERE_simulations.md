# Cooling simulations — how to run and tune them

*A short orientation for the two simulation files. Both are single, self-contained
Python scripts; you change a few labelled numbers and re-run. No other files needed.*

---

## The two simulations, and which question each answers

**1. `eit_cooling_tool.py` — the cooler itself (axial floor).**
Set the laser detunings, powers, and the delivery method; it returns the steady-state
axial phonon number ⟨n_z⟩ (how close to the motional ground state a single atom on the
trap axis gets) and prints the exact optical spectrum that arrives at the atoms. This is
the tool for exploring the **operating point** and the **delivery hardware**.

**2. `cloud_cooling_tool.py` — a whole cloud (radial floor).**
The cooler above assumes one atom sitting on the axis. A real cloud has a radial spread,
and the trap's Gaussian beam makes the cooling detuning vary across that spread — so the
edge of the cloud cools poorly. This tool answers: **given a cloud with some radial
temperature, what mean phonon number is actually reachable, and how much do the two
proposed fixes (a flat-top trap, or a second cooling tone) help?**

They are companions: run #1 to pick the operating point, run #2 to see what a real cloud
does at that operating point.

---

## Install once

```
pip install numpy scipy sympy qutip matplotlib
```

(QuTiP 5.x. The cloud tool uses only numpy for its fast part and QuTiP once to build a
small cached table.)

---

## Run them

```
python eit_cooling_tool.py              # spectrum tables + 14 fast self-checks (<1 s)
python eit_cooling_tool.py --report     # full annotated operating-point report (~30 s)
python eit_cooling_tool.py --regression # reproduce the audited floors (the trust gate, ~2 min)

python cloud_cooling_tool.py            # the 4 cloud presets (builds tables, ~3 min first run)
python cloud_cooling_tool.py --regression   # reproduce the box-collapse + two-tone results
```

The `--regression` modes are the **trust gates**: they re-derive the numbers quoted in the
brief, so you can confirm the tools reproduce the audited results before trusting any knob
you turn yourself.

---

## The recommended operating point (master brief v17), and how to set it

| quantity | value | tool field |
|---|---|---|
| single-photon detuning Δ | **+45 MHz** | `Delta=45` |
| probe/control ratio Ω_p/Ω_c | **0.12** | `OmR=0.12` |
| delivery (preferred) | dual-end, carrier-suppressed | `configuration="dual_end"` |
| delivery (fallback) | single-ended tagged retro, 400 MHz tag | `configuration="single_end_tagged", tag_2fA=400` |
| magnetic field | 1.0–1.5 G (any field works) | `B_field=1.5` |

In the axial tool:
```python
from eit_cooling_tool import Config, run
nbar, d2 = run(Config(configuration="dual_end", Delta=45, OmR=0.12, B_field=1.5))   # ~0.0059 (0.0051 at OmR=0.10)
nbar, d2 = run(Config(configuration="single_end_tagged", Delta=45, OmR=0.12,
                      tag_2fA=400))                                                  # ~0.0072
```
*Note:* the shipped presets (`preset("dual_end_optimal")`, `preset("single_end_tagged")`) are
**already at the v17 point** (Δ=45 / OmR=0.12 / tag=400), so running a preset reproduces the printed
v17 numbers directly. **The probe lever — floor vs cooling rate, decoupled on purpose:** the nominal
**OmR=0.12** gives dual **0.0059** and cools **~1.4× faster** (on-axis rate W(0)≈0.0053 vs 0.0038 MHz);
dropping to **OmR=0.10** gives dual **0.0051** (clk2 deciding-solver **0.0048**) but ~1.4× slower — a
negligible floor gain (both ≳99.4%), so 0.12 is the operating nominal. The single-tagged floor is ~flat
at **0.0072**. *(The `--regression` gate uses a fast Fock truncation Nf=6 and prints dual ≈0.0048; a
converged `run()` at the default Nf prints ≈0.0059 — same physics, different truncation.)*

---

## What to turn to explore each question

| you want to explore… | tool | turn this | start from |
|---|---|---|---|
| how the floor depends on detuning Δ | axial | `Delta` | `preset("dual_end_optimal")` |
| the weaker-probe lever (the main one) | axial | `OmR` | dual_end_optimal |
| dual-end vs retro delivery | axial | `configuration` | both presets |
| the retro tag-AOM choice | axial | `tag_2fA`, `eta_dp` | single_end_tagged |
| repumper detunings / choice | axial | `Drep1`, `Drep2`, `repump_option` | dual_end_optimal |
| **flat-top vs Gaussian trap** | cloud | `profile` (`"gaussian"`/`"box"`) | `preset("box_flat_top")` |
| **how flat the trap must be (coverage)** | cloud | `r_flat_um` | box_flat_top |
| **how a hot vs cold cloud behaves** | cloud | `T_radial_uK` (100 cold, 556 hot) | gaussian_cooled / _uncooled |
| **one cooling tone vs two** | cloud | `n_tones` (1/2), `Delta2` | two_tone_hot |

Both tools take a `Config(...)` with these as named fields, and any field can be swept
(the axial tool has `sweep1d`/`sweep2d`; the cloud tool re-runs in seconds because it
caches the slow part). Open either file — the top-of-file header lists every knob with a
one-line explanation, and marks the handful of fixed atomic constants you should *not*
change.

---

## Extending the simulations — adding your own configuration

Both tools are made to be copied and tweaked. The pattern is the same: build a `Config(...)`
with the fields you want, or add a branch to `preset(name)`.

**Axial tool (`eit_cooling_tool.py`).** Explore a new operating point directly:
```python
from eit_cooling_tool import Config, run, report
cfg = Config(configuration="dual_end", Delta=50, OmR=0.11, B_field=1.5)
nbar, delta2 = run(cfg)     # -> steady-state axial floor <n_z>, and the servoed two-photon detuning
report(cfg)                 # -> full annotated spectrum + floor + cooling time + regime check
```
To make it permanent, add a branch to `preset(name)` (Section 4), next to `dual_end_optimal`.

**Cloud tool (`cloud_cooling_tool.py`).** Edit a `Config(...)` field or add a `preset(name)` branch.
The slow per-radius engine grid is cached (`cloudgrid_*.npz`), so re-running the Monte-Carlo after
changing a *radial* knob (`profile`, `r_flat_um`, `T_radial_uK`, `n_tones`) takes seconds. Changing
the *operating point* (`Delta`, `OmR`) rebuilds the grid automatically (~1 min, cached anew).

**Reading the output — pitfalls a successor will hit:**
- **Fock truncation `Nf`.** A floor is only trustworthy once `Nf` is large enough. The `--regression`
  gate uses `Nf=6` for speed and prints dual ≈0.0048; a converged `run()` (default `Nf`) prints
  ≈0.0059 at OmR=0.12. If a floor looks suspiciously low, raise `Nf` and re-check.
- **`N_orbits` (cloud).** A hot or under-covered cloud converges slowly; raise `N_orbits` (default
  300) for the 556 µK Gaussian case or the floor reads high.
- **The probe lever is the main floor/rate dial.** Lower `OmR` → lower floor but slower cooling
  (rate ≈ ∝ OmR²). The repo operates at OmR=0.12 for speed; 0.10 is the floor-optimal edge (see the
  operating-point note above).
- **Don't touch the fixed atomic constants.** The top-of-file header marks the physical constants
  (Clebsch-Gordan, hyperfine splittings, polarizabilities) that are validated against the multilevel
  solver and the literature — change the *operating point*, not those.
- **On macOS + numpy 2.0** you may see spurious `overflow/divide-by-zero in matmul` warnings from the
  Accelerate BLAS backend; the results are unaffected (the `--regression` gate is the backstop). More
  importantly, the **multilevel axial solves are dramatically slower** on numpy-2 + Accelerate — the
  full `eit_cooling_tool.py --regression` is ~2 min on numpy<2 / OpenBLAS but can take *tens of minutes
  per solve* here. The fast smoke test (`python src/engines/eit_cooling_tool.py`) and the whole
  `cloud_cooling_tool.py --regression` are unaffected. For the full axial gate, run on numpy<2 or a
  numpy built against OpenBLAS (e.g. a conda-forge build), or just trust the smoke test + the cloud gate.

---

## The two headline results to reproduce

1. **Axial floor ~0.005–0.006** (dual-end; the `Delta=45, OmR=0.12` run prints **0.0059**, ~0.0051 at OmR=0.10) — `run(Config(configuration="dual_end", Delta=45, OmR=0.12))`. That is ≳ 99.4 % ground-state population on the axis.
2. **The cloud floor collapses to ~the on-axis value for *any* cloud temperature once the
   trap is flat-topped** — `python cloud_cooling_tool.py` and compare the `gaussian_uncooled`
   preset (a hot cloud in today's Gaussian trap, floor ~0.04+) with `box_flat_top` (the same
   hot cloud in a flat-top trap, floor ~0.003). This is the single largest improvement in the
   program, and the one thing that needs the fiber to deliver a flat-top mode.

If those two reproduce, the tools are doing what the brief says, and every other knob is
yours to turn.
