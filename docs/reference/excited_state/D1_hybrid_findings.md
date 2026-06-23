# D1 / hybrid exploration — consolidated findings (pre-S5)

**⁸⁷Rb · kagome HCPCF · 1064 nm intra-fiber lattice · 2026-06-12**
Canonical synthesis of S1–S4 + External Audit A + main-thread independent re-verifications. Companion to the layered working log `D1_hybrid_plan.md` (v7). Input to S5 / brief v11. All claims graded **[V]** verified · **[I]** inference · **[O]** open.

*v2 (2026-06-12): added the inhomogeneous-broadening axis — a real performance argument for D1 that the floor-centric S1–S4 analysis missed. The verdict moves from "robustness-only" to "robustness + a real, repump-concentrated, isotope-tempered broadening advantage; still no floor gain."*

*v3 (2026-06-12): External Audit B (independent from-scratch rebuild incl. the full 16-level × 8-Fock solver) confirms the verdict and reproduces every number, and corrected two main-thread overstatements: (i) r is flat in polarization angle only at first order — a real ~10% second-order F′-mixing drift remains, so the cap(H2) sign is geometry-ambiguous and is now logged **floor-neutral** (not slightly-negative); (ii) the m-resolved repump kernel moves the floor <2% (traffic-weighted dressed ~0.0153), so it is NOT the floor-uncertainty driver — the excursion-compounding [O] is the sole remaining floor uncertainty. Physics now locked; S5 writes v11.*

## Question

Does moving the EIT cooling light from D2 (780 nm) to D1 (795 nm) — as a full pivot or a hybrid role — beat the settled v10 D2 design?

## System

⁸⁷Rb in a 1064 nm axial lattice inside a 48 µm kagome HCPCF. ν_z=2π×430 kHz, η₇₈₀=0.094, η₇₉₅=0.092. Two cooling schemes: **m′=2 stretched** (field-sensitive, |1,+1⟩/|2,+1⟩→|F′2,2⟩) and **m′=0 clock** (field-insensitive at magic B=3.2288 G, |1,−1⟩/|2,+1⟩→|F′2,0⟩). Lines: Γ/2π=6.07 (D2)/5.746 (D1); D1 5P₁/₂ has F′=1,2 only (no F′=3, no tensor). Coherent dark-state floor (GATE A) = **0.0072**, curvature-immune; the *realized* floor is anti-trap-limited.

## Organizing theorem (pruning) [V]

A cooling Λ needs Raman phase coherence between its two legs. Same-line legs are 6.8 GHz apart — one EOM bridges them (optical phase common-mode-rejected). Cross-line legs are 7.12 THz apart — comb-only, no EOM. **∴ the cooling Λ must live on one line; the other line takes only incoherent (repump) roles.** This kills cross-line schemes and leaves three candidates: **H1** (cool D2 / rep D1), **H2** (cool D1 / rep D2), **full-D1**.

## Verdict

