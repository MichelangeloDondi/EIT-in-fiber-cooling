# One-EOM (1560 nm) architecture and the full experimental sequence
**⁸⁷Rb clock-EIT cooling in a kagome HCPCF — MOT → bright molasses → gray molasses → conveyor-belt transport → in-fibre EIT cooling → thermometry**

Compiled 2026-06-16. Flags: **[V]** computed/modelled in this program · **[I]** inference / standard practice · **[O]** open bench number. Companion: `full_sequence_config.md`, `configuration_tradeoffs_consolidated.md`. Real apparatus = Marchesini et al., Opt. Continuum **3**, 1868 (2024). Closest published analogs cited inline: Chiu 2025 (⁸⁷Rb conveyor-belt + Λ-gray-molasses + EIT-SC), Leong 2020 (in-fibre conveyor into an HCPCF), Rensburg 2025 / Wang 2022 (Λ-GMC).

Frequencies below are **offsets from F=2→F′2 ≡ 0** (5P₃/₂): F2→F′3 = **+266.6**, F2→F′1 = **−156.9**, F1→F′2 = **+6834.7**, F1→F′1 = **+6677.7** MHz. Γ_D2/2π = 6.07 MHz. ν_z = 2π·430 kHz, ν_r = 2π·5.42 kHz, U₀ ≈ 1.1 mK in the fibre.

---

## Part A — why one 1560 nm EOM covers everything

**The principle.** Every *coherent* pair in the experiment (gray-molasses Λ pair, EIT control+probe, thermometry Raman) needs two optical tones split by the 6.835 GHz ground hyperfine interval with a **stable relative phase** — that relative phase is the two-photon coherence, and it is the binding axis of the whole experiment (the EIT floor doubles at a two-photon linewidth of only 0.26 kHz [V]). If the two tones come from one laser plus one phase modulator, the laser's own phase noise appears identically on both tones and **cancels**; the residual two-photon linewidth is then just the RF synthesizer's (sub-100 Hz, passive). This is the one property that decides the design.

**Why 1560 and not 780.** The modulator sits on the telecom seed, *before* the EDFA and the doubler:
- Telecom phase-EOMs are cheap, low-Vπ, fibre-coupled, broadband, and run at low optical power.
- **Phase modulation survives second-harmonic generation.** If E₁₅₆₀ ∝ exp[i(ωt + β sinΩt)], then E₇₈₀ ∝ E₁₅₆₀² ∝ exp[i(2ωt + 2β sinΩt)]: the doubled field is phase-modulated at the **same** RF frequency Ω, with the modulation index **doubled** (β→2β). So the *sideband spacing at 780 equals the RF you apply at 1560* — to make a 6.835 GHz partner you drive the EOM at 6.835 GHz (a microwave EOM, but a telecom one). [V·analytic]
- With a single seed there is no SFG clutter; pure phase modulation doubles cleanly even at ~29% conversion (no spurious AM line). [I]

**Two seeds vs one seed + EOM — the coherence boundary.** The Marchesini source has two 1560 seeds ~3.4 GHz apart; doubled, they give two 780 colors 6.835 GHz apart (cooler + repump) plus an SFG line in between (MOT-only clutter).
- **MOT and bright molasses are incoherent** → use both seeds (or one seed + EOM; either works). Relative seed phase is irrelevant.
- **All coherent phases use ONE seed + the EOM, with the second seed switched OFF (MEMS)** — because two independent seeds can never be a Λ pair (no common-mode). The EOM-generated partner is the only phase-coherent option. [V·analytic]

**What does the tuning, and how fast.** The seed laser stays **locked and parked** in every phase. Phase-to-phase changes are entirely on RF hardware:
- **The 1560 EOM RF** (a DDS/AWG synthesizer) sets which hyperfine partner you make and the two-photon detuning. Retuned 6.568 / 6.835 / 7.13 GHz across the sequence; frequency hops are phase-continuous in DDS clock cycles (**ns**).
- **AOMs** set the single-photon detuning and gate/shape pulses (**ns–µs**), and provide the retro "tag."
- **The Rb-85 "master"** (low power, sat-abs-locked) does only the **coherence-free** jobs: absolute reference (the Eblana offset-locks to it), optical pumping (F2→F′2), and state-selective detection (F2→F′3 cycling). **It is never a Λ leg** (that would forfeit common-mode and cap the floor ≫0.044). [V/I]

