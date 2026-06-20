# Paper-planning memo — EIT cooling of ⁸⁷Rb in a kagome HCPCF
**Minardi group, UniBo · compiled 2026-06-16 · planning input, to be discussed with the PI**

The modelling program is essentially complete; remaining uncertainty is **bench-resident**. "In hand" below = computed/verified [V] from the program unless tagged *(lab)*. Two bench facts gate everything:

- **Critical-path measurement:** the as-built **6.835 GHz two-photon linewidth** (not the laser linewidth). Sub-100 Hz unlocks Papers 1–3; it's the single number the whole coherence story rests on.
- **Shared crux:** the free-space→guided **load-in efficiency** at the ferrule (the 40%-via-ferrule vs 96.5%-test-fibre gap) — gates Paper 4 and bounds the reachable n̄.
- **Already in hand *(lab)*, shared by all:** MOT, bright molasses (8–10 µK), optical conveyor transport into the fibre (Marchesini 2024), two-Eblana fibered 780 source.

| # | paper — target result | in hand (modelling [V]) | still needs (experiment) |
|---|---|---|---|
| **T** | **Rank-2 limit → P1 motivation, not standalone.** Physics correct & verified, but **prior art** (Naber–Spreeuw, PRA 94, 013427 (2016)); scope also narrower (the m=0 clock transition is Δm=0 and **coolable**). See `novelty_findings.md`. | **complete**, verified 3 ways | **n/a** — folds into P1, cited |
| **1** | **Flagship.** Field-insensitive EIT sideband cooling of ⁸⁷Rb to **n̄_z ≈ 0.007 (P₀ ≈ 99%)** on the clock pair \|1,−1⟩/\|2,+1⟩ in an HCPCF, confirmed by sideband thermometry. *First EIT-SC in HCPCF + field-insensitive clock-pair cooling in a guided geometry (novelty check needed).* | operating point (Δ, OmR, δ₂, B), floor 0.0073, single-1560-EOM common-mode drive, thermometry method, full scheme survey | EOM coherence **(gating)**; gray molasses → n_r ≈ 9; in-fibre EIT n̄_z; calibrated sideband-asymmetry R; tagged-retro delivery (η_dp) |
| **2** | **Methods/apparatus.** One seed + one 1560-EOM drives the whole sequence common-mode (passive sub-100 Hz, **no OPLL**); fast **RF-only** phase switching incl. EIT→thermometry. | architecture, spurious-comb audit (intermod 2.4×10⁻⁷), EIT→thermometry switch analysis | measured two-photon linewidth; demonstrated phase switching + comb cleanliness on the apparatus |
| **3** | **Cooling physics → P1 backbone, not standalone.** Geometry-specific floor vs radial T (clk2 T_r-gated cloud all-in ≈0.012 at 100 µK, superseding the earlier semiclassical ≈0.0095) + regime map. Mechanism is **established** (EIT bandwidth advantage; HCPCF DLS-floor literature; Wang PRR 4 L022058 (2022) — the host group). See `novelty_findings.md`. | v13 M1–M5, cloud floor, MC, regime map | floor-vs-radial-T scan; cloud-floor / coverage; direct EIT-vs-RSC |
| **4** | **3D ground state.** **~88% 3D ground** (n_z ≈ 0.007, n_r ≈ 0.06/mode) via axial EIT-SC + radial **degenerate RSC** in a 2nd-1064 tight focus above the tip + adiabatic transfer. *The eye-catching extension: the cold, field-insensitive in-fibre source.* | radial dRSC scheme (within-F=1 Δm=−1, rank-1), 2nd-1064 trap design (8 µm, η_r 0.35, B 44 mG), transfer, 3D fraction | 2nd 1064 RSC beam + transverse 780 Raman/pump; radial dRSC demo; load-in/transfer efficiency; 3D thermometry |
| **5+** | **Applications** (future). Cold-source-enabled in-fibre quantum memory / interferometry / few-photon NLO / collective 1D effects. | qualitative case + field demand (storage, interferometry want cold m=0) | the cold source (P1/P4) **plus** the application-specific capability |

## Suggested order and rationale

1. **T — fold into Paper 1** (cited motivation; **not a standalone** — prior art Naber–Spreeuw 2016). The verified core supports the why-clock-EIT-not-RSC narrative.
2. **Paper 1 — the thesis core.** Do the **two-photon-linewidth measurement first** (go/no-go); if it passes, gray molasses → EIT cooling → sideband thermometry produce the headline. Everything downstream depends on this apparatus working.
3. **Papers 2 & 3 — spun from Paper 1's apparatus/data**, in parallel with finishing P1. **P3 is P1's backbone** (the standalone option is withdrawn — mechanism is established; see `novelty_findings.md`); whether Paper 2 merges into Paper 1 or is a separate methods note is a PI call (default: P2 standalone).
4. **Paper 4 — the big extension.** Needs new hardware (2nd 1064 beam + transverse Raman) and the load-in measurement; start the **load-in efficiency** study early since it gates the result and is independent of the cooling.
5. **Applications — post-thesis.** Build on the cold source once P1/P4 deliver it.

## Critical path (one line)
two-photon coherence ✓ → **Paper 1** (EIT cooling + thermometry) → **Papers 2/3** (architecture + radial physics) → **Paper 4** (radial dRSC + load-in → 3D ground state) → applications.

## Honesty flags for the framing [I/O]
- **Novelty checked (2026-06-17):** Paper T and P3 are **not novel standalones** — both assemble established physics (T: Naber–Spreeuw, PRA 94, 013427 (2016); P3: EIT-bandwidth + HCPCF DLS-floor literature, incl. the host group's Wang, PRR 4, L022058 (2022)). They fold into **P1** as cited motivation/backbone. The first-author anchor is **P1**. See `novelty_findings.md`.
- Novelty of "first EIT-SC in HCPCF" / "field-insensitive clock-pair cooling in a guided geometry" needs a **current literature check** before the abstract — populated, fast-moving area.
- Don't claim "first cooling in a fibre" (that's RSC, Leong 2020). The defensible firsts are the two above.
- Pitch the program as the **enabling cold, field-insensitive source** for the temperature-limited in-fibre ecosystem, not as cooling for its own sake.
