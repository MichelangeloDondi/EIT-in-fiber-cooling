# Full-Sequence Best Configuration — MOT → Molasses → In-fiber EIT → Thermometry

Actionable per-phase configuration for the in-fiber clock-EIT experiment, on the real apparatus
(Marchesini 2024). Flags: **[V]** computed, **[I]** inference, **[O]** open. Companion analysis:
`architecture_consolidated_findings.md`; numbers from `eit_cooling_tool.py` (v0.2.4),
`thermometry.py` (v0.2.0).

**One-line architecture.** One Eblana 1560 nm seed → one 1560 nm phase-EOM → EDFA → PPLN → 780 nm
runs **every coherent phase** (MOT/molasses cooler+repump, gray-molasses Λ pair, in-fiber EIT
control+probe, thermometry pulses) — all **common-mode**, so the two-photon coherence is set by the
RF synthesizer, not the 0.6 MHz laser. The **Rb-85 master** (low power) does the **coherence-free**
jobs (absolute reference, optical pumping, detection). **No OPLL required.**

---

## Shared hardware (configured once)

| element | spec / role |
|---|---|
| Eblana seed (1560) | single master source for all coherent light; offset-locked to the 780 master |
| **1560 phase-EOM** (pre-EDFA) | makes the 6.835 GHz ground-HFS partner; retuned per phase (6.568 / 6.835 / 7.13 GHz). Doubling preserves spacing & RF phase, index→2β. Telecom, low-Vπ, fiber. |
| EDFA + PPLN | ≤0.27 W at 780; pure phase-mod doubles cleanly even at 29% conversion (no AM, no SFG clutter with one seed) |
| 780 master (Rb-85 sat-abs) | absolute reference (Eblana offset-locks to it) + optical pumping (F=2→F′2) + detection (F=2→F′3). Lock-point tunable ±~1.5 GHz; **never an EIT/Λ leg** (would break common-mode coherence). |
| AOMs | MOT amplitude (100 MHz, existing); control-detuning; F′2↔F′3 (267 MHz) seed/lock hop; **300 MHz retro tag** (EIT); 157 MHz EIT-repumper step |
| in-fiber EIT optics | one delivery end + retro mirror + λ/4 (helicity flip) — the no-demux delivery |
| **OPLL** | **not used.** Two-photon coherence is common-mode (EOM synthesizer). If the 0.0047 floor is wanted, add a 2nd doubling chain (no OPLL), not a phase lock. |

Frequencies below are offsets from **F=2→F′2 = 0**: F2→F′3 = +266.6, F2→F′1 = −156.9,
F1→F′2 = +6834.7, F1→F′1 = +6677.7 MHz.

---

## Phase 1 — MOT  *(free-space)* **[I, standard]**

- **Source:** Eblana, 90% port → 3 retro beams (existing 100 MHz AOM for amplitude).
- **Tones:** cooler **F=2→F′3, −2Γ** (carrier); repump **F=1→F′2** (1560 EOM sideband, **6.568 GHz**
  from the cooler carrier; β₁₅₆₀≈0.30 → ~8% repump, 83% carrier). [Two-seed mode remains a fallback
  if independent cooler/repump agility is wanted; single-seed+EOM gives the cleaner spectrum.]
- **Polarization:** standard MOT σ± with the quadrupole gradient.
- **Performance:** standard 87Rb MOT.
- **Modulators firing:** 1560 EOM @ 6.568 GHz; MOT AOM.

## Phase 2 — Molasses  *(free-space)* **[V refs / I]**

**2a Bright molasses (brief):** ramp cooler red (−5…−10Γ), repump on. → tens of µK.

**2b Λ-enhanced gray molasses (the deep sub-Doppler stage):**
- **Source:** Eblana. Coupling **F=2→F′2 (or F′3), +2Γ blue** (carrier); Raman **F=1→F′2** (1560 EOM
  sideband, **6.835 GHz**), at Raman detuning **δ ≈ −0.1 Γ**.
- **Coherence:** coupling (carrier) + Raman (sideband) are **common-mode** — δ is synthesizer-set and
  phase-coherent (this is why GM works cleanly here). **[V·an]**
- **Polarization:** **co-polarized** (Leese: both σ⁻); the gradient comes from the counter-propagating
  geometry, so the co-pol EOM sideband is correct — **no demux**. EOM-sideband repump is standard
  practice (Rensburg, (Ω₁/Ω₂)²=0.1).