**No OPLL.** Common-mode is achieved by the EOM, so the sub-100 Hz two-photon linewidth is met passively. If the dual-end 0.0047 floor is ever wanted, the route is a *second doubling chain* off the same seed (still common-mode, no phase lock), not an OPLL. [I]

---

## Part B — the sequence, phase by phase

Powers: free-space beams are **mW-class** (standard, lab-set); in-fibre guided beams are **µW-class** because the guided mode area is ~1.1×10⁻⁵ cm² (tens of nW at the input → ~0.1–1 µW including Clebsch-Gordan factors) [V scale / O exact]. The 1064 lattice/conveyor is **~W-class** (U₀ ≈ 1.1 mK in the fibre). Rabi frequencies and detunings in the EIT/thermometry tables are in **2π·MHz**.

### Phase 0 — standing configuration (set once)
Eblana seed offset-locked to the 780 master; master sat-abs-locked to Rb-85; EOM/AOM RF synthesizers programmed per phase; B-coils ready (MOT gradient ↔ bias). Nothing here is retuned shot-to-shot.

### Phase 1 — MOT (free space) [I, standard; Chiu 2025]
| knob | value |
|---|---|
| cooler | F2→F′3, **−2 to −3Γ** (≈ −12 to −18 MHz); carrier from the seed |
| repump | F1→F′2, the **1560 EOM sideband at 6.568 GHz** (= 6834.7 − 266.6); β₁₅₆₀ ≈ 0.3 → ~8% repump |
| B-gradient | ~10–15 G/cm |
| power | ~mW/beam, six (or retro) beams, large waist (~mm) |
| outcome | ~10⁷ atoms in ~80 ms |
| firing | 1560 EOM @ 6.568 GHz; MOT AOM (amplitude) |

### Phase 2a — bright molasses (free space) [I; Chiu 2025]
Ramp the cooler red (**−5 to −10Γ**, or a compression ramp toward −140 MHz) and lower the intensity; repump on; B-gradient → 0. **Outcome: 8–10 µK** (your measured value). EOM stays at 6.568 GHz.

### Phase 2b — Λ-gray molasses (free space, the deep sub-Doppler stage) [V refs: Chiu, Rensburg, Wang, Marchesini]
| knob | value |
|---|---|
| coupling (carrier) | F2→F′2, **+2 to +5Γ blue** (Chiu: +30 MHz blue of F′2; Rensburg: +6Γ) |
| Raman repump (sideband) | F1→F′2, the **1560 EOM sideband at 6.835 GHz**, at two-photon detuning **δ ≈ −0.1Γ to 0** |
| coherence | coupling + Raman are common-mode (one seed + EOM) → δ is synthesizer-set and phase-coherent — this is *why* Λ-GMC works cleanly |
| polarization | **co-polarized** (both σ⁻); the cooling gradient comes from the counter-propagating geometry — no demux needed |
| power ratio | (Ω_Raman/Ω_couple)² ≈ 0.1 (Rensburg); low total intensity |
| outcome | **2.5–4 µK** (Λ-GMC literature); ~10 ms |
| firing | 1560 EOM @ 6.835 GHz (seed offset-lock hops F′3→F′2 vs the MOT) |

This is the stage that sets the radial temperature you carry into the fibre. **Doing it as gray rather than bright molasses is the single biggest lever on the final radial state** (see Phase 3). Gray molasses cannot run *inside* the 48 µm core — it is a free-space pre-cool.

### Phase 3 — optical conveyor-belt transport into the fibre [I; Leong 2020 (in-fibre), Chiu 2025 (⁸⁷Rb)]
The 1064 lattice **is** the conveyor: two counter-propagating 1064 beams, one frequency-ramped by an AOM, form a moving standing wave that drags the atoms into the core at **v = λΔν/2**. After a few mm inside, ramp Δν→0 to a stationary lattice; a **push beam** (F2→F′3 cycling, from the master) blows away any atoms left above the tip (Leong: 2 cm/s, ~200 ms; ⁸⁷Rb scale).

