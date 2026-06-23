# v12 — six-column cooling comparison (capstone, 2026-06-14; F′=0 m=0-RSC added 2026-06-16)

> **Version note (read first).** This is a **v12 snapshot** kept for the scheme-by-scheme
> reasoning. Its clock-EIT floor (0.0064) predates the v14 refinement — the authoritative
> clock-EIT solve floor is **0.0048 (dual) / 0.0072 (single-ended)** at the v14 operating point
> (`operating_point.md`, `clock_EIT_consolidated.md`), and the certified single-atom floor is 0.008–0.010 (the v15 ~0.012–0.019 all-in was a double-count, withdrawn); the cloud floor is T_r-gated (≈0.007/0.012/0.022 at 25/100/400 µK). The
> clock-RSC ≈0.45 disqualification below is **confirmed** and fully written up in
> `clock_RSC_resolution.md` (the rank-2 obstruction; the engine's 0.0137 is an obstruction-free
> idealization, not the floor). Treat the other per-scheme floors here as v12-era values.

**Decision up front.** For the field-insensitive operation the apparatus needs (in-fibre
B-noise is the binding environmental problem), the recommended axial cooler is **clock-EIT
on the field-insensitive pair |1,−1⟩/|2,+1⟩, run at B = 1.0–1.5 G with no hardware
change** — realised floor **n̄ = 0.0064 (T_z ≈ 4.1 µK, 99.4 % ground)**, conditional on a
sub-100-Hz two-photon coherence budget (the one hardware question that decides it). The
two field-insensitive RSC alternatives do not survive: **clock-RSC is DISQUALIFIED** (its
Δm=+2 D2 Raman is rank-2/HFS-enabled and scatter-limited — the 0.00096 floor is not
realisable, it lifts to ≈0.45), and the rank-0 **m=0 RSC (|1,0⟩↔|2,0⟩ + F′=0 polarizer)** does
cool but only to **n̄ ≈ 0.05** (recoil-limited by its ~3.5-scatter recycle chain, ~7× above
clock-EIT) — **uncompetitive**, not disqualified. The lower-floor RSC/EIT schemes that remain
(stretched-RSC 0.00196, dRSC 0.0070, m′=2-EIT 0.018) are all **field-sensitive** and each
carries a tolerance or hardware cost that the clock pair does not.

Tags: **[V]** verified by computation (this program; reproducible from the named scripts) ·
**[I]** inference / design ranking · **[O]** open / bench number, deliberately not invented.

---

## System (frozen)

⁸⁷Rb, 1064 nm kagome-HCPCF axial lattice. ν_z = 2π·430 kHz, ν_r = 2π·5.4 kHz,
U₀ = 22.8 MHz (1.1 mK), η(780) = 0.094, η_eff(retro) = 0.184, η_em = η/√3, Γ_D2/2π = 6.07,
Γ_D1/2π = 5.746. Axial level spacing ℏν_z/k_B = **20.6 µK**; all T_z below are
T_z = ℏν_z / [k_B·ln(1+1/n̄)]. v11 D2 baseline frozen; this brief integrates the v12
program (RSC builders, clear geometry, noise cells, parasitics) onto it.

---

## The five columns [V floors]

| # | scheme | mechanism / pair | field-insens.? | floor n̄ | T_z | ground | binding axis | status |
|---|--------|------------------|:--------------:|--------:|----:|-------:|--------------|--------|
| 1 | **clock-EIT** | EIT Λ, m′=0, pair \|1,−1⟩/\|2,+1⟩ | **yes** | **0.0064** | 4.1 µK | 99.4 % | two-photon coherence | **RECOMMENDED** |
| 2 | stretched-RSC | std Raman SBC, \|2,+2⟩/\|2,+1⟩, σ⁺ cycling pump | no | 0.00196 | 3.3 µK | 99.8 % | pump PER + B | lowest floor, tolerance-bound |
| 3 | dRSC (geom A) | degenerate Raman, \|2,+2⟩ Zeeman ladder, D1 | no | 0.0070 † | 4.2 µK | 99.3 % | beam asymmetry + ellipticity | tie, tolerance-heavy |
| 4 | m′=2-EIT | EIT Λ, m′=2 (tensor) | no | 0.018 | 5.1 µK | 98.2 % | in-fibre B (≲30 mG) | field-sensitive fallback |
| 5 | ~~clock-RSC~~ | std Raman SBC, clock pair, F′=1 clear | yes | ~~0.00096~~ → **0.45** | 17.6 µK | 69 % | — | **DISQUALIFIED** |
| 6 | m=0 RSC (F′=0 pol.) | Raman SBC, \|1,0⟩↔\|2,0⟩ Δm=0 (rank-0), F=2 recycle + F′=0 σ± polarizer | **yes** | **~0.05** | ~6.8 µK | ~95 % | recycle-chain recoil | **UNCOMPETITIVE** |

