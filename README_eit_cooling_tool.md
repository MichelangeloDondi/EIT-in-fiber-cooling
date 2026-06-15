# EIT Cooling Tool — `eit_cooling_tool.py`

A single, self-contained Python file to **audit and explore** clock-EIT ground-state
sideband cooling of ⁸⁷Rb in the 1064 nm intra-fiber **axial** lattice (kagome HCPCF).
Given a `Config` of every experimental knob, it returns the steady-state axial mean
phonon number ⟨n_z⟩ from a multilevel QuTiP engine, and prints the explicit optical
spectrum that arrives at the atoms.

The atomic engine (Section 6 of the file) is **embedded verbatim** from the validated
solver that reproduces every number in the cooling program; the `--regression` mode
re-derives those numbers, so the tool is self-checking rather than a fresh re-derivation.

---

## Requirements
Python 3 with `numpy`, `scipy`, `sympy`, `qutip` (5.x), `matplotlib`. No other files.

```
pip install numpy scipy sympy qutip matplotlib
```

## Run modes
| command | what it does | time |
|---|---|---|
| `python eit_cooling_tool.py` | print the spectrum table for the 3 presets + 14 fast self-tests | < 1 s |
| `python eit_cooling_tool.py --report` | full operating-point reports (dual-end + single-end) | ~30 s |
| `python eit_cooling_tool.py --regression` | reproduce the audited floors (the validation gate) | ~2 min |
| `python eit_cooling_tool.py --sweeps` | write example sweep figures (PNG) | ~3 min |

## Programmatic use
```python
from eit_cooling_tool import Config, preset, run, report, build_spectrum, \
                             print_spectrum_table, sweep1d, plot_sweep1d

cfg = preset("dual_end_optimal")          # "single_end_tagged" | "clean_lambda"
nbar, delta2 = run(cfg)                    # steady-state <n_z>, servoed delta2
report(cfg)                                # full annotated report (model/assumptions/non-idealities)

# change any knob (everything is a Config field):
cfg = Config(configuration="dual_end", Delta=50, OmR=0.08, B_field=1.0, repump_option="A")
print_spectrum_table(cfg, build_spectrum(cfg))

# sweep any knob, reusing the engine:
v, nb, d2 = sweep1d(cfg, "Delta", [45, 55, 65, 80])
plot_sweep1d(v, nb, "Delta", "delta_scan.png", d2s=d2)
```
`run(cfg, want_pops=True)` also returns ground-state populations.
`sweep1d/sweep2d` accept `servo_grid=` (coarser = faster); `delta2_landscape(cfg)` maps the
dark-resonance cooling curve directly.

---

## Config knobs (everything you can vary)
All in `2π·MHz` (trap frequencies too: `nu_z=0.430` means 2π·430 kHz). Detunings positive = blue.

**(a) delivery** — `configuration`: `"dual_end"` (preferred), `"single_end_tagged"`, or `"clean_lambda"` (ideal reference).

**(b) detunings** — `Delta` (single-photon, blue of F′=2; default 55); `delta2` (**primary** two-photon detuning, default 0 — `f_mod` is derived from it); `Drep1` (15); `Drep2` (5).

**(c) intensities** — `OmR` = Ω_p/Ω_c (the key lever, default 0.10); `Omega_rep` (each repumper, 3); `Omega_tot_abs` (default `None` → Ω_tot pinned to √(4·Δ·ν_z); set a number to override).

**(d) EOM / comb** — `f_mod` (default `"auto"` → derived from `delta2`; a number overrides and `delta2` is reported back); `beta` (default `"auto"` → 2.4048 for dual-end carrier suppression, or the depth giving `OmR` for single-end); `probe_order` (which sideband is the probe; 1 = fundamental, 2 = use the 2nd overtone with f_mod≈A_HFS/2); `keep_orders` (sidebands to include in the spectrum).

**(e) retro / tag (single-end only)** — `tag_2fA` (double-passed AOM down-shift, 300); `eta_dp` (round-trip efficiency, 0.5); `quarter_wave` (helicity flip on the return, `True`).

**(f) repump** — `repump_option`: `"A"` (rep2 = F=2→F′1, σ⁺) or `"C"` (F=2→F′2, π). rep1 is always F=1→F′1, σ⁻.

**(g) apparatus / trap** (tunable — a different lattice changes these) — `nu_z` (0.430); `nu_r` (0.00542); `U0_uK` (1094); `eta_z` (axial Lamb-Dicke, 0.094).

**(h) engine** — `B_field` (G; cooling works at any field, 3.2287 G is clock-magic, default); `N_f` (Fock truncation, 6); `with_e0`/`with_e1`/`with_e3` (include the F′=0/1/3 contaminants, all `True`); `servo_delta2` (auto-optimize δ₂, `True`); `radius_um` (on-axis = 0).

