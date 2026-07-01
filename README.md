WRONG! The leakage treatment is uncorrect. The repository is going to be rebuilt step by step at https://github.com/MichelangeloDondi/Rb87-clock-EIT-infiber-cooling

# Clock-EIT sideband cooling of ⁸⁷Rb in a kagome HCPCF

Ground-state cooling of single ⁸⁷Rb atoms in a 1064 nm intra-fibre lattice inside a kagome hollow-core
photonic-crystal fibre (48 µm core, w₀ ≈ 19 µm), by **clock-EIT sideband cooling** on the
field-insensitive D2 dark pair |1,−1⟩/|2,+1⟩ → |F′2,0⟩. The payoff is a cold, field-insensitive atomic
source delivered *through* a fibre — a building block for fibre-coupled clocks, sensing, and Rydberg/EIT
nonlinear optics. Headline: **axial floor n̄_z ≈ 0.006** (>99 % motional ground state; ≈0.005 at the
floor-optimal probe; certified single-atom **0.008–0.010**), with the cloud floor set by the in-fibre
radial temperature and removable with a flat-top trap.

> **This README is the single front door** — the map, the headline, the narrative chapter guide, and the
> trust gates. (It absorbs the former `GUIDE.md`; the 8 narrative chapters live in `docs/guide/`.)

---

## If you have just inherited this project, read in this order

1. **This file** — the map + the narrative chapter guide below (10 min).
2. **The 8 chapters in `docs/guide/`** (linked below under *The narrative*) — the **front-to-back
   walkthrough**: the whole experiment, from building the setup through the cooling to the thermometry
   data analysis, with the figures and diagrams. Read these to understand *what* and *why* before the
   dense reference.
3. **[`docs/clock_EIT_consolidated.md`](docs/clock_EIT_consolidated.md) (v17)** — THE MASTER: the full
   technical state (PART I) *and* the conceptual path that produced it (PART II — the historical
   reasoning). The chapters narrate over this; it is the authority everything is subordinate to.
4. **[`START_HERE_simulations.md`](START_HERE_simulations.md)**, then run the two simulations with
   `--regression` — watch the headline numbers reproduce on your machine. This is how you learn to trust
   (then modify) the model.
5. **[`INDEX.md`](INDEX.md)** — the authority router: the single canonical file per settled question, the
   "do not mistake" list (§2), the load-bearing conventions (§3), and a 4-step **"Auditing a number?"**
   path at its top.

After those you are oriented. The rest of `docs/` (the grouped `reference/` depth) and `src/` are
reference depth.

---

## The result, in five lines

- **Scheme:** D2 clock-EIT, m′=0 pair |1,−1⟩/|2,+1⟩ → |F′2,0⟩, "config A" (dark on |1,−1⟩).
  Field-insensitive at any B (both g_F m_F = +½); cooling at 1.0–1.5 G, magic 3.229 G only for
  interrogation. Chosen over Raman SBC (it covers the cloud; the Δm=2 pair hits the Naber-2016
  rank-2 obstruction) and held against a thorough alternatives sweep (master §10).
- **Operating point:** Δ = +45 MHz, Ω_p/Ω_c = **0.12 nominal** (0.10 is floor-optimal but ~1.4×
  slower cooling — the weaker-probe lever), δ₂ servoed to the dark resonance, two repumpers.
  Authoritative in `docs/operating_point.md`.
- **Axial floor:** **~0.006 dual-end (OmR=0.12) / 0.0072 single-ended tagged retro** (clk2
  deciding-solver 0.0048 at the floor-optimal OmR=0.10; the public tool gives 0.0051→0.0059 across
  OmR 0.10→0.12); certified single-atom **0.008–0.010** with the once-only anti-trap squeezer (master §5).
- **Cloud floor:** **T_r-gated** — ≈ 0.007 / 0.012 / 0.022 at T_r = 25 / 100 / 400 µK; a
  **flat-top 1064 mode** collapses it **far below the Gaussian at every T_r** (the lever), reaching
  ≈ on-axis for the **cooled** cloud (~0.0072, verified) — the **uncooled** flat-top digit is not yet
  converged (≥ 0.021, cluster-pending; see [INDEX §1b](INDEX.md)). The single largest mover and the one
  off-desk ask (XLIM).
- **Four delivery×tone subversions:** A = 1-tone dual-end (baseline), B = 1-tone retro (fallback),
  C/D = the 2-tone versions. **Tone count is chosen by radial temperature: one tone below
  T_r ≈ 120 µK, two tones above** (master §4, §8).

---

## The narrative — the 8 chapters (in `docs/guide/`)

A front-to-back walkthrough, written so a new student or the PI can read it cover-to-cover, then **run
and optimise** the model. Read them in order the first time; each is 2–4 short sections ending in a
**Go deeper →** link into the reference layer. Canonical numbers (with convergence tier + the script that
produces each) live in **[INDEX §1b](INDEX.md)** — the chapters tell the story and link there rather than
reprinting a floor table.

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

## Repository map

