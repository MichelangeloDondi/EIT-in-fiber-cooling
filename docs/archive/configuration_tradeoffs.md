# Configuration trade-study — pros & cons consolidation

> **[v12-era snapshot — compiled 2026-06-16; superseded for numbers.]** Floor figures and version references here predate v17; the authoritative state is `docs/clock_EIT_consolidated.md` (v17) + `INDEX.md`. Kept for the configuration trade-study *reasoning*. (Cited `EIT_brief_v12_comparison.md` / `clock_EIT_consolidated_v13.md` are not in the repo — see git history.)
**87Rb axial sideband cooling in a 1064 nm kagome-HCPCF lattice (Minardi group, UniBo)**
Compiled 2026-06-16. Tags: **[V]** computed/verified · **[I]** inference/design ranking · **[O]** open bench item.

System (frozen): ν_z = 2π·430 kHz (stiff, cooled), ν_r = 2π·5.42 kHz (shallow), U₀ ≈ 1.1 mK,
η_z(780) = 0.094, η_eff(retro) ≈ 0.184, η_r = 0.84 (radial NOT resolved-sideband),
Γ_D2/2π = 6.07, Γ_D1/2π = 5.746 MHz. Excited tensor (5P₃/₂, 1064): α₀ = −1149, α₂ = +563 a.u.

---

## 0. Top-line decision

**Recommended: clock-EIT on |1,−1⟩/|2,+1⟩ via |F′2,0⟩, single_end_tagged delivery, axial B, one Eblana + one 1560 EOM, D1 thermometry (unlocked DBR + EOM + wavemeter).** Realised axial floor **0.0073** (dual-end escalation → 0.0047), field-insensitive at any B. Nothing in the scheme sweep displaces it. Two conditionals decide the program: (1) **[O]** the as-built 6.835 GHz *two-photon* linewidth must be sub-100 Hz; (2) **[O]** the radial mode must be pre-cooled (free-space) to n_r ≲ tens before load-in — at T_r ≈ 400 µK the radial is marginally trapped and dominates everything.

---

## 1. Axial cooling schemes

| # | scheme | pair / excited | field-insens.? | floor n̄ | scatters/phonon | status |
|---|--------|----------------|:--------------:|--------:|:---------------:|--------|
| 1 | **clock-EIT** | \|1,−1⟩/\|2,+1⟩ → \|F′2,0⟩ | **yes (any B)** | **0.0047–0.0073** | ~1 | **RECOMMENDED** |
| 2 | stretched-RSC | \|2,+2⟩/\|2,+1⟩, σ⁺ pump F′2 | no | 0.0020 | ~1–2 | lowest floor, tolerance-bound |
| 3 | dRSC (geom A) | \|2,+2⟩ Zeeman ladder, D1 | no | 0.0070→0.016 | ~2–3 | tie, tolerance-heavy |
| 4 | m′=2-EIT | EIT via \|F′2,+2⟩ (tensor) | no | 0.018 | ~1 | field-sensitive EIT fallback |
| 5 | F′=0 cross-F RSC | \|1,0⟩↔\|2,0⟩ + F′0 polarizer | **yes** | 0.05 → **0.011** | ~3.5 | cools, uncompetitive→near-competitive |
| 6 | ~~clock-RSC~~ | clock pair, F′1 clear | yes | ~~0.001~~ → **0.45** | — | **DISQUALIFIED** (rank-2) |
| 7 | ~~F′=0 degenerate~~ | within-F=1, F′0 σ± | (yes) | **no cooling** | — | **DEAD** (mid-ladder) |
| 8 | ~~F′=3 (m′=0)~~ | within-F=2, F′3 σ± | no | **no cooling** | — | **DEAD** (mid-ladder + unresolved) |

### 1 — clock-EIT (RECOMMENDED)
**Pros:** field-insensitive at *all* B (both legs g_F·m_F = +½; magic 3.23 G only the 2nd-order zero) → immune to in-fibre B-noise, the binding environmental problem. Scatter-minimal dark-state cooling → gentlest on the radial mode (critical at high T_r). No selection-rule pathology (the Λ runs near-detuned where the Δm=+2 coherence is fine). Common-mode 6.835 GHz drive from one laser + EOM → laser linewidth cancels. Robust to ν_z smear (Fano feature ~Γ ≫ smear) and to radial-induced intensity modulation (dark state is intensity-independent).
**Cons:** the binding axis is the **two-photon coherence — floor doubles at only 0.26 kHz** (≈18× more fragile than any other axis); wants sub-100-Hz two-photon linewidth **[O]**. Not the lowest floor on paper (stretched-RSC is lower). Slower than dRSC (W ≈ 3.2 vs 6–7/ms). Carries the 1064 5P₃/₂ anti-trap (already in the realised floor).
**Delivery sub-variants:** single_end_tagged 0.0073 (simplest, one forward + retro, double-pass tag AOM rejects return carrier, η_dp=0.5); dual_end 0.0047 (two doubling chains off one seed, common-mode, no OPLL — lower floor, more hardware).

