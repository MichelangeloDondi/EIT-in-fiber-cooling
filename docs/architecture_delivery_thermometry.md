# Laser System, Delivery & Thermometry — Consolidated Findings

Single reference for the laser/frequency architecture, in-fiber EIT delivery, sideband
thermometry, and operating-point landscape of the in-fiber clock-EIT cooling experiment.
Flags: **[V]** verified by computation, **[I]** inference from standard physics, **[O]** open.
Tools: `eit_cooling_tool.py` (v0.2.4), `thermometry.py` (v0.2.0). Apparatus: Marchesini et al.,
*Opt. Continuum* **3**, 1868 (2024).

---

## 1. Apparatus baseline (Marchesini 2024)

- Two Eblana EP-1550 1560 nm seeds (~3.4 GHz apart = 6.835 GHz at 780), 150 kHz linewidth →
  MEMS switch + 2×2 combiner → **single EDFA → single PPLN (fiber-coupled) → 780 nm**.
- 780 nm: ~0.6 MHz linewidth, power stable ~1%, **0.1–6.5 GHz** tunable, beat-locked to a third
  780 reference laser. SHG ~29% (≈0.27 W at 780 from 0.5 W at 1560).
- Known nuisance: with two seeds the PPLN also does **SFG** (a third tone at ω₁+ω₂) — power loss
  and clutter in the beat-lock spectrum.
- The 48 µm kagome HCPCF holds the 1064 nm axial lattice and guides the 780 nm cooling light.

## 2. Settled cooling scheme + operating point (anchor)

Clock-EIT, D2, dark pair **|1,−1⟩ (probe σ⁺) / |2,+1⟩ (control σ⁻) → |F′2,0⟩**; both
g_F·m_F=+½ ⇒ field-insensitive at any B. Axial ν_z=2π×430 kHz (cooled), η_z=0.094,
η_eff(2k)=0.187. **Operating point:** Δ=45, OmR=Ω_p/Ω_c=0.12, Ω_tot=√(4Δν_z)≈8.80,
δ₂ servoed ≈ +0.13, repump option A (Ω_rep=3, Drep1=15, Drep2=5), B=1 G. **Ideal dual-end floor
⟨n_z⟩=0.0048** (P₀=0.9952). **[V]**

---

## 3. Laser & frequency architecture

### 3.1 One Eblana suffices for the whole sequence **[V]**

All D2 tones lie within ≤7.1 GHz; the only large gap is the 6.835 GHz ground HFS. A **single seed
+ a retunable microwave EOM at 1560 nm (before the EDFA) + AOMs** generates every tone. The
second seed only ever supplied the F=1 partner, which the EOM replaces — and a single seed +
phase-EOM doubles to a **clean comb, removing the two-seed SFG clutter** and collapsing two
beat-locks to one. **[I]**

**SHG modulation transfer [V]:** phase modulation at f_m on the 1560 seed doubles to a 780 comb at
the **same spacing f_m** (not 2f_m) with the **index doubled** (β→2β); FFT of E² matches J_k(2β).
Because pure phase modulation keeps |E|² constant, the transfer is **undistorted even in the 29%-
depleted SHG**. Modest depth suffices: β₁₅₆₀≈0.30 for a 10%-power repump (keeps 83% carrier),
≈0.12 for EIT OmR=0.12 (keeps ~98% carrier).

**Frequency plan (seed locked at F=2→F′2 = 0):**

| phase | tone | offset (MHz) | source |
|---|---|---|---|
| MOT/bright | cooler F2→F′3 −2Γ | +254.5 | AOM |
|  | repump F1→F′2 | +6834.7 | EOM 6.835 (6.568 if carrier on F′3) |
| gray molasses | coupling F2→F′2 +2Γ | +12 | AOM |
|  | Raman F1→F′2 +2Γ | +6847 | EOM 6.835 |
| EIT | control F2→F′2 +Δ | +55 | AOM |
|  | probe F1→F′2 +Δ | +6890 | EOM (retro-tagged, §3.3) |
|  | repump2 F2→F′1 | −156.9 | EOM 0.157 |
|  | repump1 F1→F′1 | +6677.7 | EOM 6.835−0.157 |
| imaging/OP | F2→F′3 / F2→F′2 | +267 / 0 | AOM / carrier |

Distinct modulation tones across all phases: **~6.835 GHz** (F=1 partner), **~157 MHz** (excited-HFS /
EIT repumpers), AOMs **<300 MHz** (F′2↔F′3 step + detuning sweeps). The four EIT tones fall out of
two EOM tones on one seed: {0, +6835, −157, +6678} = {0, f₁, −f₂, f₁−f₂}. **Cost:** the EOM fixes
the cooler↔repump offset, so the repump tracks the cooler unless the EOM is co-ramped — for
Λ-cooling (common Δ + relative δ) this is the *correct* control structure; for the MOT ramp it is a
minor co-ramp or a tolerable repump co-shift. **[I]**