- **Performance:** T ≈ 3–10 µK (Rosi/Leese Λ-GM). Sets the radial temperature into the fiber.
- **Modulators firing:** 1560 EOM @ 6.835 GHz (seed hops F′3→F′2 vs the MOT, via offset-lock/AOM).

*(Gray molasses cannot run in the 48 µm fiber — it is the free-space pre-cool; atoms then load into the HCPCF.)*

## Phase 3 — In-fiber EIT cooling **[V]**

- **Source/delivery:** Eblana, **`single_end_tagged`** (no demux): forward beam = control carrier +
  probe sideband (σ⁻) into one end; **retro mirror + λ/4** flips the return to σ⁺ (the cross-circular
  partner); a **double-passed ~300 MHz tag AOM** lands the return sideband on the probe line and
  detunes the return-carrier parasitic (the tag is essential).
- **Pair:** control **F=2→F′2 +Δ (σ⁻)**; probe **F=1→F′2 +Δ (σ⁺, retro, tagged)**.
- **Coherence:** both legs from the Eblana (carrier + EOM sideband) ⇒ **common-mode** ⇒ two-photon
  linewidth = synthesizer (sub-100 Hz). The floor doubles at 0.26 kHz two-photon linewidth, so this
  is the binding spec — **met without an OPLL.** **[V/V·an]**
- **Operating point:** **Δ=45, OmR=0.12** (Pareto knee), **δ₂ servoed** to the dark resonance
  (single-end set-point ≈ +0.25). 1560 EOM at **≈7.13 GHz** (probe + 300 MHz tag).
- **Repumpers (option A, leak-locked):** repump1 **F=1→F′1** via a 157 MHz step (AOM preferred for
  amplitude/polarization control); **repump2 F=2→F′1 from the MASTER** (incoherent, F=2 manifold,
  Rb-85-stable — clean offload). Helicities σ⁻/σ⁺ as required.
- **Performance [V]:** floor **⟨n_z⟩ = 0.0073** (P₀≈99.3%), τ₁ₑ ≈ **0.35 ms**, t→0.1 ≈ **1.06 ms**.
  η_dp=0.5 folded in. (Idealized dual-end = 0.0047; recover via two doubling chains, no OPLL, if needed.)
  Rate/floor trade by OmR: deep 0.06→0.0037-class, fast 0.16–0.24→2× faster at higher floor.
- **Keep radial T ≲ 100 µK** (from the GM + load-in) so the axial sideband stays sharp for thermometry.
- **Modulators firing:** 1560 EOM @ 7.13 GHz; control AOM; 300 MHz tag AOM; 157 MHz repumper AOM;
  master (repump2).

## Phase 4 — In-fiber thermometry **[V]**

- **Source/delivery:** **same clock pair, same `single_end_tagged` path as EIT** (so same common-mode
  coherence — no OPLL).
- **Method:** **Blackman-shaped sideband-π pulses**, ratio **R = A_red/A_blue**, **calibrated against
  known ⟨n⟩** (heat-and-measure). Probe strength **s ≈ 0.3–0.5** → t_π ≈ **13–21 µs**; Blackman
  suppresses the carrier wing to ~6×10⁻⁹ (a square pulse would bias by ~the signal).
- **Detuning:** the **same single laser suffices** — with Blackman, R reads ⟨n⟩ faithfully and
  **independently of Δ** (uniform scatter cancels in R). A dedicated 4 GHz thermometry laser is only a
  ~2× shot-count (SNR) upgrade, **not required**.
- **Re-entry pedestal:** branching puts ~10% of scatter into the detected state; the master-equation
  pedestal is a **near-constant offset on R that calibration absorbs**. **Calibrate R vs ⟨n⟩ — never
  naive R/(1−R), never off-sideband subtraction** (the latter over-subtracts). **[V]**
- **Readout:** state-selective detection on **F=2→F′3 via the MASTER** (Rb-85-stable, precise). ~2000
  shots for ±33% on 1−P₀; BSB-flop fit recovers P₀ to ~±5% at any Δ≥0.8 GHz.
- **Modulators firing:** 1560 EOM (probe, pulsed) + tag AOM (shared with EIT) + master (detection).

---

## Consolidated modulator / frequency map

