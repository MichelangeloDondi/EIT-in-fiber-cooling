# v13 S4 — radial inhomogeneity of the Gaussian 1064 profile: the M3 (Δ_eff(r)) effect

## System / model
Dual-end clock-EIT, ⁸⁷Rb D2, F′=2, m′=0 dark pair, B=3.229 G, OmR=Ω_p/Ω_c=0.12, option-A repump. 1064 lattice Gaussian, w_L=19 µm, U₀=22.8 MHz (1094 µK), ν_z0=430 kHz. Solver: clock_tagged_solve (dual-end), driven per-radius via its nu_z / eta_z / Otot_abs / Dc hooks. Thermal floor = frozen-turning-radius average over the 2D radial Boltzmann distribution (atom placed at its classical turning radius — conservative).

Three radial effects, with s(r)=exp(−2r²/w_L²):
- **M1** ν_z(r)=ν_z0·√s, η(r)=η₀·s^(−¼)  (motional).
- **M2** Ω(r)=Ω₀·√s  (the 780 EIT beam is itself ~19 µm in the same core, so Ω drops off-axis).
- **M3 (NEW)** Δ_eff(r)=Δ₀ + c·(1−s), **c = 60.9 MHz** — the differential excited−ground 1064 light shift moves the F′2 resonance down as the atom moves out, so the fixed laser becomes more blue-detuned. **S1/S2 omitted this** (held Δ_eff fixed). [c is now computed, not estimated: the |F′2,0⟩ shift is **purely scalar +38.1 MHz** because the hyperfine tensor polarizability of the entire F′=2 manifold vanishes (α₂(F′=2)=0, the 6j {2 2 2;3/2 3/2 3/2} is null), so c=38.1+22.8 is geometry-independent. The earlier 65.1 used an excited shift +42.3; the correct scalar is +38.1.]

## Tentative conclusion
1. **M3 is the dominant radial-inhomogeneity effect for T ≳ 50 µK and was missing from S1/S2.** Without it the floor is nearly flat in T; with it the floor climbs steeply off-axis because the EIT resonance slides off the sideband (bright shift ∝ Ω²/4Δ_eff ∝ s/Δ_eff falls faster than ν_z ∝ √s).
2. The **cloud-optimal detuning is higher than the on-axis optimum** (~80 vs ~45–60 MHz). On-axis wants low Δ (least F′3 contamination); the cloud wants higher Δ (M3 matching improves as 1/Δ). Δ₀≈80 minimizes the thermal floor at both 100 and 400 µK.
3. At the cloud-optimal Δ₀=80 the **frozen** floor is 0.0081 / 0.0254 / 0.060 at 25 / 100 / 400 µK (corrected c=60.9). **But the frozen bound over-counts the tail (see point 6) — the physical floor is ~2–3× lower.** Even so, M3 means 100 µK does not reach the on-axis ~0.005; to get there across the cloud, re-cool to ≲50–100 µK or flatten the 1064 (super-Gaussian removes M1/M2/M3).
6. **Non-frozen refinement (definitive — MC semiclassical, supersedes the frozen floors).** The frozen approximation places every atom at its turning radius (outermost, weakest cooling). The correct treatment integrates classical 2D radial trajectories sampled from the thermal phase space, each carrying the axial rate equation ṅ=−W(r)·n+A(r) with the local Liouvillian-gap rates. Results at 100 µK:

   | Δ₀ | frozen | floor-avg ⟨A/W⟩ | rate-avg ⟨A⟩/⟨W⟩ | **MC trajectory (true)** |
   |---|---|---|---|---|
   | 45 | 0.0399 | 0.0190 | 0.0068 | **0.0094** |
   | 80 | 0.0254 | 0.0153 | 0.0083 | **0.0102** |

   The MC lands between the two analytic bounds, closer to the rate-average (radial period 185 µs is ~3× shorter than the 625 µs cooling time). **The 100 µK cloud floor:** the earlier semiclassical-MC estimate ≈0.0095 is **superseded** by the clk2 quasi-static ceiling 0.0169 and the dynamic-MC result (realized sits below quasi-static); the T_r-gated all-in is ≈0.012 at 100 µK. **Δ₀=45 remains the cloud optimum (the semiclassical 0.0094 < 0.0102 at Δ₀=80): the on-axis-optimal detuning needs no radial correction.** The frozen-based "move to Δ₀=80" was a tail-weighting artifact, now overturned. To approach the on-axis ~0.005 across the cloud, re-cool to ≲25–50 µK; flattening the 1064 (super-Gaussian) removes M3 entirely.
