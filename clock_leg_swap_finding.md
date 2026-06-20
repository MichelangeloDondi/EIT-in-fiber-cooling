# Clock-scheme leg assignment: DECIDING RUN — the swap is rejected; A holds

**Status:** [V] resolved — solver-verified. The full repumped + re-pointed two-leg
optimization has been run. **It reverses this note's own earlier "swap is favored" call.**
2026-06-19.

> ⚠️ This note previously concluded (from a diffusion + branching argument) that the
> leg-swap was favored — "possibly ~1.5× diluted, the solver decides." **The solver decided
> against it.** The earlier argument under-weighted repump topology — exactly the failure
> mode flagged as having mis-called this question before. The branching numbers below remain
> [V]; the *consequence* drawn from them ("swap favored") was wrong. Verdict: **do not swap.**

## System & operating point [V]
Rb-87 D2, m′=0 magic-clock Λ, single-ended retro. Dark resonance = clock pair
|1,−1⟩↔|2,+1⟩ in **both** configs. Solver `clock_combined_solve.py`
(:5 *"cooling Lambda : |2,+1> sigma- / |1,-1> sigma+ -> |F'2,0>"*). Point: B=1.5 G,
Dc=80, Om_r=1.5, axial ν_z=0.430, Γ=6.07 (:44 *"GAMMA,NU,ETA=6.07,0.430,0.094"*),
η=0.094 symmetric (no standing-wave enhancement).
- **Config A (current):** control = forward σ− strong on |2,+1⟩; probe = retro σ+ weak on
  |1,−1⟩. Dark on |1,−1⟩ (F=1, **edge** sublevel).
- **Config B (swap):** control = forward σ+ strong on |1,−1⟩; probe = retro σ− weak on
  |2,+1⟩. Dark on |2,+1⟩ (F=2, **interior** sublevel). Forward stays strong/+k, retro
  weak/−k; only launched helicity flips.

## DECIDING-RUN RESULT [V]
Steady-state Lindblad floor (axial), each config at its **own** repump optimum:

| config | dark leg | best ⟨n⟩ | convergence | optimum |
|---|---|---|---|---|
| **A** | \|1,−1⟩ (F=1 edge) | **0.0048** | hard-converged Nf=6→16 (flat) | Drep1=20, Drep2=5, δ₂=0, OmR=0.25 |
| **B** | \|2,+1⟩ (F=2 interior) | **≈0.018** (best *bounded*) | only bounded for OmR≳0.4; **diverges with Nf** at matched OmR=0.25 | rep2=A forced, Drep2≈20, δ₂=0 |

**Net: A is ~3.8× better, and B has a convergence pathology A does not.** [V]

### Why B loses — repump clearability [V]
The F=2-interior dark leg |2,+1⟩ admits **exactly one** protecting F=2 repump topology
(rep2=A, σ+ F2→F′1). Sanitized topology scan (config B, Nf=6, valid ⟨n⟩ only): rep2=A
(σ+ F2→F′1) **0.018 — only survivor**; C (π F2→F′2) 0.19; spF2 (σ+ F2→F′2) 0.51; smF1
(σ− F2→F′1) 2.29 (heats); piF1 and smF2 → ∞ (population traps). σ+ F2→F′1 spans only m≤0,
so it protects |2,+1⟩ **and cannot reach |2,+2⟩**. Every topology that *can* reach |2,+2⟩
is m-adjacent to the dark leg and drives |2,+1⟩→|F′,0/±1⟩ — heating or trapping. The
unclearable |2,+2⟩ (+|2,0⟩,|2,−1⟩) leak injects axial heating EIT cannot remove: the
steady-state Fock tail is **near-flat** (P(n+1)/P(n) → 0.97 at Nf=16) → ⟨n⟩ grows
~linearly with truncation. Config A's tail is heavily damped (ratios 0.08–0.19; P(n) falls
6 decades by n=8) → robust floor. **frame-conflict = 0.00 for both** ⇒ B's divergence is
physics, not a rotating-frame artifact (re-verification of the overturning result).

A frequency-resolved |2,+2⟩ drain (σ− F2→F′2 on |2,+2⟩→|F′2,+1⟩, scanned over detuning and
Rabi) made B **worse** (0.027 > 0.018): at B=1.5 G the ~1 MHz Zeeman gap is unresolved
against Γ=6 MHz, so the drain spills onto the dark leg. **No re-pointing recovers the
clean-Λ floor.**

### Fair comparison [V]
At matched OmR=0.25 (each own repump optimum): A=0.0048, B=0.0173 → 3.6×. Across OmR
0.15–0.35 A dominates B at every point. A keeps dropping toward low OmR (0.0021 at 0.15)
but that is the degenerate weak-probe / vanishing-cooling-rate limit; at physical OmR the
gap holds. B's *bounded* optimum (OmR≈0.4) ≈ 0.0187 → A better ~3.9×.

### F′=3 increment [I/O] (solver omits F′=3; analytic)
F′=3 couples to F=2 only. Config A's strong control sits on F=2 → off-resonant F′=3 scatter
R₃ ≈ (Γ/2)(Ω_c/2)²/Δ₃² with Ω_c≈11.4, Δ₃≈Dc+267≈347 ⇒ **≈1.6 kHz**. Config B's strong
control sits on F=1 → immune; only its weak probe sees F′=3, ≈0.1 kHz. So F′=3, if modeled,
**marginally favors the swap** (~1.5 kHz relief on A) — but to flip the verdict it would have
to raise A's floor ~3.8× (0.0048→~0.018), implausible for a ~kHz parasitic. **Sub-dominant;
does not overturn A.** Exact size needs the F′=3 build (separate).

