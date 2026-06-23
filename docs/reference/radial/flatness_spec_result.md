# Flat-top flatness spec — computed (the number for XLIM)

**Our-side deliverable from the flat-top brief: how flat must the 1064 profile be?**
Per-radial-depth axial floor on the validated config-A engine (`flatness_spec.py`; gate: s=1 →
0.00485 = validated config A). The floor degrades with fractional lattice-depth deficit ΔU/U =
1−U(r)/U₀, driven by the *combined* radial scaling (M3 detuning shift c=60.9 MHz **and**
ν_z(r)∝√s, Ω(r)∝√s, η(r)∝s^(−¼)) — not M3 alone (the floor is flat in single-photon detuning
over 45–80 MHz, so M3 alone would give a far looser, wrong spec).

## Per-depth floor [V]
| ΔU/U | r (µm) | ⟨n_z⟩ | ×on-axis |
|---|---|---|---|
| 0% | 0 | 0.00485 | 1.0 |
| 2% | 1.9 | 0.00517 | 1.07 |
| 5% | 3.0 | 0.00633 | 1.31 |
| 10% | 4.4 | 0.01008 | 2.08 |
| 15% | 5.4 | 0.01619 | 3.34 |
| 20% | 6.4 | 0.02478 | 5.11 |

Sensitivity ≈ 6× (floor rises ~30% per 5% depth deficit near the operating point).

## The spec [V, frozen / conservative]
| floor budget | ΔU/U tolerance | Δ-spread |
|---|---|---|
| +0.0005 (+10%) | **≤ 2%** | ≤ 1.2 MHz |
| +0.001 (+20%) | **≤ 3%** | ≤ 1.8 MHz |
| +0.002 (+40%) | **≤ 5%** | ≤ 3.0 MHz |

**Number to hand XLIM:** intensity flat to **ΔU/U ≲ 3% over the cloud extent (±~6 µm = ±2σ_r at
100 µK)** recovers the cloud floor from 0.0085 toward ~0.006. Two-part: flatness ≤3% **and** the
flat region must cover ±2–3σ_r. σ_r=2.9 µm at 100 µK (σ_r∝√T_r — a colder cloud relaxes the
coverage requirement, not the flatness).

## Caveats [important]
- **Frozen / conservative [I].** This is the per-depth *static* floor (atom pinned at r). The
  **S3 dynamic MC** (atom orbiting radially, W~ν_r) averages center+edge → motional narrowing →
  **relaxes this spec** (likely toward ≤5%). Run S3 first; this 3% is the conservative bound.
- **Combined scaling, not M3 alone [V].** The steepness is ν_z/Ω/η + M3 together; a detuning-only
  scan would give a wrong (too-loose) spec because the floor is flat in single-photon Δ over 45–80.
- **Repumps held fixed [I, sub-dominant].** The depth-dependent repump AC-Stark is not scaled
  (off-resonant; sub-dominant to the cooling Λ). Refine if a tighter spec is needed.
- **Box-trap caveat [V].** A flat-bottomed profile removes ν_r (radial confinement) in the flat
  region — the spec assumes the walls (beyond ±6 µm) still confine; the S3-box re-run quantifies
  the thin wall shell.

## Bottom line
The flat-top must hold **≲3% intensity flatness over ±6 µm** (100 µK, frozen) — demanding (a
few-% flat region inside a 19 µm-waist mode), and the make-or-break for whether the headline mover
is deliverable. S3 dynamic will relax it somewhat; that is the next refinement before the XLIM ask
is finalized.
