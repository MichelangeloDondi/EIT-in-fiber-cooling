# Audit / kickoff — S3 radial dynamic Monte-Carlo: the realized cloud floor

**This is the headline computation.** The axial scheme is closed (every Λ/recycle lever swept); the
all-in band **0.012–0.019** is radial-inhomogeneity-dominated, and its *realized* value — as opposed to
the frozen-position ceiling — has **never been computed dynamically**. This brief specifies that run.
House style: concise, [V]/[I]/[O], cite source+line, attack [I]. Compute, don't assert.

**Dispatch note:** this is a *new computational thread* (radial trajectories + per-radius EIT solve), not
the recycler/scatter context of the D1-Raman auditor — cleanest in a fresh chat. Self-contained below.

## What is settled — do not re-derive
- **Radial scaling laws [V]** (`radial_frozen.py`; v16 §8), s(r)=exp(−2r²/w²), w=w₀≈19 µm:
  ν_z(r)=ν_z0·√s, η(r)=η0·s^(−¼), Ω(r)=Ω0·√s, and the **radial detuning shift
  Δ_eff(r)=Δ₀+c·(1−s), c=60.9 MHz** (the "M3" term, from the +38.1 MHz scalar shift of |F′2,0⟩;
  dominates radial degradation beyond ~50 µK).
- **S2 frozen bound (turning-point ceiling) [V]:** n̄_z ≤ **0.0064 / 0.0126 / 0.0266 at 25 / 100 / 400 µK**
  — atom pinned at r_max, no re-cooling. Conservative; over-weights the tail.
- **Quasi-static per-radius MC (semiclassical, v16 §8) [I, provenance-gap]:** ≈ **0.0085 at 100 µK** (Δ=45, OmR=0.10) — *driver code absent; superseded as the quasi-static reference by the clk2 grid_avg_cloud ceiling 0.0169 at 100 µK; the dynamic-MC suppression RATIO below is what transfers* — each atom
  assumed to reach the *local* frozen floor at its instantaneous radius, then averaged over the radial
  distribution. This is the **W≫ν_r limit** (cooling instantaneous vs radial motion). Coverage ~99%
  (feature 150 kHz, r<12.45 µm). Absolute ±0.001 (coarse per-radius δ₂ grid).
- **The timescale crux [V] — why neither limit is the answer.** Radial period 1/ν_r ≈ **184 µs**
  (ν_r=5.42 kHz); axial cooling rate W ≈ 2–7 kHz (Liouvillian gap ~2.4 kHz / 1/τ ~7 kHz at Δ=45).
  **W ~ ν_r within a factor ~2–3.** So the atom cools roughly *once per radial orbit* — it neither freezes
  at r_max (S2) nor instantly re-cools at each radius (quasi-static). The realized floor sits in the
  bracket **[0.0085, 0.0126]** at 100 µK — and *where* is the headline question S3 answers.

## The proposal — the dynamic MC
Semiclassical radial trajectories with quantum axial cooling:
1. **Radial trajectory:** each atom a 2-D harmonic oscillator at ν_r; radial energy E_r sampled from the
   thermal (Boltzmann) distribution at T_r; r(t) from the resulting orbit (phase/eccentricity randomized).
2. **Per-radius cooling data [from the engine]:** at a grid of r, solve the steady-state EIT for the
   instantaneous {ν_z(r), Δ_eff(r), Ω(r), η(r)} → the **local cooling rate W(r)** (Liouvillian gap) and
   the **local frozen floor n̄_ss(r)**. (Reuse the multilevel solver; this is the v16 §8 per-radius pass,
   now also returning W(r).)
3. **Axial evolution along the trajectory:** integrate the rate equation
   **d⟨n⟩/dt = −W(r(t))·(⟨n⟩ − n̄_ss(r(t)))** with r(t) from step 1, W and n̄_ss interpolated from step 2.
   (First-pass ⟨n⟩-ODE; escalate to the full Fock-distribution master equation only if the ⟨n⟩ closure
   proves inadequate — see check 4.)
4. **Cloud average:** many trajectories, long-time ⟨n⟩, averaged over the thermal radial distribution.
   Sweep **T_r ∈ {25, 100, 400 µK}** at the cloud-optimal **Δ=45, OmR=0.10**.

