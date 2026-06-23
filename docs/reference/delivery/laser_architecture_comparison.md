# Laser Architecture: Cooling + Thermometry from One Laser, Two Lasers, or Hybrid

Scope: 87Rb clock-EIT axial sideband cooling + asymmetric-sideband thermometry, kagome HCPCF,
1064 nm axial lattice (ν_z = 2π×430 kHz, η_eff = 0.187). All beams here are D2 (~780 nm); the
1064 nm trap is separate. Tags: **[V]** = verified by the tool / direct calc, **[I]** = engineering inference.

## Conclusion (now computed — see thermometry.py)

Cooling and thermometry share the *same* Λ pair, beams, microwave EOM, and field-insensitive
states — they differ only in **operation** (CW near-resonant vs pulsed far-detuned). The single
real conflict is the **single-photon detuning** (cooling ~55 MHz, thermometry far-detuned). The
thermometry simulation now resolves this: with **Blackman-shaped sideband-π pulses and a
calibration curve, the ratio R = RSB/BSB reads ⟨n⟩ faithfully and the result is independent of Δ**
(coherent carrier leak is shaped away; the incoherent scatter re-entry is a near-constant offset
that calibration absorbs), so a single laser at the AOM-reachable ~0.8 GHz is **sufficient**, not a
compromise. The dedicated thermometry laser is now an **SNR/throughput upgrade** (it cuts the
scatter-driven atom loss from ~13% to ~2.5% per pulse, roughly halving the shot budget), not a
requirement. **Recommendation: Config 1+ (single laser + double-pass AOM offset arm), with a
calibrated R — never the naive R/(1−R).**

## What must be generated

**Near-resonant family** (all within Δ ~ tens of MHz of D2, one laser spans it with EOM+AOMs):

| tone | transition | pol | offset from control |
|---|---|---|---|
| control | F=2→F′2 | σ− | 0 |
| probe | F=1→F′2 | σ+ | +6834.68 (6.835 GHz EOM) |
| repump1 | F=1→F′1 | σ− | +6692.74 |
| repump2 | F=2→F′1 | σ+ | −151.94 |
| readout | F=2→F′3 (cycling) | — | +267 (AOM) |

Plus state-prep (optical pumping, reuses probe/repump) and an imaging repump (F=1→F′2).

**One far-detuned task:** thermometry Raman on the *same* |1,−1⟩↔|2,+1⟩ pair, Δ ~ 1–4 GHz,
two-photon difference scanned to A_HFS, A_HFS±ν_z. Microwave (6.835 GHz) sideband thermometry is
impossible (η≈0 — no photon momentum), so far-detuned optical Raman is mandatory. **[V/I]**

## The crux: the detuning jump

Scattering per Raman π-pulse (balanced beams, Γ=2π×6.07 MHz) **[V, thermometry.py]**. The
realistic probe is a **sideband-π** (full transfer), which is 1/η_R ≈ 5.3× longer than a carrier-π
and so scatters that much more:

| Δ | carrier-π | sideband-π (realistic) |
|---|---|---|
| 300 MHz | 6.4% | 34% |
| 1 GHz | 1.9% | 10% |
| 4 GHz | 0.5% | 2.5% |

The thermometry signal is **R = P₁/P₀ = 0.43%**, 1−P₀ = 0.45% **[V]**. The key fact (verified):
- **Uniform scatter cancels exactly in the ratio R** → Δ only costs atom survival/SNR, not bias.
  So Δ ~ 0.8 GHz (single laser, double-pass AOM) is fine; the ~13% loss is a statistics hit. **[V]**
- The dominant *bias* is instead the coherent carrier wing of a square pulse (0.39% ≈ the signal),
  which **Blackman shaping removes** (suppressed ~10⁶). **[V]**

## Config 1 — Single laser

One master locked near F=2→F′2; every tone via EOM/AOM. Detuning jump by AOM (~0.3–0.8 GHz,
double-pass) or by re-locking the master between cooling and thermometry.

**Pros**
- Cheapest, most compact, one frequency reference — best for a fiber / portable system. **[I]**
- Raman pair **automatically phase-locked** (both tones are EOM sidebands of one carrier); thermometry
  coherence is then limited only by motion/trap + the field-insensitive pair. **[V/I]**