| quantity | value |
|---|---|
| distance | ~7 mm (MOT/molasses region → inside the core) |
| 1064 power | ~W-class; U₀ ≈ 1.1 mK in-fibre |
| waist | **126 µm → 19 µm** as the beams focus toward the tip |
| adiabatic heating | T_z ∝ 1/w → **×6.6**; T_r ∝ 1/w² → **×44** [V] |
| radial T in | from 2.5–4 µK (gray) → **~110–176 µK** ; from 8–10 µK (bright) → 350–500 µK |
| near-resonant light | **none** during transport (dark, just the 1064) except the final push |

**Adiabaticity caveat [V].** At the 126 µm waist ν_r ≈ 123 Hz (oscillation period **8.1 ms**), so the transport ramp must be **≫ 8 ms** to keep the radial compression adiabatic; faster ramps heat the radial *above* the ×44 estimate. η_r = U₀/k_BT_r is **invariant** under the compression, so the compression scales T_r up but does not by itself worsen the trapping margin — the radial precondition is inherited from the molasses temperature. Keep the radial **≲ 100 µK** so the axial sideband stays sharp for cooling and thermometry; if gray-molasses-before-transport isn't enough, a free-space re-cool at the small-waist focal trap (just outside the tip, within the ~1 mm Rayleigh range) reaches 2.5 µK / n_r ≈ 9 with no atom loss — preferred over a trap-lower/raise (which is lossy evaporation, not reversible cooling). [V/I]

### Phase 4 — in-fibre EIT cooling [V]
| knob | value |
|---|---|
| delivery | **single_end_tagged**: forward = control carrier + probe sideband (σ⁻); **retro mirror + λ/4** flips the return to σ⁺; a **~300 MHz double-pass tag AOM** lands the return sideband on the probe line and rejects the return-carrier parasitic |
| dark pair | control **F2→F′2 +Δ (σ⁻)**; probe **F1→F′2 +Δ (σ⁺, retro, tagged)** → |1,−1⟩/|2,+1⟩ via |F′2,0⟩, field-insensitive at any B |
| Δ (single-photon) | **55 MHz** (single-end-tagged optimum; broad — 55–80 MHz works) |
| Ω_c (control) | **≈ 9.7** (slaved by the EIT condition Ω_c²/4Δ = ν_z; = 11.39 at Δ=80) |
| OmR = Ω_p/Ω_c | **0.10** (probe weak; power ratio ~1%) — Pareto knee for rate vs floor |
| δ₂ (two-photon) | **servoed to the dark resonance** (≈ −0.25 single-end; ≈ 0 dual-end) |
| B | 1.0–1.5 G |
| repumpers | repump1 **F1→F′1** (157 MHz AOM step, σ⁻); repump2 **F2→F′1 from the master** (incoherent, clean offload) |
| 1560 EOM | **≈ 7.13 GHz** (= 6.835 + ~0.30 tag) |
| in-fibre power | ~0.1–1 µW (control); probe ~1% of that |
| performance [V] | floor **⟨n_z⟩ = 0.0073**, P₀ ≈ 99.3%, τ₁ₑ ≈ 0.35 ms, t→0.1 ≈ 1.06 ms; cool ~1–2 ms |
| firing | 1560 EOM @ 7.13 GHz; control AOM (Δ); 300 MHz tag AOM; 157 MHz repump-1 AOM; master (repump-2) |

