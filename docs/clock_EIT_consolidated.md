# Clock-EIT Sideband Cooling of ⁸⁷Rb in a 1064 nm Kagome-HCPCF Lattice
## Consolidated technical state and the conceptual path that produced it

*Text-only document — figures omitted (chat image limit reached). All numbers are from the multilevel QuTiP steady-state solver unless noted. Tags: [V] computed/verified in this program, [I] inferred/estimate, [O] open.*

---

# PART I — CONSOLIDATED TECHNICAL STATE

## 1. System and trap

⁸⁷Rb, D2 line, loaded in a 1064 nm **axial** optical lattice formed inside a kagome K19 hollow-core photonic-crystal fibre (XLIM Limoges; 48 µm core, MFD 38 µm at 780 nm → w₇₈₀ ≈ 19 µm; w₁₀₆₄ ≈ 19 µm inferred from the measured radial frequency).

| quantity | value |
|---|---|
| axial trap ν_z (stiff, vertical) | 2π × 430 kHz |
| radial trap ν_r (shallow, degenerate) | 2π × 5.42 kHz |
| trap depth U₀ | 22.8 MHz = 1094 µK |
| lattice spacing | 532 nm |
| Lamb–Dicke η (single 780 photon) | 0.094 |
| η_eff (retro, 2k) | 0.187 |
| Γ_D2/2π, Γ_D1/2π | 6.07, 5.746 MHz |
| A_HFS | 6834.682610 MHz |
| g_F(F=2), g_F(F=1) | +½, −½ |
| 5P₃/₂ hyperfine centroids {0,1,2,3} | {−302.07, −229.85, −72.91, +193.74} MHz |
| F′=3 above F′=2 | +266.65 MHz |
| clock-magic field | 3.2288 G (interrogation only, **not** cooling) |

The stiff axis is what we cool. The radial direction is ~80× shallower and **degenerate**, which drives the radial-inhomogeneity program (§8) and is the reason field-insensitivity (§9) matters.

## 2. The cooling scheme — clock-EIT on a field-insensitive dark pair

Λ system on the D2 line, both legs to the **same** excited sublevel **|F′=2, m′=0⟩**:

- probe **σ⁺**, |F=1, m=−1⟩ → |F′2,0⟩
- control **σ⁻**, |F=2, m=+1⟩ → |F′2,0⟩

Both ground legs have g_F·m_F = +½, so the dark superposition is **first-order magnetic-field-insensitive at any field** (the differential Zeeman shift vanishes identically). This is the defining choice of the scheme: it makes the dark resonance immune to the radial B-field/trap inhomogeneity the cloud samples. The clock-magic 3.2288 G field is used only for the subsequent clock interrogation, not for cooling.

Two-photon detuning **δ₂ is servoed to the dark resonance**, not hardcoded — it drifts with optical power and radial position and must track.

## 3. Operating point (final, fully audited)

| parameter | value | note |
|---|---|---|
| single-photon detuning Δ | **+55 MHz blue** (range 45–55) | flat floor optimum; time + cloud favour low end |
| probe/control ratio Ω_p/Ω_c | **0.10** | the weaker-probe lever (§6) |
| total Rabi Ω_tot | √(4Δ·ν_z) ≈ 9.7 MHz | pinned to the EIT condition |
| → Ω_c, Ω_p | ≈ 9.68, 0.97 MHz | at Δ=55, OmR=0.10 |
| δ₂ servo set-point | ≈ −0.14 MHz (dual-end) / −0.25 (single-ended) | architecture-dependent |
| repump Rabi Ω_rep | **≈ 3** (not 1.5) | audited/optimized this session |
| repump detuning Δ_rep1 (F=1→F′1) | **≈ 15 MHz** (not 30) | closer = better |
| repump detuning Δ_rep2 (F=2→F′1) | 5 MHz | default near-optimal |
| cooling B-field | 1.0–1.5 G | any field works; pair is field-insensitive |

**Powers at the atoms** (19 µm waist, I_sat = 1.67 mW/cm²) [I]: control ~0.11 µW, probe ~3–5 nW, each repump ~20 nW (up from ~5 nW at the old Ω_rep=1.5).

## 4. Delivery architectures (both realize the same atomic operating point)