- One microwave (6.835 GHz) EOM serves both the cooling probe and the thermometry Raman
  (time-multiplexed; retune the synthesizer by a few MHz between phases). **[I]**
- No relative-frequency drift between cooling and thermometry. **[I]**

**Cons**
- The detuning jump is the bottleneck: AOM range caps Δ at ~0.8 GHz → ~2% scatter (ratio-only
  thermometry); a full re-lock to ~GHz is slow and perturbs the cooling lock each cycle. **[I]**
- One crowded comb (5+ tones) must be reconfigured between cooling, thermometry, and readout. **[I]**
- Cooling and thermometry cannot be developed/debugged independently. **[I]**

## Config 2 — Two lasers (A = EIT/near-resonant family, B = thermometry)

Laser A locked at Δ≈55 (control + probe + repumps + readout). Laser B locked far-detuned (~4 GHz),
with its **own** 6.835 GHz EOM for the pulsed Raman pair + the ±ν_z scan. A and B run sequentially
(cool with A, measure with B), time-multiplexed into the shared delivery via a switch.

**Pros**
- Each laser sits at its optimal detuning → thermometry scatter ≪ signal; all observables (ratio,
  absolute, BSB fits) available. **[I]**
- No detuning jump; the **cooling lock is never disturbed**. Clean cycle timing, high throughput. **[I]**
- B needs **no phase lock to A** — the Raman coherence comes from B's own EOM (B's carrier phase is
  common to both tones, cancels in the difference). B can be loosely locked (~MHz). **[V/I]**
- Cooling and thermometry are independent subsystems. **[I]**

**Cons**
- Two lasers, two locks, two references → cost, space, complexity. Worst for portability. **[I]**
- Two microwave EOMs (one per laser), unless shared (see Hybrid 2a). **[I]**
- A and B are the **same color** (both D2, ~GHz apart): not dichroic-separable, so they must be
  combined by a switch / non-polarizing BS into the same counter-propagating delivery. **[I]**

## Hybrids

**2a — Two lasers, shared modulation chain.** Time-multiplex A and B into ONE EOM+AOM chain *after*
the switch. Gives two independent detunings but **one microwave EOM and one AOM set**. Best
cost/performance of the two-laser family; the switch lives in the dead time. **[I]**

