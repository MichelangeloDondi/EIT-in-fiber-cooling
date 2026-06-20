# D2 baseline — consolidation (post-alternatives sweep)

> **⚠ SUPERSEDED 2026-06-20 by `clock_EIT_consolidated.md` v16 (on `main`).** This is a **2026-06-19 snapshot, taken *before* the floor-budget correction.** Its headline framing below is **withdrawn**: §3/§7 say "all-in **0.012–0.019**… the number to quote" and §6 says the S3 dynamic MC is "not run" — both wrong now. The corrected state: **single-atom ⟨n_z⟩ = 0.008–0.010** (the 0.012–0.019 was a double-count), **cloud T_r-gated**, and the radial dynamic MC **is run** (benign; suppression 1.2/3.0/7.4×). Retained only as a dated provenance record of the adopted-scheme + alternatives-sweep decision state — **not an authority** (`INDEX.md` does not route to it). For the current state read **v16 / the SSOT / `INDEX.md`**.


**⁸⁷Rb · 1064 nm axial lattice · kagome HCPCF · 2026-06-19.** Authoritative record of the **adopted D2
scheme** and the disposition of every alternative explored since the v14 consolidated brief. Purpose:
fix the D2 baseline as the reference *before* the D1-Raman repump audit returns, so any audit result is
compared against a settled scheme rather than a moving one. Grades: **[V]** verified · **[I]** inference ·
**[O]** open. Intended to update/append `clock_EIT_consolidated.md` (→ now **v16**, merged); reference only.

## 1. The adopted scheme [V — settled]
- **m′=0 magic clock Λ**, single-ended retro: dark pair |1,−1⟩ (probe σ⁺, retro, weak, tagged) /
  |2,+1⟩ (control σ⁻, forward, strong) → |F′2,0⟩. Both g_F·m_F=+½ → **first-order field-insensitive**.
- **Config A (dark on |1,−1⟩, F=1 edge) — do NOT swap.** Settled this cycle by the deciding run (below).
- 1064 nm axial lattice, kagome HCPCF (48 µm core, 38 µm MFD@780, w₀≈19 µm). **1D axial cooler** — radial
  is cooled *upstream* (free-space gray molasses, a precondition, not an in-fiber stage).

## 2. Operating point [V]
Δ ≈ 45 MHz (flat 40–55), Ω_p/Ω_c ≈ 0.10–0.12, δ₂ servoed; single-ended tag 2f_A = 400 MHz (retro
reflectivity 20–40 % **non-binding** at this tag — atom-frame point identical across caps, only EOM
depth/launch power scale). ν_z = 2π×430 kHz, ν_r = 2π×5.42 kHz (ratio 79.3), U₀ = 22.8 MHz = 1094 µK,
η_z = 0.094, η_z,eff(retro) = 0.187. Magic B = 3.2288 G; cooling at ~1.5 G.

