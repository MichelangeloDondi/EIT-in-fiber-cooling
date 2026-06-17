# SCOPE — what the model is and isn't

One page, so claims aren't over-extended. Numbers and evidence: `CLAIMS.md`,
`src/operating_point.py`.

## What this is
- A **1D (axial) cooler.** The 1064 nm axial lattice mode (ν_z ≈ 430 kHz) is resolved-sideband
  cooled by clock-EIT. Floors are **steady-state Lindblad solver** results (`tagged_solver.py`),
  carrying a declared model band of **×/÷2**.
- The cooled observable is the **axial** motional ground-state fraction. Thermometry is the
  red/blue sideband asymmetry R = A_red/A_blue, read out as an **ensemble optical depth**
  (absorption), not single-atom fluorescence.
- The cooling/clock transition uses the **field-insensitive** pair |1,−1⟩/|2,+1⟩ → |F′=2, m′=0⟩
  (insensitive at any B, 1st-order vector-immune).

## What this is NOT
- **Not a 3D ground-state cooler.** The radial mode (ν_r ≈ 5.42 kHz) is soft, **not cooled**, and
  ends *warm* (~107–130 µK); the 3D ground fraction is ~1 %. Headline the **axial** ground state.
- **Not single-atom.** In-fibre detection is **ensemble absorption (OD)**; single-atom resolution
  is not available. Collisions and density-dependent effects are **out of scope** (treated
  separately, not in these floors).
- **Not a technical-noise model.** The two-photon coherence linewidth is **assumed sub-100 Hz**
  (the floor doubles at 0.26 kHz). The actual linewidth, the loaded atom number, and the in-situ
  trap depth are **bench inputs [O]**, not model outputs.

## Boundaries that load-bear
- **ν_z and U₀ are inferred** from the 1064 mode waist, not measured [O]. The cooling/thermometry
  scaling (η ∝ 1/√ν_z) rides on this.
- The **all-in floor (0.012–0.019)** folds in an *estimated* anti-trap/leak increment [I]; the
  solver floor alone is 0.0048 (dual) / 0.0072 (single).
- **Polarization purity** rests on the low-birefringence kagome beat-length condition [I]/[O].
- The radial result is an **input/consequence**, not a cooled output: the radial temperature is
  set by loading + recoil during cooling, and it feeds the inhomogeneity floor.

## Honesty rails (for the thesis and the papers)
- NEVER claim **"first cooling in a fibre."**
- NEVER headline a **3D ground state.**
- Defensible firsts: **EIT-SC in an HCPCF**, **field-insensitive clock-pair cooling**, and the
  **single-EOM common-mode** delivery (no OPLL).
- **Sr transfer:** EIT cooling does **not** transfer (689/698 resolve sidebands; ⁸⁸Sr is J=0), but
  the **radial recoil floor is atom-independent** and does transfer — that is the P3 result and
  the strongest Sr-relevant claim.
