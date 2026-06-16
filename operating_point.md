# Operating point (authoritative) — corrected, with retro-reflectivity-capped optimization

Replaces the Δ=80 / Ω_p/Ω_c=0.25 block. The scheme, the F′=3-in-Hamiltonian conclusion, the "don't use the eroded-bare-shift criterion," and the carrier-suppressed dual-end realization (memo §3) all stand. What changes: the floor optimum is at **lower Δ and lower probe**, not at Ω_c=11.4. Tags [V] verified/computed, [I] inferred, [O] open.

## §1. Operating point (atomic, delivery-independent) [V]

clock-EIT, field-insensitive pair |1,−1⟩ / |2,+1⟩ → |F′=2, m′=0⟩ (both g_F m_F=+½):

- Single-photon detuning **Δ = +45 MHz** blue (was +80). Flat floor optimum ≈40–50; degrades above ~80. Also the **radial-cloud optimum** (S4 MC: 0.0094 at Δ=45 vs 0.0102 at Δ=80), so no separate cloud correction is needed.
- **Ω_p/Ω_c = 0.12** (was 0.25). Control σ−, Ω_c = 8.74 (2π MHz); probe σ+, Ω_p = 1.05. Ω pinned to the EIT condition Ω_tot=√(4Δ·ν_z); the *ratio* is the new lever (see §2).
- Two-photon detuning **δ₂ servoed to the dark resonance**, set-point ≈ −0.1 MHz (dual-end) / ≈ −0.22 MHz (single-ended tagged). Parking at the bare hyperfine still costs the floor; the offset drifts with power/radius and must be servoed, not hardcoded.
- B flexible 1.0–1.5 G for cooling (the cooling pair is first-order field-insensitive at any field; the 3.229 G clock-magic field is only for interrogation). Two repumpers (|1,0⟩ and |2,−2⟩ leaks), Δ_rep = +20…+40 MHz.

**Floors (clock_tagged_solve, B=3.229, N_f-stable, δ₂-optimized):** clean Λ **0.0032** / dual-end **0.0048** / single-ended tagged **0.0076**. Cooling time τ ≈ 0.55 ms (sub-ms; ~1.5× slower than the OmR=0.25 point — see §2). Powers at the atoms (19 µm waist): control 0.11 µW, probe 4.8 nW, repump 5.0 nW.

*Model note:* the absolute floor depends on the recycler model — reduced 3-level ~0.0035, this multilevel-tagged 0.0048–0.0076, full-recycler limit ~0.002–0.004 if re-optimized at this point. The **3.5× improvement over the Δ=80/OmR=0.25 memo point is model-independent** (verified head-to-head in clock_tagged: 0.0166 → 0.0048).

## §1b. Delivery [V] — two options, same atomic operating point

- **Dual-end, carrier-suppressed EOM (preferred; from memo §3, validated).** Arm A control (σ−, direct, clean tone); arm B probe via a plain phase EOM at the 6.835 GHz hyperfine, depth **β = 2.405** (first J₀ zero) so the carrier vanishes and the σ+ probe is a J₁ sideband; all other sidebands land ≥6.835 GHz off-resonance and are harmless. Opposite-end injection, **f_A = 0** (AOMs for intensity/pulsing only). Floor **0.0048**. At OmR=0.12 the arm power split is **A:B ≈ 95:5** (was 81:19 at OmR=0.25), since probe field = J₁·(arm-B field) = 0.12·(arm-A field). No SSB modulator, slave laser, or filter cavity required.
- **Single-ended tagged retro (fallback if two-ended vacuum access is impractical).** One fiber end: control carrier + probe upper-sideband from a phase EOM at **β ≈ 0.59**, co-propagating; double-passed tag AOM **2f_A = 300 MHz** down-shifts the return; λ/4 in the retro arm flips helicity. This is a *different* architecture from the dual-end one — its 2f_A=300 is correct here (δ₂ servoed, F′=3 in-model), not the "f_A=0" of the dual-end case. Floor **0.0076** (rejected-field scatter is the 0.0076 vs 0.0048 difference; intrinsic F′3,0 admixture sets 0.0048 vs 0.0032).

