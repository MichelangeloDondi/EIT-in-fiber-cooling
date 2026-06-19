# Clock-scheme leg assignment: the |F′2,0⟩ branching reverses the diffusion lever — but NOT the verdict

**Status:** [O] OPEN. The branching reversal and the isolated diffusion lever are **verified**
(independently reproduced by an external auditor); the earlier headline "the verdict inverts,
swap favored, high-confidence direction" is **FALSIFIED** — the naive swap (current repumps)
is 3.3× *worse* in the realizable system. The decision turns on a repump re-pointing rebuild
and is unresolved. Pending the **deciding run** (below). 2026-06-19, rev. after auditor round 2.

> **Calibration note.** This finding's headline was overturned the same way round 1 was: a
> clean diffusion/branching argument that ignored the repump topology, which is the actual
> deciding factor. The diffusion argument is *necessary, not sufficient.* No leg-assignment
> direction should be stated without the repumped solve.

**Origin.** Audit of the control↔probe leg-swap brief. The brief cited *stretched*-scheme
solvers while describing the *clock* scheme; an external auditor flagged a state-label
mismatch (|1,−1⟩ vs |1,+1⟩) which, on investigation, is a full scheme-conflation. This
note records the corrected finding and supersedes the brief's "A holds, don't swap."

## Config we run (confirmed)
m′=0 magic-clock Λ, **single-ended**: |1,−1⟩ σ+ (probe, retro) / |2,+1⟩ σ− (control,
forward) → |F′2,0⟩; freq-tagged retro+λ/4. Solver: `clock_combined_solve.py`
(:5 *"cooling Lambda : |2,+1> sigma- / |1,-1> sigma+ -> |F'2,0>"*).

## Scheme split — provenance (do not repeat the conflation)
- **m′=2 STRETCHED** (|1,+1⟩/|2,+1⟩→|F′2,2⟩): `verify_tagged_solve.py`
  (:7 *"g1=|1,+1>, g2=|2,+1>, e2=|F'2,2>, e3=|F'3,2>"*), `dm2_coherent_solve.py`,
  `tagged_operating_point.py`, `combined_solve.py`. Floors **0.0034** (swapped) /
  **0.0085** (unswapped), 2.51× — **STRETCHED-ONLY; do not apply to the clock scheme.**
  `verify`'s *"THE ADOPTED SCHEME"* comment is **stale** (v9-era, `[brief Sec. 9A.6]`).
- **m′=0 CLOCK** (|1,−1⟩/|2,+1⟩→|F′2,0⟩): `clock_combined_solve.py`,
  `clock_combined_H2.py`, `clock_lowB_S3.py`, `clock_parasitic_solve.py`. The adopted
  (v14) scheme.

