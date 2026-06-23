# The Guide — clock-EIT sideband cooling of ⁸⁷Rb in a kagome fibre

*A front-to-back walkthrough of the whole experiment, from building the setup to analysing the
thermometry data — written so a new PhD student or the PI can read it cover-to-cover, then **run and
optimise** the model on their own. It narrates; the [master brief](docs/clock_EIT_consolidated.md) and
the [authority router](INDEX.md) hold the audited detail.*

---

## What this experiment is

Cool a single ⁸⁷Rb atom (and then a small cloud) to the **motional ground state** of a 1064 nm optical
lattice that lives **inside a hollow-core photonic-crystal fibre**, using **clock-EIT sideband
cooling** on a magnetic-field-insensitive dark pair. The payoff is a cold, field-insensitive atomic
source delivered *through* a fibre — a building block for fibre-coupled clocks, sensing, and
Rydberg/EIT nonlinear optics.

![Clock-EIT cooling scheme on the m′=0 dark pair](figures/fig_scheme_d2.png)

*The cooling scheme in one picture: a Λ system on the D2 line, both legs driving the same excited
sublevel |F′=2, m′=0⟩ from the field-insensitive ground pair |1,−1⟩ (probe σ⁺) and |2,+1⟩ (control
σ⁻). Chapter 02 explains why this exact pair.*

---

## The headline result

> **Single atom, on axis:** ⟨n_z⟩ ≈ **0.008–0.010** certified (the steady-state solve is ~0.005–0.006
> dual-end / ~0.0072 single-ended, plus a once-only anti-trap squeezer ≈0.003) — **> 99 % axial
> ground-state population.**
> **A whole cloud:** the floor is set by the **in-fibre radial temperature**; a **flat-top trap
> profile removes that dependence**, collapsing the cloud floor to ≈ the on-axis value at *every*
> radial temperature. (The cooled-cloud floor is computed and settled; the uncooled hot-cloud digit is
> still converging — Chapter 06 gives the honest status.)

Canonical numbers, with their convergence tier and the script that produces each, live in **[INDEX
§1b](INDEX.md)** — the chapters quote the story and link there rather than reprinting a floor table.

---

## The chapters

Read them in order the first time; each is 2–4 short sections ending in a **Go deeper →** link into the
reference layer.

| # | Chapter | What you come away knowing |
|---|---|---|
| 01 | [Apparatus & the experimental sequence](docs/guide/01_apparatus_and_sequence.md) | the fibre, the trap, and the full shot (MOT → molasses → load → cool → read) |
| 02 | [The cooling scheme — why EIT, not Raman](docs/guide/02_cooling_scheme.md) | the clock-EIT Λ, the field-insensitive pair, and the rank-2 obstruction that rules out stretched-pair RSC |
| 03 | [Laser & delivery](docs/guide/03_laser_and_delivery.md) | one 1560 nm EOM → SHG generates every tone; dual-end vs tagged-retro delivery |
| 04 | [The operating point](docs/guide/04_operating_point.md) | Δ, the weaker-probe lever, the δ₂ servo, and the magic field |
| 05 | [The axial cooling floor](docs/guide/05_axial_cooling_floor.md) | the multilevel solve, why F′=1 dominates, and the certified single-atom floor |
| 06 | [The cloud floor & the dead-wall](docs/guide/06_cloud_floor_and_deadwall.md) | radial inhomogeneity, why a flat-top freezes the edge cold, and what is settled vs pending |
| 07 | [Thermometry & data analysis](docs/guide/07_thermometry_and_analysis.md) | sideband-asymmetry readout, Blackman pulses, and how to extract ⟨n_z⟩ without bias |
| 08 | [Running & optimising the model](docs/guide/08_running_and_optimizing.md) | the two PI tools, the trust gates, and the knob → tool table |

---

## How this guide fits the rest of the repo

The repository is built in **three layers** — this guide is the first:

1. **Narrate (you are here).** `GUIDE.md` + `docs/guide/*` — the story, with the figures and diagrams.
   It states the headline once and routes onward; it does **not** hold canonical numbers or re-derive
   the physics.
2. **Run.** [`START_HERE_simulations.md`](START_HERE_simulations.md) + the two tools in `src/` — how to
   reproduce every number and turn the knobs yourself.
3. **Reference.** [`INDEX.md`](INDEX.md) (the authority router) → the
   [master brief](docs/clock_EIT_consolidated.md) → `docs/reference/<topic>/` (the audited findings) →
   [`CLAIMS.md`](CLAIMS.md) / [`SCOPE.md`](SCOPE.md). This is where every claim's evidence tier lives.

If a number in a chapter ever disagrees with INDEX, **INDEX wins** — tell the maintainer. The chapters
are the map; the reference layer is the territory.
