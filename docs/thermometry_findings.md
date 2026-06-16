# External audit — thermometry / readout configuration (Δm=0 clock Raman under tagging)

Purpose: falsify the readout scheme that verifies the cooling. The cooling floor is worthless if ⟨n_z⟩ cannot be measured without bias at the 0.02 level. Each claim tagged **[V]** verified (computed/derived or validated prior work), **[I]** inference (reasoned, not computed), **[O]** open (needs computation or a spec). Attack the **[O]** items first — unlike the cooling, this configuration has **no solve behind it**: the contrast and the inferred-⟨n⟩ bias are the explicitly-deferred "sandbox-sized computation not yet run."

> **AUDITOR RETURN — verified (re-run independently this session; `thermometry_sim.py`, `thermometry_phase.py`, figure).** The deferred Q1/Q2/Q4 were computed; both gates pass (weak-probe recovery to ±0.0002; Nf-stable to 1e-15) and I reproduce every number. Outcome: **[O1] CLOSED** — the raw red/blue ratio carries a clean **additive +0.010 pedestal bias** at the operating point (= half the floor, exactly the audit's worry), the *finite-pulse carrier-wing* mechanism; removed to ±0.0002 by either a carrier-only pedestal subtraction or Blackman apodization (which suppresses the wing by ~10³, raw ratio then faithful up to 1/t_π ≈ 85 kHz). **[O2] CLOSED** — a safe square window is t_π ≈ 20–60 µs (1/t_π ≈ 17–50 kHz ≪ ν_z); raw bias explodes above ~120 kHz. **[O4] CLOSED** — the retro Raman first sideband ∝ sin θ on *both* red and blue, so it cancels in the ratio: ⟨n⟩ is θ-independent (subtracted ⟨n⟩ flat across all θ); contrast ∝ sin²θ is an SNR knob (antinode θ=π/2), and time-separated readout makes a readout-specific θ free regardless. **Residual:** [O3] (cooling/tagging-field extinction during the readout window) and the two differential-shift sub-mechanisms of [O1] (scan-dependent AC-Stark, Fano background of nearby lines) are *not* in this isolated clock-pair model — they are gated by [O3], i.e. they vanish if the cooling fields are well extinguished during readout. [I5]/[I7] confirmed (η_R=0.188 used; sin θ structure verified analytically and numerically).

## Configuration under audit
After cooling, read ⟨n_z⟩ by resolved-sideband Raman spectroscopy on the **clock pair** |F=1,m=0⟩ ↔ |F=2,m=0⟩, through the **same bare-mirror retro path** used for cooling (one nm-stabilized mirror, double-duty).
- **Geometry/polarization:** bare normal-incidence mirror → σ-label preserved → forward σ⁺ × return σ⁺ drives a Δm=0 two-photon operator that is *Doppler-sensitive* (counter-propagating, k₁+k₂ ≈ 2k) → couples to axial motion. (QWP+mirror would instead give Δm=±2, the interferometry transition — not used here.)
- **Frequencies:** Raman pair split by the 6.835 GHz ground hyperfine (the EOM generates it, clock-referenced synthesizer), scanned about the clock carrier; red sideband (n→n−1) and blue (n→n+1) at ∓ν_z = ∓430 kHz.
- **Observable:** red/blue amplitude ratio R = A_red/A_blue → ⟨n⟩ = R/(1−R). After good cooling the red sideband is suppressed (Leong-type spectrum).
- **Required pre-step (park → read):** cooling parks ≈94 % of the population in the dark state |1,+1⟩ (swapped m′=2), not in the clock state. A microwave/RF Δm=−1 carrier π-pulse transfers |1,+1⟩ → |1,0⟩ before readout. This same clock transfer is independently required for the m′=2 echo-T₂ measurement, so it is not extra apparatus.
- **Timing:** pulsed, cooling fields off during the readout window (Leong: 250 µs Raman / 25 µs pump cycles; Chiu/Rensburg: separate readout phase).

## Tentative conclusion
The readout *architecture* is sound and field-robust by construction: the clock pair is first-order B-insensitive, decoupling the measurement from the very B-noise the m′=2 cooling is exposed to, and the bare-mirror reflection rule that makes the Δm=0 path Doppler-sensitive is computed, not assumed. The exact scheme (clock-state Raman sideband asymmetry) is demonstrated in HCPCF (Leong) and in fiber/tweezer Rb (Chiu, Rensburg). **Following the auditor return (above), the quantitative case is now largely [V]:** the dominant bias mechanism is a +0.010 finite-pulse pedestal, removable to ±0.0002, with a clear safe pulse window and no standing-wave-phase bias. The thermometer reads ⟨n_z⟩=0.02 faithfully provided the readout pulse is shaped (or its pedestal subtracted) and the cooling/tagging fields are extinguished during readout. **Only [O3] (the extinction spec) now gates a measured ⟨n_z⟩.**

## Settled — do not re-litigate
- **[V, law]** Bare-mirror reflection rule (explicit Jones + dipole): σ⁺→σ⁺, helicity flips with **k**. This is what makes forward × return a Δm=0, Doppler-sensitive operator. The earlier "retro nulls the sideband Raman" was a transition/optic mismatch, since retired — it is not a selection-rule impossibility.
- **[V]** The clock pair |1,0⟩↔|2,0⟩ is first-order magnetically insensitive (the readout does not smear under the in-fiber B-noise; quadratic Zeeman only, ~Hz-level at 3 G). This is the reason to read on the clock pair rather than the field-sensitive cooling pair.
- **[V]** 1064 differential scalar F=1↔F=2 ≈ 1.9 kHz (stark audit S4) — common to red and blue sidebands → cancels in the ratio.
- **[V, lit]** Clock-state Raman sideband thermometry is standard and demonstrated for trapped Rb in fiber/tweezers (Leong HCPCF; Chiu, Rensburg). The method is not in question; its fidelity *in this geometry, under tagging* is.

## Claims tagged for falsification

**[O1] — CLOSED (verified). The inferred-⟨n⟩ bias is the finite-pulse pedestal: +0.010, removable.**
R = A_red/A_blue → ⟨n⟩ assumes the only red/blue asymmetry is thermal. Any non-thermal asymmetry (differential AC-Stark across the scan, unequal red/blue Rabi from the Fano background of nearby resonances, finite-pulse lineshape overlap of carrier into the sidebands) biases ⟨n⟩. At ⟨n⟩≈0.02 the red sideband is ~2 % of the blue; a 1 % systematic on either amplitude moves the inferred ⟨n⟩ by ~0.01 — half the floor. **Falsify with a Raman-pulse-on-Fock simulation** at the operating point (ν_z=430 kHz, η_R≈0.19, B=3 G, the planned pulse): is the extracted ⟨n⟩ unbiased to ≪0.02?

**[O2] — CLOSED (verified). Safe pulse window t_π ≈ 20–60 µs (1/t_π ≪ ν_z).**
Resolved-sideband readout needs the Raman feature linewidth Γ_R ≪ ν_z = 430 kHz (red and blue are ±430 kHz about carrier; carrier and sidebands must not overlap). Γ_R is set by the π-pulse Fourier width (~1/t_π) and the two-photon laser phase noise. The EOM-pair phase is common-mode (clock-referenced) so laser linewidth largely cancels — a genuine strength — **but t_π and the thermometer Rabi Ω_R were never specified.** Leese's WFMC shows the temperature read degrades steeply once the Raman linewidth approaches ~0.5 MHz. Confirm Γ_R ≪ 430 kHz for the intended pulse.

**[O3] — cooling-beam extinction during readout unspecified.**
The readout assumes cooling fields off. Residual control (near F=2→F′=2) leaking through the tag AOM or as EOM carrier during the readout window AC-Stark-shifts and scatters on |1,0⟩,|2,0⟩, biasing the ratio. What AOM off-ratio / EOM carrier suppression keeps this negligible over the readout pulse? No spec set.

**[O4] — CLOSED (verified). No phase bias: sideband ∝ sin θ cancels in the ratio.**
The thermometer uses the same mirror and the same 6.835 GHz split, so it sits at the cooling-optimal standing-wave phase (θ≈0, dθ≈π). Whether that phase gives good Raman sideband contrast — or whether the thermometer wants a *different* mirror position, which would conflict with cooling — is uncomputed. If they conflict, "one mirror, double-duty" fails and a separate Raman path returns.

**[I5] — the park→read transfer is motion-preserving.**
|1,+1⟩→|1,0⟩ by a microwave/RF Δm=−1 *carrier* π-pulse: Lamb-Dicke parameter for a 6.8 GHz / RF photon is ~10⁻⁶, so no momentum kick — no heating, the measured ⟨n⟩ is the post-cooling value. Selectivity against |1,0⟩→|1,−1⟩ relies on starting with population only in |1,+1⟩ plus the quadratic-Zeeman offset at 3 G. *Confirm the π-pulse fidelity and that it is carrier, not a sideband.*

**[I6] — common-mode shifts cancel in the ratio.**
The 1064 trap scalar, the clock-carrier AC-Stark from balanced Raman beams, and any uniform offset shift both sidebands equally → cancel in R to first order. *Holds only if the red and blue scan points see the same intensity and the same trap excursion;* an intensity imbalance or a scan-dependent shift breaks it (folds into [O1]).

**[I7] — the thermometer measures the axial mode that was cooled, with stronger coupling.**
Counter-propagating Raman along the fiber axis (= the cooling axis) → measures axial ⟨n_z⟩; effective η_R ≈ 2η ≈ 0.19 (two-photon 2k recoil) vs the cooling η=0.094, so sideband coupling is ~2× stronger — favorable for contrast. *Geometry argument; the 0.19 was not separately recomputed for the Raman pair.*

## Checkable questions (ordered by decision weight)
- **Q1 [O1].** Simulate the clock-Raman sideband spectrum on a Fock ladder at the operating point with the intended pulse; extract ⟨n⟩ from the red/blue ratio and compare to the input. Bias ≪0.02? This is the deferred sandbox computation — run it.
- **Q2 [O2].** Specify t_π and Ω_R; is the Raman feature linewidth Γ_R ≪ 430 kHz? Include the EOM-pair residual phase noise (expected small, common-mode).
- **Q3 [O3].** Set the cooling-beam extinction spec for the readout window (AOM off-ratio, EOM carrier suppression); confirm residual scatter+shift on the clock states is negligible.
- **Q4 [O4].** Is the cooling-optimal (θ, dθ) acceptable for the Raman sideband contrast, or does the thermometer need a conflicting mirror position?
- **Q5 [I5].** π-pulse |1,+1⟩→|1,0⟩: fidelity and selectivity at 3 G; confirm carrier (Δn=0).
- **Q6 [I6/O1].** Verify red/blue Stark symmetry — balanced Raman intensities and equal trap excursion at both scan points.

## Model scope (what backs the numbers, and what doesn't)
There is **no thermometry simulation**. The [V] claims are the bare-mirror reflection rule (computed prior), clock-state field-insensitivity (atomic physics), the 1.9 kHz scalar cancellation (stark audit), and literature precedent — none is a contrast computation. The [I] claims are geometry/Lamb-Dicke and shift-cancellation arguments. Every quantitative readout claim ([O1]–[O4]) requires the Raman-pulse-on-Fock simulation (ν_z, η_R, B, pulse shape, the carrier + both sidebands, the nearby-resonance Fano background) that has not been run. Until Q1 returns, the cooling result ⟨n_z⟩≈0.02 is **verified as produced but not yet verifiable as measured.**
