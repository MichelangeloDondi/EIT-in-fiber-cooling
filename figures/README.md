# Figures

Every figure is regenerated from the validated engines in `../src/` (and, for the cloud floor, the
rate grid in `../data/`); each `fig_*.py` writes the matching `fig_*.png`. They depict the v17 scheme:
the field-insensitive clock pair `|1,-1>` (probe σ⁺) / `|2,+1>` (control σ⁻) → `|F'2, m'=0>`.

The curated `.png`s are committed (the repo-wide `fig_*.png` ignore is for regenerated outputs at the
working root; the figures here were force-added). They are embedded across the
[guide chapters](../docs/guide/), the [master brief](../docs/clock_EIT_consolidated.md), and
[`thermometry.md`](../docs/thermometry.md).

## Guide / master figures

| script | output | shows | engine | embedded in |
|---|---|---|---|---|
| `fig_scheme_d2.py` | `fig_scheme_d2.png` | cooling scheme (level diagram) | hand-drawn | GUIDE, Ch 02, master §2 |
| `fig_rsc_vs_eit.py` | `fig_rsc_vs_eit.png` | EIT vs RSC floors: field-insensitive clock pair vs field-sensitive stretched | `raman_sbc` + `tagged_solver` | Ch 02 |
| `fig_retro_flatness.py` | `fig_retro_flatness.png` | single-ended floor vs retro reflectivity: a large tag (2f_A=400) is flat | `tagged_solver` | Ch 03, master §4 |
| `fig_delta2_landscape.py` | `fig_delta2_landscape.png` | floor vs two-photon detuning δ₂ (shallow optimum) | `tagged_solver` | Ch 04 |
| `fig_stark_5P32.py` | `fig_stark_5P32.png` | 5P₃/₂ tensor-Stark manifold (m′=0 = EIT target, pure scalar) | self-contained | Ch 05, master §7 |
| `fig_cloud_floor_multilevel.py` | `fig_cloud_floor_multilevel.png` | **cloud floor (post-retraction multilevel union)**: Gaussian rises with T_r; flat-top box cooled 0.0072 [V] / uncooled ≥0.021 [O] | baked (INDEX §1b) | **Ch 06, master §8** |
| `fig_cloud_floor.py` | `fig_cloud_floor.png` | *(earlier 3-level view)* cloud floor vs radial T (MC below quasi-static column) | `radial_floor_mc` (needs `../data/rategrid.npz`) | superseded by the multilevel figure; kept for reference |
| `fig_thermometry.py` | `fig_thermometry.png` | sideband-asymmetry thermometry at the floor + calibration | `thermometry` | Ch 07, `thermometry.md` |
| `fig_apparatus.py` | `fig_apparatus.png` | apparatus/trap schematic + the ~80× anisotropy | hand-drawn | Ch 01 |
| `fig_knobspace.py` | `fig_knobspace.png` | floor lever (OmR) + speed lever (Δ) | baked (operating_point §2, master §6) | Ch 04 |
| `fig_floor_budget.py` | `fig_floor_budget.png` | floor-budget waterfall (F′=1 dominates) | baked (master §5/§7) | Ch 05 |
| `fig_radial_efficiency.py` | `fig_radial_efficiency.png` | the dead-wall: W(r) collapse vs n_ss(r) climb | baked (`cloud_multilevel_union` grid) | Ch 06 |

## Paper-T figures (theory paper, not the guide)

| script | output | shows | engine |
|---|---|---|---|
| `fig_level_scheme.py` | `fig_level_scheme.png` / `.pdf` | Paper-T level scheme | self-contained |
| `fig_fom_vs_detuning.py` | `fig_fom_vs_detuning.png` | Paper-T two-photon figure-of-merit vs detuning | self-contained |

## Notes & caveats

- **Stale on-figure pixels (compute-bound regen queued — INDEX §4).** Two `.png`s carry numbers that
  disagree with the SSOT and need a `tagged_solver` re-run (numpy<2 / cluster) to refresh the pixels:
  `fig_delta2_landscape` shows δ₂=+0.25 (tagged_solver's state-energy sign; canonical is **−0.19 field**
  — INDEX §3), and `fig_retro_flatness` plots ~0.0049 for the single-ended 2f_A=400 floor whose canonical
  value is **0.0072** (`operating_point.md` §3 — it understates the floor, and the ≤0.006 band is not the
  canonical floor; flagged by the 2026-06 figure red-team, removed from the master). Both captions quote
  the current numbers and link [INDEX §1b](../INDEX.md); only the pixels lag. **The cloud-floor figure is
  resolved** — `fig_cloud_floor_multilevel` (post-retraction, baked from §1b) is the primary; the 3-level
  `fig_cloud_floor` is kept as the earlier dynamic-MC view.
- **Every committed `.png` has a regen script** (the orphan `fig_radial_mc.png` — no script, superseded by
  the cloud-floor figures — was retired). If you add a figure, add its `fig_*.py`.
- **`fig_rsc_vs_eit`** marks the clock-pair RSC floor as a **lower bound** (Nf=10; higher Fock cutoff
  does not converge within budget). The defensible claim is comparative — EIT beats RSC on the
  field-insensitive pair.
- **The 4 newest figures are baked / hand-drawn, not live-solve.** A single multilevel solve is
  ~10 min on a typical Mac (the INDEX numpy-pin note), so `fig_knobspace`, `fig_floor_budget`, and
  `fig_radial_efficiency` *plot documented or cached engine values* (provenance in each script's
  docstring) rather than re-solving; `fig_apparatus` is hand-drawn. To regenerate the underlying
  numbers from scratch, run the cited engine/grid on a fast-numpy box or a cluster. (The
  originally-planned EIT-cycle figure was dropped as redundant with `fig_thermometry`; the
  floor-budget waterfall replaces it.)

Regenerate all:
```sh
cd figures && for f in fig_*.py; do python3 "$f"; done
```