### magic-B survives the swap [V]
Clock pair |1,−1⟩↔|2,+1⟩ is identical in both configs (swap changes only which leg is
strong/weak). Solver Breit-Rabi energies give df/dB=0 at **B=3.2288 G**, config-independent.
Operating B=1.5 G has df/dB≈−1.49 kHz/G in both. **Preserved.**

### GATE 1 — σ+-forward polarization (apparatus) [I] — MOOT
Whether launching σ+ forward keeps circular purity through the fibre is an apparatus
question the ideal-polarization solver cannot answer. **Moot for the decision:** B loses on
the floor regardless, so this gate no longer needs asking for the leg-assignment choice.

## Caveats
- **Absolute floors provisional** pending `cloud_floor_spec.md` revision; the **relative**
  A-vs-B comparison is robust (same solver, point, η). The deciding-run absolutes are on the
  **η=0.094 symmetric** convention, **not** the headline retro **η=0.187 + tag** — so
  **A=0.0048 here is NOT a new single-end floor**; the pinned headline ~0.0077 stands. The
  verdict is the convention-robust **relative 3.8×**.
- A larger η worsens B's heating tail, so the symmetric-η reading is **conservative toward A**.
- Solver omits F′=3 (RWA) — see above.

## Disposition
- This note's earlier "swap favored" conclusion is **withdrawn.** Verdict: **A holds — do
  not swap.** Reason is solver-verified (repump clearability + Fock convergence), distinct
  from the original stretched-scheme reasoning.
- **The EOM-Raman |2,+2⟩ clearer rescue was also tested and rejected** (separate audit,
  same engine): an ideal recoil-free clearer of arbitrary strength still floors B at ≈0.005
  (the repump cycle, not the leak, is the limiter), and the clearer's mandatory single-photon
  scatter depletes the 93.5%-occupied dark state (0.0065→0.062, ~10×, via population
  redistribution not recoil). Window empty — A holds against the Raman clearer too.
- Branching numbers (below) stand, reproduced by `clock_branching_check.py` (gate-checked
  against `verify_tagged_solve.py`:32 → 0.75/0.25 stretched). The resolution overturns the
  *verdict*, not the branching reversal.
- Reproduction: `clk2.py` = `clock_combined_solve.py` with surgical `swap` / `rep2mode` /
  `rep2_extra` / `want_fock` / clearer hooks only (audited physics byte-identical; gate
  swap=False → 0.0064/0.0072 exactly).

---

### CLAIMS.md entry
> **LS2 → resolved [V] — Clock m′=0 leg-swap rejected.** Axial EIT-cooling floor,
> single-ended retro, B=1.5 G, OmR=0.25, η=0.094: **config A (dark |1,−1⟩) = 0.0048,
> hard-converged**; **config B (swap, dark |2,+1⟩) ≈ 0.018 best-bounded, non-convergent at
> matched OmR.** A favored ~3.8×. Cause: F=2-interior dark leg forces rep2=A (unique
> protecting repump), which cannot clear the |2,+2⟩ leak → near-flat Fock heating tail.
> Magic-B and F′=3 sub-dominant; GATE 1 moot. Engine `clock_combined_solve.py` / `clk2.py`;
> frame-conflict 0.0. Also holds against the EOM-Raman clearer (window empty). Supersedes the
> open "swap favored" finding.

---

## Branching record [V] (unchanged — reproduced by `clock_branching_check.py`)
The |F′2,0⟩ dark-leg branching is **reversed** vs |F′2,2⟩ (exact CG):

| excited state | → F=1 dark leg | → \|2,+1⟩ | raw spectator/leak |
|---|---|---|---|
| \|F′2,2⟩ stretched | \|1,+1⟩ **0.75** | 0.25 | 0.333 (→\|2,+2⟩) |
| \|F′2,0⟩ clock | \|1,−1⟩ **0.25** | **0.75** | 0.667 (→\|1,0⟩,\|2,−1⟩,\|1,+1⟩) |

(renormalized over the two dark legs; raw clock: |1,−1⟩ 0.083, |2,+1⟩ 0.25, |1,0⟩ 0.333,
|2,−1⟩ 0.25, |1,+1⟩ 0.083.)

**Why the branching did NOT decide it (the lesson).** The earlier note reasoned: the dark
state sits ~94% on the probe leg, so seating it on the higher-decay leg (0.75, i.e. swap)
maximizes recycling → swap favored. That diffusion lever is real and isolated-clean it is
~3.3× (config-B clean-Λ 0.0022 vs config-A 0.0072). **But it is dominated by the repump
penalty:** moving the dark to |2,+1⟩ moves it to the F=2 *interior*, where the edge rule that
protects an F=1-edge dark leg no longer isolates it, the protecting repump cannot clear
|2,+2⟩, and the leak heats faster than the recycling gain saves. Branching/diffusion in
isolation pointed the wrong way; only the repumped solve is decisive. (The question turned on
repump topology, not diffusion — the lesson now earned four times across this thread.)
