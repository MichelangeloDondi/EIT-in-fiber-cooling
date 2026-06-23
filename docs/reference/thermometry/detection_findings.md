# In-fibre detection budget (fundamental issue #4)

**Verdict.** Detection is viable, and the method is **absorption (optical depth)**, not
fluorescence. OD ≈ 1 at N ≈ 3900 atoms; the probe is shot-noise-limited but probe photons are
essentially free (~10 fJ for ΔOD = 0.01), so **detection is not the bottleneck** — the per-shot
floor on a population fraction is atom-number/projection noise √(f(1−f)/N). Guided-mode
fluorescence is intrinsically an ensemble method (<1 collected photon per atom) and, in the
forward direction, is swamped by the co-propagating same-wavelength readout beam. **Single-atom
in-fibre detection is not available; the experiment is an ensemble OD measurement.** (`src/detection_snr.py`)

## Numbers
- Mode: w = 19 µm, A_mode = 1.13×10⁻⁵ cm²; σ₀ = 2.9×10⁻⁹ cm² → **OD/atom = 2.6×10⁻⁴**.
- Absorption: OD = 0.26 / 1.03 / 2.56 at N = 1000 / 3900 / 10⁴. ΔOD = 0.01 needs ~4×10⁴ probe
  photons (~10 fJ) — trivial.
- Recoil: 0.18 µK/photon (radial ≈ 0.06) → ~15,400 usable scatters/atom before trap loss
  (cycle-leak-limited; recoil-loss 16,500 comparable).
- Fluorescence: NA_eff = λ/πw = 0.013 → η_couple = 4.3×10⁻⁵/direction → **0.20 collected
  photons/atom/shot** (backward, one direction).
- Readout-beam background: 18.9 nW = 7.4×10¹⁰ photons/s guided, **same wavelength** as the
  fluorescence. Forward signal/background = 5.5×10⁻⁵ → swamped (~1.8×10⁴×). Backward detection
  rejects the forward readout by direction; residual = fibre backscatter × readout [O].

## Why absorption, not fluorescence
- Fluorescence and the readout share the **same transition (780 nm)** → no spectral filter
  separates them; the readout is **guided** (same mode) → forward collection sees the full
  readout beam, and temporal gating fails (the fluorescence *is* the scattered readout).
- Backward collection avoids the forward beam but is limited by HCPCF backscatter [O] and still
  collects <1 photon/atom.
- Absorption uses the readout beam's **attenuation** (the signal you want), is photon-rich, and
  measures the ensemble column density (∝ N in F=2) directly.

## Implications
- Thermometry (red/blue sideband asymmetry) is read out as **OD ∝ population**, ensemble-
  averaged. The asymmetry R = A_red/A_blue is a ratio of populations, so absorption-OD delivers
  it without single-atom resolution.
- Ties to the 1D/ensemble scope and the OD-vs-cooling tension: high OD (large N) helps detection
  but means an optically dense, inhomogeneous sample; cooling and thermometry act on the
  ensemble, not on single atoms.
- **Bench inputs to close it [O]:** loaded N_atoms (sets OD), 780 transmission over the readout
  path, and — only if a fluorescence route is pursued — the HCPCF backscatter fraction at 780.

## Caveats
- s, QE, T_fibre, and T_rad0 are estimates [I]; OD/atom, η_couple, and the recoil heating are
  computed from fixed constants [V]. The conclusion (absorption viable, forward fluorescence
  swamped) is robust to order-unity changes in the [I] inputs.
