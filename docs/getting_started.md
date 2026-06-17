# Getting started

A 15-minute onboarding for collaborators who want to **run the model, reproduce the
numbers, and explore operating points**. It assumes you know the physics; it does not
assume you know this codebase. For the full physics state read
`clock_EIT_consolidated.md` (v14); for code conventions read the module docstring at the
top of `../src/eit_cooling_tool.py`.

## 1. Install

```sh
pip install -r ../requirements.txt        # numpy, scipy, qutip 5.x, sympy, matplotlib; Python 3
```

QuTiP must be 5.x. Everything runs as plain scripts — there is no package to install, no
build step, and no service to start.

## 2. First run (under a second)

```sh
python ../src/eit_cooling_tool.py
```

This prints the **optical-spectrum table** for each delivery preset (every tone the atoms
see: frequency, Rabi, polarization, direction, nearest resonance, and whether it is
intended / repump / parasitic) and then runs 14 fast self-tests of the delivery model. If
the self-tests pass, your install is good. **Run this after any edit to that file** — it is
the fast smoke test.

## 3. Reproduce the headline numbers

```sh
python ../src/eit_cooling_tool.py --report       # full reports: spectrum + floor + dynamics (~45 s)
python ../src/eit_cooling_tool.py --regression    # the validation gate: benchmarked floors (~2 min)
```

`--regression` is the **trust anchor**: it re-derives the validated steady-state floors
(clean-Λ recoil limit 0.0072; full dual-end 0.0048; full single-end 0.0075). If these
numbers move, something is wrong — they are the benchmark the embedded engine was validated
against.

## 4. Read a single operating point

A run is driven by one `Config` object. Named, validated operating points are returned by
`preset(...)`:

```python
import sys; sys.path.insert(0, "src")          # from the repo root
from eit_cooling_tool import Config, preset, run, report

# one number, fast:
nbar, delta2 = run(preset("dual_end_optimal"))  # -> (<n_z>, servoed two-photon detuning)

# the full annotated report (knobs, spectrum, floor, populations, cooling time, regime):
report(preset("single_end_tagged_v14"))
```

The four presets are `dual_end_optimal`, `single_end_tagged`, `single_end_tagged_v14`
(retro-capped, 2f_A = 400 MHz), and `clean_lambda` (ideal 3-field reference). The `report`
output is organized as **KNOBS → OPTICAL SPECTRUM AT THE ATOMS → RESULT (⟨n_z⟩, P(n=0),
where the ground population sits) → COOLING DYNAMICS → regime/model/assumption notes** — read
top to bottom.

## 5. Explore your own operating point

Every experimental knob is a field on `Config` (detunings, Rabi ratio `OmR`, repumpers,
trap, field, tag AOM, retro efficiency …); each is documented inline where the dataclass is
defined in `src/eit_cooling_tool.py` (Section 2). Start from a preset and override:

```python
from dataclasses import replace
cfg = replace(preset("dual_end_optimal"), Delta=45.0, OmR=0.12)
nbar, delta2 = run(cfg)
```

To map the floor across a knob, use the built-in sweeps (they re-servo the two-photon
detuning at every point when `cfg.servo_delta2=True`):

```python
from eit_cooling_tool import sweep1d
import numpy as np
vals, nbars, d2s = sweep1d(cfg, "Delta", np.linspace(35, 60, 8))
```

Set `cfg.servo_delta2=False` for fast scouting (holds `delta2` fixed, ~15× faster);
`delta2_landscape()` scans `delta2` itself to show the cooling resonance and how tight the
lock must be.

## 6. The other engines (run each directly)

The centerpiece tool answers "what is the on-axis floor at this operating point?". The other
`src/` modules answer specific sub-questions and print/plot their own self-checks:

| run this | answers |
|---|---|
| `python src/tagged_solver.py` | validated tagged-EIT floor, single-ended retro (workhorse behind several figures) |
| `python src/radial_inhomogeneity.py` | radial-cloud average of the on-axis floor (reuses the validated engine) |
| `python src/radial_floor_mc.py` | semiclassical ensemble MC of the cloud floor (needs `data/rategrid.npz`) |
| `python src/raman_sbc.py` | resolved-sideband Raman engine, for the RSC-vs-EIT comparison |
| `python src/thermometry.py` | sideband-asymmetry thermometry / readout model |

## 7. Regenerate the figures

```sh
cd figures && for f in fig_*.py; do python3 "$f"; done
```

Each `fig_*.py` writes the matching `fig_*.png` from the engines in `src/`. See
`figures/README.md` for which engine and result each figure shows.

## 8. Where to read before changing a number

The `docs/` set is the authoritative record of the physics and design state. **Read the
relevant doc before changing the corresponding code or numbers**; the README's "Canonical
doc map" routes each topic to its file. Two things are easy to trip on and worth internal-
izing up front (both pinned in the tool's module docstring):

- **Units:** every optical frequency, detuning, and Rabi is **angular, written as ordinary
  frequency in 2π·MHz** — a literal `5` means 2π·5 MHz; `nu_z = 0.430` is 2π·430 kHz.
- **Reference:** the bare |F=2⟩→|F′=2⟩ transition is 0 MHz; "bluer" is more positive; every
  detuning is (field) − (transition). `delta2` is the primary two-photon knob and the EOM
  drive `f_mod` is derived from it. The docstring's "DETUNING REFERENCE" block (the 1064 nm
  trap subtleties) is required reading before trusting a repump or contaminant detuning.