### Fixed physical constants (NOT knobs)
Atomic/EM properties, in Section 1 of the file: `A_HFS`, the 5P₃/₂ hyperfine centroids,
`GAMMA_D2`/`GAMMA_D1`, the Landé/nuclear g-factors and μ_B/h, the dipole recoil distribution,
the hyperfine decay branching, and the F=2→F′2 frequency reference (= 0). These cannot be
varied because no experiment changes them.

---

## What the engine models / assumes / omits
(The `--report` output states this per-config; summarized here.)

**Modeled:** 8 ground sublevels via Breit-Rabi; 5P₃/₂ F′=0..3 via full tensor diagonalization;
the clock Λ (σ⁻ control |2,+1⟩, σ⁺ probe |1,−1⟩ → |F′2,0⟩) plus the coherent |F′3,0⟩ control
admixture; contaminant ladders into F′=0/1/3; two repumpers; one axial mode with Lamb-Dicke
displacement and 3-point recoil on every absorption/emission; full m-resolved hyperfine decay;
steady state of the Liouvillian. For `single_end_tagged`, the two rejected retro tones are
entered as **linearized** dissipators with analytic AC-Stark shifts (valid: (Ω/2f_A)²~10⁻³).

**Assumed:** steady state (no loading transient, finite pulse time, or atom loss); classical
drive fields; radial motion frozen/decoupled (k·v_r = 0 by geometry, ν_r ≪ ν_z — radial spread
is handled by the separate Monte-Carlo tool); Lamb-Dicke regime; for dual-end, **perfect** carrier
suppression (β = 2.4048); δ₂ held at the servo optimum.

**Flagged in the spectrum but NOT yet folded into ⟨n_z⟩:** a carrier-leak tone if β≠2.4048;
EOM overtones that land near a line; the single-end down-shifted **retro carrier sitting ~88 MHz
from F=2→F′1** (the rejected tones are laddered to F′2/F′3 only). The spectrum table prints a
warning for each of these.

**Out of scope (bound separately in the program's noise studies):** magnetic-field noise and
Zeeman dephasing of the dark state; laser phase/frequency noise (finite linewidth) and relative
control–probe phase noise; intensity noise; polarization impurity; beam pointing / non-axiality
(~0.08 kHz/°); trap anharmonicity and higher bands; radial–axial coupling beyond the frozen
approximation; collisions / background-gas loss.

---

## Validated floors (regression baseline, N_f=6, δ₂ servoed)
| case | ⟨n_z⟩ | servo δ₂ |
|---|---|---|
| clean-Λ recoil limit (OmR=0.25) | 0.0072 | 0 |
| clean base (contaminants off) | 0.0014 | −0.01 |
| + F′1 (common level, dominant) | 0.0048 | +0.02 |
| + F′3 (control leg) | 0.0024 | −0.13 |
| + F′0 (probe leg, negligible) | 0.0015 | −0.01 |
| **dual-end full (preferred)** | **0.0048** | −0.13 |
| **single-end tagged full** | **0.0075** | −0.25 |

Contaminant increments over the clean base are non-additive; F′1 dominates. The Δ floor is flat
across 45–80 (with F′1 on) and rises monotonically with OmR (the weaker-probe lever) — both
reproducible with `--sweeps`.

---

## The two delivery architectures
**`dual_end` (preferred, floor ~0.005).** Control σ⁻ as a clean tone one end; probe = upper J₁
sideband of a phase-EOM carrier injected the other end, with β=2.4048 so the carrier vanishes.
Two-photon detuning δ₂ = probe_order·f_mod − A_HFS. No SSB, slave, filter, or tag AOM.

**`single_end_tagged` (fallback, floor ~0.0075).** Control carrier + probe sideband co-propagate
one end; a retro with a double-passed tag AOM (down-shift 2f_A = 300) and a λ/4 (helicity flip)
returns them; the intended probe is the return sideband. δ₂ = probe_order·f_mod − A_HFS − 2f_A.
Watch the rejected retro carrier (−88 MHz from F=2→F′1, flagged in the table).

---

## Adding a sweep
Any `Config` field name works as the swept knob. Pass `servo_grid` to trade accuracy for speed.
```python
base = preset("single_end_tagged")
# tag-AOM sensitivity (single-end):
v, nb, d2 = sweep1d(base, "tag_2fA", [220, 260, 300, 360], servo_grid=[-0.30,-0.25,-0.20])
# 2D map:
x, y, Z = sweep2d(base, "Delta", [45,55,65], "OmR", [0.08,0.10,0.12])
```
With `servo_delta2=True` on the base config, δ₂ is re-optimized at every point (honest, since the
dark resonance moves with the swept knob); set it `False` to hold δ₂ fixed for fast scouting.
