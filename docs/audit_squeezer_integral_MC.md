# audit_squeezer_integral_MC.md — Computation 2: radial anti-trap squeezer on the MC pipeline

**System.** ⁸⁷Rb clock-EIT, kagome HCPCF (w₀=19 µm, U₀=1094 µK, ν_z0=2π·430 kHz, ν_r=2π·5.42 kHz).
The validated S3 dynamic-MC pipeline (`mc.py`/`grid_build.py`/`engine.py`, fig `s3_radial_mc.png`)
settled the **cooling half** of the cloud floor: realized sits *below* quasi-static (W(r) peaks at
the cold center, anti-correlated with n_ss(r)), frozen 0.0126 superseded, dynamics benign [V, 3-level
engine → ratio result]. Cloud **all-in = cooling(r) + anti-trap squeezer integral**. This computation
= the squeezer half — the only open piece, and the one with the *adverse* radial sign.

**Goal.** Fold the radius-dependent anti-trap squeezer into the MC ⟨n⟩-ODE as a heating term,
dwell-weighted by the orbit, and return the cloud all-in. Settle whether the off-axis squeezer rise
survives the dwell-weighting that made cooling benign.

> **UPDATE 2026-06-20 — the input is computed and the rate-rise half is disproven.** P_e(F′2)(r) was
> measured on clk2 (`radial_pe.py`): it **falls** off-axis (1.53×10⁻⁵ on-axis → 8.8×10⁻⁶ at r=10 µm),
> *not* rises — because the M3 shift is **common** to both legs (δ₂ unchanged, dark state preserved),
> so the dominant off-axis effect is the weaker field (Ω∝√s), which lowers P_e. With kernel ∝ ν_z(r)²
> also falling, the squeezer **heat rate R_sq(r)=P_e·kernel falls to 0.32× at r=10**. So the
> "rate-rise vs kernel-falloff" contest is settled — the kernel-falloff is *unopposed*; there is no
> rate-rise. The brief's "off-axis-rising / adverse-sign / sign-uncertain" framing below is
> **superseded**: the only open question is whether the dwell-weighting beats the residual off-axis
> **1/W** tail amplification (R_sq falls ~3×, W falls ~10³×, so the static increment still rises in the
> tail) — and the cooling MC is the existence proof that the dwell-weighting defeats exactly that.
> Expected cloud ≈ single-atom ≈ 0.008–0.010. The MC pass below now *confirms the magnitude*, not the
> sign. The δ₂-preservation is engine-independent (a level-structure fact), so it survives the
> 3-level-vs-clock gap; only the absolute P_e magnitude is engine-specific.

**The two competing channels (the crux) [V, physics].**
- *Per-excursion kernel* ⟨n⟩_exc = (s+1/s)²ω_e²/(2(Γ²−4ω_e²)), ω_e=ν_z(r)√|r_ratio|, |r_ratio|=2.435
  FIXED (excited/ground polarizability ratio, geometry-independent) ⇒ kernel ∝ ν_z(r)² ∝ U(r) →
  **FALLS** off-axis. On-axis 0.0311 (`antitrap_kernel_grid.py`).
- *Excursion rate* ∝ P_e(Δ_eff(r))·Γ·b_leak. On dark resonance P_e~4×10⁻⁵ (pinned). Off-axis
  Δ_eff(r)=Δ₀+60.9(1−s) detunes the dark state → P_e **RISES** → rate rises off-axis.
- Squeezer heat rate R_sq(r) ∝ P_e(r)·kernel(ν_z(r)) = rise × fall; and cooling W(r) (falls off-axis)
  dissipates it poorly there (1/W rises). Net sign: **open** — this is the whole question.

**Method (cheap; one-term addition to the validated pipeline).**
1. Extract P_e(r) from the engine per-radius pass (`grid_build` already solves per-r; the engine
   returns P_e — on-axis 4×10⁻⁵ already in hand). [Cheap.]
2. Squeezer heating term, **anchored to the faithful on-axis increment** (NOT the Markov overcount):
   R_sq(r) = R_sq(0)·[P_e(r)/P_e(0)]·[kernel(ν_z(r))/kernel(ν_z0)], with R_sq(0)=0.003·W(0) so the
   on-axis MC steady state reproduces the certified faithful 0.003 (faithful − no-squeezer), **not**
   the recycle-dwell Markov 0.07 (which overcounts ~20× by summing N_rep·kernel without re-cooling).
3. Add to the MC ⟨n⟩-ODE:  d⟨n⟩/dt = −W(r)(⟨n⟩ − n_ss_cool(r)) + R_sq(r).  Re-run the same
   limit-cycle MC (full-Boltzmann sampling, init-independence check) at 25/100/400 µK.
4. Return cloud all-in (cooling + squeezer) and the squeezer's *marginal* contribution (with − without).

**Tentative conclusion [I].** The dwell-weighting that made cooling benign — atom spends little
proper time at large r, moves fast through the tail — should also suppress the off-axis squeezer
rise. Expected: squeezer integral ~0.002–0.004 (≲ on-axis 0.003), cloud all-in ~0.008–0.012
(cooling ~0.006–0.007 + squeezer ~0.002–0.004), i.e. the cloud **stays benign**. But the off-axis
P_e rise (rate) *and* the 1/W rise (poor dissipation) could beat the kernel fall + dwell discount;
the integral settles it. The 400 µK case (fattest tail) is where it would break first.

**Claims to falsify.**
- [I] R_sq factorizes as P_e(r)·kernel(r) anchored to faithful 0.003. The rigorous check is a
  per-radius *faithful* grid (position-basis ME with the squeezer at each r) — a workstation job; the
  factorization is the cheap proxy.
- [I] cooling W(r) dissipates the squeezer heat (same EIT cooling removes phonons regardless of
  source). Reasonable but assumed.
- [I] P_e(Δ_eff(r)) shape from the 3-level engine transfers to the clock engine; magnitude is
  engine-specific (cooling was a ratio result), clock magnitude via clk2.

**Checkable questions.**
1. Does the squeezer's marginal contribution rise, fall, or stay flat with T_r? If it rises faster
   than cooling falls, the cloud degrades at warm T_r — 400 µK is the test.
2. Where along the orbit is the squeezer heat injected — center (P_e low, atom dwells) or turning
   points (P_e high, atom fast)? The dwell-vs-rate balance, made explicit.
3. Is R_sq ∝ P_e·kernel within ~30% of a per-radius faithful grid at r = 3, 6, 9 µm? If not, the cheap
   proxy fails and the cloud needs the full per-radius grid.
4. Does the cloud all-in stay below the withdrawn 0.012–0.019 (confirming the headline drop), or does
   the squeezer push it back up?

**Gate.** R_sq→0 must reproduce the cooling-only MC (0.00237/0.00716/0.030 at 25/100/400 µK). On-axis
the increment must = 0.003 (faithful), not 0.07 (Markov). Init-hot ≡ init-cold (limit cycle).

**Scope.** Same 3-level ratio caveat as the cooling MC: this returns the cloud all-in *in the engine's
own units / bracket*, not the clock floor. The clock magnitude needs the clk2 per-radius re-run
(the high-dwell computation #1). What transfers here is the **sign and the dwell-survival** of the
squeezer — which is exactly the open question.