### 3.2 Sequence split: free-space vs in-fiber **[I]**

Gray molasses cannot run in the 48 µm fiber, so the sequence is **free-space MOT → bright → gray
molasses → load HCPCF → in-fiber EIT cooling (+ thermometry)**. All free-space phases set
polarization with ordinary per-beam waveplates; gray-molasses coupling+Raman are **co-polarized**
(Leese 2025, both σ⁻; Raman δ≈−0.1Γ optimal), so the co-polarized EOM sideband fits directly. The
EOM-sideband repump is standard practice (Rensburg 2025: repumper = EOM sideband, (Ω₁/Ω₂)²=0.1).
**No frequency demux is needed anywhere in free space.**

### 3.3 In-fiber EIT delivery **without a 6.835 GHz demux** → tagged retro **[V]**

A passive 6.835 GHz etalon/filter is unavailable, so the cross-circular control/probe pair cannot
be frequency-split after the single fiber output. Use the **single-end tagged-retro** delivery
(`single_end_tagged`): forward carrier = control (σ⁻); a **λ/4 in the retro flips the return to σ⁺**
(the cross-circular partner); a **double-passed ~300 MHz tagging AOM** lands the return sideband on
the probe line and detunes the parasitics. Hardware = mirror + λ/4 + 300 MHz AOM — **no GHz filter**.
The two wrong-leg copies (forward sideband, return carrier) are in the model as parasitics. **The tag
is essential**: without it the return carrier (σ⁺, control frequency) drives |2,+1⟩→|F′2,+2⟩ at near-
control strength and breaks the dark state.

| delivery | floor ⟨n_z⟩ | servoed δ₂ | τ₁ₑ | t→0.1 | hardware |
|---|---|---|---|---|---|
| dual-end (ideal; needs demux or 2 chains) | 0.0047 | −0.13 | 0.32 ms | 0.96 ms | demux **or** 2nd EDFA+PPLN |
| **single_end_tagged (no demux)** | **0.0073** | −0.25 | 0.35 ms | 1.06 ms | mirror + λ/4 + 300 MHz AOM |

No-demux cost: **~1.5× in floor (0.0047→0.0073) at the same rate**; still deep (P₀≈99.3%). The EIT
EOM sits at f_mod = A_HFS + 2f_A + δ₂ ≈ **7.13 GHz** (with a +300 MHz tag); retro round-trip
η_dp=0.5 is folded in. **Alternative recovering 0.0047 on one Eblana:** two doubling chains (split
the 1560 seed → control arm + probe arm with a 6.835 GHz EOM → separate EDFA+PPLN, polarized
independently) — more hardware (2nd EDFA+PPLN), no retro loss. **[I]**

---

## 4. Sideband thermometry (m′=0) **[V]**

Reads the **same** clock pair |1,−1⟩/|2,+1⟩ (no park/transfer). **Blackman-shaped sideband-π
pulses**, ratio R = A_red/A_blue; probe strength s = Ω₀/ν_z sets t_π (s=0.12→52.7 µs … s=0.5→12.7 µs;
larger s shortens the pulse since Blackman decouples the carrier-leak constraint).

- **Carrier leak:** a square pulse leaks 0.39% of the carrier into the sideband (≈ the 0.43% signal,
  ~2× bias); **Blackman suppresses it to 6×10⁻⁹**. With Blackman, R reads ⟨n⟩ faithfully and
  **independently of Δ** (uniform scatter cancels in R).
- **Scatter** (sideband-π) is ~13%/pulse at 0.8 GHz, ~2.5% at 4 GHz — cancels in R.
- **Branching-resolved re-entry:** a scatter event lands in the detected state |2,+1⟩ with
  P(g→e)≈0.10, P(e→e)≈0.21 (recoil 0.012 phonons/scatter). The master-equation pedestal is a
  **near-constant offset on R** (~+0.009 at the floor) that **preserves dR/d⟨n⟩** ⇒ **calibration
  absorbs it**. Naive R/(1−R) is biased ~3× at 0.8 GHz, and off-sideband subtraction
  *over*-subtracts ⇒ **calibrate R vs known ⟨n⟩; never naive R/(1−R), never off-sideband
  subtraction.**
- **BSB Rabi-flop fit** recovers P₀ to ~±5% at any Δ≥0.8 GHz with ~2000 shots (shot-noise, not
  Δ-limited).
- **Conclusion:** the single laser is sufficient for calibrated ratio thermometry; a dedicated 4 GHz
  thermometry laser is a **~2× shot-count (SNR) upgrade**, not a requirement. Keep **radial T ≲ 100 µK**
  so the axial sideband stays sharp (≤19 kHz spread vs 20–80 kHz pulse bandwidth).

---

## 5. Operating-point landscape **[V]**

### 5.1 Rate ↔ floor (the lever is OmR; Δ is a sweet spot)

