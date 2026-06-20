# Resolution of the m′=0 floor gap (realized ≈0.0028 vs GATE A 0.0072)

*Investigation note — supports the v11 §12.2 fix. Both numbers re-run from `clock_combined_H2.py` (the single solver that produces both); no reduced engine involved.*

## The question

v11 §12.2 (and §1, §8) states the realized m′=0 floor ≈0.003 sits **below** the coherent GATE A floor 0.0072, and explains it as “different reductions — the reduced engine carries a lower recoil baseline.” That explanation is **wrong**: GATE A (`clean_lambda=True`) and the realized floor (full 8-ground, rate repumps) are the **same full solver** in two modes. A realized floor below the coherent floor, with a false explanation, is the one unforced inconsistency a rigorist pounces on.

## The finding — two different recycler closures, not one number at two fidelities

|                                                                         |excited pop on cooling F′2|excited pop on repump F′1|total P_e|⟨n⟩ (Nf-converged)|
|-------------------------------------------------------------------------|--------------------------|-------------------------|---------|------------------|
|**GATE A** (clean_lambda, reps off, **all decay redirected to the legs**)|1.97×10⁻⁵                 |0                        |1.97×10⁻⁵|**0.00718**       |
|**Realized** D2-pure (reps on, real leak, R=2)                           |8.52×10⁻⁶                 |1.26×10⁻⁵                |2.11×10⁻⁵|**0.00276**       |
|**Realized** H2 (cool D1)                                                |—                         |—                        |—        |**0.00260**       |

Three facts, all from the runs:

1. **Total excited population is the same** (1.97 vs 2.11 ×10⁻⁵). The realized system is **not** scattering less overall — it scatters on **two** transitions instead of one. GATE A’s redirect funnels 100 % of recycling traffic back onto the cooling transition (F′2); the realized recycler routes the 2/3 leak through the incoherent F′1 repump, so the excited population **splits ~40/60** between cooling (F′2) and repump (F′1).
1. **The motional floor tracks the cooling-transition population.** ⟨n⟩ ratio (GATE A / realized) = **2.60**; P_e(F′2) ratio = **2.31**. The realized recycler carries ~2.3× less population on the cooling transition, and the floor — set by recoil deposited via cooling-transition scatter — falls ~2.3× with it.
1. **GATE A is NOT the instant-repump limit.** Repump-rate sweep (D2-pure, real leak, no redirect):
   
   |R  |0.25   |0.5    |1      |2      |4      |8      |20     |80     |400    |
   |---|-------|-------|-------|-------|-------|-------|-------|-------|-------|
   |⟨n⟩|0.00296|0.00277|0.00271|0.00276|0.00285|0.00293|0.00300|0.00302|0.00303|
   
   The floor is **flat at 0.0028–0.0030 across R ∈ [0.25, 400]**, with a shallow optimum near R≈1. Even instant repump (R→∞) gives **0.0030, never 0.0072**. So GATE A’s redirect is a genuinely different (cooling-transition-overloaded) construction — a conservative **upper bound** on the coherent floor, not a target the realized system misses. Under-repumping (R<1) strands leak population (P_e(F′2) rises); over-repumping (R≫1) adds repump recoil (P_e(F′1) rises) — both lift ⟨n⟩ slightly; R≈1–2 is optimal.

## Physical anchor — emission recoil η_em² = η²/3

|quantity                     |value  |/ η_em² |
|-----------------------------|-------|--------|
|η_em²(D2) = 0.094²/3         |0.00295|1.00    |
|η_em²(D1) = 0.0919²/3        |0.00282|1.00    |
|realized D2-pure 0.00276     |       |**0.94**|
|realized H2 0.00260          |       |**0.92**|
|GATE A 0.00718               |       |**2.44**|
|§7.1 single-Λ baseline 0.0068|       |**2.31**|

The realized floor sits at **≈0.93 η_em²** for *both* lines — the single-emission-recoil scale, where a well-behaved sideband-cooling floor belongs (and a second, independent reason the D1/D2 floor is neutral: η_em is nearly line-equal). GATE A and §7.1’s “recoil baseline that no detuning beats” both sit at **~2.3–2.4 η_em²** — they are the **single-Λ recoil reference**, inflated relative to η_em² because the redirect re-injects every emission recoil back onto the cooling-transition motional state. The realized 8-ground recycler lets 2/3 of those recoils land on the repump path, so the cooling-Λ equilibrates near the bare single-emission scale.

**This reconciles §7.1 and §12.2:** 0.0068 is the *single-Λ* floor; 0.0028 is the *multi-level recycler* floor. The “no detuning beats 0.0068” claim is about Δ within one Λ — not violated by a structurally different 8-ground system whose recycling redistributes the recoil-depositing scatter.

## Corrected text for v11 §12.2 (replaces the parenthetical after “GATE A = 0.0072 [V]”)

> The underlying coherent cooling-Λ reference is GATE A = 0.0072 **[V]**. The realized ≈0.003 sits below it **not** because of any reduced-engine baseline — both are the same full solver, Nf-converged — but because the two are different recycler **closures**. GATE A redirects all leaked decay back to the cooling Λ, loading 100 % of the steady-state excited population (~2×10⁻⁵) onto the cooling transition: a single-Λ recoil reference, ≈2.4 η_em². The realized 8-ground recycler instead routes the 2/3 leak through the incoherent F′=1 repump, so the excited population splits ~40/60 between the cooling (P_e(F′2)=8.5×10⁻⁶) and repump (P_e(F′1)=1.3×10⁻⁵) transitions. The motional floor scales with the cooling-transition recoil, so the realized floor falls ~2.3× to ≈0.93 η_em² (0.00276 D2-pure, 0.00260 H2 — at the single-emission-recoil scale). GATE A is therefore a conservative **upper bound** on the coherent floor, not a target the realized system fails to meet: a repump-rate sweep holds the floor flat at 0.0028–0.0030 across R∈[0.25,400], so even instant recycling never climbs to 0.0072.

Optional one-line touch-up to §7.1 (so the sub-baseline number never reads as contradictory): after “the recoil baseline ~0.0068 that no detuning beats,” add “— this is the *single-Λ* reference (≈2.3 η_em²); the m′=0 8-ground recycler sits below it (≈0.93 η_em², §12.2) because recycling redistributes the recoil-depositing scatter off the cooling transition.”

## Verdict impact: NONE

Floor-neutral stands and is reinforced — D2-pure 0.00276 ≈ H2 0.00260, both the same realized closure, both ≈0.93 η_em². The D1 evaluation, the leakage axis, and the broadening axis are all untouched. This fix corrects an *explanation*, not a number.

## The one question to be ready for (PI)

“How does the recycler cool below the single-Λ recoil baseline?” Answer: GATE A’s idealized redirect re-injects every emission recoil onto the cooling-transition motional state (≈2.4 η_em²); the realized recycler routes 2/3 of leaked population through the F′1 repump, so that recoil lands on the repump path and the cooling-Λ equilibrates near 1 η_em². It is a population-routing effect, fully converged, and both numbers agree the m′=0 floor is well below 0.01. *(If one wanted GATE A and the realized number to coincide, the redirect would have to deposit the leaked-decay recoil on a separate repump mode rather than back on the cooling-Λ mode — i.e. model the repump explicitly, which is exactly the realized run.)*