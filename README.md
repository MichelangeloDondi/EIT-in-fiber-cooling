# EIT-in-fiber cooling — ⁸⁷Rb ground-state cooling in a kagome HCPCF

Modeling and design program for **clock-EIT sideband cooling** of ⁸⁷Rb to the motional
ground state in a 1064 nm **axial lattice inside a kagome hollow-core photonic-crystal fibre**,
on a **first-order field-insensitive clock pair** |1,−1⟩ / |2,+1⟩ → |F′=2, m′=0⟩. This repo holds
the validated solvers, a self-checking exploration tool, the consolidated technical brief, and
the paper plan.

## Headline results
- **Axial cooling-physics (solve) floor ⟨n_z⟩ ≈ 0.005** (dual-end) / **≈ 0.0072** (single-ended tagged retro; the 20–40 % retro reflectivity is **non-binding** at a 2f_A = 400 MHz tag) → >99 % *axial* ground-state population; field-insensitive at any B.
- **All-in single-atom floor ⟨n_z⟩ ≈ 0.012–0.019** once the anti-trap/leak increment (+0.007–0.012) is folded into the solve floor; cloud-inhomogeneity floor ≈ 0.0094 at 100 µK. The ~0.005/0.0072 figures are the cooling-physics floor, **not** the all-in number, and all floors carry a ~2× recycler-model band.
- Operating point: **Δ ≈ 45 MHz (flat 40–55), Ω_p/Ω_c = 0.12**; cloud-robust to ~100 µK (semiclassical MC).
- This is a **1D (axial) cooler**: the radial mode is not cooled (n̄_r ≈ 380 at 100 µK, ≈ 10 at 2.5 µK), so the 3D ground-state fraction is set by the radial temperature, not the axial floor. A designed route to lower the radial (compression + degenerate RSC + adiabatic transfer) is planned but unproven.

See `docs/clock_EIT_consolidated.md` (v14) for the full technical state and the conceptual path.

## Layout
- `docs/` — consolidated brief + per-topic findings + `papers/`
- `src/` — validated solvers + the exploration tool
- `data/` — inputs the scripts need (`rategrid.npz`)
- `figures/` — key figures

### Canonical doc map
| topic | authoritative doc |
|---|---|
| full technical state + history | `docs/clock_EIT_consolidated.md` (v14) |
| operating point (+ retro-cap) | `docs/operating_point.md` |
| experimental sequence | `docs/full_sequence_config.md` |
| laser / delivery / thermometry | `docs/architecture_delivery_thermometry.md` |
| radial inhomogeneity | `docs/radial_inhomogeneity_findings.md` |
| scheme comparison / tradeoffs | `docs/scheme_comparison.md`, `docs/configuration_tradeoffs.md` |
| 5P₃/₂ 1064 nm polarizability | `docs/polarizability_5P32_1064.md` |
| D1 / hybrid | `docs/D1_hybrid_findings.md` |
| paper plan | `docs/papers/paper_planning_memo.md` |

## Engines (`src/`)
| file | what it is |
|---|---|
| `eit_cooling_tool.py` | self-contained, self-checking exploration tool (embeds the validated engine) |
| `tagged_solver.py` | validated tagged-EIT steady-state solver (single-ended retro) |
| `raman_sbc.py` | Raman sideband-cooling engine (RSC vs EIT comparison) |
| `radial_inhomogeneity.py` | radial M1/M2/M3 light-shift physics |
| `radial_floor_mc.py` | semiclassical ensemble MC of the radial-cloud floor (needs `data/rategrid.npz`) |
| `thermometry.py` | sideband-thermometry / readout engine |

## The tool (`eit_cooling_tool.py`, v0.3.0)
Requirements: Python 3 + `numpy scipy sympy qutip` (5.x) `matplotlib` — `pip install -r requirements.txt`.

| command | what it does | time |
|---|---|---|
| `python src/eit_cooling_tool.py` | spectrum tables for the presets + 14 fast self-tests | < 1 s |
| `python src/eit_cooling_tool.py --report` | full reports (spectrum, floor, cooling dynamics, regime) | ~45 s |
| `python src/eit_cooling_tool.py --regression` | reproduce the validated floors (the validation gate) | ~2 min |

Presets: `dual_end_optimal`, `single_end_tagged`, `single_end_tagged_v14` (retro-capped, 2f_A = 400), `clean_lambda`.
```python
from eit_cooling_tool import Config, preset, run, report
nbar, delta2 = run(preset("single_end_tagged_v14"))
report(preset("dual_end_optimal"))
```

## Status
The internal physics budget is closed: scheme, operating point, both delivery architectures, the
F′=0–3 contaminant budget, the optimized repumpers, the radial cloud, the anti-trap, and
field-insensitivity all agree. Remaining open items are bench-resident (the as-built 6.835 GHz
two-photon linewidth; the radial pre-cool + ferrule load-in number) and the applications
OD-vs-cooling question (`docs/clock_EIT_consolidated.md` §11).

License: `LICENSE`. Citation: `CITATION.cff`.