4. **The floor is tail-dominated.** At 100 µK / Δ₀=45, the inner 25% of the cloud (r<r_rms=4 µm) contributes only **4%** of the thermal floor; the outer tail (r>r_rms), where the mismatch is several feature-widths and ⟨n_z⟩≈0.07–0.24, sets the rest. So the single-atom "mismatch vs feature-width at the rms edge" comparison (≈0.4 widths, ⟨n_z⟩≈0.009, modest) is correct but is the **wrong diagnostic for the floor** — the floor lives in the tail. Optimizing the floor = controlling the tail (re-cool / flatten / raise Δ₀), not the core.
5. **Per-scheme verdict (cloud axial-cooling coverage).** The schemes diverge mainly in radial *coverage*, set by feature width:

   | scheme | on-axis floor | window | coverage @100µK | cloud-avg ⟨n_z⟩ @100µK | field-insensitive |
   |---|---|---|---|---|---|
   | **clock-EIT (m′=0)** | 0.005 | 150 kHz | **99%** | **≈0.03** (M3-degraded) | **yes (magic)** |
   | m′=2 EIT | 0.018 | 150 kHz | 99% | ≈0.03 (same M3) | no |
   | RSC (stretched) | 0.002 | 16 kHz | **19%** | ≈4 (81% uncooled) | no |
   | dRSC | 0.007 | 16 kHz | 19% | ≈4 | partial |

   RSC's narrow resolved sideband restricts it to ≲25–50 µK, well-centered clouds (coverage 83%/48%/19% at 25/50/100 µK); at 100 µK it leaves 81% of the cloud axially hot (~5 quanta). EIT's ~10× broader window cools ~99% at 100 µK. So for any cloud warmer than ~25–50 µK there is no contest. Combined with field-insensitivity (magic), **clock-EIT is decisively preferred**; m′=2 is radially identical but field-sensitive and dominated; RSC's low on-axis floor is moot at cloud scale. There is no field-insensitive RSC variant that also cools the cloud. *(Low-T caveat: at ≲25 µK RSC's on-axis floor 0.002 beats EIT's 0.005 for the ~83% it reaches — RSC wins only for a very cold, centered sample.)*

## Verified vs inference
- **[V]** Radial tables and thermal floors above (solver, Nf=8, dual-end, c=65.1): see the M1+M2 vs +M3 comparison. The +M3 radial table at Δ₀=45 rises 0.005(r=0)→0.030(6µm)→0.26(12µm); at Δ₀=80 it rises more slowly.
- **[V]** Δ₀-scan minimum of the thermal floor at Δ₀≈80 (100 µK: 0.043→0.0285→0.052 across Δ₀=45/80/100; 400 µK monotone-favoring 80 over 45 by 2.4×).
- **[V]** Sign/direction of M3: Δ_eff increases off-axis, bright shift falls below ν_z, atoms under-cooled.
- **[V]** c=60.9 MHz computed from the polarizabilities: |F′2,0⟩ shift is purely scalar +38.1 MHz (α₂(F′=2)=0), geometry-independent. Floors above are robust to c (65.1→60.9 barely moves them).
- **[V]** Frozen turning-radius weighting is conservative by ~2–3×: the spatial-Boltzmann rate-average gives 0.0089 (Δ₀=80, 100 µK) vs frozen 0.0254. Physical floor ~0.010–0.015 (between rate-avg and floor-avg limits, radial ~3× faster than cooling).
- **[I]** δ₂ locked at the center-optimal value across radii (the two-photon detuning is 1064-scalar-common-mode, so off-axis drift is second-order via the 780 differential shift only).

## Checkable questions
1. Does a full trajectory-averaged (non-frozen) treatment bring the 100 µK floor at Δ₀=80 down from 0.0285 toward ~0.011, and does it change the cloud-optimal Δ₀?
2. Confirm c for |F′2,0⟩ from the measured polarizabilities + the actual 1064 polarization geometry in the fiber (⊥ vs ∥ to B). This sets both the magnitude of the degradation and the cloud-optimal Δ₀.
3. A super-Gaussian / flat-top 1064 removes M3: does the cloud floor then recover to the on-axis ~0.005 at 100 µK, and is such a profile realizable in the K19 core (higher-order-mode superposition vs engineered fiber)?
4. Should the operating-point recommendation move from the on-axis Δ=45 to the cloud-optimal Δ≈80 if the experiment runs at ~100 µK radial? (Trade: on-axis 0.0048→0.0055, but 100 µK cloud 0.043→0.0285.)