### Phase 5 — in-fibre thermometry [V]
| knob | value |
|---|---|
| pair / path | **same clock pair, same single_end_tagged path, same polarizations** as EIT |
| method | **Blackman-shaped sideband-π pulses**, ratio **R = A_red/A_blue**, **calibrated against known ⟨n⟩** (heat-and-measure) — never naive R/(1−R), never off-sideband subtraction |
| probe strength | **s ≈ 0.3–0.5** → **t_π ≈ 13–21 µs**; Blackman suppresses the carrier wing to ~6×10⁻⁹ |
| single-photon Δ | **same as EIT** — with Blackman, R reads ⟨n⟩ faithfully and *independently of Δ* (uniform scatter cancels in R). A dedicated far-detuned / D1-795 laser is only a ~2× shot-count (SNR) upgrade, **not required** |
| two-photon | EOM RF at **6.835 + tag ± ν_z** (the red/blue motional sidebands, ±0.43 MHz) |
| repumpers | **OFF** during the π-pulse (they would dephase the coherent transfer) |
| readout | state-selective **F2→F′3 cycling via the master**; ~2000 shots → ±33% on 1−P₀, P₀ to ±5% |
| honesty [V] | confirms n̄ at the ~10⁻² level; pinning 0.0073 to 3 figures is beyond the asymmetry (D1 narrows it) |
| firing | 1560 EOM (probe, pulsed, ±ν_z); tag AOM (shared); master (detection) |

---

## Part C — the EIT → thermometry transition (the switch you asked about)

The worry is that thermometry "needs different powers and detunings," and that switching them fast seems hard. The resolution is that **almost nothing optical changes, and what changes is all RF.** Concretely:

**What stays fixed across the switch:**
- Both lasers stay **locked and parked** — no optical retuning, no lock reacquisition.
- The single_end_tagged **beam path, polarizations (σ⁻/σ⁺), and the 300 MHz tag** are reused unchanged.
- The **single-photon detuning Δ** is unchanged — the Blackman-shaped, calibrated-R method is *Δ-independent*, so thermometry runs at the EIT Δ. (This is the key fact: thermometry does **not** require a large detuning change. The "different detuning" intuition is wrong for the single-laser Blackman method; a separate far-detuned laser is optional, not required.)
- The atom is **already in the right initial state**: EIT cooling parks it in the dark state |1,−1⟩ near n=0, which is exactly the state the sideband-π drives from. No extra state-prep step.

**What actually changes — three RF moves, all µs or faster:**
1. **EOM RF frequency hop:** from 6.835 + tag (+ δ₂ ≈ −0.25 MHz, the dark resonance) to **6.835 + tag ± ν_z** (± 0.43 MHz, the motional sidebands). That's a ~0.43 MHz step on a 7.13 GHz carrier — a **phase-continuous DDS hop in clock cycles (ns)**.
2. **Probe AOM amplitude + envelope:** from the weak CW EIT probe (OmR = 0.10) to the thermometry π-pulse level (s ≈ 0.3–0.5), with a **Blackman amplitude envelope over 13–21 µs**, gated on/off. The AOM responds in the acoustic transit time (**ns–100s of ns**); the envelope is just the AWG waveform.
3. **Repumpers OFF, master ON for readout:** gate the repumpers off during the coherent π-pulse, then gate the master (F2→F′3) on for state-selective detection afterward — both simple AOM/shutter gates.

**Why it is fast — the design reason.** Every optical frequency in the experiment is *parked-laser ± RF*. The single-photon detuning lives on an AOM; the two-photon detuning and the hyperfine partner live on the EOM RF. RF synthesizers (DDS/AWG) change frequency, amplitude, and phase in nanoseconds, and the modulators follow within their (ns–µs) response. **You never move a laser or re-lock anything between cooling and thermometry** — you reprogram RF. That is what makes the switch instantaneous on the scale of the sequence.

**Timescale budget of one cooling→thermometry cycle:**

| step | time | what moves |
|---|---|---|
| end EIT cooling | gate-off, ~µs | control/probe AOM off |
| EOM RF hop to a sideband | **sub-µs** | DDS frequency word |
| set probe to π-level + Blackman | **ns–µs** | probe AOM amplitude/envelope |
| sideband-π pulse | **13–21 µs** | the measurement itself |
| state-selective readout | **~ms** | master F2→F′3 cycling |

The cycle is **detection-limited (~ms), not switch-limited.** Repeat on red then blue, accumulate R = A_red/A_blue over ~2000 shots, convert to ⟨n_z⟩ via the calibration.