## The dispositive question [O]
With W ~ ν_r, does the radial motion **average** the inhomogeneity (the atom's orbit samples both good
(small-r) and bad (large-r) cooling, and the small-r dwell re-cools the large-r heating → realized floor
toward or below the quasi-static 0.0085) — or does the cooling **lag** the orbit (⟨n⟩ can't track the
fast-moving n̄_ss(r(t)) → realized floor toward the frozen 0.0126, or *above* it if orbital heating
accumulates)? **Report the realized cloud ⟨n_z⟩ at 25/100/400 µK and where it lands in [quasi-static,
frozen].**

## Checks — the things that decide the answer (don't assume them away)
1. **Orbital heating sign [the one that can break the bracket].** If Δ_eff(r) pushes the dark resonance
   far enough at large r that the *local cooling rate goes negative* (net heating) somewhere on the orbit,
   the dynamic floor can **exceed** the quasi-static (the orbit pumps energy in near r_max faster than the
   small-r arc removes it). Report W(r) across the orbit and flag any sign change — this is the difference
   between "dynamic lands in the bracket" and "dynamic is worse than both limits."
2. **δ₂ servo strategy [load-bearing, and optimistic in the quasi-static MC].** Is δ₂ servoed to the
   *on-axis* dark resonance (one fixed set-point — physical; off-axis atoms are then detuned by the
   Δ_eff(r) shift) or re-servoed *per radius* (the v16 §8 "coarse per-radius δ₂ grid" — optimistic, not
   physically realizable since one laser serves the whole cloud)? The realized floor depends strongly on
   this. **Run the physical fixed-δ₂ case** as the headline; the per-radius case is the upper-optimism
   bound. State which produced which number.
3. **T_r endogeneity [links to the open reabsorption [O]].** Is T_r the *upstream-prepared* radial
   temperature (gray molasses, static input) — or does the axial cooling's reabsorption heat the radial
   bath during the run (the `cloud_floor_spec` 2b-static coupling, currently [O])? If T_r is endogenous,
   S3 and the reabsorption revision are coupled: σ_r grows → worse sampling → the floor is self-consistent,
   not a fixed-T_r read. **First pass: fixed T_r** (decouple); flag the endogenous version as the follow-on
   once the reabsorption spec lands.
4. **Convergence [V required].** Trajectory count (≥few×10³); integration timestep resolving ν_r
   (≤ T_r/20); and the ⟨n⟩-ODE closure — verify against a few full-Fock-distribution trajectories that the
   rate-equation ⟨n⟩ tracks the distribution mean (the closure can fail if the Fock distribution skews
   under the time-varying rate). If it fails, escalate to the Fock-resolved MC.

## Gate — the two limits that must reproduce
- **W→∞ (cooling instantaneous):** the MC must reduce to the **quasi-static per-radius average ≈0.0085**
  at 100 µK (atom always at its local floor).
- **W→0 (no re-cooling):** the MC must reduce to the **frozen turning-point bound ≈0.0126** at 100 µK
  (atom sits at r_max). 
- The physical W ~ ν_r result lands **between** (unless check-1 fires). If it lands outside the bracket,
  that is either orbital heating (check 1) or a bug — distinguish before reporting.

## Stakes and scope
- **This moves the thesis number.** Unlike the axial-scheme sweep (all sub-dominant), S3 sets where in
  0.012–0.019 the realized floor sits — or revises the band. If the dynamics average favorably, the
  headline drops toward ~0.009–0.012; if cooling lags or orbital heating fires, it sits at the upper end
  or worse.
- **Scope:** S3 quantifies the inhomogeneity *with the Gaussian profile*. The **flat-top lever** (separate
  brief, XLIM/Marchesini) is the *intervention* that removes ν_z(r) at the root — if a flat-top mode is
  deliverable it collapses this term for every scheme at once, making S3's Gaussian number the
  "without-flat-top" baseline. The two are complementary: S3 says how bad the Gaussian is; flat-top says
  whether you can avoid it.

## Definition of done
The realized cloud ⟨n_z⟩ at 25/100/400 µK, fixed-δ₂ (physical) and per-radius (optimism bound), with the
orbital-heating sign reported, Nf/closure convergence shown, and the result placed in the
[quasi-static, frozen] bracket. That number — fed into the reabsorption and survival terms — is the
honest all-in headline, replacing the current 0.012–0.019 [I] estimate with a computed value.
