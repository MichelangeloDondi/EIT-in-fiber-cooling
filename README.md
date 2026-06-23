# EIT/Raman sideband cooling of ⁸⁷Rb in a kagome HCPCF — project guide

Ground-state cooling of single ⁸⁷Rb atoms in a 1064 nm intra-fibre lattice inside a kagome
hollow-core photonic-crystal fibre (48 µm core, w₀ ≈ 19 µm). The scheme is **clock-EIT
sideband cooling** on the field-insensitive D2 dark pair |1,−1⟩/|2,+1⟩ → |F′2,0⟩. Headline:
**axial floor n̄_z ≈ 0.006** (>99 % motional ground state; ≈0.005 at the floor-optimal probe), with
the cloud floor set by the in-fibre radial temperature and removable with a flat-top trap.

---

## If you have just inherited this project, read in this order

1. **This file** — the map (10 min).
2. **`GUIDE.md`** — the **narrative walkthrough**: the whole experiment front-to-back, from building
   the setup through the cooling to the thermometry data analysis, with the figures and diagrams.
   Read this first to understand *what* and *why* before the dense reference. Its 8 chapters live in
   `docs/guide/`.
3. **`docs/clock_EIT_consolidated.md` (v17)** — THE MASTER. The full technical state (PART I)
   *and* the conceptual path that produced it (PART II — the historical reasoning). The guide
   narrates over this; this file is the authority everything is subordinate to.
4. **`START_HERE_simulations.md`**, then run the two simulations with `--regression` — watch the
   headline numbers reproduce on your machine. This is how you learn to trust (then modify) the
   model.
5. **`INDEX.md`** — the authority router: the single canonical file per settled question, the
   list of intermediate/superseded files that *look* authoritative but are not (§2), and the
   load-bearing conventions you must know before quoting any floor (§3). When in doubt about
   which file to believe, this is the arbiter.

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
  Authoritative in `operating_point.md`.
- **Axial floor:** **~0.006 dual-end (OmR=0.12) / 0.0072 single-ended tagged retro** (clk2
  deciding-solver 0.0048 at the floor-optimal OmR=0.10; the public tool gives 0.0051→0.0059 across
  OmR 0.10→0.12 — the probe lever trades ~1.4× cooling rate for a negligible floor change); certified
  single-atom **0.008–0.010** with the once-only anti-trap squeezer (master §5).
- **Cloud floor:** **T_r-gated** — ≈ 0.007 / 0.012 / 0.022 at T_r = 25 / 100 / 400 µK; a
  **flat-top 1064 mode** collapses it **far below the Gaussian at every T_r** (the lever), reaching
  ≈ on-axis for the **cooled** cloud (~0.0072, verified) — the **uncooled** flat-top digit is not yet
  converged (≥ 0.021, cluster-pending; see [INDEX §1b](INDEX.md)). The single largest mover and the one
  off-desk ask (XLIM).
- **Four delivery×tone subversions:** A = 1-tone dual-end (baseline), B = 1-tone retro (fallback),
  C/D = the 2-tone versions. **Tone count is chosen by radial temperature: one tone below
  T_r ≈ 120 µK, two tones above** (master §4, §8).

---

## Repository map

```
GUIDE.md                         THE NARRATIVE WALKTHROUGH (8 chapters, front to back)
docs/
  guide/                         the 8 narrative chapters (01 apparatus … 08 running & optimising)
  clock_EIT_consolidated.md      THE MASTER (v17): technical state + conceptual path
  operating_point.md             SSOT operating point + retro-cap optimization
  thermometry.md                 consolidated thermometry/readout authority (method -> spec)
  reference/                     the ~17 findings docs, grouped by topic (scheme, delivery, floor,
                                 radial, thermometry, excited_state) — see the DOCUMENT MAP at INDEX.md §6
  papers/                        P1 (in-fibre cooling) + Paper T (rank-2 obstruction theory)
  archive/                       superseded snapshots, kept for the reasoning (anti-museum:
                                 superseded briefs live in git history, not here)
src/
  engines/                       validated numerical solvers (the floor authority; see INDEX.md §5)
    eit_cooling_tool.py          PI tool #1 — AXIAL floor + delivery (self-contained, --regression)
    cloud_cooling_tool.py        PI tool #2 — RADIAL/cloud floor (flat-top, two-tone; --regression)
    clk2.py clock_combined_solve.py  the multilevel deciding-run solvers
    raman_sbc.py                 RSC engine (anchors the RSC-vs-EIT comparison)
    …                            (tagged_solver, radial_inhomogeneity, thermometry, operating_point, …)
  tools/                         supporting scripts (diagnostics, paper-T, sensitivity checks)
  radial_mc/                     the S3 radial-MC subsystem (engine/grid_build/mc; subsumed by cloud_cooling_tool)
START_HERE_simulations.md        how to run/tune the two PI tools (read before src/)
INDEX.md                         authority router + "do not mistake" list + conventions + document map (§6)
CLAIMS.md                        audited ledger: every headline number → evidence tier + script
SCOPE.md                         what the model covers, and what it does not
figures/                         curated publication figures
refs/                            literature PDFs — LOCAL ONLY, never committed (copyright)
LICENSE  CITATION.cff  requirements.txt
```