| OmR | floor ⟨n_z⟩ | τ₁ₑ | t→0.1 | note |
|---|---|---|---|---|
| 0.04 | 0.0035 | 1.97 ms | 5.92 ms | deepest probed, slow |
| 0.06 | 0.0037 | 0.87 ms | 2.62 ms | deep/slow |
| **0.10** | **0.0047** | **0.32 ms** | **0.96 ms** | **knee (current)** |
| 0.16 | 0.0077 | 0.18 ms | 0.54 ms | 1.8× faster |
| 0.24 | 0.0131 | 0.145 ms | 0.45 ms | 2.1× faster |

Δ flat (~0.005–0.0065, scan at OmR=0.10) over 35–90; **Δ=130 collapses** (floor 0.116, τ₁ₑ 6.1 ms). OmR=0.12 sits at the
Pareto knee; deep (0.06) and fast (0.16–0.24) configs are selectable by whether the run is floor- or
cycle-limited.

### 5.2 Robustness — the only tight lock is δ₂

| parameter | window (floor ≲ 0.0067) | character |
|---|---|---|
| **δ₂** | **±20 kHz** (±50→0.015–0.019; red flank steeper) | tight; synthesizer-set, servo tracks AC-Stark drift |
| OmR | ~±20% | moderate |
| Ω_tot (power) | ±10% → ≤0.0051; ±20% → 0.0077 | loose (δ₂ re-servoed) |
| Δ | 35–90 | very loose |
| Ω_rep, B | wide / 1–3.23 G (Δn̄≤0.0003) | irrelevant (field-insensitive) |

δ₂ is the EOM/Raman difference frequency (synthesizer-stable ≪20 kHz); the servo's job is tracking
the AC-Stark drift of the dark resonance (the optimum δ₂ slides ~6 kHz per % of Ω_tot). **First light
is servo-limited, not stability-limited.**

---

## 6. Recommended configuration

- **One Eblana** seed → EDFA → PPLN; one retunable 1560 nm EOM (≈6.5–7.1 GHz) + a 157 MHz tone +
  AOMs (<300 MHz). One beat-lock to the 780 reference. (Clean comb; no SFG clutter.)
- **Free-space** MOT/bright/gray molasses + imaging/OP with per-beam waveplates (GM co-polarized).
- **In-fiber EIT** via **single_end_tagged** (mirror + λ/4 + 400 MHz tag AOM): floor **0.0072**,
  τ₁ₑ≈0.35 ms. Escalate to two doubling chains only if the 0.0072→0.0048 gain is needed.
- **EIT operating point** Δ=45, OmR=0.12 (Pareto knee), δ₂ servoed to the dark resonance.
- **Thermometry** Blackman sideband-π, calibrated R; single laser; radial T ≲ 100 µK.

---

## 7. Open items & checkable questions **[O]**

1. **δ₂ tolerance at the single-end set-point (≈ +0.25, steeper flank than dual-end)** — does it need a tighter
   servo than the dual-end ±20 kHz?
2. **Realistic η_dp** for the HCPCF retro (end-face vs external mirror, λ/4 + double-pass AOM losses);
   where does the floor land at η_dp=0.3, and is a larger tag worth a lower floor?
3. **Cascaded-EOM/SHG spurious comb** — do intermodulation products of the 6.835 GHz + 157 MHz tones
   (and doubling) land on any D2 line and pump/heat, especially during EIT (floor 0.0047–0.0073)?
4. **Two-chain vs tagged-retro decision** — is a 2nd EDFA+PPLN worth Δfloor≈0.0026, given the
   clock/gate requirement?
5. **Repump co-shift over the MOT cooler ramp** — co-ramp the EOM, or accept the shift?
6. **AOM range/power budget** — realize ~±300 MHz of shifting and split the ≤270 mW across MOT(×6) +
   GM + EIT + imaging without starving any beam.
7. **Lock discriminant** — does the EIT-transmission (dark-resonance) peak coincide with the ⟨n⟩-minimum
   δ₂, so a standard EIT-transmission lock is the δ₂ servo?
8. **Thermometry recoil-resolved re-entry** — add the 3-point recoil to the re-entry-to-|g⟩ channel to
   confirm it stays ≪ signal (does not change the calibration conclusion).
9. **Carried:** v0.3.0 θ-aware Stark referencing → re-baseline the operating point / repump detunings.

---

## 8. Provenance

- Floors, rates, robustness, delivery comparison, branching, pedestal, calibration, SHG transfer:
  computed in `eit_cooling_tool.py` / `thermometry.py` (see §-level [V] tags).
- Apparatus: Marchesini 2024. Gray-molasses facts: Leese 2025 (Λ-GM, co-pol, δ≈−0.1Γ),
  Rensburg 2025 (EOM-sideband repump, (Ω₁/Ω₂)²=0.1).
- Extends `laser_architecture_comparison.md` (single-laser cooling/thermometry conclusion) to the full
  sequence and the real apparatus.
