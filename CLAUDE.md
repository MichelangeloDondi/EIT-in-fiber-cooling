# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A physics **modeling and design program** (not a deployed application) for clock-EIT
sideband cooling of ⁸⁷Rb to the motional ground state in a 1064 nm axial lattice inside a
kagome hollow-core photonic-crystal fibre. It ships validated numerical solvers, a
self-checking exploration tool, figure generators, and a set of authoritative technical
documents. There is no package, no build step, no service, and no CI — work is run as
standalone Python scripts and verified against an internal regression gate.

## Commands

Install: `pip install -r requirements.txt` (numpy, scipy, qutip 5.x, sympy, matplotlib; Python 3).

Primary tool (`src/engines/eit_cooling_tool.py`):
- `python src/engines/eit_cooling_tool.py` — spectrum tables for the presets + 14 fast self-tests (< 1 s). **This is the fast smoke test; run it after any edit to that file.**
- `python src/engines/eit_cooling_tool.py --report` — full reports: spectrum, floor, cooling dynamics, regime (~45 s).
- `python src/engines/eit_cooling_tool.py --regression` — **the validation gate**: reproduces the benchmarked steady-state floors (~2 min). Run this after any change touching the atomic engine or delivery model and confirm the floors are unchanged.

Other engines are run directly and print/plot their own self-checks, e.g. `python src/engines/tagged_solver.py`, `python src/engines/raman_sbc.py`, `python src/engines/radial_inhomogeneity.py`, `python src/engines/thermometry.py`. `python src/engines/radial_floor_mc.py` needs `data/rategrid.npz`.

Regenerate figures: `cd figures && for f in fig_*.py; do python3 "$f"; done` (each `fig_*.py` writes the matching `fig_*.png` from the engines in `src/engines/`).

There is no separate test runner: the tests *are* the in-file `_selftests()` and the `--regression` gate.

## Architecture

**`src/engines/eit_cooling_tool.py` is the centerpiece** — a single ~2000-line self-contained file
organized into numbered sections (see its module docstring's table of contents). Two
logically distinct halves live in it:
- **Delivery / spectrum model** (Section 3): maps hardware knobs (EOM depth/frequency, sideband orders, tagging AOM, quarter-wave plate, retro efficiency) onto the explicit set of optical tones at the atoms. This is where the delivery *architectures* differ: `dual_end`, `single_end` tagged retro, and ideal `clean_lambda`. Selected via named `preset(...)` strings on a `Config`.
- **Atomic engine** (Section 6): a multilevel QuTiP Lindblad steady-state solver (8-state Breit-Rabi ground manifold; tensor-diagonalized 5P₃/₂ F′=0..3; Clebsch-Gordan dipole couplings; multi-rotating frame; recoil). **It is included verbatim from a separately validated solver.** The regression gate (Section 6b) reproduces the validated floors so reported numbers match the benchmarked ones. Treat the engine internals as frozen: changes here must keep `--regression` numbers identical, or the change is wrong.

Public API of the tool: `Config`, `preset(name)`, `run(cfg) -> (nbar, delta2)`, `report(cfg)`.

The other validated engines in `src/engines/` answer specific sub-questions; several
**reuse the validated engine** rather than reimplementing it:
- `tagged_solver.py` — validated tagged-EIT steady-state floor (single-ended retro); the workhorse behind several figures.
- `radial_inhomogeneity.py` / `radial_floor_mc.py` — radial-cloud average of the on-axis floor (`radial_inhomogeneity.py` calls `eit_cooling_tool.run`/`Config` unchanged; `radial_floor_mc.py` is a semiclassical ensemble MC over `data/rategrid.npz`).
- `raman_sbc.py` — standalone resolved-sideband Raman engine for the RSC-vs-EIT comparison (deliberately *not* a wrap of the dark-resonance engines).
- `thermometry.py` — sideband-asymmetry thermometry / readout model.

`src/tools/` holds supporting scripts (diagnostics, paper-T computations, sensitivity checks) that
import the engines but are not part of the validated-engine set.

`docs/` is the authoritative record of the physics and design state — **read the relevant
doc before changing the corresponding code or numbers.** `docs/clock_EIT_consolidated.md`
(v17) is the consolidated technical brief and history; the top-level `INDEX.md` is the authority
router that maps each settled question (operating point, delivery, radial, polarizability, floors)
to its authoritative file.

## Conventions that are easy to get wrong

These are pinned in the `src/engines/eit_cooling_tool.py` module docstring and assumed throughout:
- **All optical frequencies, detunings, and Rabi frequencies are ANGULAR, written as ordinary frequency in 2π·MHz** — a literal `5` means 2π·5 MHz. Trap frequencies too (`nu_z = 0.430` = 2π·430 kHz).
- **Single frequency reference:** the bare |F=2⟩→|F′=2⟩ transition is defined as 0 MHz; "bluer" = more positive. Every detuning is (field) − (transition).
- **Sign conventions:** `Delta > 0` is blue of |F′=2⟩ (blue-detuned EIT cooling). `delta2` is the primary two-photon knob; the EOM drive `f_mod` is *derived* from it per configuration (a numeric `f_mod` overrides, and `delta2` is then reported back as derived).
- **Detuning-reference subtleties with the 1064 nm trap** (the docstring's "DETUNING REFERENCE" block is required reading before trusting a number): `delta2` is referenced to the ground hyperfine splitting and is trap-independent to leading order; `Delta` is referenced to the actual in-trap on-axis |F′2,0⟩ transition; repump/contaminant detunings are referenced to *bare* 5P₃/₂ hyperfine spacings and omit the differential tensor Stark shift (a known, documented limitation — see the ROADMAP note in the docstring).
- Reported floors are evaluated at the magic field; the cooling floor is field-insensitive, so the 1 G cooling default and the regression anchor agree.

## Git workflow

The v17 consolidation merged via PR #8; the pedagogical layer (guide + figures + reference/src
restructure + the 0.0118 retraction) plus the 2026-06 cross-chat figure red-team (multilevel cloud
figure added; `fig_knobspace`/`radial_survival` fixes; `fig_retro_flatness`/`fig_delta2_landscape`
flagged for a compute-bound regen — INDEX §4) merged via **PR #10**. Start a new `claude/*` branch
for further work. Commit with clear messages and push with `git push -u origin
<branch>`. Do not push to other branches or open PRs unless explicitly asked.

Project version: **0.3.0**, single source `CITATION.cff` (the redundant empty `0.3.0` marker file
was removed in the v17 tidy; the README cites no version). Keep `CITATION.cff` authoritative when bumping.