**D1 buys a real performance advantage on inhomogeneous broadening — concentrated in the repump (~18 MHz of F′=1 tensor spread eliminated) — plus structural cleanliness, but no floor improvement.** The advantage is **isotope-tempered**: the ⁸⁷Rb F′=2 antisymmetry protects the cooling resonance (|F′2,0⟩ shifts only ~0.3 MHz vs ⁸⁵Rb's ~10 MHz), so this is *not* the first-order cooling-resonance catastrophe that drives the ⁸⁵Rb field to D1. Adoption is a **performance-and-cleanliness decision** (stronger than the earlier cost-only framing), gated on the PI fiber data — never justified by the floor.

| variant | verdict | basis |
|---|---|---|
| **full-D1** | **dead** | b_leak exactly line-independent (no leak advantage); F′=1 inversion makes its recycler 1.65× worse |
| **H2** (m′=0 clock, D1 cooling) | **cleanliness; floor-neutral** | floor-NEUTRAL vs D2-pure (Audit B: D2 cooling kernel 0.0179⊥–0.0198∥ brackets D1's 0.0202; cap-sign retired); no shared-manifold dead zone, no F′3 forbidden zone; removes the modest 1.5 MHz F′=2 broadening but leaves the dominant D2 repump broadening |
| **H1** (m′=2, D1 repump) | **cleanliness + repump broadening** | removes the D2-repump dead zone AND the ~18 MHz F′=1 repump tensor broadening; floor move < 0.003 (negligible). Putting the *repump* on D1 is what kills the dominant broadening — but on D1 the F′=1 inversion costs recycler traffic (see [O]) |

The "−35% D1 cooling advantage" carried through earlier drafts is **retracted** — it rested on a wrong cooling curvature (see erratum 2).

## Findings

### [V] — verified (re-derived independently in the main thread; ✦ = also confirmed by External Audit A)

- **b_leak is exactly line-independent** ✦: 1/3 (m′=2), 2/3 (m′=0), identical D1≡D2 — the F′2→F hyperfine branching is 1/2:1/2 on both lines (a 6j identity), m-routing pure CG. Full-D1 has no leak-metric opening.
- **v10's quoted b_s = 0.417/0.625 are a bug** ✦ — a CG-transposition in `antitrap_audit_code.py` PART B (double-counts the (2F+1)(2F′+1) degeneracy → spurious 3/8:5/8). Correct = 0.333/0.667. *Fixed* (corrected file produced; `part_D` and the sweep updated). The gated full solvers used the correct branchings, so GATE A and the dead zone are uncontaminated.
- **F′=1 branching inverts**: D2 5/6:1/6, D1 1/6:5/6 → the σ⁻ funnel-back to |1,−1⟩ collapses 5/12 (D2) → 1/12 (D1), worsening the full-D1 recycler.
- **The m′=0 recycler is repump-dominated**: per leak event N_cool≈3.0, N_rep≈7.0, ρ≈2.3 (D2-rep); full-D1 4.69/13.16/2.81. Triple-confirmed: S3 absorbing-Markov + main-thread rebuild + S4 QuTiP steady state.
- **The first-order H2 floor cap (0.032) is wrong**: repump traffic dilutes the cooling-kernel gain (realized heat ratio 0.85, not 0.65). Reviving even a 0.035 cap needs ρ→0.31 (7× drop) — structurally impossible.
- **v10's cooling curvature r=−2.435 (kernel 0.0311) is wrong** — it used the bare-electronic (a0−a2)/α_g form. Correct = **−1.63 (kernel 0.0180)**, pure scalar. Reason: F′=2 (and F′=0) are antisymmetric under I↔J for ⁸⁷Rb (I=J=3/2), so their **first-order** tensor polarizability vanishes at any polarization — a hyperfine-projection effect (Audit B confirmed the exact 6j zero {2 2 2; 3/2 3/2 3/2}=0), **not** geometry. *Audit B refinement*: r is flat in angle only at first order; a real ~10% second-order F′-mixing drift remains (r = −1.63 at E⊥B → −1.76 at E∥B, kernel 0.0179→0.0198), so the cap(H2) sign is geometry-ambiguous and is logged floor-NEUTRAL.
- **H2 cooling leg is floor-neutral**: corrected D2 cool kernel 0.0179 (E⊥B) – 0.0198 (E∥B) brackets D1 flat 0.0202, so across polarization H2 is neutral, not the earlier "slightly worse." Floor-irrelevant either way (cooling leg dark-protected). No floor gain from H2.
- **D2-pure ≈ H2 on the floor** (robust): both share the D2 repump, so the dominant leg cancels in the comparison even as it dominates the absolute number.
- **GATE A coherent floor = 0.0072**, reproduced bit-for-bit in the S4 solver with repumps off.
- **Hardware** ✦: 795 nm needs no tapered amplifier (in-fiber EIT runs at ~0.1–1 µW); the 6.8 GHz EOM ports to 795 (line-independent HFS, no F′3 forbidden zone). The in-fiber cooling precedent is **D1** (Wang radial ΛGM, Leong axial RSC); the only D2 ΛGM (Rensburg) is tweezers.
- **Inhomogeneous broadening — a real D1 advantage, isotope-tempered** (main-thread 5P₃/₂ diagonalization, full F′-mixing, Zeeman-subtracted, E⊥B). Tensor m-spread at full trap depth: **cooling F′=2** 1.5 MHz (⁸⁷Rb) vs 23.9 MHz (⁸⁵Rb) vs 0 (D1); **clock resonance |F′2,0⟩** 0.30 MHz (2× EIT) vs 10.1 MHz (67× EIT) vs 0; **repump F′=1** 18.2 MHz (⁸⁷Rb) vs 0 (D1). The ⁸⁷Rb cooling resonance is tensor-protected by the F′=2 antisymmetry (16–33× cleaner than ⁸⁵Rb), so the ⁸⁵Rb "D2 smears the cooling line" motivation is largely absent here; the real ⁸⁷Rb broadening lives in the **F′=1 repump** (symmetric → unprotected, 18 MHz), which D1 eliminates. Scales with sampled intensity → largest when warm → limits **capture / cooling rate / robustness**, not the floor. *Audit B reproduced all five numbers* and showed the 18 MHz F′=1 spread is **sweepable by a power-broadened incoherent repump** (the shifts are dynamic — motion-chirped through resonance at 2ν≈0.86 MHz, not static dead spots; worst-case rate penalty ~10–37× vs a demonstrated 16× floor-flat R window). So D1 repump is NOT forced; the cost stays capture/rate.

### [I] — inference (model-dependent)

- **Absolute m′=0 floor ≈ 0.003** (S4), repump-dominated, anti-trap a ~5% correction — *smaller* than the old 0.015–0.05 bracket (which was inflated by the −2.435 kernel + a leak_repump grid runaway). Rests on the two [O] items below.
- **The repump kernel is m-resolved (real), but floor-immaterial** — *Audit B closed this*. Bare first-order values |F′1,±1⟩ 0.0228 / |F′1,0⟩ 0.0102 temper at full depth to dressed {0.010, 0.020, 0.021}; the F′=1 traffic splits ≈0.48/0.48/0.04, so the traffic-weighted dressed kernel is **~0.0153 (geometry-insensitive)**, moving the floor 0.00293→0.00291 (<2%). The flat 0.0180 was adequate-but-lucky. My earlier "this is where the floor uncertainty lives" is **retracted** — the compounding [O] is the sole floor uncertainty.
- **Cost** (no-TA): H1 ~€3–6k, H2 ~€6–12k, below v10's €12–20k TA-inclusive figure — pending vendor quotes.

### [O] — open

- **The converged absolute m′=0 floor** — now reduces to a single question, time-resolved excursion compounding (the repump-kernel piece was closed by Audit B). Linear → ~0.003; superlinear → toward the old ~0.04–0.05. Needs quantum trajectories with a continuous position basis (Fock squeezer and finite grid both fail on the inverted potential). **The one genuine workstation item.**
- **PI fiber data** — kagome axial transmission + MFD @795, transverse transmission + PER @795, 780+795+1064 coexistence. Gates whether any 795 variant is buildable in *this* fiber.
- **Repump-line tradeoff surfaced by the broadening axis** — putting the F′=1 repump on **D1** eliminates the dominant ~18 MHz tensor broadening (better capture/rate) but incurs the F′=1-inversion penalty (funnel-back 5/12→1/12 → ~1.65× recycler traffic, worse floor). D2 repump is the reverse. Audit B: broadening alone does NOT break the tie (D2 repump survives via mid-spread parking, ~10× rate penalty inside the 16× R margin), so it stays a genuine S5 weighing item — D2 repump (favorable funnel-back, manageable broadening) vs D1 repump (no broadening, 1.65× traffic).
- **α₀(5S,1064) bookkeeping** — Audit B flagged that the broadening numbers used 687 while the kernels used 703. RESOLVED: use **703 consistently** in v11 (broadening figures scale ×0.977, immaterial); pin to a literature value (Safronova/Arora-class) if convenient.

## Erratum list for v11

1. b_s 0.417/0.625 → **0.333/0.667** (CG-transposition bug; fixed).
2. Cooling curvature −2.435/0.0311 → **−1.63/0.0180** — reason is F′=2 hyperfine tensor vanishing (projection, exact 6j zero), **not** geometry; note the ~10% second-order drift (0.0179⊥–0.0198∥) → cap(H2) is **floor-neutral**, not "slightly worse." Quote F′=1 repump kernels as full-depth dressed (~0.0153 traffic-weighted), not the bare 0.0228/0.0102. Use α₀(5S)=703 consistently.
3. §13: Leong 2020 used **D1 795 / 821 nm Raman / 3.036 GHz ⁸⁵Rb**, not "two 780 beams at 6.835 GHz on the same fibered source."
4. §9/§13: tag the Leong/Wang precedent lines (Wang in-fiber gray molasses is **D1**).
5. The "b_leak depth-independent" phrasing over-reaches for D2 (sub-percent F′-admixture); exact only for D1.
6. **Add the inhomogeneous-broadening axis** as a real argument *for* D1 (repump-concentrated ~18 MHz, isotope-tempered) — the floor-centric v10/early drafts treated D1 as floor-relevant only; the genuine performance case is broadening, not floor.

## Clock-scheme leg assignment (control↔probe) — distinct OPEN question

*Added 2026-06-19 (after auditor round 2). A different question from the D1-vs-D2 verdict above, and it does not reopen it: within the **m′=0 clock** scheme on D2, should the control leg stay on |2,+1⟩ (status quo, inherited from the stretched scheme) or swap to |1,−1⟩? Headline was overturned the same way round 1 was — a clean diffusion/branching argument that ignored the repump topology, which is the actual deciding factor.*

**[V] The |F′2,0⟩ dark-leg branching is REVERSED vs |F′2,2⟩** — exact CG/6j, reproduced in-repo by `src/clock_branching_check.py` and validated against the stretched 0.75/0.25 anchor of `tagged_solver.py`:

| excited state | → dark/probe leg | → \|2,+1⟩ control | renorm probe:control |
|---|---|---|---|
| \|F′2,2⟩ stretched | \|1,+1⟩  1/2 | 1/6 | **3/4 : 1/4** |
| \|F′2,0⟩ clock | \|1,−1⟩  1/12 | 1/4 | **1/4 : 3/4** |

Raw clock decays: |1,−1⟩ 1/12, |1,0⟩ 1/3, |1,+1⟩ 1/12, |2,−1⟩ 1/4, |2,+1⟩ 1/4 (|2,0⟩ CG-forbidden); F′=2→F hyperfine split 1/2:1/2 both (consistent with the b_leak 2/3 m′=0 entry above). The dark state sits ~94% on the probe leg, so the clock scheme **routes 3/4 of dark-leg decay onto the bright/control |2,+1⟩ leg → diffuses** (the stretched scheme recycles 3/4 onto the probe leg). The same physical assignment as stretched, but the branching flipped under it ⇒ the current clock leg assignment is **diffusion-suboptimal**.

**[F] "verdict inverts / swap wins" is FALSIFIED** (auditor round 2; external `clock_combined_solve.py`, not in this repo — floors in-repo-unverified). The isolated diffusion lever is real and large — clean closed-Λ 0.0072→**0.0022** (3.29×, bigger than the stretched 2.5×) — **but the naive swap with the current option-A repumps is 3.3× WORSE** (0.0061→**0.0204**, at every δ₂). Cause: the swap parks ~92% in F=2 and the existing rep2 (σ+ F=2→F′1) mis-clears the F=2-dark spectator load → ~2.3% F=2 leak. Diffusion is **necessary, not sufficient** — the repump topology decides, as in round 1, now biting the other way.

**[V] Decision RESOLVED — swap REJECTED, A holds ~3.8×.** Deciding run `clk2.py` (= `clock_combined_solve.py` + surgical hooks, audited byte-identical; both now in-repo): config A (dark |1,−1⟩, F=1 edge) floor **0.0048 hard-converged** (Nf=6–10 flat, frame-conflict 0.0); config B (swap, dark |2,+1⟩, F=2 interior) **≈0.018 best-bounded, diverges with Nf** at matched OmR=0.25 → A favored ~3.8×. Cause: F=2-interior dark leg forces rep2=A (σ+ F=2→F′1, the unique protecting topology), which cannot clear |2,+2⟩ → near-flat Fock heating tail (P(n+1)/P(n) → 0.97 at Nf=16). Isolated diffusion lever (0.0072→0.0022, 3.29×) real but dominated by the repump penalty — the lesson now earned four times. Magic-B survives (pair |1,−1⟩↔|2,+1⟩ unchanged). EOM-Raman |2,+2⟩ clearer also rejected (window empty: ideal clearer floors B at ≈0.005 ≫ A=0.0048; mandatory scatter depletes the dark state ~10×). F′=3 sub-dominant (~1.5 kHz marginal relief on A, cannot flip verdict). Convention: η=0.094 symmetric; relative 3.8× is convention-robust. **Do not swap.** → CLAIMS LS2 [V].

## Process state

- **Sessions**: S1 ✓ · S2 ✓ · S3 ✓ · S4 ✓ · **S5 pending** (writes v11 — physics now locked).
- **Audits**: A ✓ (brief #1) · **B ✓** (brief #3, strong pass — verdict confirmed, two main-thread overstatements corrected, 5 bookkeeping items resolved) · C pending (S5 → PI).
- **PI**: not contacted. The entire D1 arc is internal until v11.

## Next

1. **External Audit B** on brief #3 — three targets: (a) the F′=2 tensor-vanishing vs Steck / the {3/2 2 3/2; 2 3/2 2} 6j; (b) that S4's E⊥B geometry mechanism is wrong (r flat in polarization angle); (c) the missed m-resolved geometry-dependent F′=1 repump kernel (the dominant leg).
2. **S5** writes v11: the D1 section (robustness-led verdict), the erratum list above, and an honest absolute-floor statement (two open items, one a workstation trajectory calculation).
3. Optional laptop refinement before S5: combine the F′=1 m-resolved kernels with the S3 repump-visit distribution for a sharper absolute floor in the correct geometry (does not close the compounding question).