```
README.md                        THE FRONT DOOR — map + headline + the chapter guide above + trust gates
docs/
  guide/                         the 8 narrative chapters (01 apparatus … 08 running & optimising)
  clock_EIT_consolidated.md      THE MASTER (v17): technical state + conceptual path
  operating_point.md             SSOT operating point + retro-cap optimization
  thermometry.md                 consolidated thermometry/readout authority (method → spec)
  reference/                     the findings docs, grouped by topic (scheme, delivery, floor, radial,
                                 thermometry, excited_state) — see the DOCUMENT MAP at INDEX.md §6
  papers/                        P1 (in-fibre cooling) + Paper T (rank-2 obstruction theory)
  archive/                       superseded snapshots (anti-museum: superseded briefs live in git history)
src/
  engines/                       validated numerical solvers (the floor authority; see INDEX.md §5)
    eit_cooling_tool.py          PI tool #1 — AXIAL floor + delivery (self-contained, --regression)
    cloud_cooling_tool.py        PI tool #2 — RADIAL/cloud floor (flat-top, two-tone; --regression)
    clk2.py clock_combined_solve.py  the multilevel deciding-run solvers
    …                            (tagged_solver, raman_sbc, radial_inhomogeneity, thermometry, operating_point, …)
  tools/                         supporting scripts (diagnostics, paper-T, sensitivity checks)
  radial_mc/                     the S3 radial-MC subsystem (subsumed by cloud_cooling_tool)
INDEX.md                         authority router + "do not mistake" + conventions + doc map (§6) + audit path
CLAIMS.md                        audited ledger: every headline number → evidence tier + script
SCOPE.md                         what the model covers, and what it does not
START_HERE_simulations.md        how to run/tune the two PI tools (read before src/)
audit/check.py                   the repo consistency gate (run it; see INDEX's "Auditing a number?")
figures/                         curated publication figures (each fig_*.png has a fig_*.py)
data/                            committed engine inputs (rategrid.npz, …); outputs/ holds run artifacts (gitignored)
refs/                            literature PDFs — LOCAL ONLY, never committed (copyright)
LICENSE  CITATION.cff  requirements.txt
```

The two PI simulations are the runnable face of the program; use the tools to explore, and `clk2` /
`clock_combined_solve` for the authoritative multilevel floor numbers. Engine grids/caches are written
to `outputs/` (gitignored), so a clone-and-run stays clean.

---

## How to reproduce every number (the trust gates)

Requires Python 3 + `numpy scipy sympy qutip` (5.x) `matplotlib` (`pip install -r requirements.txt`).

```bash
python src/engines/eit_cooling_tool.py --regression     # axial floors at the v17 preset: dual ~0.0048 / single ~0.0072 (Nf=6 gate; a converged run gives dual ~0.0059 at OmR=0.12). ~2 min on numpy<2; slower on numpy-2 + macOS Accelerate
python src/engines/cloud_cooling_tool.py --regression   # box collapse + two-tone crossover (~3 min)
python audit/check.py                                   # the repo consistency gate (SSOT ⇄ engines ⇄ docs)
```

Each claim in the master is tagged **[V]** verified / **[I]** inference / **[O]** open, with the
verifying script named at the point of use. **[`CLAIMS.md`](CLAIMS.md)** is the audited ledger that
collects every headline number with its evidence tier and the script that establishes it;
**[`SCOPE.md`](SCOPE.md)** states what the model covers and what it does not. **The fastest way to audit
a number is the 4-step "Auditing a number?" box at the top of [`INDEX.md`](INDEX.md)**: §1b/CLAIMS →
§3 convention → §5 script → run the gates. **Read §3 before comparing any two floor numbers** — most
apparent disagreements in the history were convention mismatches, not physics.

---

## What is open (the frontier for the next student)

In rough priority:
1. **Two-photon coherence budget** — the floor doubles at a 0.26 kHz two-photon linewidth; the scheme
   wants sub-100 Hz. **Falsify by measuring the two-photon (not laser) linewidth in fibre.** The single
   binding bench question.
2. **Flat-top fibre feasibility** (XLIM/Marchesini) — mode content at 1064, walk-off over ~2 m,
   multimode standing-wave contrast. The headline cloud mover hinges on it.
3. **Cooling time vs trap/coherence lifetime** for an uncooled cloud — the box reaches the floor but
   slowly (~tens of ms for a hot cloud); needs the real in-fibre lifetime. A *rate* check.
4. **Two-tone production number** — the two-field *coherent* solve + (Δ₁,Δ₂,split,δ₂) optimization, if
   cells C/D are pursued (the crossover here uses an additive single-rate estimate).
5. **Bench inputs:** in-fibre radial temperature (the cloud-floor swing input), 1064 RIN at 860 kHz,
   B-noise / T₂ / PER / tag-AOM extinction, 795 nm fibre characterization.

Two figure pixels also lag the SSOT (compute-bound regens, captions are correct) — INDEX §4.

---

## How this was produced (so you can trust the method)

The repo is built in **three layers** — **narrate** (this README's chapter guide + `docs/guide/*`),
**run** (`START_HERE_simulations.md` + the two `src/` tools), **reference** (`INDEX.md` → the master →
`docs/reference/<topic>/` → `CLAIMS.md`/`SCOPE.md`). If a number in a chapter ever disagrees with INDEX,
**INDEX wins.**

Every overturning result was re-checked by an independent computation, not asserted; the program ran an
explicit red-team loop (a separate auditing thread tried to falsify each claim, and the deciding
multilevel solve settled leg/repump questions that diffusion arguments got wrong — master §10, Stage 9).
The recurring lesson, earned several times: *for a leg-assignment or leak-clearing question, the repump
topology decides, not the branching/diffusion lever.* Treat the master's [I]/[O] tags as live — they
mark where a number is a design inference or an open bench measurement, not a verified computation.

License: `LICENSE`. Citation: `CITATION.cff`.