The two PI simulations are the runnable face of the program; `cloud_cooling_tool.py`
**consolidates** the `engine.py`/`grid_build.py`/`mc.py` subsystem (whose own README describes
that subsystem) into one tunable file. Use the tools to explore; use `clk2` /
`clock_combined_solve` for the authoritative multilevel floor numbers.

---

## How to reproduce every number (the trust gates)

Requires Python 3 + `numpy scipy sympy qutip` (5.x) `matplotlib` (`pip install -r requirements.txt`).

```bash
python src/engines/eit_cooling_tool.py --regression     # axial floors at the v17 preset: dual ~0.0048 / single ~0.0072 (Nf=6 gate; a converged run gives dual ~0.0059 at OmR=0.12). ~2 min on numpy<2; slower on numpy-2 + macOS Accelerate
python src/engines/cloud_cooling_tool.py --regression   # box collapse + two-tone crossover (~3 min)
```

Each claim in the master is tagged **[V]** verified / **[I]** inference / **[O]** open, with the
verifying script named at the point of use. **`CLAIMS.md`** is the audited ledger that collects every
headline number with its evidence tier and the script that establishes it; **`SCOPE.md`** states what
the model covers and what it does not. The fastest way to audit a number: find its [V] tag in
`docs/clock_EIT_consolidated.md`, open the named script, run it. `INDEX.md` §5 lists the engines
with their gate values; §3 lists the conventions that decide *which* number a given script reports
(solve vs all-in, single-atom vs cloud, low- vs high-dwell). **Read §3 before comparing any two
floor numbers** — most apparent disagreements in the history were convention mismatches, not physics.

---

## What is open (the frontier for the next student)

In rough priority:
1. **Two-photon coherence budget** — the floor doubles at a 0.26 kHz two-photon linewidth; the
   scheme wants sub-100 Hz. **Falsify by measuring the two-photon (not laser) linewidth in fibre.**
   The single binding bench question.
2. **Flat-top fibre feasibility** (XLIM/Marchesini) — mode content at 1064, walk-off over ~2 m,
   multimode standing-wave contrast. The headline cloud mover hinges on it.
3. **Cooling time vs trap/coherence lifetime** for an uncooled cloud — the box reaches the floor
   but slowly (~tens of ms for a hot cloud); needs the real in-fibre lifetime. A *rate* check.
4. **Two-tone production number** — the two-field *coherent* solve + (Δ₁,Δ₂,split,δ₂) optimization,
   if cells C/D are pursued (the crossover here uses an additive single-rate estimate).
5. **Bench inputs:** in-fibre radial temperature (the cloud-floor swing input), 1064 RIN at 860 kHz,
   B-noise / T₂ / PER / tag-AOM extinction, 795 nm fibre characterization.

---

## How this was produced (so you can trust the method)

Every overturning result was re-checked by an independent computation, not asserted; the program
ran an explicit red-team loop (a separate auditing thread tried to falsify each claim, and the
deciding multilevel solve settled leg/repump questions that diffusion arguments got wrong — master
§10, Stage 9). The recurring lesson, earned several times: *for a leg-assignment or leak-clearing
question, the repump topology decides, not the branching/diffusion lever.* Treat the master's
[I]/[O] tags as live — they mark exactly where a number is a design inference or an open bench
measurement rather than a verified computation.

License: `LICENSE`. Citation: `CITATION.cff`.
