# CLAIMS — audited ledger

Every headline number with its **evidence tier** and **source**. The canonical numbers live in
`src/engines/operating_point.py` (the single source of truth); this ledger maps each to its evidence so
the thesis and the papers draft from one audited place rather than scattered docs.

**Tiers.** **[V]** verified — computed by a solver/script in this repo, or a closed analytic
result. **[I]** inference — physically-motivated estimate, order-unity uncertainty. **[O]** open
— a bench input, not yet measured.

The consistency gate (`audit/check.py`) keeps the SSOT, the engines, the master doc, and the
README mutually consistent; this ledger is the human-readable face of that.

## Operating point — `src/engines/operating_point.py`, `src/engines/eit_cooling_tool.py`
| # | Claim | Tier | Source |
|---|---|---|---|
| OP1 | Δ = 45 MHz (floor flat 40–55) | [V] | Δ-scan, `tagged_solver.py` |
| OP2 | OmR = Ω_p/Ω_c = 0.12 (Ω_c = 8.74, Ω_p = 1.05 MHz) | [V] | EIT condition Ω_tot = √(4Δν_z) + scan |
| OP3 | δ₂ ≈ −0.10 (dual) / −0.19 (single), **field convention** (probe−transition) | [V] | tracks the ≈−0.2 MHz e3 Stark shift; `eit_cooling_tool.py` at v17. `tagged_solver.py` corroborates with the opposite state-energy sign (optimum d2=+0.20). See INDEX §3. |
| OP4 | 2f_A = 400 MHz single-end tag (DOWN-shift) | [V] | tagged-delivery design |
| OP5 | η_dp delivery-efficiency acceptance flat 20–50 % | [V] | scan |

## Floors — the headline — `tagged_solver.py`, `raman_sbc.py`, `radial_inhomogeneity.py`
| # | Claim | Tier | Source |
|---|---|---|---|
| F1 | Clock-EIT **solve** floor ⟨n_z⟩ = 0.0048 (dual) / 0.0072 (single-tagged) | [V] | `tagged_solver.py`; model band ×/÷2 = 0.002–0.0076 |
| F2 | Anti-trap **squeezer** increment +0.003 (= faithful − no-squeezer, counted **once**); supersedes the withdrawn +0.007–0.012 lumped increment (double-counted the solve bulk + bare recoil) | [I] | grid→clk2 transfer; `ANTITRAP_RESOLUTION.md` (2026-06-20 floor correction) |
| F3 | **Certified low-dwell all-in single-atom floor ⟨n_z⟩ = 0.008–0.010** (the honest headline); old 0.012–0.019 **withdrawn** | [V]+[I] | SSOT `FloorBudget.all_in_single_atom_lowdwell` |
| F4 | **Cloud floor T_r-gated, [O]**: clk2 clock-unit quasi-static 0.0056 / 0.0169 / 0.130 at T_r = 25 / 100 / 400 µK (conservative ceiling; realized < quasi-static per dynamic MC) → cloud all-in ~0.007 / 0.012 / 0.022. Old flat 0.0094 semiclassical = legacy unverified | [I]/[O] | SSOT `FloorBudget.cloud_qs_clk2`; dynamic-MC brief (pending) |
| F5 | Axial recoil bound η_em² ≈ 0.003 | [V] | recoil |
| F6 | Stretched-RSC floor 0.00196 (**field-SENSITIVE** pair) | [V] | `raman_sbc.py` self-test |
| F7 | Clock-RSC floor ~0.45 — **DISQUALIFIED** (rank-2 obstruction) | [V] | `audit_C_rank2.py` + FoM; `docs/reference/scheme/clock_RSC_resolution.md` |
| F8 | clock-RSC 0.0137 = obstruction-free **idealization**, NOT the floor | [V] (not physical) | `raman_sbc.py`; see resolution |

## Clock-scheme leg assignment (control↔probe) — `src/tools/clock_branching_check.py`, `docs/reference/excited_state/D1_hybrid_findings.md`
| # | Claim | Tier | Source |
|---|---|---|---|
| LS1 | \|F′2,0⟩ dark-leg branching is **reversed** vs \|F′2,2⟩: clock probe leg \|1,−1⟩ collects 1/4 (stretched \|1,+1⟩ 3/4) ⇒ 3/4 of dark-leg decay diffuses onto the \|2,+1⟩ control leg | [V] | `clock_branching_check.py` (exact CG/6j; validated vs the stretched 0.75/0.25 anchor) |
| LS2 | Control↔probe **swap REJECTED** — config A (dark \|1,−1⟩) = **0.0048 hard-converged**; config B (swap, dark \|2,+1⟩) ≈ 0.018 best-bounded, non-convergent at matched OmR. A favored ~3.8×. Cause: F=2-interior dark leg forces rep2=A (unique protecting repump, cannot clear \|2,+2⟩) → near-flat Fock heating tail. Magic-B and F′=3 sub-dominant; GATE 1 moot. Frame-conflict 0.0. EOM-Raman clearer also rejected (window empty). Convention: η=0.094 symmetric; relative 3.8× is convention-robust. | [V] | `clock_combined_solve.py` / `clk2.py` (in-repo, gate-verified); `docs/reference/excited_state/D1_hybrid_findings.md` |

