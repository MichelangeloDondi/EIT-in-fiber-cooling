# Feasibility — flat-top 1064 profile: the one lever that removes the radial inhomogeneity at its root

**Why this matters most.** The cloud floor (T_r-gated — ~0.012 at 100 µK, up to ~0.022 uncooled) is set by the radial inhomogeneity (the single-atom floor is 0.008–0.010; the v15 0.012–0.019 all-in was a withdrawn double-count), and the
inhomogeneity comes entirely from the **Gaussian transverse profile** of the 1064 lattice — the atoms at
different radii sit in different trap depths, so ν_z(r) and the dark-resonance shift Δ_eff(r) vary across
the cloud. A profile that is **flat over the cloud region** removes that variation at the source and
collapses the radial term for *every* cooling scheme at once. This brief states the requirement precisely
(including a tension that constrains what "flat-top" must mean), separates the **fiber-expert questions**
(XLIM/Marchesini — measurement/design) from the **modelable-first questions** (our side), and gives the
go/no-go. House style: [V]/[I]/[O].

## The requirement — and the tension that defines it
- **The inhomogeneity source [V].** U(r)=U₀·exp(−2r²/w²), w=w₀≈19 µm → ν_z(r)=ν_z0·√(U(r)/U₀) and the
  M3 shift **Δ_eff(r)=Δ₀+c·(1−s), c=60.9 MHz** (s=exp(−2r²/w²)). At 100 µK the cloud has σ_r≈**2.9 µm**
  (σ_r/w=√(k_BT_r/4U₀)=0.15), so it samples ±2–3σ_r ≈ **±6–9 µm**, where Δ_eff shifts **11 MHz (6 µm)
  to 22 MHz (9 µm)** — a large fraction of the 45 MHz detuning on a 150 kHz feature. That is the spread
  to flatten.
- **Waist/power do NOT help [V].** The fractional inhomogeneity is set by **k_BT_r/U₀, which is
  waist-independent** (`radial_frozen`): at fixed U₀, a bigger waist lets the cloud expand to fill it
  (σ_r/w fixed); at fixed power a bigger waist lowers U₀ and makes it *worse*. The only structural fixes
  are a deeper trap (power/scatter-limited), a colder cloud (incremental), or **flattening the profile**.
- **The tension — "flat-top" must mean "flat-BOTTOMED" [V, the key constraint].** The *same* Gaussian
  curvature sets both the axial frequency variation ν_z(r) (the thing to kill) **and** the radial
  confinement ν_r (the thing that traps the atoms): ν_r²∝U₀/w². Flatten U(r) over the cloud and you
  remove ν_z(r) variation **and** ν_r — a perfectly flat profile does not radially confine. So the
  deliverable is not a Gaussian, nor a uniform top-hat, but a **box-like radial potential: flat over
  ±6–9 µm, with confining walls beyond.** This changes the radial trap from harmonic to box-like — which
  is fine for cooling (flat ⇒ uniform ν_z) but changes the radial dynamics (couples to S3, below).

## Questions for the fiber experts (XLIM / Marchesini) — measurement & design
These decide optical feasibility; we cannot answer them from our side.
1. **Mode content of the K19 at 1064 [O].** Is the fundamental core mode approximately Gaussian, or does
   the 48 µm core support a usable mode (or low-order superposition) with a **flatter central profile**?
   What is the measured transverse intensity profile at 1064 (not just at 780)?
2. **Flat-bottomed profile — deliverable and stable over 2 m? [O].** Can a flat-over-±6–9 µm profile be
   launched (beam-shaping at the input + mode-matched coupling, or a mode converter) and **maintained over
   the 2 m length** — i.e. is it a single low-loss mode, or a superposition that would **walk off via
   modal dispersion** (different β per mode → the profile evolves flat→ring/speckle along the fiber)? The
   walk-off length vs 2 m is the make-or-break.
3. **Higher-mode loss [O].** If the flat-bottomed profile requires higher-order modes, what is their
   **differential loss** in the K19's inhibited-coupling windows? High differential loss means the profile
   **degrades along the fiber** (the flat part attenuates faster than the fundamental).
