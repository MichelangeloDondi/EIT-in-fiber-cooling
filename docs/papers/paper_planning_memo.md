# Paper-planning memo — EIT cooling of ⁸⁷Rb in a kagome HCPCF
**Minardi group, UniBo · compiled 2026-06-16 · planning input, to be discussed with the PI**

The modelling program is essentially complete; remaining uncertainty is **bench-resident**. "In hand" below = computed/verified [V] from the program unless tagged *(lab)*. Two bench facts gate everything:

- **Critical-path measurement:** the as-built **6.835 GHz two-photon linewidth** (not the laser linewidth). Sub-100 Hz unlocks Papers 1–3; it's the single number the whole coherence story rests on.
- **Shared crux:** the free-space→guided **load-in efficiency** at the ferrule (the 40%-via-ferrule vs 96.5%-test-fibre gap) — gates Paper 4 and bounds the reachable n̄.
- **Already in hand *(lab)*, shared by all:** MOT, bright molasses (8–10 µK), optical conveyor transport into the fibre (Marchesini 2024), two-Eblana fibered 780 source.

| # | paper — target result | in hand (modelling [V]) | still needs (experiment) |
|---|---|---|---|
| **T** | **Rank-2 limit** (theory note). The Δm=2 clock Raman is HFS-enabled → coherence-per-scatter pinned → clock-RSC floor lifts to ~0.45; EIT (near-detuned) is immune. | **complete**, verified 3 ways incl. two-manifold diagonalisation | **nothing** — publishable now |
| **1** | **Flagship.** Field-insensitive EIT sideband cooling of ⁸⁷Rb to **n̄_z ≈ 0.007 (P₀ ≈ 99%)** on the clock pair \|1,−1⟩/\|2,+1⟩ in an HCPCF, confirmed by sideband thermometry. *First EIT-SC in HCPCF + field-insensitive clock-pair cooling in a guided geometry (novelty check needed).* | operating point (Δ, OmR, δ₂, B), floor 0.0073, single-1560-EOM common-mode drive, thermometry method, full scheme survey | EOM coherence **(gating)**; gray molasses → n_r ≈ 9; in-fibre EIT n̄_z; calibrated sideband-asymmetry R; tagged-retro delivery (η_dp) |
| **2** | **Methods/apparatus.** One seed + one 1560-EOM drives the whole sequence common-mode (passive sub-100 Hz, **no OPLL**); fast **RF-only** phase switching incl. EIT→thermometry. | architecture, spurious-comb audit (intermod 2.4×10⁻⁷), EIT→thermometry switch analysis | measured two-photon linewidth; demonstrated phase switching + comb cleanliness on the apparatus |
| **3** | **Cooling physics.** Axial floor **vs radial T**; the inhomogeneous-light-shift **cloud floor** (tail-dominated, n̄_z ≈ 0.0095 at 100 µK); the **EIT-tolerant / RSC-fragile** regime map. *Addresses the inhomogeneous-broadening limiter the HCPCF field cites.* | v13 M1–M5, differential-light-shift cloud floor, semiclassical MC, regime map | floor-vs-radial-T scan; cloud-floor / coverage; direct EIT-vs-RSC comparison |
| **4** | **3D ground state.** **~88% 3D ground** (n_z ≈ 0.007, n_r ≈ 0.06/mode) via axial EIT-SC + radial **degenerate RSC** in a 2nd-1064 tight focus above the tip + adiabatic transfer. *The eye-catching extension: the cold, field-insensitive in-fibre source.* | radial dRSC scheme (within-F=1 Δm=−1, rank-1), 2nd-1064 trap design (8 µm, η_r 0.35, B 44 mG), transfer, 3D fraction | 2nd 1064 RSC beam + transverse 780 Raman/pump; radial dRSC demo; load-in/transfer efficiency; 3D thermometry |
| **5+** | **Applications** (future). Cold-source-enabled in-fibre quantum memory / interferometry / few-photon NLO / collective 1D effects. | qualitative case + field demand (storage, interferometry want cold m=0) | the cold source (P1/P4) **plus** the application-specific capability |

## Suggested order and rationale

1. **T — write now** (or fold into Paper 1's supplement). No experiment; clean negative result; clears the narrative for why clock-EIT, not clock-RSC.
2. **Paper 1 — the thesis core.** Do the **two-photon-linewidth measurement first** (go/no-go); if it passes, gray molasses → EIT cooling → sideband thermometry produce the headline. Everything downstream depends on this apparatus working.
3. **Papers 2 & 3 — spun from Paper 1's apparatus/data**, in parallel with finishing P1. **Decide with the PI** whether Paper 3 (radial physics) is strong enough to stand alone or is better as Paper 1's backbone, and whether Paper 2 merges into Paper 1 or is a separate methods note. Default: P3 as P1's backbone, P2 as a short standalone methods paper.
4. **Paper 4 — the big extension.** Needs new hardware (2nd 1064 beam + transverse Raman) and the load-in measurement; start the **load-in efficiency** study early since it gates the result and is independent of the cooling.
5. **Applications — post-thesis.** Build on the cold source once P1/P4 deliver it.

## Critical path (one line)
two-photon coherence ✓ → **Paper 1** (EIT cooling + thermometry) → **Papers 2/3** (architecture + radial physics) → **Paper 4** (radial dRSC + load-in → 3D ground state) → applications.

## Honesty flags for the framing [I/O]
- Novelty of "first EIT-SC in HCPCF" / "field-insensitive clock-pair cooling in a guided geometry" needs a **current literature check** before the abstract — populated, fast-moving area.
- Don't claim "first cooling in a fibre" (that's RSC, Leong 2020). The defensible firsts are the two above.
- Pitch the program as the **enabling cold, field-insensitive source** for the temperature-limited in-fibre ecosystem, not as cooling for its own sake.