## Field insensitivity — Audit-C (`audit_C_rank2.py`, `audit_C_breitrabi.py`, …)
| # | Claim | Tier | Source |
|---|---|---|---|
| B1 | Dark pair \|1,−1⟩/\|2,+1⟩→\|F′2,m′=0⟩ field-insensitive at **any B** (both g_F·m_F = +½) | [V] | Breit-Rabi diagonalization |
| B2 | 1st-order vector-light-shift immune (B_fict = 0.336 G / unit circ.) | [V] | Audit-C rank-1 |
| B3 | Magic B = 3.2288 G (interrogation only; cooling 1–1.5 G) | [V] | Breit-Rabi |
| B4 | Δm=+2 clock Raman rank-2-null in J=½ → only via I·J ∝ Δ_HFS/Δ² | [V] | `audit_C_rank2.py` |

## Detection — `src/tools/detection_snr.py`
| # | Claim | Tier | Source |
|---|---|---|---|
| D1 | OD/atom = 2.6×10⁻⁴ → OD ≈ 1 at N ≈ 3900 atoms | [V] | σ₀/A_mode |
| D2 | Absorption (OD) viable and **not photon-limited** (~10 fJ for ΔOD = 0.01) | [V] | shot-noise budget |
| D3 | Guided-mode fluorescence <1 photon/atom (η_couple = 4.3×10⁻⁵/dir) | [V] | NA_eff = λ/πw = 0.013 |
| D4 | Forward fluorescence swamped ~1.8×10⁴× by the same-λ readout beam | [V] | readout 18.9 nW guided |
| D5 | Single-atom in-fibre detection NOT available → **ensemble OD** | [V] | composite |
| D6 | HCPCF backscatter at 780 nm (only matters for a backward-fluorescence route) | [O] | bench |

## Survival — `src/tools/radial_survival.py`
| # | Claim | Tier | Source |
|---|---|---|---|
| S1 | Survival ~100 % through cooling (radial heats 7–30 µK ≪ 1094 µK depth) | [V] | recoil 0.06 µK/photon × N_cool |
| S2 | Anti-trap benign: ρ_ee ~ 0.01 ≪ confining threshold 0.29–0.55 | [V] | curvature ratio U_e0/U₀ = 0.83–2.5 |
| S3 | Anti-trap heating <1 % of recoil (additive 0.7 %, parametric 0.5 %/ms) | [V] | dwell 26 ns; R_sc ≫ ν_r |
| S4 | Trap-depth scatter limit ~16,500 photons (bounds the READOUT) | [V] | (U₀−T)/0.06 |
| S5 | Radial ends warm ~107–130 µK → feeds inhomogeneity (not a loss channel) | [V] | consequence |

## Radial state — `src/engines/operating_point.py` (`n_radial`, `p0_3d`)
| # | Claim | Tier | Source |
|---|---|---|---|
| R1 | ν_r = 5.42 kHz (soft, NOT cooled; η_r = 0.84 → not resolved-sideband) | [I]/[O] | w1064 inferred; measure directly |
| R2 | n̄_r(100 µK) ≈ 384, n̄_r(2.5 µK) ≈ 10 | [V] | thermal occupation at ν_r |
| R3 | 3D ground fraction ~1 % even at 2.5 µK radial (axial-alone >99 %) | [V] | `p0_3d` |

## Apparatus / architecture — `docs/architecture_*`, `laser_architecture_comparison.md`
| # | Claim | Tier | Source |
|---|---|---|---|
| A1 | Marchesini-2024 apparatus; 2× Eblana 1560 → EDFA → PPLN → 780 nm | [V] | design |
| A2 | Single 1560 EOM makes the 6.835 GHz partner — common-mode, **no OPLL** | [V] | design |
| A3 | ν_z = 2π×430 kHz (axial, cooled) | [I]/[O] | w1064 inferred; measure directly |
| A4 | U₀ = 22.8 MHz = 1094 µK | [I]/[O] | inferred; measure in situ |
| A5 | 5P3/2 anti-trapped at 1064 nm (+19 to +57 MHz) | [V] | `docs/reference/excited_state/polarizability_5P32_1064.md` |

## Decisive open questions — bench
| # | Claim | Tier | Source |
|---|---|---|---|
| O1 | **Two-photon coherence linewidth sub-100 Hz** — the floor doubles at 0.26 kHz (~2.6× margin) | [O] | the one hardware question that sets the clock-EIT floor |
| O2 | Loaded N_atoms (sets OD and the cloud floor) | [O] | bench |
| O3 | Polarization purity (low-bi kagome beat-length condition) | [I]/[O] | fibre spec / bench |

## Per-paper cross-reference (which claims each paper rests on)
- **Paper T** — rank-2-obstruction note. Physics rests on **B4 + F7 + F8** (+ the FoM), all **[V] and correct**. But **NOT NOVEL** (prior art: Naber–Spreeuw, PRA 94, 013427 (2016)) and scope is narrower (the m=0 clock transition is Δm=0 and coolable). **DEMOTED → P1 motivation, cited; not standalone.** See `docs/papers/novelty_findings.md`.
- **P1** — flagship EIT-SC to the *axial* ground state + thermometry. Rests on **OP1–5, F1, F3, D1–5, S1–5**; bench-gated on **O1** (the two-photon linewidth).
- **P2** — single-EOM common-mode methods (no OPLL). Rests on **A1–A2**; bench-gated on **O1**.
- **P3** — inhomogeneous-light-shift / radial-recoil floor. Rests on **F4, R1–R3, S5**; atom-independent ⇒ transferable. Mechanism **established** (EIT bandwidth advantage; HCPCF DLS-floor literature; host group Wang 2022) ⇒ **P1 backbone, not a novel standalone**. See `docs/papers/novelty_findings.md`.

**Honesty rails.** NEVER "first cooling in a fibre". NEVER headline a 3D ground state (it is ~1 %).
Defensible firsts: **EIT-SC in an HCPCF**, **field-insensitive clock-pair cooling**, **single-EOM
common-mode** delivery.