| device | MOT | gray molasses | in-fiber EIT | thermometry |
|---|---|---|---|---|
| **1560 EOM** | 6.568 GHz (repump) | 6.835 GHz (Raman) | 7.13 GHz (probe) | 7.13 GHz (probe, pulsed) |
| seed/offset-lock | cooler F′3 −2Γ | coupling F′2 +2Γ | control F′2 +Δ | = EIT |
| control/coupling AOM | — | small (blue) | Δ=45 | — |
| 300 MHz tag AOM | — | — | retro tag (essential) | shared |
| 157 MHz (AOM) | — | — | repump1 (F′1) | — |
| 100 MHz AOM | MOT amplitude | — | — | — |
| **780 master** | (reference) | (reference) | repump2 (F2→F′1) | **detection** + OP |
| polarization | σ± (MOT) | co-pol σ⁻ + gradient | σ⁻/σ⁺ via λ/4 retro | = EIT |

---

## OPLL decision **[I]**

- **Recommended config needs none.** Every coherent pair is one-laser-+-EOM ⇒ common-mode ⇒ the
  two-photon linewidth is the synthesizer's (sub-100 Hz), meeting the 0.26-kHz-doubling spec.
- **Not a quick add.** A useful OPLL here is a sub-100-Hz phase lock at the ~7 GHz master↔Eblana beat
  — fast PD + microwave mixing + tight loop; non-trivial, and the existing offset lock is almost
  certainly not OPLL-grade.
- **Not the best route to 0.0047 anyway.** If the extra ~0.0026 in floor matters, **two doubling
  chains off the one seed** (split 1560 → control arm + probe arm with the 6.835 GHz EOM → separate
  EDFA+PPLN, polarized independently) give the clean dual-end floor **passively common-mode, no OPLL**.
- **Verdict:** skip the OPLL; baseline = tagged-retro (0.0073). Escalate to two doubling chains only
  if a clock/gate spec demands 0.0047.

---

## Open / checkable questions **[O]**

1. **Two-photon linewidth, as built** — measure the 6.835 GHz two-photon (not laser) linewidth from
   the EOM/DDS chain; sub-100 Hz confirms the whole EIT/thermometry coherence story. *The one gating spec.*
2. **Tagged-retro differential path** — the round-trip is the only non-common-mode residual; confirm
   fiber-retro length jitter keeps differential phase noise ≪ 300 Hz.
3. **δ₂ tolerance at the single-end set-point (≈ −0.25, steeper red flank)** — does it need a tighter
   servo than the dual-end ±20 kHz?
4. **Realistic η_dp** for the HCPCF retro (end-face vs external mirror, λ/4 + double-pass AOM); where
   does the floor sit at η_dp=0.3, and is a larger tag worth a lower floor?
5. **In-fiber repumper delivery** — repump1 (σ-handed, F′1) faces the same cross-circular question as
   the probe; confirm the tagged-retro geometry (or master for repump2) delivers correct helicities.
6. **Spurious-comb audit** — with 6.835 GHz and 157 MHz modulation cascaded (and doubled), check no
   product tone (e.g. 2×157=314 MHz) lands on a transition strongly enough to pump/heat during EIT.
7. **MOT repump co-shift** — single-seed cooler ramp co-shifts the EOM repump; co-ramp the synthesizer
   or accept the few-MHz shift (vs keeping two seeds for the MOT only).
8. **Carried:** v0.3.0 θ-aware Stark referencing → re-baseline the EIT operating point / repump detunings.

---

## Performance summary

| phase | observable | best config | result |
|---|---|---|---|
| MOT | trapped sample | Eblana cooler + 6.568 GHz EOM repump | standard 87Rb MOT |
| gray molasses | sub-Doppler T | Eblana Λ pair (common-mode, co-pol), δ≈−0.1Γ | ~3–10 µK |
| in-fiber EIT | axial ⟨n_z⟩ | single_end_tagged, Δ=45, OmR=0.12 | **0.0072** (P₀≈99.3%), τ₁ₑ≈0.35 ms |
| thermometry | ⟨n_z⟩ readout | Blackman sideband-π, calibrated R, master detection | faithful; P₀ to ±5% (~2000 shots) |

**Bottom line:** one Eblana + one 1560 EOM + AOMs + the Rb-85 master, **no OPLL**, covers the entire
sequence. In-fiber EIT/thermometry run common-mode on the tagged-retro at n̄≈0.0073; the master
supplies reference, optical pumping, and detection. The only escalation worth considering is a second
doubling chain (still no OPLL) if the 0.0047 floor is required.
