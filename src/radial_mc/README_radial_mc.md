# S3 radial dynamic Monte-Carlo — EIT cooling of ⁸⁷Rb in a Gaussian tweezer

Computes the **realized cloud ⟨n_z⟩** (axial phonon floor) when the per-radius EIT
cooling rate W(r) and local steady state n_ss(r) are inhomogeneous and the atom
samples them *dynamically* via its radial orbit. Answers the S3 brief's dispositive
question: does radial motion **average** the inhomogeneity (floor → cold) or does
cooling **lag** (floor → warm)?

**Answer: averaging wins**, and more sharply than a [quasi-static, frozen] bracket
implies — because W(r) peaks at the cold center, the steady-state limit cycle is the
*cooling-rate-weighted* spatial average, pulled below the plain spatial average.

> **PI-facing consolidation:** `src/cloud_cooling_tool.py` embeds this same 3-level Λ engine
> + trajectory MC in one self-contained, tunable file (with a `--regression` trust gate) and
> adds the flat-top box profile and the two-tone lever. Use it for exploration; this `radial_mc/`
> subsystem remains the original validated S3 implementation and the `s3_radial_mc.png` figure
> generator.

---

## Files

| file | role |
|------|------|
| `eit_common.py`   | **(from the project repo, unmodified)** 3-level Λ EIT physics. Dependency. |
| `engine.py`       | Exposes `_build_L(...)` (Liouvillian + N operator) with explicit `Otot` so guided beams Ω(r)=Ω₀√s can be set. Physics byte-identical to `eit_common.eit_floor`. |
| `grid_build.py`   | Per-radius `n_ss(r)` and small-deviation `W(r)`. Writes `grid_cache.npz`. |
| `mc.py`           | Vectorized radial dynamic MC + analytic gates. Reads `grid_cache.npz`. |
| `make_figure.py`  | Two-panel figure (`s3_radial_mc.png`). Reads `grid_cache.npz` + `scan_400.npz`. |
| `grid_cache.npz`  | Computed grid, r=0…17 µm (artifact; regenerable). |
| `scan_400.npz`    | Converged 400 µK curve (artifact; regenerable). |

Dependencies: `qutip` (5.x), `numpy`, `scipy`, `matplotlib`.

---

## Reproduce

```bash
# 1. physics gate: engine reproduces eit_common.eit_floor (validates _build_L)
python3 engine.py

# 2. build the per-radius grid (n_ss(r), W(r)); ~8-14 s/radius
rm -f grid_cache.npz
python3 grid_build.py 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17
#   NOTE: grid_build APPENDS to grid_cache.npz and does not de-duplicate radii.
#         Always rm the cache before a fresh full build.

# 3. dynamic MC scan at a temperature (T in uK); 'v' = cold/hot convergence check
python3 mc.py 25  v
python3 mc.py 100 v
python3 mc.py 400 v          # 400uK low-Dratio needs many orbits; see caveat

# 4. figure (regenerates 25/100uK curves inline, loads scan_400.npz)
python3 make_figure.py
```

---

## Method, and the non-obvious decisions (the audit points)

**Operating point (S3, headline).** Δ₀=45, OmR=0.10, guided Ω(r)=Ω₀√s, M3 detuning
shift Δ_eff(r)=45+60.9(1−s), δ₂=0. Radial laws s=exp(−2r²/w₀²), ν_z=ν₀√s, η=η₀s^(−¼),
w₀=19 µm, U₀=1094 µK. (`grid_build.py` lines 22-38.)

**W(r) extractor — why a relaxation fit, not the eigenvalue gap.**
The instantaneous-derivative method (prepare ρ_int,ss⊗thermal, read d⟨n⟩/dt) returns ≈0:
that product state sits OFF the slow cooling manifold, so fast internal relaxation (~1/Γ)
doesn't move ⟨n⟩ and the instantaneous slope vanishes. The Liouvillian-gap method
(`engine.solve` / `radial_frozen.W_clock`) is **unreliable** here — ARPACK shift-invert at
σ=0 returns spurious *positive*-real-part modes and the n-content pick is ambiguous in the
dense small-|λ| cluster. **Used instead** (`grid_build.nss_and_W`): evolve thermal(n_ss+0.15)
under L via `expm_multiply` and fit the slope of ln(⟨n⟩−n_ss) over a post-transient window
t∈[40,160] t_H → the **near-equilibrium (small-deviation) cooling rate**. This is the rate
that governs tracking when the atom stays near its local n_ss. Nf-converged to 5 digits
(Nf=12/16/20 agree; checked to r=14). The local rate is ~20% non-constant across the decay
(3.0→3.8×10⁻³ on-axis) — the single-rate closure is therefore only ~20% accurate, but the
realized floor is insensitive to W magnitude (see below), so this does not propagate.

