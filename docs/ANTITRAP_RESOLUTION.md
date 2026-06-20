# Anti-trap floor — RESOLUTION (converged after two-instance cross-audit)

Supersedes the Fock-basis "~0.7" (C5) AND this note's own earlier "≈0.05 fixed" and "≳0.05
runaway-prone" framings. The runnable analysis is **`antitrap_kernel_grid.py`**. This is the
converged answer after an adversarial cross-audit that found two artifacts and two opposite over-reads,
each caught and verified.

---

## Converged verdict

1. **The 0.7 was a Fock squeezer-truncation artifact** — settled.
2. **The cooling leg is clean** — anti-trap negligible *during EIT cooling* (grid ⟨n⟩=0.0087,
   grid-independent; the dark state pins P_e ≈ 4×10⁻⁵).
3. **The m′=0 floor is repump-gated, bracketed ~0.01–0.05 — pinned in range, NOT runaway.** The
   exposure is the repump/leakage path; the lever is excited-repump **dwell** P_e_rep.

## The two artifacts (both settled, in both bases)

- **Boundary/truncation in ⟨n⟩_full.** The inverted excited oscillator forced into a finite shared
  basis piles a tiny population at the boundary, inflating ⟨n⟩_full as the basis grows — Fock cutoff
  *and* position-grid edge alike (⟨n⟩_full grows with Nf and with Ng). It is **not** a physical
  unbounded floor.
- **Low-n squeezer leakage in the Fock bulk.** The (ν/4)(r−1)(a²+a†²) term leaks P₀→P₂→P₄
  *cutoff-stably*, so cutoff-stability does NOT certify a Fock bulk. Signature: non-geometric low-n
  shape (a flat P₂≈P₃≈P₄ shelf) instead of the geometric decay a faithful (grid) basis gives
  (P₀,P₁,P₂,P₃ = 0.994, 0.0041, 0.0011, 0.0003, ratios ~0.27).

## How the floor is read (the bracket logic)

Dropping the squeezer removes **two** things — the truncation leakage (artifact) *and* genuine
squeezing heating (physical; the inverted potential really squeezes). The grid proves the split:
faithful (grid) bulk 0.0095 sits **above** no-squeezer bulk 0.0069 → ~0.003 is real squeezing heat.
So:

    no-squeezer bulk  ≤  faithful floor  ≤  contaminated-Fock bulk

i.e. no-squeezer is a *lower* bracket, contaminated-Fock an *upper* bracket, faithful in between
(≈ the position-grid value where the basis is large enough).

## Per-excursion kernel (closed form, grid-validated — finite, well-behaved)

⟨n⟩_exc = (s+1/s)²ω_e²/(2(Γ²−4ω_e²)), s=√|r|, ω_e=νs. Values 0.031 (m′=0 cool), 0.018 (F′=1 rep),
0.009 (m′=2 cool); bare recoil 0.012. Convergence edge (2ω_e→Γ) is at r≈−49, far from the physical
−2.435 — the single excursion is finite; the floor question is about *how many/how long*, not the
kernel.

## m′=2 vs m′=0 (converged)

- **m′=2 (r=−0.834, bs=0.417):** faithful bulk **~0.011–0.016**, basis-stable; corroborates the prior
  ~0.019. Fine — weak inversion × modest leakage × low dwell.
- **m′=0 (r=−2.435, bs=0.625):** repump-gated by P_e_rep, **bracketed ~0.01–0.05**:
  - low-dwell repump (P_e_rep ~ 4×10⁻⁵): faithful bulk **~0.01** (grid = Fock, confirmed).
  - high-dwell repump (P_e_rep ~ 3.5×10⁻⁴, a structural routing bottleneck): faithful bulk
    **~0.03–0.05** (no-squeezer 0.026 ≤ faithful ≤ contaminated 0.053).
  Which end you hit is a **repump-design output**, set by how often/long the atom must traverse the
  anti-trapped 5P on the recycling path. Not runaway, not a single number.

The lever (confirmed, basis-independent): the no-squeezer lower brackets differ ~4× across the two
repump models (0.007 low-dwell vs 0.026 high-dwell) — that is physical dwell, not representation.
**Engineer the repump to minimise P_e_rep** (few-photon, fast return to the dark pair, no Rabi-holding
on the inverted state) → the ~0.01 end. **RSC-to-|F=2,m=0⟩ forces this structurally** (the single
low-dwell excursion confined to one optimisable OP step) — the robust route to the low end.

## What is still open (and what it needs)

The *converged point-number* for a chosen repump needs a **faithful** (position-grid or two-mode
Franck–Condon) steady state of the **actual** repump scheme — where the squeezer is represented
exactly and cannot leak into low-n. The 5-internal-state × spatial-grid dense Liouvillian **OOMs** in
these environments (direct solve dies past Ng≈64); it is a workstation / sparse-iterative-solver run.
Until then m′=0 is honestly a **range ~0.01–0.05**, with the end set by the real F′=1 repump routing.

## Re: D1

D1 is ruled out independently (binding constraints line-independent; decision gated by ground-state
T₂; computed α₀(5P₁/₂,1064) ≈ −1254 a.u., every-leg r=−1.78, worse than D2's −1.63). Do not model D1.

---

## Bottom line for the simulation

Two D2-EIT branches, selected by in-fiber spin-echo **T₂**:

- **T₂ good → m′=2**, floor ~0.015–0.02, anti-trap negligible.
- **T₂ poor → m′=0**, field-insensitive; anti-trap floor **repump-gated ~0.01–0.05** (pinned in
  range, not runaway). With an engineered low-dwell repump it reaches ~0.01; RSC-to-|F=2,m=0⟩ is the
  structural route to that end.

The deciding input is still experimental (T₂). The anti-trap is a **repump-design cost on the
field-insensitive branch, bounded ~0.01–0.05** — not a runaway, and not a fixed 0.05.