4. **Lattice contrast [O].** The axial lattice is **retro-formed** (forward + retro 1064). Does a
   flat-bottomed forward+retro maintain adequate **standing-wave contrast** (depth modulation) across the
   flat region — or does a multimode profile reduce/vary the contrast with radius (which would re-introduce
   a different ν_z(r) variation through the contrast, defeating the purpose)?
5. **Coexistence [O].** Does the flat-bottomed-launch optics coexist with the 780 (cooling/repump) and
   795 (if D1 ever) guidance, and with the single-ended-retro tag geometry?

## Modelable on our side first — do these before/in parallel with asking XLIM
These quantify the *payoff* and the *cost*, so the expert ask is well-motivated.
1. **The floor payoff [I → compute].** If U(r) is flat over the cloud, ν_z(r) and Δ_eff(r) are constant →
   the inhomogeneity term vanishes → the axial floor collapses to the **cold on-axis value (~0.0064) for
   all T_r**, and the cloud floor drops from its T_r-gated value (up to ~0.022 uncooled) to the on-axis single-atom **0.008–0.010** (axial-floor- and
   survival-limited, the radial term gone). Confirm the magnitude with the engine at flat-profile
   parameters; this is the number that justifies the whole effort.
2. **Box-trap radial dynamics [O → couples to S3].** A box-like radial potential changes the radial
   motion from harmonic (the S3 MC's premise) to **free-expansion-plus-wall-reflection**. The flat region
   means the atoms see *no* ν_z(r) variation while inside it — so the inhomogeneity is gone **regardless
   of the radial dynamics** — but the wall region (where the profile rolls up) re-introduces a thin
   inhomogeneous shell. Quantify: what fraction of the cloud sits in the flat bottom vs the walls, and
   does the wall shell matter? (This is the S3 MC re-run with a box profile — and it should come out
   *much* better than the Gaussian S3 number.)
3. **Residual flatness tolerance [I].** How flat is flat *enough*? The feature is 150 kHz wide; the
   tolerable Δ_eff spread across the cloud is ≲ that. Back out the required profile flatness (peak-to-peak
   ΔU/U over ±6–9 µm) that keeps the Δ_eff spread under ~150 kHz–1 MHz — this is the **spec to hand XLIM**
   (e.g. "≤X% intensity variation over ±8 µm"), turning a vague "flat-top" into a number they can assess.

## Stakes — this is the headline mover, the only one left
- **If feasible:** collapses the radial term → cloud floor falls to the on-axis single-atom **0.008–0.010** (from the T_r-gated up-to-~0.022 uncooled; the v15 0.012–0.019 all-in was withdrawn), for every
  scheme. This is the single largest available improvement in the whole program, and the *only* one that
  moves the headline (the axial-scheme space is swept and closed).
- **If infeasible** (no stable flat mode / walk-off over 2 m / contrast lost): the Gaussian radial
  inhomogeneity is **structural**, the headline stays at the S3-computed value, and the program's honest
  ceiling is set there. Either outcome is decision-relevant.

## Go/no-go — definition of done
- **Our side first:** (a) confirm the flat-profile floor payoff (~0.006–0.008) with the engine; (b) back
  out the flatness spec (ΔU/U over ±8 µm) that holds the Δ_eff spread under the feature width; (c) S3 with
  a box profile to confirm the radial term collapses. Deliver (b) as a single number to XLIM.
- **Fiber experts:** given the flatness spec, is a flat-bottomed 1064 mode **deliverable and stable over
  2 m with adequate lattice contrast** — single-mode, or a walk-off-free superposition? Yes → the headline
  mover is real, build it. No → the inhomogeneity is structural, and S3 sets the honest floor.
- The decision hinges on **question 2 (walk-off over 2 m)** and **question 4 (contrast)** for the experts,
  and **payoff (1) + flatness spec (3)** on our side. Everything else is secondary.