### 2 — stretched-RSC (lowest floor, tolerance-bound)
**Pros:** lowest floor in the matrix (0.0020, T_z ≈ 3.3 µK). Efficient σ⁺ pump → few scatters/phonon → low recoil. Dephasing-robust (doubles at 2.0 kHz).
**Cons:** **field-sensitive** (Δm=1 Zeeman). Two knife-edge tolerances: magnetic ≤4.3 mG for +10% floor; **σ⁻ cycling-pump leak doubles the floor at 32 dB PER** (recoil-amplified). 32 dB in-fibre circular purity + 4 mG in kagome HCPCF is the open question — likely the disqualifier. Bare floor is a model lower bound (anti-trap pump-excursion adds on top). **[O]**

### 3 — dRSC geometry A (tie, tolerance-heavy)
**Pros:** fast (W ≈ 6–7/ms). On D1 (no tensor, larger effective HFS, favourable repump branching). Dephasing-robust to 4.5 kHz.
**Cons:** **field-sensitive** (needs ~0.31 G Zeeman degeneracy or a B-tracked offset). With the 1064 anti-trap the realistic floor is ~0.016 — a tie with clock-EIT, never a decisive win. Asymmetry/ellipticity-tolerance-heavy: floor ∝ 1/x² but the asymmetry-induced vector shift ∝ (x²−1/x²) tightens the ellipticity-uniformity budget ~x²-fold; parity needs x≥3 where adiabaticity breaks. **[V/O]**

### 4 — m′=2-EIT (field-sensitive fallback; the tensor-isolation idea done right)
**Pros:** uses a genuinely tensor-isolated stretched excited state |F′2,+2⟩ (the well-resolved edge, gap ~3 Γ). Dephasing-robust (doubles 4.6 kHz, 18× less fragile than clock-EIT). Same EIT machinery.
**Cons:** **field-sensitive**, needs in-fibre B ≲ 30 mG (933× more sensitive than the clock). Warmest viable floor (0.018). Vector-shift exposed. Field-sensitivity is the whole reason it is a fallback. **[V]**

### 5 — F′=0 cross-F m=0 RSC (cools; near-competitive only with transverse pumps)
**Pros:** rank-0 cooling Raman |1,0⟩↔|2,0⟩ (escapes the rank-2 death that killed clock-RSC). First-order field-insensitive. F′=0 polarizer is a clean F=1→|1,0⟩ funnel that **decays only to F=1** (closed sub-loop, no F=2 leak from the polarizer; off-resonant F′1 leak only ~0.44%). **With transverse/tilted pumps the floor improves 4–5× (0.05 → ~0.011)** — nearly competitive.
**Cons:** recoil-limited by the **~3.5-scatter recycle chain** (F=2 recycle ~2 + F′0 polarizer ~1.5, the 1/3 branching its cost); even optimized ~0.011 is ~1.5× above clock-EIT. Not the elegant closed cycle — still needs the 6.835 GHz Raman *and* a separate F=2 recycle. The transverse-pump trick **backfires at high T_r** (dumps recoil into a marginal radial mode → loss). **[V floor / V no-cool variants / I ranking]**