**One genuine subtlety [O].** The π-pulse area depends on the in-fibre Rabi frequency, which depends on the guided power; calibrate t_π against a known ⟨n⟩ (the heat-and-measure curve) rather than from first principles. If you later add the optional D1-795 thermometry laser for sharper readout, the "switch" becomes even simpler — it is an independent source you gate on, with its own 6.835 GHz EOM, so it doesn't touch the D2 EIT settings at all.

---

## Consolidated modulator / frequency / power map

| device | MOT | bright molasses | gray molasses | conveyor transport | in-fibre EIT | thermometry |
|---|---|---|---|---|---|---|
| **1560 EOM (RF)** | 6.568 GHz | 6.568 GHz | 6.835 GHz | off | **7.13 GHz** (δ₂) | **7.13 GHz ± ν_z** (pulsed) |
| seed / offset-lock | cooler F′3 −2Γ | cooler red ramp | coupling F′2 +2–5Γ | (parked) | control F′2 +Δ | = EIT |
| control / coupling AOM | — | — | small (blue) | — | Δ = 55 | — (Δ unchanged) |
| 300 MHz tag AOM | — | — | — | — | retro tag | shared |
| 157 MHz AOM | — | — | — | — | repump-1 (F′1) | off (during π) |
| MOT AOM (~100 MHz) | amplitude | amplitude ramp | — | — | — | — |
| 1064 conveyor AOM | (lattice on) | — | — | **Δν ramp (v=λΔν/2)** | static lattice | static lattice |
| **780 master** | (reference) | (reference) | (reference) | **push (F′3)** | repump-2 (F2→F′1) | **detection (F′3)** |
| polarization | σ± (MOT) | σ± | co-pol σ⁻ + gradient | — | σ⁻/σ⁺ via λ/4 retro | = EIT |
| power scale | mW free-space | mW | mW (low) | W (1064) | µW guided | µW guided (pulsed) |

---

## Open / checkable items [O]
1. **Two-photon linewidth as built** — measure the 6.835 GHz two-photon (not laser) linewidth from the EOM/DDS chain; sub-100 Hz confirms the whole EIT + thermometry coherence story. *The one gating spec.*
2. **Tagged-retro differential path** — the round trip is the only non-common-mode residual; confirm fibre-retro length jitter keeps differential phase noise ≪ 300 Hz.
3. **Conveyor ramp adiabaticity** — verify the transport time ≫ 8 ms (the 126 µm-waist radial period) so the radial isn't heated above ×44; and that the radial lands ≲ 100 µK after gray-molasses + transport.
4. **t_π calibration** — the in-fibre Raman Rabi (hence t_π) is power-dependent; calibrate against a known ⟨n⟩.
5. **Spurious-comb audit** — with 6.835 GHz and 157 MHz cascaded and doubled, confirm no product tone lands on a transition strongly enough to pump/heat during EIT (largest unintended intermod was 2.4×10⁻⁷ in the prior audit).
6. **In-fibre repumper helicity** — repump-1 (σ-handed F′1) faces the same cross-circular question as the probe in the tagged-retro geometry.
7. **MOT repump co-shift** — a single-seed cooler ramp co-shifts the EOM repump; co-ramp the synthesizer or keep two seeds for the MOT only.

---

## Bottom line
One Eblana seed + one 1560 nm phase-EOM + AOMs + the Rb-85 master, **no OPLL**, runs the entire sequence. The EOM makes the 6.835 GHz partner for every coherent phase with common-mode coherence (two-photon linewidth = the RF synthesizer). The whole sequence is driven by **parked lasers and agile RF**: phase-to-phase changes — including EIT→thermometry — are EOM-RF hops and AOM gates (ns–µs), never laser retuning. EIT→thermometry in particular keeps Δ, the beam path, and the polarizations fixed; it only hops the EOM RF by ±ν_z, shapes the probe AOM into a Blackman π-pulse, and gates the master for readout — a switch that is detection-limited (~ms), not switch-limited.