## §2. Why Ω_c = 11.4 is not the floor optimum [V, corrects memo §2]

The memo's two claims that **stand**: (i) F′=3 (−186.65 MHz from the +80 control, or −212 from the +45) erodes the bare bright–dark splitting; (ii) the "set the eroded shift = ν_z" criterion **overshoots** — pushing Ω_c up is a floor regression (verified: at Δ=80, Ω_c 11.4→13.5 worsens the floor).

What the memo **missed**: it scanned Ω_c only *upward*. The dominant lever is the opposite direction — **weaker probe**. The cooling rate *saturates* with Ω_p/Ω_c (Liouvillian gap 0.0017/0.0024/0.0027 MHz at 0.11/0.18/0.25) while the floor keeps dropping. Verified:

- At Δ=80 (the memo's own Δ), dual-end floor vs Ω_p/Ω_c: 0.25→**0.0166**, 0.15→0.0072, 0.10→**0.0041** — a 4× drop the memo never tested.
- Δ=45 / Ω_p/Ω_c=0.12 → **0.0048** vs the memo point's 0.0166 (same solver) — **3.5×**.

So neither the naive Ω²/4Δ=ν_z slaving *nor* the eroded-shift criterion sets the operating point; both are resonance-placement guides. The floor optimum is found by a 2D scan over (Δ, Ω_p/Ω_c) and lands at low Δ and low probe, bounded below only by the cooling rate (τ must stay ≪ trap lifetime; at OmR=0.12, τ≈0.55 ms is comfortable). F′=3 kept in the Hamiltonian still costs only ~4% on the floor and ~0 on the operating point. [I] The exact floor-optimal OmR (0.10–0.12) is set by the trap-lifetime/τ budget; tighten once the in-fibre coherence time (§6) is measured.


## §3. Retro-reflectivity-capped optimization (single-ended tagged) [V, this session]

The single-ended tagged retro delivers the probe via the AOM-tagged, helicity-flipped return; its efficiency η_dp (AOM double-pass × re-injection into the core) was expected to limit the floor. It does **not**, provided the tag shift is large.

**Result (validated tagged solver, δ₂-optimized, N_f-stable).** At **2f_A = 400 MHz** (200 MHz AOM, double-passed, down-shift) the tagged-inclusive floor is **flat in η_dp over 20–50 %**: 0.0073 / 0.0072 / 0.0072 / 0.0073 at η_dp = 0.20 / 0.30 / 0.40 / 0.50 (Δ=40, OmR=0.12, δ₂=+0.18). Mechanism: lower η_dp forces a stronger forward-probe launch (∝1/η_dp), whose *rejected* component is the dominant tagged-extra scatter — but the 400 MHz tag pushes it far enough off-resonance that the amplification washes out. The η_dp×tag interaction shrinks monotonically with the tag (OmR=0.25 spread across 20–40 %: 0.0016 at 2f_A=160 → 0.0010 at 220 → 0.0005 at 300 → **0.0003 at 400**).

**Consequence.** The atom-frame operating point {B, Δ, Ω_c, Ω_p, δ₂, 2f_A} is **identical across 20/30/40 %**. Only two lab settings scale, both trivially small:

| η_dp | EOM depth β (rad) | launch-probe power at atoms |
|---|---|---|
| 0.20 | 0.310 | 3.6 nW |
| 0.30 | 0.253 | 2.4 nW |
| 0.40 | 0.219 | 1.8 nW |

**Use 2f_A = 400 (200 MHz tag AOM) and the retro cap is a non-issue** — it costs a little more EOM depth and nW-scale launch power, not floor and not operating point. This refines §1b (2f_A = 300 → 400) and lowers its single-ended floor from ~0.0092 to ~0.0072 at OmR=0.12.

*Caveat:* the `solve()` floor is tagged-extra-inclusive; the all-in system floor adds the separately-budgeted leak/anti-trap increment (+0.007–0.012), and the absolute number carries a ~2× calibration spread. The *relative* result — flat in η_dp, dominated by the tag — is robust.