### 6 — clock-RSC (DISQUALIFIED)
**Pros:** would be field-insensitive, dephasing-robust, and lowest-floor (0.001) *if the coherent model were complete*.
**Cons:** the Δm=+2 D2 Raman is **rank-2/HFS-enabled** (J=½ ground can't supply Δm_J=+2; amplitude ∝ Δ_HFS/Δ²) → coherence-per-scatter is **Δ-independent and pinned at FoM ≈ 2–4**; with slow Lamb-Dicke cooling the scatter beats the cooling ~11–23:1 → **floor lifts to ≈0.45**, B-independent, unrecoverable. Verified three ways incl. explicit two-manifold diagonalisation. **[V]**

### 7 — F′=0 degenerate (within-F=1) (DEAD)
**Cons:** σ± on F′=0 forces the dark state to **|1,0⟩, mid-ladder**; the Δm=−1 cooling and Δm=+1 heating sidebands are mirror images, both resonant at Zeeman=ν_z → cancel (model: n̄≈10, flat in all Ω_R, Γ_p). dRSC needs an *edge* dark state; F′=0 (only m′=0) structurally cannot make one. **[V]**
**Pro:** the only thing salvaged — F′=0 σ± is a clean m=0 *selector* and *polarizer* for scheme #5.

### 8 — F′=3 (m′=0) (DEAD)
**Cons:** (i) the 1064 tensor puts **m′=0 only 3.7 kHz... 3.7 MHz from m′=±1 (0.62 Γ) → unresolved**; the tensor isolates the *edges* (m′=±3, gap 18.7 MHz = 3 Γ), not m′=0 (the parabola vertex). So |2,0⟩ isn't even dark (off-resonant m′=±1 pumps it). (ii) Even idealized, |2,0⟩ is mid-ladder → can't rectify (same as #7), plus |2,±2⟩ also dark → 3 dark states. (iii) F′=3 connects to F=2 only (ΔF=2 forbids F=1) → **field-sensitive**, and decays to F=2 only (cycling) → can't recycle a cross-F |2,0⟩. Strictly worse than F′=0 on every axis. **[V]**

---

## 2. Excited-state F′ choice (the structural backbone)

| F′ | reaches | decays to | m′=0 isolated? | role |
|----|---------|-----------|----------------|------|
| 0 | F=1 only | F=1 only (closed) | n/a (only m′=0) | F=1→\|1,0⟩ polarizer (scheme 5) |
| 1 | F=1 & F=2 | F=1 & F=2 | — | two dark states with σ⁺ (bad); leaks F=2 |
| **2** | **F=1 & F=2** | **F=1 & F=2** | yes (vertex, but field-insens. geometry) | **the working choice** — clock-EIT, stretched/dRSC |
| 3 | F=2 only | F=2 only (cycling) | **no** (gap 0.62 Γ, unresolved) | none usable (field-sensitive + can't recycle) |

**Key rules [V]:** F=1→F′=3 and F=2→F′=0 are ΔF=2, dipole-**forbidden**. Only **F′=1 and F′=2** are reachable from *both* ground hyperfines → only they can host a field-insensitive clock Λ (which needs an F=1 leg). F′=2 wins over F′=1 (F′=1 gives two dark states / worse branching). Tensor isolation is a parabola (∝ 3m′²−F′(F′+1)) with vertex at m′=0 → it isolates **stretched** states, never m′=0.

---

## 3. Beam geometry & B-field orientation (the new freedoms)

| geometry | enables | axial recoil/scatter | best regime |
|----------|---------|:--------------------:|-------------|
| axial beams, axial B | σ±, Δm=0,±2; clock-EIT, cross-F RSC | η_z²·4/3 = 0.0118 | default; field-insensitive |
| transverse/tilted pumps, axial B | same Λ; absorption recoil → radial | η_z²(cos²θ + ⅓): 0.0029 (⊥) | **low T_r RSC** (floor 4× lower) |
| any beams, transverse B | Δm=±1 (axial beams gain π) → within-F schemes | — | within-F=1 closed RSC (field-sensitive) |

**Transverse/tilted pump beams [V]:**
- **Pro (low T_r):** absorption recoil goes radial (harmless when radial is cold/deep), leaving only the emission's axial ⅓ → **4× less axial recoil** → F′=0 RSC floor 0.05 → ~0.011 (with slower recycle to drop the blue floor). Field-insensitive clock-Λ needs *only* transverse pumps, **no B rotation** (k⊥ẑ, E along the other transverse axis = σ± rel. axial B). A 45° tilt captures ~half the gain.
- **Con (high T_r):** **backfires** — dumps recycle recoil into the radial mode; at T_r ≈ 400 µK (η_trap = 2.73, marginal) this drives evaporative loss. Use transverse beams for *radial* cooling there, not the axial recoil trick.

**B-field rotation [V/I]:**
- **Pro:** transverse B lets axial beams carry π → enables the within-F=1 *closed-cycle* RSC (cooling Raman |1,0⟩↔|1,−1⟩, F′0 does funnel + recycle, ~3 scatters → floor ~0.010, marginally below scheme 5).
- **Con:** the within-F=1 cooling resonance is a **Zeeman transition → field-sensitive** (the *endpoint* |1,0,0⟩ stays field-insensitive, but the cooling process needs B stable). Trades the design's headline immunity for ~10% of floor — not worth it. **Keep B axial** for the recommended (field-insensitive) scheme.

---

## 4. Laser & modulator architecture

**One Eblana (1560) + one 1560 EOM — RECOMMENDED [V]**
- **Pros:** covers the *whole* sequence (MOT repump, gray-molasses Raman, in-fibre EIT, thermometry) by retuning the EOM (6.57–7.13 GHz). Telecom EOM is cheap, low-Vπ, broadband, fibre-coupled, pre-EDFA (low power); phase-mod survives SHG. **Both legs from one laser+EOM → laser's 0.6 MHz linewidth cancels common-mode → two-photon linewidth = RF synthesizer (sub-100 Hz, met *passively*).** Multi-tone EIT drive audited clean (largest unintended intermod 2.4×10⁻⁷).
- **Cons:** needs a multi-tone-capable RF chain (AWG/DDS) for the EIT phase. MEMS settle / beat-lock re-acquisition when switching the second seed off for coherent phases.

**780 EOM — only as broadband add-on [V]**
- **Pro:** path-selective option (low-power EOM on the EIT path only, isolates from MOT).
- **Cons:** the tag forces the EOM ≥200 MHz above 6.835, and GM(6.835)+EIT(7.13) are 300 MHz apart → must be *broadband* (6.5–7.2 GHz) microwave EOM = expensive, high-Vπ, high-power. A resonant 6.835 device covers free-space GM only, not in-fibre EIT. 1560 EOM preferred.

**Two doubling chains (for dual-end 0.0047) [I]:** common-mode via two SHG chains off one seed, **no OPLL**. Pro: floor 0.0073→0.0047. Con: more hardware (two PPLN chains).

**OPLL — SKIP [I]:** not needed (common-mode achieved via EOM), not the route to 0.0047 (the doubling chains are), and a sub-100-Hz lock at ~7 GHz is hard. Would *break* common-mode if a separate laser were an EIT leg.

**Rb-85 master role [V/I]:** coherence-free jobs only — absolute reference, optical pumping (F2→F′2), detection/imaging (F2→F′3 cycling). The two-laser split runs along the **coherence boundary** (Eblana = all coherent phases; master = state-prep + readout). **The master must NEVER be an EIT/Λ leg** (would cap the floor ≫0.044).

---

## 5. Thermometry

**D1 vs D2 [V/I]:**
- **D1 — preferred (opportunistic):** F′1–F′2 = 814 MHz vs D2's 157 MHz → ~5× more detuning room inside the rank-allowed window → ~5× less scatter; 5P₁/₂ has **no tensor** → sharper sidebands, better R/B contrast. The scatter pedestal is the bottom-end limiter, so this is the lever. Gated on **[O]** whether the kagome guides 795.
- **D2 — works but marginal at the floor:** limited HFS → larger scatter pedestal (~0.005–0.01) → can confirm n̄≪1 but not cleanly resolve 0.007.
- **Don't reach for 795 to "far-detune"** — the rank-2 FoM is detuning-proof; reach for it because the larger HFS allows detuning further *inside* the allowed window. Detection stays on the D2 master (F2→F′3).

**Locked vs unlocked 795 [V]:** a **free-running 795 DBR + 6.835 GHz EOM + wavemeter is sufficient — no lock.** Linewidth cancels (common-mode, both legs from one laser+EOM); drift is benign (rank-2 → scatter pedestal is Δ-flat; R = A_red/A_blue is pulse-area-independent at low n). Need only coarse monitoring: stay below the 814 MHz HFS and a few hundred MHz off resonance, and prevent slow drift toward resonance (where the scaling breaks and atoms heat/lose). Re-calibrate the π-duration (∝ Δ²) keyed to the wavemeter. **[O]** check EOM sideband purity (the one place a modulator imperfection could inject a parasitic).

**Bottom-end honesty [V/I]:** the asymmetry at the floor is R = 0.72% (sub-1%); statistics need ~3k–14k shots or ensemble averaging (not the bottleneck). The **pedestal** (scatter during the sideband-π) is the limiter. You can robustly state "deep ground state, n̄ at the ~10⁻² level"; the model's 0.0073 to three figures is beyond what the asymmetry certifies (D1 narrows this).

**Radial does NOT bias the axial readout [V]:** the axial probe (k∥ẑ) has zero Debye-Waller coupling to the radial motion (⊥ k). The only channel is the Gaussian-curvature ν_z smear (~0.2–0.8 kHz at pre-cooled n_r = 9–30), which is **symmetric** in red/blue → cancels in the ratio. Recipe: integrate sideband *area* across a detuning scan, not peak height. (At n_r ~ 1360 the 35 kHz smear is hopeless — pre-cool first.)

---

## 6. Radial mode — the binding constraint (not a "scheme", a precondition)

**Facts [V]:** ν_r level spacing = 0.26 µK ≪ Γ, η_r = 0.84 → the radial is **NOT resolved-sideband and cannot be sideband-cooled in-fibre**; the in-fibre beams are axial and can't cool the perpendicular motion. The radial relies entirely on **free-space pre-cool before load-in**.

| radial state | n_r | ν_z smear | trap-depth η | verdict |
|--------------|----:|----------:|-------------:|---------|
| gray molasses (2.5 µK) | ~9 | 0.24 kHz | ~440 | clean axial cooling/thermometry |
| bright molasses (8 µK) | ~30 | 0.78 kHz | ~140 | fine |
| **T_r = 400 µK** | ~1540 | 39 kHz | **2.73 (marginal)** | radial dominates; cool it first |
| post-transport (raw) | ~1360 | 35 kHz | ~3 | hopeless until pre-cooled |

**Pros/cons of options:**
- **Free-space molasses / gray molasses (pre-cool outside the tip) — REQUIRED.** Pro: only way to get the radial cold; full optical access (no transverse-PER gate); n_r → 9–30. Con: needs the free-space→guided load-in to be clean (the 40%-via-ferrule vs 96.5%-test-fibre gap, **[O]**, separable, affects all axial schemes equally).
- **Transverse-beam Doppler / gray molasses (in-fibre or at-tip) — the use for transverse beams at high T_r.** Pro: gives the unresolved radial mode the Doppler-type cooling it actually needs; rescues T_r ≈ 400 µK before it evaporates. Con: needs transverse optical access into the core (hard mid-fibre; feasible at the tip) **[O]**.

**Operating-regime ranking [I]:**
- **Low T_r (n_r ≲ tens):** full matrix applies; clock-EIT recommended; transverse-pump trick *safe* and useful for chasing the RSC floor.
- **T_r ≈ 400 µK:** clock-EIT is clearly best (robust to 39 kHz smear + radial intensity modulation; gentlest → least evaporative loss); transverse-pump RSC trick **backfires**; **cool the radial first** with transverse Doppler cooling.

---

## 7. One-line verdicts

- **Cool with:** clock-EIT, |1,−1⟩/|2,+1⟩→|F′2,0⟩, single_end_tagged, axial B. Floor 0.0073 (→0.0047 dual-end). **[V/O coherence]**
- **Drive with:** one Eblana + one 1560 EOM, common-mode; master = Rb-85 for prep/readout only; no OPLL. **[V]**
- **Measure with:** D1 (if 795 guides), unlocked DBR + EOM + wavemeter; report n̄ ~ 10⁻², not 3 figures. **[V/O]**
- **Precondition:** radial pre-cool to n_r ≲ tens (free-space; transverse Doppler if stuck hot). **[O]**
- **F′=0 / F′=3 m=0 cooling:** rejected (F′=0 cross-F cools but ~0.011 > 0.0073; the rest dead). Transverse pumps = a real but regime-limited RSC tool, not a reason to switch off EIT. **[V/I]**

## Provenance (scripts / docs, in /mnt/user-data/outputs/ unless noted)
`eit_cooling_tool.py` (clock-EIT, presets) · `m0_rsc.py` v0.3.0 (cross-F m=0 RSC + transverse-pump tilt) ·
`f0_drsc.py` (degenerate F′=0 no-cool) · `thermometry.py` (sideband thermometry) ·
`EIT_brief_v12_comparison.md` (six-column matrix incl. F′=0) · `clock_EIT_consolidated_v13.md` ·
`D1_hybrid_consolidated_findings.md` · `full_sequence_config.md` · project Stark/anti-trap docs.