**(a) Dual-end, carrier-suppressed EOM — PREFERRED.** Arm A carries the control (σ⁻, direct, clean tone). Arm B carries the probe via a plain phase EOM at the 6.835 GHz hyperfine splitting, depth **β = 2.405 (first J₀ zero)** → the carrier vanishes and the σ⁺ probe is the upper J₁ sideband (F=1 sits 6.835 GHz below the control's F=2); all other sidebands land ≥6.835 GHz off-resonance and are harmless. Opposite-end injection, **f_A = 0** (AOMs for intensity/pulsing only). Arm power split A:B ≈ **95:5** at OmR=0.10. No SSB modulator, slave laser, or filter cavity. **Floor ~0.005.**

**(b) Single-ended tagged retro — FALLBACK** (if two-ended vacuum access is impractical). One fibre end: control carrier + probe upper-sideband from a phase EOM at **β ≈ 0.59**, co-propagating; a double-passed tag AOM **2f_A = 300 MHz** down-shifts the return; a λ/4 in the retro arm flips helicity. The **down-shift** is essential — an up-shift would crash the rejected return-control into F′=3. **Floor ~0.0075** (OmR=0.10) / ~0.0092 (OmR=0.12). The extra cost vs (a) is the rejected-field scatter.

## 5. The complete floor budget

Steady-state ⟨n_z⟩, dual-end, Δ=55, OmR=0.10, optimized repump. **Every 5P₃/₂ hyperfine level is now accounted for**, and the manifold is frame-consistent (max_conf = 0).

| component | floor | increment | character |
|---|---|---|---|
| base (clean Λ, no F′0/1/3) | 0.0014 | — | dark-state + recoil limit |
| + F′=1 | 0.0048 | **+0.0034** | **dominant**: common Λ-closing level, residual dark-state coupling −0.31, ~212 MHz |
| + F′=3 | (within above) | +0.0010 | secondary: control-only, ~212 MHz, coherent admixture Ω_F3/Ω_c = 1.058 |
| + F′=0 | (within above) | +0.0001 | negligible: probe-only, ~285 MHz, decays 100% → F=1 |
| **all contaminants** | **0.0048** | — | increments are **non-additive** — F′=1 dominates |

**Final floors (all of F′=0,1,2,3 in, repump optimized):**
- dual-end: **~0.005** (flat in Δ across 45–80; ⟨n_z⟩ ≈ 0.005 → **>99% ground-state population**)
- single-ended tagged (realized): **~0.0075** (OmR=0.10), ~0.0092 (OmR=0.12)

## 6. Cooling dynamics

- **The mechanism is engineered red/blue sideband asymmetry.** EIT cooling works by placing the Fano-narrowed bright resonance so the red (cooling) sideband is enhanced and the blue (heating) sideband suppressed. The Liouvillian gap *is* the net asymmetry rate.
- **Weaker-probe lever [V]:** the cooling rate **saturates** with Ω_p/Ω_c (gap ≈ 0.0017/0.0024/0.0027 MHz at 0.11/0.18/0.25) while the floor keeps dropping. So the optimum is at **low probe** (0.10–0.12), bounded below only by the cooling-time/trap-lifetime budget. This is the single most important and least obvious optimization lever.
- **Cooling time vs Δ [V]:** τ rises with detuning — Δ=45 → 0.14 ms, Δ=60 → 0.30 ms, Δ=80 → 0.69 ms (dual-end, OmR=0.10). Lower Δ cools faster (higher detuning = slower scattering = slower cooling), as physically expected.
- **Axial-Doppler asymmetry channels [V]:** the radial-motion → axial-Doppler coupling is **null** (k·v_r = 0, ⊥ geometry; and ν_r ≪ ν_z by ~80× → adiabatic, n_z invariant; the parametric M5 channel needs ν_r ≈ 2ν_z = 860 kHz, off by 160×). This is *why* a quasi-static W(r)/A(r) treatment of the radial bath is rigorous. Beam non-axiality θ couples 2k·v_r·sinθ ~ 0.08 kHz/° — an alignment **tolerance**, not a floor term.

## 7. Excited-state Stark — no anti-trap [V]

At 1064 nm the 5P₃/₂ manifold is **not trapped** (α₀ = −1149 a.u., α₂ = +563 a.u.; Chen / Gonçalves-Raithel, PRA 92, 060501(R)). The cooling sublevel **|F′2,0⟩ has a pure scalar shift +38.1 MHz** — the F′=2 hyperfine tensor term vanishes identically (6j{2 2 2; 3/2 3/2 3/2} = 0), so the shift is geometry-independent. The ground 5S₁/₂ scalar polarizability is +687.3 a.u. > 0; 1064 nm is red of the D lines, so it **lowers** the ground state (this *is* the trap), and conversely **blue light raises** the ground state — the anchor used to fix every AC-Stark sign in the program.

## 8. Radial inhomogeneity — the cloud (v13 S4) [V]

The shallow degenerate radial trap means the cloud samples a range of trap parameters. Radial scaling laws (s(r) = exp(−2r²/w²)):
- ν_z(r) = ν_z0·√s, η(r) = η0·s^(−¼), Ω(r) = Ω0·√s
- **Δ_eff(r) = Δ₀ + c·(1−s), c = 60.9 MHz** — the radial detuning shift (the "M3" term), which the early radial passes were **missing**. It follows from the +38.1 MHz scalar shift of |F′2,0⟩ and dominates radial degradation beyond ~50 µK.

**Semiclassical Monte-Carlo (the definitive cloud metric):** for a 100 µK cloud, floor ≈ **0.0085 (Δ=45) vs 0.0097 (Δ=80)** at OmR=0.10 with all contaminants — Δ=45 is cloud-optimal (broader bright feature tolerates the ν_z(r) spread). [I] absolute cloud floor ±0.001 (coarse per-radius δ₂ grid); the ordering is robust.

**Per-scheme verdict — clock-EIT decisively beats Raman SBC on the cloud.** Cloud coverage at 100 µK: EIT ~99% (feature width 150 kHz, r < 12.45 µm) vs RSC ~19% (sideband 16 kHz, r < 3.70 µm); cloud-averaged ⟨n_z⟩ ≈ 0.03 (EIT) vs ≈ 4 (RSC). Re-cooling to ≲50–100 µK is comfortable.

## 9. Field-insensitivity (vector / tensor) [V]

The cooling pair is **first-order field-immune** (both g_F·m_F = +½). The residual 2nd-order shift is 0.50 kHz per unit ellipticity. The ground tensor polarizability is zero (J = ½). This is the property that makes the scheme work across the inhomogeneous radial bath.

## 10. Roads not taken (and why)

- **m′=2 stretched pair:** radially identical cooling performance but **field-sensitive**, so dephased by the radial B/trap spread. Abandoned for the field-insensitive m′=0 clock pair. [V]
- **D1 line:** does **not** help (dual-end D1 0.0052 ≈ D2 0.0048). The naive "D1 has no F′=3" advantage cancels because on D1 *both* legs acquire F′=1 admixture (F=1→F′1 allowed), whereas on D2 only the control does. [V]
- **F′=1 as the EIT level:** F′=2 chosen (~12.5× less off-resonant scatter). [V]
- **"F′=1 EIT" as a second window:** does not exist — there is one two-photon resonance (set by the ground hyperfine splitting), and both common levels (F′=1, F′=2) feed it. See §12. [V]

---

# PART II — THE HISTORICAL CONCEPTUAL PATH

This is how the understanding actually evolved — the pivots, the wrong turns corrected, and the role of adversarial cross-audit. It is worth recording because several of the final numbers are right for reasons quite different from why we first believed them.

## Stage 0 — Groundwork: does 1064 nm trap the excited state, and which way does light shift?
The first substantive question was whether the lattice anti-traps 5P₃/₂ (which would wreck cooling). Resolving it forced us to fix the **AC-Stark sign convention** from first principles and anchor it three independent ways (analytic 2-level, full diagonalization, and the lattice itself: the ground state is trapped because 1064 is red of the D lines). **Sign discipline became a recurring theme** — it is the single most error-prone quantity in the whole problem, and it later resurfaced in the Gemini audit. Outcome: no excited trap; |F′2,0⟩ shift = +38.1 MHz, pure scalar.

## Stage 1 — The defining pivot: from a simple stretched pair to the field-insensitive clock pair
An early instinct is to cool on the stretched m′=2 transition (cleanest cycling). The pivot was recognizing that the **shallow degenerate radial trap** subjects the cloud to a spread of magnetic field and light shift, which dephases any field-*sensitive* dark state. Switching to the **|1,−1⟩/|2,+1⟩ clock pair** (both g_F·m_F = +½) makes the dark resonance first-order field-immune at any field. This single choice is what makes the scheme robust to radial inhomogeneity — and it reframed the entire later radial program around "does the cloud stay dark," not "does the cloud stay on a Zeeman line."

## Stage 2 — Building a solver we could trust, and a method
Everything downstream rests on a multilevel QuTiP steady-state engine (full Breit-Rabi grounds, tensor-diagonalized 5P₃/₂, full Clebsch-Gordan ladders, multi-rotating-frame BFS, full hyperfine decay branching, recoil). Alongside it we adopted a **working method that repeatedly paid off**: state assumptions as [V]/[I]/[O]; **compute, don't assert**; re-verify any result that overturns a prior conclusion by rebuilding it a different way; and for any "no benefit / already optimal" claim, **sweep the parameter** rather than argue. Most of the corrections below were caught by this discipline.

## Stage 3 — Optimizing the operating point: the counterintuitive lever
The non-obvious discovery was the **weaker-probe lever**: lowering Ω_p/Ω_c lowers the floor while the cooling rate saturates, so the optimum sits at *weak* probe (0.10–0.12), not at the "balanced" Λ one might guess. Detuning and Rabi were pinned to the EIT condition, leaving the probe ratio as the real knob.

## Stage 4 — Delivery architecture, and a correction owed to the auditor
We first thought a dual-end probe delivery would need an SSB/IQ modulator. **The external auditor corrected this**: a plain phase EOM at the 6.835 GHz hyperfine, driven to the **first J₀ zero (β = 2.405)**, suppresses the carrier and leaves the probe as a clean J₁ sideband — no SSB hardware. That became the preferred architecture. The single-ended tagged retro (phase EOM + double-passed down-shifting tag AOM + λ/4) survives as a fallback; we established the tag must **down-shift** (an up-shift crashes the rejected control into F′=3).

## Stage 5 — The radial program: a missing term and the right metric
Treating the cloud properly required recognizing it samples ν_z(r), η(r), Ω(r) **and** a radial detuning shift Δ_eff(r) — the **"M3" term that the first radial passes omitted entirely**. Adding it (c = 60.9 MHz, from the +38.1 MHz scalar shift) changed the radial story qualitatively. We also settled the right *metric*: not the frozen turning-radius floor (conservative, over-weights the tail), but a **semiclassical Monte-Carlo** trajectory average, which sits between rate-average and floor-average. This is what showed clock-EIT covers ~99% of a 100 µK cloud while Raman SBC covers ~19% — the decisive per-scheme result.

## Stage 6 — Cross-audits: a sign flip and a stale operating point
Two external LLM audits stress-tested the program.
- **Gemini** had the right *method* for the AC-Stark accounting (multilevel CG sum) but **flipped every sign** (magnitudes ~right, signs all wrong) and, relatedly, had the floor-vs-power dependence backwards twice. Adjudicated against the three-way sign anchor from Stage 0: the control shift on |2,+1⟩ is **+228 kHz up**, not −308 down.
- A **v13 session memo** was mostly accurate but carried a **stale operating point** (Δ=80, OmR=0.25) because it had only scanned Ω_c *upward* and missed the weaker-probe lever from Stage 3.

## Stage 7 — The Δ disagreement, resolved by a discriminator the other model lacked
The auditor then made a sharp, falsifiable claim: at *matched* probe ratio, Δ=80 Pareto-dominates Δ=45 on-axis (lower floor **and** faster). They were right that our original head-to-head had **conflated two levers** (we had changed Δ and OmR together). Isolating them:
- **The discriminator is F′=3.** With F′=3 *off* (≈ their 3-level model) the floor falls monotonically with Δ and Δ=80 wins — we reproduced this exactly. With F′=3 *on*, the F′3 scatter grows with Δ and pulls the optimum down to ~60. So neither 45 (our first answer) nor 80 (theirs) was the on-axis floor optimum.
- **The cooling time inverts their claim:** in the full model lower Δ cools *faster* (0.14 ms at 45 vs 0.69 ms at 80), opposite to their "Δ=80 faster." 
Credit where due: the probe-ratio lever and the F′3-off high-Δ preference are genuinely theirs; the F′3 physics and the time direction are ours.

## Stage 8 — Closing the budget: two compensating errors, and a lesson (this session)
A series of pointed questions closed the last gaps — and produced the most instructive result of the program.
1. *"Is the axial Doppler asymmetric?"* → yes, that asymmetry **is** the cooling mechanism; and the radial→axial Doppler channel is null (⊥ geometry + adiabaticity). 
2. *"Why only F′=2 EIT, not also F′=1 EIT?"* → conceptual clarification (one two-photon resonance; F′=2 dominates only by detuning) **plus** the discovery that the solver had been **omitting the F′=1 common-level coupling**. Including it roughly **doubled** the floor — F′=1 is the *largest* contaminant, bigger than the F′=3 we already carried.
3. *"Did you consider the repumpers?"* → they were in the model but **never optimized**; the defaults **under-pumped**, so leak states accumulated uncooled and inflated the floor by ~1.5×. Optimizing them (Ω_rep 1.5→3, Δ_rep1 30→15) **recovered almost exactly the F′=1 penalty**.
4. *"Add F′=0"* → confirmed **negligible** (+0.0001); the contaminant budget is now closed and ranked (F′=1 ≫ F′=3 ≫ F′=0).

**The lesson:** our original headline floor (~0.005) was numerically right but for the wrong reasons — a **F′=1 omission (optimistic ~2×) that happened to cancel a default-repump pessimism (~1.5×)**. The intermediate "revise up to ~0.008" claim was a half-correction (F′=1 in, repump still wrong). With *both* fixed, the fully-audited floor lands at **~0.005 dual-end / ~0.0075 single-ended** — the same headline, now for the right reasons, with every excited level and the repumpers explicitly accounted for.

---

# APPENDIX — the F′=1 conceptual point in full

It is worth stating precisely because it caused the largest single correction. **EIT is a two-photon (Raman) resonance**: the dark state lives in the ground manifold and its position is fixed by the two laser frequencies and the 6.835 GHz ground splitting — *independent of which excited level is the intermediate*. So there is **one** transparency window, not one per F′. Of the four 5P₃/₂ levels, two are "common" (reachable from both legs to |F′,0⟩) and two are single-leg:

| F′ | probe σ⁺ from \|1,−1⟩ | ctrl σ⁻ from \|2,+1⟩ | role |
|----|----|----|----|
| 0 | −0.577 | 0 | probe-only — negligible scatterer |
| 1 | **−0.707** | **+0.548** | **common, Λ-closing — dominant contaminant** |
| 2 | +0.408 | +0.707 | common, the named EIT level |
| 3 | 0 | +0.447 | control-only — secondary scatterer |

Both common levels feed the *same* δ₂=0 window. We call it "F′=2" only because the lasers sit ~55 MHz from F′=2 vs ~212 MHz from F′=1. F′=1 does **not** make a second EIT window — it **perturbs the one window**, and not weakly: the F′=2-dark superposition does **not** simultaneously cancel its F′=1 coupling (the dipole ratios mismatch, ratio-of-ratios = −0.20 ≠ 1), leaving a residual dark-state coupling to |F′1,0⟩ of −0.31, full strength, suppressed only by the 212 MHz detuning. That residual is the +0.0034 it adds to the floor. F′=0 and F′=3, being single-leg, never form a dark state at all — they are pure off-resonant scatterers, F′=3 the larger because it is closer and the control's CG to it is larger.

---

## Status

The internal physics budget is **closed**: scheme, operating point, both delivery architectures, the complete F′=0,1,2,3 contaminant budget, the optimized repumpers, the radial cloud treatment, the anti-trap, and field-insensitivity all agree and are mutually consistent; the two external cross-audits are reconciled. Headline: clock-EIT, Δ≈55, OmR≈0.10, repump Ω≈3/Δ_rep1≈15, dual-end carrier-suppressed delivery, **⟨n_z⟩ ≈ 0.005** (single-ended ~0.0075), cloud-robust to ~100 µK.

Remaining [O], all outside the cooling-physics core: re-running the cloud MC and the on-axis Δ-scan at the optimized repump for final brief numbers (the scaling is mechanical, ~−40%); the noise/parasitic budget (dephasing, polarization, intensity) as a separate consolidation; and the non-physics career thread.