## The finding [V computation / I consequence]
The |F′2,0⟩ dark-leg branching is **reversed** vs |F′2,2⟩ (exact CG, `clock_branching_check.py`;
validated — |F′2,2⟩ reproduces `verify`:32's 0.75/0.25):

| excited state | → F=1 dark leg | → \|2,+1⟩ | raw spectator/leak |
|---|---|---|---|
| \|F′2,2⟩ stretched | \|1,+1⟩ **0.75** | 0.25 | 0.333 (→\|2,+2⟩) |
| \|F′2,0⟩ clock | \|1,−1⟩ **0.25** | **0.75** | 0.667 (→\|1,0⟩,\|2,−1⟩,\|1,+1⟩) |

(renormalized over the two dark legs; raw clock: |1,−1⟩ 0.083, |2,+1⟩ 0.25, |1,0⟩ 0.333,
|2,−1⟩ 0.25, |1,+1⟩ 0.083.)

The dark state sits on the **probe** leg (|D⟩ ∝ Ω_c|g_probe⟩, ~94%), so decays landing on
the probe leg recycle (good) and decays on the control/bright leg diffuse (floor-raising).
- **Stretched:** probe on F=1 (0.75 decay) → recycles → optimal (the adopted choice is correct *there*).
- **Clock (current):** the *same* physical assignment was inherited (control |2,+1⟩, dark on
  F=1), **but the branching flipped** — |1,−1⟩ collects only 0.25; **3/4 of dark-leg decays
  land on |2,+1⟩ = bright/control → diffuse out.** The current clock leg assignment is
  **diffusion-SUBOPTIMAL.**

## Consequence: the DIFFUSION LEVER flips (verified, large) — but the verdict does NOT invert
The isolated diffusion lever favors the swap, **more strongly than first claimed** — but the
realizable swap is net harmful, and the decision is open. Auditor-run numbers (independent):

| configuration | floor | vs current |
|---|---|---|
| current (control \|2,+1⟩, dark \|1,−1⟩), full option-A repumps, δ₂-opt | **0.0061** | — |
| swapped, **clean closed-Λ** (repumps off, decays recycled, GATE A) | **0.0022** | 3.29× better |
| swapped, **full** option-A repumps **unchanged**, δ₂-opt | **0.0204** | **3.3× worse** |

- **Diffusion lever (verified, isolated):** clean closed-Λ 0.0072 → 0.0022 = **3.29×** — bigger
  than the stretched 2.5×. (The earlier "~1.5× diluted" reasoning was wrong: the 2/3 spectators
  *recycle* onto the two legs in steady state, so the lever acts on the whole population, not
  just the 1/3 that lands directly.)
- **But the naive swap is net harmful (verified):** full system 0.0061 → 0.0204 = **3.3× worse**,
  at every δ₂ (both optimal at δ₂=0 — not a servo artifact). **Cause:** the dark state forms fine
  (swapped dark |2,+1⟩ 91.9%), but the swap parks ~92% of population in F=2, and the existing F=2
  repump (rep2-A σ+ F=2→F′1) mis-clears the F=2-dark spectator load → ~2.3% leaks into
  |2,+2⟩/|2,0⟩/|2,−1⟩ (vs ~0.1% current) → extra scatter triples the floor.

**So the verdict does NOT invert.** The diffusion gain is real and large, but it is *necessary,
not sufficient* — the repump topology decides, exactly as in round 1, now biting in the opposite
direction. Neither "A holds" nor "swap wins" is established.

**Reframe.** Two competing levers: **diffusion** (favors F=2-dark = swap, 3.29× isolated) vs
**repump clearability** (favors F=1-dark = status quo). Structural hypothesis (for the deciding
run to test, *not* asserted): F=1 has 3 sublevels with the dark leg at the *edge*; F=2 has 5 with
the dark leg in the *interior*, so clearing F=2 spectators without disturbing |2,+1⟩ may be
intrinsically harder — which could make the current config correct for a *clearability* reason
the branding never named.

## Open [O] — the real state of the question
- **Decision bracketed, unresolved.** True swapped floor ∈ [0.0022 (clean, optimistic
  instant-recycle, zero repump cost), 0.0204 (full, current repumps untuned)] vs 0.0061 current.
  Only the swapped solve **with repumps re-pointed and re-optimized for the F=2-dark topology**
  resolves it.
- **F′=3 (the "second mechanism") is unquantified** at the clock detuning Dc=80; round-1 found
  it sub-dominant in the stretched case. Measure before treating it as co-equal with diffusion.
- **Single-ended feasibility** (launch σ+ forward; check leak/polarization with Prevedelli)
  remains, but is now secondary to the repump-re-pointing question above.

## ACTION — the deciding run (queued behind regression discovery + reabsorption-brief)
**The single number that settles swap-vs-stay:** swapped legs **+ repumps re-chosen for
F=2-dark** (lines/polarizations and D_rep1/D_rep2/Ω_rep re-optimized) **+ δ₂ re-servoed**, in
`clock_combined_solve` (m′=0, single-ended). Does it recover the clean-Λ 3.29× (→ ~0.002–0.003)
or stay near 0.0204?
1. The deciding floor (above) vs the current 0.0061.
2. Which channel must re-pointing fix? The |2,+2⟩/|2,0⟩ F=2-leak is the verified culprit at
   0.0204 — does a re-pointed rep2 (different line/detuning) clear it without touching the
   |2,+1⟩ dark leg?
3. F′=3 increment at Dc=80 for the current config (toggle its coupling) — material or
   sub-dominant as in stretched?
4. Confirm magic-B field-insensitivity survives the swap *in the solver* (dark pair unchanged,
   so expected — but verify, don't infer from g·m alone).

The repump re-pointing is the risky part (edge-rule re-assignment is where an error hides) — do
not hack the existing repump flags; rebuild deliberately. Per R2: the deciding floor becomes a
tracked `CLAIMS` entry; the branching numbers are reproduced by `clock_branching_check.py`.

## Disposition
- Branching reversal + diffusion-lever-flips: **verified** (auditor reproduced both).
- Headline "verdict inverts / swap wins": **falsified** — naive swap 3.3× worse; decision open.
- Earlier auditor reply (config + concessions + scheme correction) stands; its "swap favored,
  high confidence" claim is **superseded by this revision**.
- Leg-swap brief: retire its stretched numbers and *both* directional claims ("A holds" and
  "swap wins"). This note is the clock-scheme record; the deciding run is the only resolver.