† dRSC 0.0070 is the anti-trap-free solver floor at beam-asymmetry x=2; **with the 1064 D1
anti-trap kernel the realistic value is n̄_TOT ≈ 0.016 (T_z ≈ 4.9 µK)**.

**Field-insensitive branch collapses to one entry.** Of the two field-insensitive schemes,
clock-RSC is out (below), so the design-driving requirement is met only by clock-EIT. The
other three are field-sensitive — usable only with tight B control or as a separate
cool-then-use stage, not for the field-noisy in-fibre environment the clock pair was chosen
to defeat. **[I]**

---

## Per-column analysis

### 1 — clock-EIT  (recommended)  [V floor, O coherence]

**Hardware.** EIT probe+control on D2 with the field-insensitive ground pair |1,−1⟩/|2,+1⟩.
No magic field needed — the pair is first-order field-insensitive at *all* B (g_F·m_F = +½
both legs; magic 3.229 G is only the 2nd-order zero), so it runs at the achievable
1.0–1.5 G. The cost is a phase-coherent **6.835 GHz** two-photon drive (DDS/PLL EOM chain +
short common differential path). The 1064 anti-trap on 5P₃/₂ F′=2 is carried in the v11
realised floor.
**Realistic axial T.** n̄ = 0.0064 → **T_z ≈ 4.1 µK** (option A, D_rep2=5, B=1.5 G; option C
≈ 0.0094 → 4.4 µK). v11-realised, anti-trap-included.
**Noise robustness.** Magnetic **immune** (1.49 kHz/G = 75 Hz per 50 mG). Vector-shift
**immune** (2nd-order, 0.50 kHz/unit-circular). **Binding axis = two-photon dephasing: floor
doubles at only 0.26 kHz** — the most dephasing-fragile column in the matrix — so the scheme
wants a **sub-100-Hz** two-photon linewidth for ≥4× margin. This single axis decides it:
met → clock-EIT wins outright on field-insensitivity; not met in fibre → the clock vs m′=2
comparison tightens. Falsify by measuring the two-photon (not laser) linewidth. **[O]**

### 2 — stretched-RSC  (lowest floor, tolerance-bound)  [V]

**Hardware.** Textbook Raman SBC on the stretched pair |2,+2⟩/|2,+1⟩ with a σ⁺ cycling pump
on F′=2 (|2,+2⟩ is σ⁺-dark). Far-detuned Raman + cycling pump; the pump rides the 1064-
anti-trapped 5P, adding pump-excursion heating not included in the bare floor. **Field-
sensitive** (Δm=1 Zeeman).
**Realistic axial T.** n̄ = 0.00196 → **T_z ≈ 3.3 µK** (the lowest of the five), *if both
tolerance axes are met* — and the bare floor is a model-internal lower estimate (anti-trap
pump-excursion adds on top).
**Noise robustness.** Dephasing-robust (doubles 2.02 kHz). But **two knife-edge axes, both
tighter than the EIT analogues**: (i) magnetic 0.70 MHz/G → **≤4.3 mG** for +10 % floor;
(ii) the binding axis — the **cycling-pump σ⁻ leak depumps the dark |2,+2⟩, doubling the
floor at ε ≈ 0.0006 wrong-handed intensity (32 dB PER)**, recoil-amplified. 32 dB in-fibre
circular purity + 4 mG field stability in kagome HCPCF is the open question; if unreachable,
stretched-RSC disqualifies on tolerances despite the best floor. **[V mechanism / O bench]**

### 3 — dRSC geometry A  (tie, tolerance-heavy)  [V]

