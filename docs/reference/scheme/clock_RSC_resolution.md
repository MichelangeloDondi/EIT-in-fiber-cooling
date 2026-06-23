# Clock-RSC floor: resolution of 0.45 vs 0.0137

**Verdict.** No contradiction — the two numbers answer different questions. The clock-pair
RSC floor is **≈ 0.45 (DISQUALIFIED)**, set by the rank-2 obstruction. `raman_sbc.py`'s
**0.0137** is the floor of an *idealized* standard-SBC model that omits the obstruction and is
therefore **not** the physical floor. **Paper T's claim stands and is unblocked.**

---

## The apparent disagreement
- `scheme_comparison.md`: clock-RSC floor ≈ **0.45** (rank-2 obstruction → off-resonant scatter
  beats cooling 11–23:1; T_z ≈ 18 µK, 69 % ground).
- `raman_sbc.solve('clock')`: **0.0137** (Nf=10).

## What `raman_sbc` actually models — verified this session
The clock-pair Raman is `H ⊃ −(OmR/2)(|hi⟩⟨lo|⊗D + h.c.)` with **OmR a free input** (default
0.02); the only dissipators are the **pump legs**. There is **no** rank-2 suppression of the
Δm=+2 coupling and **no** off-resonant spontaneous scatter from the Raman beams. Scanning OmR:

| OmR | n̄ | R_scatter (total) |
|---|---|---|
| 0.005 | 0.0134 | ~0 |
| 0.010 | 0.0134 | ~0 |
| 0.020 | 0.0137 | ~0.0001 |
| 0.040 | 0.0150 | ~0.0005 |

The floor is ~0.0134 with **essentially zero scatter** and barely moves with OmR. So 0.0137 =
"the clock-pair floor *if* the Δm=+2 Raman were a normal, strong, scatter-free Raman." It is an
**obstruction-free idealization**, not the clock-RSC floor.

## The obstruction is computed, not asserted — `audit_C_rank2.py`
1. **Rank-2 electronic null.** ⟨J=½‖T⁽²⁾‖J=½⟩ requires triangle(½,2,½) ⇒ need 0 ≤ 2 ≤ 1 ⇒
   **reduced matrix element = 0**. A pure electronic rank-2 (scalar Δm=2) two-photon operator
   vanishes in a J=½ ground manifold.
2. **m_I bookkeeping.** |2,0⟩ has m_I ∈ {−½,+½}; |2,2⟩ has m_I = {3/2} → **disjoint**. Two Δm_I=0
   dipole vertices cannot connect |2,m⟩ to |2,m+2⟩; only excited-state I·J exchange (Δm_I=±1 in
   5P) bridges them ⇒ amplitude **∝ Δ_HFS/Δ²**, so coherence-per-scatter is **detuning- and
   field-proof**.
3. **Mirror-ladder geometry.** A guided Δm=+2 cooling = absorb σ⁻ + emit σ⁺; the dark state has
   no σ⁺ partner, so it sees only σ⁻ and scatters ∝ Ω₋². The *rate* Ω_R=Ω₊Ω₋ is not bounded
   (you can crank the beams), but **one beam always lands on the dark state** — so cranking the
   rate cranks the depumping scatter in lockstep. What is bounded is the **coherence-per-scatter
   FoM (≈ 4)**, not the rate.

Re-verified three independent ways (product-basis amplitude → exact zero in the degenerate
limit; full-resolvent Δ-scaling; explicit Breit-Rabi + excited HFS+Zeeman diagonalization at
1.5 G → allowed 1/Δ coefficient = 1×10⁻⁴).

## Why the floor is ≈ 0.45
With FoM ≈ 4 and RSC's slow Lamb-Dicke cooling (W ≈ Ω₂ph/44), the off-resonant scatter beats
the cooling **11–23:1**, so the dark state depumps faster than it cools: floor lifts
0.00096 → **≈ 0.45**, B-independent. **Robust to ×3 in the scatter prefactor; needs ×170 to
recover** — i.e. *disqualified* regardless of FoM-level uncertainty. (The specific value 0.45 is
FoM-precision, ±factor; the **disqualification** is robust.)

## Why clock-EIT is not hit
EIT operates **near-detuned**, where the excited HFS is resolved and the Δm=+2 coherence is
fine, and its floor already includes scattering. It is RSC's **far-detuned** operation that
exposes the rank-2 limit; you cannot pull RSC near-resonant without enormous scatter.

---

## Implications
- **Paper T (rank-2-obstruction note) is UNBLOCKED.** It rests on the selection-rule null
  (`audit_C_rank2.py`, rigorous) + the coherence-per-scatter FoM (→ disqualified, robust to ×3).
  It does **not** rest on `raman_sbc`, which is the wrong tool (a standard-SBC engine that takes
  OmR as free and has no Raman-beam scatter).
- The earlier "0.45 NOT reproduced / OPEN" framing was a **category error**: it treated
  `raman_sbc` as the authority on a floor it structurally cannot compute. Retired.
- **To fix in the repo:**
  - SSOT: clock-RSC status OPEN → **DISQUALIFIED (rank-2)**; 0.0137 relabeled
    "obstruction-free idealization, not the physical floor." *(done)*
  - `fig_rsc_vs_eit.py`: the "≥0.0137 / 0.45 NOT reproduced" annotation is **wrong** — plot
    ≈0.45 as the clock-RSC floor (rank-2-limited) and label 0.0137 as the obstruction-free
    idealization. *(figure regen — follow-up)*
  - `scheme_comparison.md` is a **v12** doc; its clock-EIT floor (0.0064) is stale (v14: 0.0048
    dual / 0.0072 single). Mark historical or update.
- **Optional gold-standard** (not required for a theory note): one engine carrying the
  rank-2-suppressed coupling + the off-resonant σ⁻ scatter that reproduces ≈0.45 numerically.
  The analytic obstruction + FoM is sufficient and standard.