**2b — Thermometry on D1 (795 nm), cooling on D2 (780 nm).** The two colors are **dichroic-separable**,
so combining/splitting into the shared fiber delivery is lossless and clean (the main pain of Config
2 disappears). The ground pair is still field-insensitive (a ground-state property), so the same
|1,−1⟩↔|2,+1⟩ thermometry works through 5P₁/₂. Cost: a D1 laser + re-validating the D1 Raman
branching/Stark (the project's D1 hybrid files are the starting point). **[I — needs D1 check]**

**2c — Offset-phase-locked B (OPLL to A at ~GHz).** Gives A–B mutual coherence — but thermometry
doesn't need it (2b/Config 2 argument). Usually **overkill** unless you later want A–B
interferometry. **[I]**

**1+ — Single laser + double-pass AOM offset arm.** The practical middle: one laser/reference/EOM
(all of Config 1's simplicity and phase coherence), but the detuning jump is a clean ~0.8 GHz
double-pass AOM in a switchable arm rather than a re-lock. Enables ratio-method thermometry at ~2%
scatter with fast switching. This is the recommended *single-laser* implementation. **[I]**

## Comparison

| dimension | 1 (single) | 1+ (single+AOM arm) | 2 (two) | 2a (shared chain) | 2b (D1) |
|---|---|---|---|---|---|
| lasers / locks | 1 | 1 | 2 | 2 | 2 |
| microwave EOMs | 1 | 1 | 2 | 1 | 2 |
| Raman phase coherence | auto | auto | B-internal | B-internal | B-internal |
| thermometry Δ | ≤0.8 GHz / re-lock | ~0.8 GHz | ~4 GHz | ~4 GHz | ~4 GHz |
| scatter / π-pulse | 2% / low | ~2% | <0.5% | <0.5% | <0.5% |
| observables | ratio (+) | ratio | all | all | all |
| cooling lock disturbed | maybe | no | no | no | no |
| beam combination | n/a | n/a | switch/BS (same color) | switch (same color) | dichroic |
| compactness / cost | best | best | worst | mid | mid |
| independent debug | no | no | yes | yes | yes |

## Recommendation (resolved by computation)

**Build Config 1+ (single laser + double-pass AOM offset arm, Δ ≈ 0.8 GHz), with
Blackman-shaped sideband-π thermometry pulses.** The thermometry simulation shows:

- **Ratio method is exact and Δ-independent.** With Blackman, R→⟨n⟩ recovers the input with no
  bias (0.005→0.0050, 0.05→0.0500, ...) and the curve at Δ=0.8 GHz is *identical* to Δ=4 GHz,
  because uniform scatter cancels in R. A *square* pulse instead leaks 0.39% of the carrier into
  the sideband (≈ the 0.43% signal → ~2× bias); Blackman suppresses that wing by ~10⁶. **[V]**
- **Scatter is an SNR cost, not a bias — *if you calibrate*.** Sideband-π scatter is ~13%/pulse at
  0.8 GHz, ~2.5% at 4 GHz. Uniform loss cancels in R, but the branching-resolved **re-entry** of
  scattered atoms into the *detected* state |2,+1⟩ (P(g→e)≈0.10, P(e→e)≈0.21) puts an incoherent
  pedestal on the tiny red signal. The master equation shows this pedestal is a **near-constant
  offset on R that preserves the slope dR/d⟨n⟩** → a **calibration** curve R-vs-known-⟨n⟩ absorbs
  it. Naive R/(1−R) is biased ~3× at 0.8 GHz, and off-sideband subtraction *over*-subtracts (the
  off-resonant pedestal is undepleted) — so **calibrate, don't subtract**. **[V]**
- **The dedicated laser is a ~2× shot-count upgrade.** The pedestal inflates shots ~2–3× at
  0.8 GHz vs ~1.3× at 4 GHz, so a 4 GHz thermometry laser roughly halves the shot budget — a real
  but non-blocking SNR gain. **[V]**
- **Even the BSB Rabi-flop fit works at 0.8 GHz:** P₀ recovers to ~±5% (within the ±10% target)
  with ~2000 shots at every Δ ≥ 0.8 GHz — limited by shot noise, not detuning. **[V]**

So the dedicated thermometry laser (2a/2b) is an **optional ~10% SNR/throughput upgrade**
(13%→2.5% atom loss), reserved for if photon budget or cycle rate becomes the bottleneck. **2c
(OPLL) — skip.** Keep radial T ≲ 100 µK so the axial sideband stays sharp (≤19 kHz spread vs the
~20–80 kHz pulse bandwidth); shorter pulses (larger s, Blackman) tolerate more radial spread. **[V]**

## Open / checkable questions

- **Q1 [RESOLVED, V].** R-vs-⟨n⟩ at Δ≈0.8 GHz is *exact* with Blackman (scatter cancels);
  square-pulse bias is +0.002 additive at the floor, removed by shaping. → Config 1+ suffices.
- **Q2 [RESOLVED, V].** BSB-fit recovers P₀ to ~±5% at all Δ ≥ 0.8 GHz (2000 shots) — shot-noise
  limited, not Δ-limited. → No high-Δ requirement.
- **Q3 [D1, open].** Hybrid 2b only: does a D1 Raman on |1,−1⟩↔|2,+1⟩ keep clean branching + a
  workable Rabi/scatter ratio at the 1064 trap? (Re-use the project D1 files.) Now lower priority,
  since Config 1+ is sufficient.
- **Q4 [bench, open].** Achievable double-pass AOM offset (→ confirm ~0.8 GHz reachable) and switch
  extinction/timing in the cooling→thermometry dead time.
- **Q5 [RESOLVED, V].** Branching-resolved scatter re-entry into the detected state |2,+1⟩
  (P(g→e)≈0.10) makes a master-equation pedestal that is a *near-constant offset* on R (slope
  preserved). **Calibration absorbs it** (naive R/(1−R) biased ~3× at 0.8 GHz; off-sideband
  subtraction over-subtracts). Net: an SNR cost (~2–3× shots at 0.8 GHz, ~1.3× at 4 GHz), not a
  bias on calibrated ⟨n⟩. Recoil heating is 0.012 phonons/scatter. (Recoil omitted in the pedestal
  collapse motion — valid since detection counts |e⟩ at all n; a recoil-resolved refinement would
  only touch the small re-entry-to-|g⟩ channel.)