## 3. Performance [V on comparisons / I on absolutes — absolute floor still [O] pending §6 budget revision]
- **Axial coherent floor (GATE A, repumps off) = 0.0072 [V]**, reproduced bit-for-bit; regression-pinned.
- **Realized axial:** dual-end carrier-suppressed ≈ 0.005; single-ended tagged ≈ **0.0072** (post-qutip-5
  re-pin, +3 %). *(These are different recycler closures/conventions — do not conflate; e.g. the leg-swap
  comparison's A=0.0048 is on an η=0.094-symmetric convention, a relative number, not the headline.)*
- **All-in headline band = 0.012–0.019 [I]**, **dominated by radial inhomogeneity**, not the axial
  single-atom floor. This is the number to quote.
- **The axial floor is repump-recycle-limited** (per leak event N_cool≈3, N_rep≈7, ρ≈2.3) — established by
  the leg-swap deciding run + the EOM-Raman clearer audit (both below). The recycle recoil, not the cooling
  or the leak, sets ≈0.005.

## 4. Leg assignment — settled: A holds, do not swap [V, F-NN]
Deciding run (`clk2.py` = `clock_combined_solve.py` + swap/want_fock hooks, re-pointed repumps, δ₂
re-servoed): **config A = 0.0048 hard-converged vs config B (swap) ≈ 0.018, non-convergent at matched OmR
→ A favored ~3.8×.** Cause: B's F=2-*interior* dark leg admits only one protecting repump (σ⁺ F2→F′1),
which cannot clear the |2,+2⟩ leak → near-flat Fock heating tail. Frame-conflict 0.0 (physics, not a frame
artifact). The branching reversal (clock 0.25/0.75 vs stretched 0.75/0.25) is verified
(`clock_branching_check.py`) but does **not** decide it — repump topology does (the lesson, now earned
four times). Recorded in `clock_leg_swap_finding.md`, committed `5bce37c`.

## 5. Alternatives evaluated — none beats the D2 baseline
| alternative | verdict | basis |
|---|---|---|
| **Leg-swap** (control↔probe) | **REJECTED** | deciding run: A holds 3.8×; F=2-interior repump clearability [V] |
| **EOM-Raman |2,+2⟩ clearer** | **REJECTED — window empty** | ideal clearer floors B at ≈A (repump cycle, not leak); single-photon scatter depletes the 93.5 %-occupied dark state (3–10×) [V] |
| **Double-EIT** (2 excited states) | **no headline gain** | preserves the clock; sharper feature lowers only the *axial* floor, which is sub-dominant to inhomogeneity [I] |
| **Tripod / quadrupod** | **REJECTED** | the g·m=+½ Zeeman-matched subspace of |F′2,0⟩ is exactly 2-D; any third leg breaks field-insensitivity [V] |
| **Alternation EIT↔RSC** | **marginal (axial)** | sequential EIT→RSC lowers the axial floor modestly; sub-dominant. The *headline* version is EIT↔**radial-GM**, gated on transverse access [I] |
| **Pulsed re-preparation** | **right target, likely wash** | attacks the recycle floor (correct), but the 2/3 spectator branching fills the leak on the cooling timescale; gated on the Q3 recycle-floor trace [I] |
| **D1 (795) — pivot/hybrid** | **no floor gain; cost/cleanliness only** | floor line-independent (b_leak exact D1≡D2); full-D1 recycler 1.65× worse; broadening advantage isotope-tempered & [I]-conditional on repump parking; gated on G1 fiber [V/I] |
| **D1-Raman repump** | **UNDER EXTERNAL AUDIT** | could challenge the line-independent floor *if* coherent recoil-free returns work — but same dark-state-scatter risk that killed the D2 clearer; gated on G1 [I, uncomputed] |

**Net:** the D2 m′=0 clock + 2 refined repumpers (config A) is the validated baseline. Every alternative
either breaks field-insensitivity, fails on repump topology, or targets the *axial* floor — which is
already below the dominant radial-inhomogeneity term.

## 6. Where the headline can actually move (the real open items)
The axial scheme is settled; the leverage is elsewhere.
- **[O] Radial-inhomogeneity floor (the dominant limiter).** S2 frozen bound 0.0064/0.0126/0.0266 @
  25/100/400 µK (conservative ceiling); the realized floor needs the **S3 semiclassical-radial dynamic MC**
  (not run). This is the headline term.
- **[O] Flat-top intensity profile — the one lever that attacks inhomogeneity at its root** (kills ν_z(r)
  variation → axial floor decouples from T_r; the only thing beating the T_r/U₀ lock). Gated on a kagome
  mode-content / flat-top-stability feasibility study (XLIM/Marchesini). The genuine headline mover.
- **[O] Repump-recycle floor (Q3)** — what caps the axial ≈0.005 (N_rep≈7 recoil + the F′1→F2 re-feed);
  decompose it (recoil vs re-feed vs irreducible rate). Pulsed re-prep is the candidate intervention; the
  D1-Raman audit also bears on it. Trace it before building any scheme to attack it.
- **[O] `cloud_floor_spec.md` revision** (reabsorption red-team) — the floor-budget restructure
  (endogenous-T_r via 2b-static). Leads the spec; held pending the brief revision.
- **[O] Thermometry m′=0 reconciliation** — dark leg now resolved to |1,−1⟩ → park-transfer |1,−1⟩→|1,0⟩
  (Δm=+1); the `thermometry_audit.md` edit is now unblocked.
- **[O] Bench inputs** gating final commitment: in-fiber B-noise (≲30 mG), echo T₂, fiber PER, tag-AOM
  efficiency, **1064 trap-laser RIN @860 kHz** (parametric-heating term, currently unquantified), and the
  **795 fiber characterization** (the full transmission curve, gates all D1).

## 7. Honesty rails (carry into any write-up)
- Headline is **0.012–0.019**, not 0.005 (the bare axial floor is not the all-in number).
- **AXIAL** ground state, never bare "3D ground state."
- "**first EIT cooling in a fibre**," never "first cooling in a fibre" (Leong 2020 = RSC, D1).
- D1 buys **no floor gain**; adoption (if ever) is cost/cleanliness/fiber, never floor.

## Disposition
The D2 baseline is consolidated and stable. The D1-Raman audit, when it returns, is compared against
this — and per §5/§6 its *best* case challenges the axial recycle floor, which is sub-dominant to the
radial inhomogeneity, so even a positive result does not move the headline (it would refine the axial
term and reopen the D1 cost/cleanliness question). The headline moves only via §6: the radial dynamic MC
and, above all, the flat-top feasibility.
