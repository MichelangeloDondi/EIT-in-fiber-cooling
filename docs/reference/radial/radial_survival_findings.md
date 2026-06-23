# Radial heating + survival budget (fundamental issue #2)

**Verdict.** Survival through the cooling window is **~100%**. The soft radial mode (uncooled,
ν_r = 5.42 kHz) heats only by recoil — ~7–30 µK over the ~124–492 photons of the EIT cooling
transient — staying far below the 1094 µK trap depth. The anti-trapped 5P₃/₂ state is **benign
during cooling**: the excited fraction is small (ρ_ee ≈ 0.01), so the time-averaged radial trap
stays confining, and the anti-trap adds <1% to recoil heating. The trap-depth scatter limit
(~16,500 photons) bounds the **readout**, not the cooling. (`src/tools/radial_survival.py`)

## Numbers
- Recoil: 0.18 µK/photon → radial heating ~0.06 µK/photon.
- Cooling photon budget N_cool ≈ Δn_z/η² ≈ 124 (η_2k = 0.187) … 492 (η_780 = 0.094), Δn_z ≈ 4.4.
- Radial T over the cooling window: 100 → 107–130 µK (random-walk spread ±1–2 µK). Depth 1094 µK
  → survival ~100%.
- Loss limit: N_loss = (U₀ − T_init)/0.06 ≈ 16,500 photons → this is the readout regime (the same
  recoil-loss limit found in the detection budget), not the cooling.

## Anti-trap is not catastrophic, and not a heating channel
- **Confinement.** Curvature ratio |κ_excited|/κ_trap = U_e0/U₀ = 0.83 (19 MHz) … 2.5 (57 MHz).
  The time-averaged radial trap stays confining iff ρ_ee < 1/(1+ratio) ≈ 0.29–0.55; with
  ρ_ee ≈ 0.01 it softens only ~2–5% in frequency.
- **Additive heating.** The excited-state dwell is 1/Γ ≈ 26 ns — far too short for the anti-trap
  force to impart much impulse: per excitation the impulse is ~5% of a photon recoil → ~0.7% of
  the recoil heating.
- **Parametric heating.** Spring-constant telegraph noise at 2ν_r is tiny because R_sc ≫ ν_r (the
  modulation sits far above the parametric resonance): Γ_param ≈ 4.8 /s → ~0.5% over 1 ms.

## Consequence (this is the real effect — a floor, not a loss)
The radial mode ends **warm** — ~107–130 µK, up from ~100 µK — because the uncooled radial mode
takes recoil during the axial cooling. This feeds the **inhomogeneous-light-shift / cloud floor**
(already tracked), it is not a loss channel. The honest statement: the sample survives, but the
radial temperature you detect is slightly *higher* than what you loaded, not lower.

## Caveats
T_axial_init, T_rad_init (100 µK), and the trap waist (19 µm) are estimates [I]; the recoil
heating, curvature ratios, and the loss limit are computed from fixed constants [V]. The
conclusion (survival ~100% through cooling; anti-trap benign) is robust to order-unity changes in
the [I] inputs.

## Bench [O]
Post-molasses radial T and atom number; in-situ trap depth at 1064 nm.