**Unit convention.** The |e⟩ total decay rate is GAMMA=6.07 in code units; matching Rb's
26.2 ns lifetime fixes t_H=0.159 µs ⇒ **W[kHz]=2π·10³·λ** (λ in /t_H). Consistent with
`radial_frozen.W_clock` (`return 2*np.pi*best*1e3`). On-axis W(0)=3.78×10⁻³/t_H = **23.7 kHz**,
so this engine's **W(0)/ν_r ≈ 4.4** (ν_r=5.42 kHz). The dial `Dratio` in `mc.py` IS W(0)/ν_r.

**Orbit + closure (`mc.py`).** 2D radial motion in the Gaussian potential, dimensionless
(lengths in w₀, τ=ω_r t): ξ''=−ξ·exp(−2ρ²), velocity-Verlet. Axial phonon via single-rate
closure d⟨n⟩/dτ = −shape(r)·(Dratio/2π)·(⟨n⟩−n_ss(r)), shape=W(r)/W(0). W clamped ≥0
(no spurious heating from frozen-regime fit noise at r≥16).

**Thermal sampling.** Positions from the *full* radial Boltzmann (inverse-CDF), velocities
Gaussian. Harmonic position sampling is wrong here: orbits explore the anharmonic Gaussian
tail and bias the high-T gate. A finite-depth trap is not normalizable under position-only
Boltzmann, so **boundedness (E/U₀<1) is imposed in phase space** — the retained set is the
bound-cloud distribution. (At 400 µK only ~17% of sampled atoms are bound; the rest evaporate.)

**Limit cycle / convergence.** The realized floor is the periodic steady state (limit cycle)
of the driven linear ODE, reached after the initial ⟨n⟩ is forgotten. The effective relaxation
rate is g·⟨W(r)/W(0)⟩ over the orbit; since W collapses off-axis, ⟨W/W(0)⟩≪1 and **low-Dratio
runs need many orbits** (Norbit ~ 1/(Dratio·⟨shape⟩)). Convergence is verified by running
`n_init` cold vs hot (the `v` flag): they must agree. `scan()` uses Norbit=clip(500/Dratio,…);
400 µK at low Dratio needs Norbit up to ~5000 (see `make_figure`/`scan_400` generation).
Also checked: timestep nstep 24→90 stable <10⁻⁴; seed scatter std ~1.3×10⁻⁴.

**Gates (analytic, bound-corrected; `mc.gates`).** Dratio→∞ ⇒ plain spatial average
⟨n_ss⟩ (instant tracking). Dratio→0 ⇒ W-weighted average ⟨W·n_ss⟩/⟨W⟩ (n constant over an
orbit ⇒ ∮W(n−n_ss)dτ=0). The realized MC curve must lie between these and reduce to each in
the corresponding limit. P_b(ρ)∝ρ·exp(−u/θ)·(1−exp(−(1−u)/θ)), u=U/U₀, the (1−e^…) being the
bound-velocity fraction that makes the distribution normalizable and matches the MC's reject-unbound.

---

## Results (converged; init-independent)

| T (µK) | realized ⟨n_z⟩ | W→0 (W-weighted) | W→∞ (quasi-static) | suppression vs q-s |
|--------|----------------|------------------|--------------------|--------------------|
| 25  | 0.00237 | 0.00221 | 0.00286 | 1.2× |
| 100 | 0.00716 | 0.00406 | 0.02181 | 3.0× |
| 400 | ≈0.030  | 0.00846 | 0.21761 | 7.4× |

Realized floor is **flat across W(0)/ν_r ∈ [0.5,10]** (a factor 20), so the conclusion is
robust to whether the true operating point is the clock engine's ~0.5–1.3 or this engine's 4.4.

---

## Caveats / scope (what an auditor should not over-read)

1. **Cross-engine.** This is the reduced 3-level Λ engine (the only one in the file set that
   runs the dynamic machinery). Its absolute n_ss(r=0)=0.0016 vs the clock solver's 0.0064;
   it cools ~3–6× faster. So the *absolute* floors here are this engine's, not the clock's.
   The brief's clock anchors (0.0064/0.0085/0.0126) come from the full clock solver plus a
   v15 §8 semiclassical-MC driver **not present in the repo** — they cannot be regenerated here.
   The **qualitative** findings (W center-peaked; floor = W-weighted average; averaging wins;
   no orbital heating; flatness in W/ν_r) are engine-independent.
2. **400 µK** carries the largest uncertainty: low bound fraction (~17%), large-r grid
   extrapolation (n_ss clamped at the r=17 µm value beyond the grid), and slowest convergence.
   The ≈0.030 value is stable to N and Norbit but should be read as ≈0.03, not 3 sig figs.
3. **Not executed:** per-radius δ₂ servo (optimism bound) and endogenous radial T (T_r held
   fixed at the cloud T). Per-radius δ₂ is expected to help little — it matters only where the
   EIT feature is detuned (large r), and those radii carry W≈0 and are already discounted.
4. `grid_build.py` appends without de-duplication — `rm grid_cache.npz` before a full rebuild.