**Hardware.** Degenerate/dark-resonance Raman on the |2,+2⟩ Zeeman ladder, on D1 (effective
excited HFS 576 vs D2's 129 MHz; repump branching favourable). Needs a Zeeman degeneracy
field (~0.31 G, or a B-tracked Raman offset at higher B) — the |2,+2⟩ ladder is field-
sensitive, so **not field-insensitive**. Requires beam-asymmetry control (x = Ω₊/Ω₋) and a
λ/4 double-pass retro. Fast (W ≈ 6–7/ms vs clock-EIT's 3.2).
**Realistic axial T.** anti-trap-free 0.0070 → 4.2 µK at x=2; **with the D1 anti-trap kernel
n̄_TOT ≈ 0.016 → T_z ≈ 4.9 µK** — at/just below the EIT band, a **tie, never a decisive win**.
**Noise robustness.** Dephasing tracks m′=2 (doubles 4.5 kHz; the earlier "selection-rule
floor is dephasing-flat" claim was falsified — it rises 0.007→0.084 over 0–40 kHz).
**Binding axis = the asymmetry/ellipticity tolerance**: the dark |2,+2⟩ scatters only the σ⁻
beam, so floor ∝ 1/x² at fixed cooling rate — but the asymmetry-induced vector shift grows
∝(x²−1/x²) (16× at x=4), tightening the ellipticity-uniformity budget ~x²-fold in a
birefringent fibre, plausibly washing out the homogeneous gain. Parity with the clock needs
x≥3, where adiabaticity also breaks (Ω₊/Δ→0.2). **[V / O bench]**

### 4 — m′=2-EIT  (field-sensitive fallback)  [V]

**Hardware.** EIT through excited m′=2 (5P₃/₂ F′=2). Same EIT machinery as clock-EIT but on
a **tensor-shifted, field-sensitive** transition; needs in-fibre **B ≲ 30 mG** (933× more
field-sensitive than the clock).
**Realistic axial T.** n̄ = 0.018–0.021 → **T_z ≈ 5.1 µK** (the warmest of the viable four).
**Noise robustness.** Dephasing-robust (doubles 4.63 kHz — 18× less fragile than clock-EIT).
But magnetic 1.40 MHz/G (≲30 mG) and vector-shift exposed (0.470 MHz/unit-circular, +8.2 %
floor at 5 % circular error). The field-sensitivity is the whole reason it is a fallback, not
the primary. **[V]**

### 5 — clock-RSC  (DISQUALIFIED)  [V]

**The result that closes the program.** A two-circular F′=1 clear (one axial linear beam)
gives a coherent-model floor of 0.00096 — ~7× below clock-EIT — and it is field-insensitive
and dephasing-robust (1.59 kHz). But the coherent model **omitted the cooling beams' own
off-resonant scatter**, and on D2 that is fatal: the Δm=+2 clock Raman is **rank-2 / HFS-
enabled** — a J=½ ground manifold cannot supply Δm_J=+2 and the dipole conserves m_I, so the
transition vanishes in the degenerate-HFS limit and proceeds only via the excited I·J′
coupling (amplitude ∝ Δ_HFS/Δ²). Coherence-per-scatter is therefore **Δ-independent** and
pinned at a figure of merit of order a few (FoM = A2_INF/Γ·(3/2) ≈ 3.95; A2_INF ≈ 16 MHz).
With RSC's slow Lamb-Dicke cooling (W ≈ Ω₂ph/44), the scatter beats the cooling ~11–23:1, so
the dark state depumps faster than it cools: **floor lifts 0.00096 → ≈0.45 (T_z ≈ 18 µK,
only 69 % ground)**, B-independent, no operating point recovering it (robust to ×3 in the
scatter prefactor; needs ×170 to recover). Corroborates S1's "D2 m′=2 marginal" from an
independent direction.

This was re-verified three independent ways this session (product-basis amplitude → exact
zero in the degenerate limit; full-resolvent Δ-scaling; **explicit diagonalisation of both
manifolds with ground Breit-Rabi + excited HFS+Zeeman at 1.5 G**, the allowed 1/Δ coefficient
= 1×10⁻⁴, i.e. the rank-2 null survives full F and m_F mixing). **Why clock-EIT is not hit:**
EIT operates near-detuned, where the excited HFS is resolved and the Δm=+2 coherence is fine,
and its floor already includes scattering — it is RSC's far-detuned operation that exposes
the rank-2 limit, and you cannot pull it near-resonant without enormous scatter. **[V]**

### 6 — m=0 RSC, F′=0 polarizer  (field-insensitive, recoil-uncompetitive)  [V]

**The other field-insensitive RSC route — cools, but doesn't compete.** Motivated by escaping
clock-RSC's rank-2 death: cool on the **0-0 clock Raman |1,0⟩↔|2,0⟩**, which is **Δm=0 =
rank-0 (allowed)** and first-order field-insensitive. Rectified by **red-sideband detuning**
(δ=+ν_z; blue off by 2ν_z), not by a ladder edge. Recycle |2,0⟩ via an **F=2→F′2 σ± pump**;
funnel F=1 back to the dark |1,0⟩ with an **F′=0 σ± polarizer** (F′=0 has only m′=0, so |1,0⟩
is σ-dark — only the absent π reaches it — and F′=0 decays to F=1 only, ΔF=2 forbidding F=2,
so the polarizing sub-loop is closed; the off-resonant F′1 leak at 72 MHz is ~0.44 %).

**Floor.** Multilevel solve (8 ground states × Fock, `m0_rsc.py` v0.2.0, via mesolve — the
steadystate solver is rank-deficient on this manifold): recoil-free n̄→~0.02 (the cooling
mechanism is sound, |1,0⟩ duty cycle ~80 %); **with physical diffusion recoil, floor ≈ 0.05
(T_z ≈ 6.8 µK, ~95 % ground)**. **Recoil-limited** by ~**3.5 spontaneous photons per phonon
removed** (recycle ~2, F′=2→F1 being ½; F′=0 polarizer ~1.5, its 1/3 branching the cost) ×
η_z²·4/3 ≈ 0.012 each → ~0.04 floor, roughly operating-point-independent (the scatter count
is fixed by branching, so tuning R/Ω_R won't push below ~0.04). **~7× above clock-EIT.** This
is the expected ordering: EIT cools through a Fano dark state with minimal scattering, whereas
any RSC needs an optical-pumping recycle, and in-fibre every recycle photon is delivered along
the cooled axis and heats it — RSC pays a recoil tax that dark-state EIT avoids.

**Degenerate variant is worse — it does not cool at all** (`f0_drsc.py`). A *within-F=1*
degenerate dRSC pumped by F′=0 σ± puts the dark state at **|1,0⟩, mid-ladder**, where the
Δm=−1 cooling and Δm=+1 heating sidebands are mirror images, both resonant at Zeeman=ν_z →
they cancel (model: n̄≈10, flat in all Ω_R, Γ_p). dRSC needs an **edge** dark state to rectify,
and F′=0 (only m′=0) structurally cannot make one. So F′=0 is a clean m=0 *selector* but never
a degenerate-dRSC engine; its only cooling use is the non-degenerate cross-F scheme above.

**Status: field-insensitive but uncompetitive** (~0.05 vs clock-EIT 0.0064), and not the
elegant closed cycle — it still needs the 6.835 GHz Raman *and* a separate F=2 recycle. Adds
no reason to displace clock-EIT. **[V floor / V no-cool / I ranking]**

---

## Shared front-end (applies to all columns equally)  [V / O interface]

Transport from the MOT (7 mm above the tip) into the fibre adiabatically compresses the
lattice (waist 126→19 µm), heating T_z ∝ 1/w (×6.6) and T_r ∝ 1/w² (×44): an atom arrives at
n̄_z ≈ 2, **n̄_r ≈ 1360** (radial excursion 7.6 µm = 40 % of the waist, deeply non-Lamb-Dicke),
which would smear ν_z and spoil any axial scheme. **Resolution (verified): 3D pre-cool just
*outside* the fibre in the focal trap, then load in and do final axial cooling inside.**
Cooling in the tight focal trap (within the 1.07 mm Rayleigh range it is ~as tight as
in-fibre) to molasses 8 µK → n̄_r ≈ 30 (excursion 1.2 µm = 6 %, ν_z smear ~2 kHz, negligible),
or gray molasses 2.5 µK → n̄_r ≈ 9. Doing the radial cooling outside buys **free-space optical
access from all directions → no transverse-PER gate, keeps every column bench-unconditional.**
The only residual is the free-space→guided load-in at the tip ([O], experimental, separable,
affects all columns identically). The axial *floor* is start-independent (steady state), so
none of the five floors changes; the front-end is what makes them reachable.

---

## Decision and ranking  [I]

The apparatus requirement is **field-insensitivity** (in-fibre B-noise is the binding
problem). On that axis:

1. **clock-EIT — recommended.** The only field-insensitive scheme that survives. Floor 0.0064
   (4.1 µK), B-immune, vector-immune. Conditional on the sub-100-Hz two-photon coherence
   budget — the #1 bench question. No hardware change from v11.
2. **If field-sensitive operation is acceptable** (tight B control, or cool-then-use):
   - **stretched-RSC** gives the lowest floor (0.00196, 3.3 µK) but demands 32 dB PER + 4.3 mG
     — likely the disqualifier in kagome HCPCF.
   - **dRSC** ties the EIT band (~0.016, 4.9 µK) but is asymmetry/ellipticity-tolerance-heavy
     and only fast, not low.
   - **m′=2-EIT** is the field-sensitive EIT fallback (0.018, 5.1 µK; ≲30 mG).
3. **clock-RSC — disqualified.** Not realisable on D2 (scatter-limited).
4. **m=0 RSC (F′=0 polarizer) — uncompetitive.** Field-insensitive and rank-0 (it cools, unlike
   clock-RSC), but recoil-limited at n̄≈0.05 (~7× above clock-EIT); its degenerate within-F=1
   variant doesn't cool at all (mid-ladder dark state can't rectify). No reason to displace
   clock-EIT.

The floor differences among the survivors are µK-scale and not the deciding factor;
**field-insensitivity, tolerances, and the two-photon coherence budget are.** The clock pair
wins because it needs none of the tolerance controls (PER, mG-field, beam-asymmetry,
ellipticity-uniformity) the field-sensitive schemes do — at the cost of one demanding but
well-posed hardware spec.

---

## Ledger

**[V] computed/verified:** all six floors (0.0064 / 0.00196 / 0.0070 / 0.018 / 0.45 / ~0.05);
clock magnetic & vector immunity (75 Hz/50 mG, 0.50 kHz/unit, 2nd-order); stretched 0.70 MHz/G
+ σ⁻-leak 32 dB PER; dRSC x-scaling (x=2 → 0.0070/0.016) + 4.5 kHz dephasing; m′=2 1.40 MHz/G;
all five dephasing doublings (0.26 / 2.02 / 4.5 / 4.63 — clock-RSC moot); the clock-RSC rank-2
disqualification (FoM ≈ 2–4, floor → 0.45) verified three ways incl. explicit two-manifold
diagonalisation with full F/m_F mixing; transport-heating factors and the re-cool-outside
resolution. **m=0 RSC (F′=0 polarizer):** rank-0 cooling confirmed (recoil-free n̄→0.02), realistic
recoil floor ≈0.05 from a ~3.5-scatter recycle chain (recycle ~2 + F′=0 polarizer ~1.5);
within-F=1 degenerate variant does not cool (mid-ladder dark state cannot rectify; n̄≈10 flat).
**[I] inference/ranking:** the field-insensitive branch reduces to clock-EIT; the survivor
ranking; "tolerances not floor decide it."
**[O] bench, not invented:** in-fibre two-photon coherence (clock-EIT binding); in-fibre
circular PER + birefringence drift (stretched/dRSC binding); in-fibre B amplitude;
clock Raman AC-Stark RIN coefficient (needs Δ_R); absolute cooling times W (solver-unreliable);
the tip load-in transition.

---

## Open bench items (decision-relevant)

1. **clock-EIT two-photon coherence** — measure the 6.835 GHz two-photon linewidth (not the
   laser linewidth); sub-100-Hz → recommended scheme confirmed.
2. **In-fibre circular PER + field stability** — only needed if a field-sensitive RSC is
   pursued; decides stretched-RSC (32 dB / 4.3 mG) and dRSC (ellipticity uniformity).
3. **Tip load-in** — the free-space→guided interface (the 40 %-via-ferrule vs 96.5 %-test-fibre
   gap); shared, separable, affects all columns.

---

## Files (all verified, in project knowledge / outputs)

- cooling builders: `multilevel_ss.py`, `eit_common.py`, `clock_combined_solve.py`,
  `clock_clear_geometry.py`, `raman_sbc.py`, `gates.py`, `drsc_solve_A.py`,
  `m0_rsc.py` (v0.2.0, m=0 RSC + F′=0 polarizer), `f0_drsc.py` (degenerate F′=0, no-cool),
  `lattice_raman.py`
- noise: `rsc_noise.py`, `noise_dephasing.py`, `noise_polarization.py`, `verify_noise.py`
- audits feeding this brief: `audit_brief_v12_S1/S2/S3.md`, `audit_C_report.md`,
  `audit_brief_v12_noise.md`, `audit_brief_v12_RSC_noise.md` (Parts 1–2),
  `audit_brief_clockRSC_clear.md`, `audit_brief_clockRSC_parasitics.md`,
  `clock_parasitic_solve.py`, `rank2_verify.py`; v11: `EIT_brief_v11.md`, `v12_decision.md`
- ledger: `v12_plan.md`
