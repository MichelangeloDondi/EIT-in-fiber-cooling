# 07 · Thermometry & data analysis

*How the cooling result ⟨n_z⟩ is actually measured — the readout physics, the pulse you fire, and how
to turn raw sideband amplitudes into an unbiased phonon number.*
[← Cloud floor](06_cloud_floor_and_deadwall.md) · [Next: running the model →](08_running_and_optimizing.md)

---

## Read the cooling pair directly

A cooling floor is worthless if ⟨n_z⟩ cannot be read without bias at the 0.01 level (half the floor).
The readout is **resolved-sideband Raman spectroscopy on the cooling pair itself**,
|1,−1⟩ ↔ |2,+1⟩, through the same retro path used for cooling.

- **No park-and-transfer.** Because the cooling pair *is* the field-insensitive pair (Chapter 02), the
  thermometer reads it **directly** — there is no microwave/RF transfer step before reading. (This
  supersedes an earlier park→read scheme; see the provenance note in the authority doc.)
- **Geometry.** Counter-propagating 2k Raman along the fibre measures the **axial** mode that was
  cooled, with an effective Lamb–Dicke parameter η_R ≈ 2η_z ≈ 0.187 — about twice the cooling value, so
  sideband contrast is *favourable*.
- **The observable** is the red/blue amplitude ratio **R = A_red/A_blue**. After good cooling the red
  (n→n−1) sideband is suppressed relative to the blue (n→n+1) — the classic Leong-type asymmetry.

## Turning R into ⟨n_z⟩ without bias

![Sideband-asymmetry thermometry at the floor + calibration](../../figures/fig_thermometry.png)

The data-analysis rules are where naive thermometry goes wrong:

- **Fire a Blackman-shaped sideband-π pulse.** A finite *square* π-pulse leaks 0.39 % of the carrier
  into the sideband — comparable to the ~0.43 % floor signal, a ~2× bias. A **Blackman** pulse
  suppresses that carrier wing to 6×10⁻⁹, so R reads ⟨n⟩ faithfully and independently of Δ.
- **Calibrate R against known ⟨n⟩ — never use the naive ⟨n⟩ = R/(1−R)** (biased ~3×), and never use
  off-sideband subtraction (it over-subtracts). Off-resonant scatter, the standing-wave phase, and the
  common-mode AC-Stark shifts all **cancel in the ratio R**; a branching re-entry leaves a *near-constant
  pedestal* that a calibration absorbs while preserving dR/d⟨n⟩.
- A blue-sideband Rabi-flop + fit recovers the ground-state population P₀ to ±5 % with ~2000 shots —
  shot-noise-limited, not detuning-limited.

In practice: the **single cooling laser is sufficient** for calibrated ratio thermometry (a dedicated
~4 GHz thermometry laser is a ~2× SNR upgrade, not a requirement), and keep the radial temperature
**T_r ≲ 100 µK** so the axial sideband stays sharp — the same T_r the cloud floor
([Chapter 06](06_cloud_floor_and_deadwall.md)) wants.

## What is verified, and the one gap that gates a measured number

Be precise about the evidence here. The results above run on the **generic two-level ⊗ Fock sideband
core** with the states relabelled to the m′=0 pair. They are **transition-agnostic** — pulse shape,
2k recoil, standing-wave phase, generic scatter — so they carry **[V]** to the Δm=+2 readout.

What they do **not** contain is the |1,−1⟩↔|2,+1⟩-**specific** spectral environment, and there is one
intrinsic, *amplified*, already-documented systematic that gates a truly *measured* number: the
**rank-2-amplified intensity-ratio differential AC-Stark** on the Δm=+2 pair. The rank-2 null
(Chapter 02) makes the two-photon Rabi weak, forcing higher readout intensity, whose single-beam shift
imbalance *is* a differential shift — and being scan-asymmetric, it does **not** calibrate out.
**Naber–Spreeuw (PRA 94, 013427, 2016)** measured exactly this on this pair and found the shift
**vanishes at an optimal intensity ratio** (a built-in diagnostic — the linewidth narrows there). So
the single computation between "thermometry consolidated" and "thermometry *verified*" is a multilevel
Δm=+2 readout simulation that **reproduces Naber's optimal-ratio null** and confirms the red/blue
asymmetry sits below the floor at that ratio. This is the project's theory paper ("Paper T").

---

**Go deeper →** the full method, readout spec, validation scope, and open-items list are the consolidated
authority [`docs/thermometry.md`](../thermometry.md); the falsification audit of record is
[`reference/thermometry/thermometry_findings.md`](../reference/thermometry/thermometry_findings.md), and
detection/SNR is
[`reference/thermometry/detection_findings.md`](../reference/thermometry/detection_findings.md).
