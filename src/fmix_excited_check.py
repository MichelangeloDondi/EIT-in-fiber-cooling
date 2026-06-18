#!/usr/bin/env python3
"""
src/fmix_excited_check.py -- tracked verification of the 5P3/2 inter-F' (F'-mixing)
tensor light shift.

The 1064 nm tensor light shift is a second-order, proportional-to-I^2 effect that
mixes the four 5P3/2 hyperfine manifolds. The cooling engine
(eit_cooling_tool.excited_energies) captures it by diagonalizing
H0 - C_TENSOR*tensor_scale*T0 over all 16 |F',m'> sublevels (T0 is the bare rank-2
tensor operator). This script isolates the inter-F' ("mixing") piece -- the FULL
shift minus the block-diagonal-in-F' ("diagonal-only") shift, i.e. the part that
comes purely from coupling BETWEEN manifolds -- and locks its magnitudes, its
proportional-to-I^2 scaling, and its field (in)sensitivity.

Run:  python src/fmix_excited_check.py
      -> prints the 16-row mixing table + per-manifold I^2 scaling, then runs verify().
verify(B) raises AssertionError with a clear message on the first failure; it is wired
into audit/check.py as the [5] fmix gate.

PROVENANCE (on-axis, s=1, B=1.5 G):  F'=0,m'=0 ~ -1.52 ; F'=1,m'=0 ~ -1.64 ;
F'=2,m'=0 ~ -0.46 ; F'=3,m'=0 ~ +0.025 MHz ; per-manifold I^2 exponent p ~ 2.0.
Net effect on the included parasitics: ~1% (F'=0 probe leg) / negligible (F'=3 control
leg) -- the load-bearing point is that F'=3 (the control's |2,+1>->|F'3,0> target) is
~untouched by mixing.

KNOWN CAVEAT -- THIS GATE IS INTENTIONALLY RED (assertion 6).  The engine's
excited-state Zeeman uses gJ_5S/2 (~1.5x the true 5P3/2 hyperfine g_F), so the inter-F'
mixing is more field-dependent than it physically should be: the B = 1.5 -> 3.2288 G
shift is ~0.108 MHz (F'=2) / ~0.085 (F'=3), exceeding the < 0.05 MHz B-insensitivity
bound, and F'=3 mixing at the magic field (~0.109) slips just past the |.| < 0.10 band.
The fix is the correct excited g_F, which changes excited_energies (and therefore the
floors) -- so it is tracked separately, NOT silently relaxed here.  Assertions 1-5
(the on-axis magnitudes, the proportional-to-I^2 scaling, and the engine tie-in) PASS.
"""
import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from eit_cooling_tool import C_TENSOR, EHF, Ex, excited_energies, excited_hamiltonian

# The engine's excited_hamiltonian Jx matmul trips benign FPU flags on some BLAS
# backends (numpy 2.x / Accelerate) that np.errstate does not always catch; the
# computed values are exact (they reproduce the provenance to 4 decimals). Silence
# ONLY those matmul warnings, and only within this check script.
warnings.filterwarnings("ignore", message=".*encountered in matmul", category=RuntimeWarning)

# ---- evaluation points and assertion bands (all 2*pi MHz; kept exactly as specified) ----
B_COOL = 1.5          # cooling field (on-axis evaluation point)
B_MAGIC = 3.2288      # clock-magic field (B-insensitivity robustness point)
F2_BAND = (-0.60, -0.30)   # (3) F'=2,m'=0 mixing band
F3_ABS = 0.10              # (4) |F'=3,m'=0 mixing| upper bound
P_BAND = (1.85, 2.20)      # (5) per-manifold proportional-to-I^2 exponent band
B_SHIFT_TOL = 0.05         # (6) |mixing(B_MAGIC) - mixing(B_COOL)| upper bound -- RED (see caveat)


def _assigned(H):
    """Eigen-decompose H and assign each eigenvalue to its max-overlap |F',m'>
    sublevel -- the identical scheme used by eit_cooling_tool.excited_energies."""
    w, v = np.linalg.eigh(H)
    return {(Fp, mp): w[np.argmax(np.abs(v[Ex.index((Fp, mp)), :]) ** 2)] for (Fp, mp) in Ex}


def mixing_decomposition(B, s=1.0):
    """Return (full, diag_only, mixing) over the 16 |F',m'> sublevels at field B (G)
    and intensity scale s.
        full      = eigh(H0 - C_TENSOR*s*T0)            (the engine's computation)
        diag_only = same, but with the inter-F' blocks of T0 zeroed (block-diagonal in F')
        mixing    = full - diag_only                     (the inter-F' tensor shift)
    """
    with np.errstate(all="ignore"):     # excited_hamiltonian's Jx matmul trips benign FPU flags
        H0, T0, _ = excited_hamiltonian(B)
        T0_diag = T0.copy()
        for i, (Fi, _) in enumerate(Ex):
            for j, (Fj, _) in enumerate(Ex):
                if Fi != Fj:
                    T0_diag[i, j] = 0.0
        full = _assigned(H0 - C_TENSOR * s * T0)
        diag = _assigned(H0 - C_TENSOR * s * T0_diag)
    return full, diag, {k: full[k] - diag[k] for k in Ex}


def manifold_rms_exponent(B, Fp, scales=(1.0, 0.5, 0.25)):
    """rms-over-sublevels mixing vs intensity scale -> power-law exponent p (mixing ~ s^p).
    Returns (p, [rms at each scale])."""
    subs = [k for k in Ex if k[0] == Fp]
    rms = []
    for s in scales:
        _, _, mix = mixing_decomposition(B, s)
        rms.append(float(np.sqrt(np.mean([mix[k] ** 2 for k in subs]))))
    p = float(np.polyfit(np.log(scales), np.log(rms), 1)[0])
    return p, rms


def print_table(B=B_COOL):
    full, diag, mix = mixing_decomposition(B, 1.0)
    print("=" * 78)
    print(" 5P3/2 inter-F' tensor MIXING   (s=1, B=%.4f G)   [full - diag-only, 2pi MHz]" % B)
    print("=" * 78)
    print("   F'   m'        full     diag-only        mixing")
    for (Fp, mp) in Ex:
        print("   %d   %+d   %10.4f   %10.4f    %+9.4f"
              % (Fp, mp, full[(Fp, mp)], diag[(Fp, mp)], mix[(Fp, mp)]))
    print("-" * 78)
    print(" per-manifold rms-mixing  proportional-to-I^2  exponent p   (s = 1.0, 0.5, 0.25):")
    for Fp in (0, 1, 2, 3):
        p, rms = manifold_rms_exponent(B, Fp)
        print("   F'=%d:  p = %.3f    rms = [%.4f, %.4f, %.4f]" % (Fp, p, rms[0], rms[1], rms[2]))
    print("=" * 78)


def verify(B=B_COOL):
    """Lock the inter-F' mixing properties. Raises AssertionError (clear message) on the
    first failing check. Assertion (6), B-insensitivity, is RED on the current engine by
    design -- see the module KNOWN CAVEAT."""
    full, diag, mix = mixing_decomposition(B, 1.0)

    # (1) engine consistency: this script's full assignment == the engine's, at s=1.
    ee = excited_energies(B)
    d = max(abs(full[k] - ee[k]) for k in Ex)
    assert d < 1e-6, "engine consistency: max|full - excited_energies(%.3f)| = %.2e (>= 1e-6)" % (B, d)

    # (2) F'=0 carries NO rank-2 (triangle(0,2,0) fails): diag-only == bare centroid, and the
    #     whole F'=0 shift is mixing (< -1 MHz).
    assert abs(diag[(0, 0)] - EHF[0]) < 1e-6, \
        "F'=0,m'=0 diag-only = %.6f, expected bare centroid EHF[0] = %.6f (no rank-2 for F'=0)" \
        % (diag[(0, 0)], EHF[0])
    assert mix[(0, 0)] < -1.0, "F'=0,m'=0 mixing = %+.4f, expected < -1.0 MHz" % mix[(0, 0)]

    # (3) F'=2,m'=0 mixing band.
    assert F2_BAND[0] <= mix[(2, 0)] <= F2_BAND[1], \
        "F'=2,m'=0 mixing = %+.4f not in [%.2f, %.2f]" % (mix[(2, 0)], F2_BAND[0], F2_BAND[1])

    # (4) F'=3,m'=0 mixing ~ untouched -- load-bearing: the control's |2,+1>->|F'3,0>
    #     parasitic target stays put.
    assert abs(mix[(3, 0)]) < F3_ABS, \
        "F'=3,m'=0 |mixing| = %.4f, expected < %.2f" % (abs(mix[(3, 0)]), F3_ABS)

    # (5) proportional-to-I^2 scaling, every manifold.
    for Fp in (0, 1, 2, 3):
        p, _ = manifold_rms_exponent(B, Fp)
        assert P_BAND[0] < p < P_BAND[1], \
            "F'=%d  I^2 scaling exponent p = %.3f not in (%.2f, %.2f)" % (Fp, p, P_BAND[0], P_BAND[1])

    # (6) B-insensitivity: the mixing magnitudes should barely move to the magic field, and
    #     (3)-(4) should still hold there. RED on the current engine (gJ_5S/2 excited Zeeman).
    _, _, mix_m = mixing_decomposition(B_MAGIC, 1.0)
    for Fp in (2, 3):
        shift = abs(mix_m[(Fp, 0)] - mix[(Fp, 0)])
        assert shift < B_SHIFT_TOL, \
            "B-insensitivity: F'=%d,m'=0 mixing shifted %.4f MHz (%.3f -> %.4f G), exceeds %.2f " \
            "[engine excited Zeeman uses gJ_5S/2 ~1.5x the true 5P3/2 g_F -- tracked caveat]" \
            % (Fp, shift, B, B_MAGIC, B_SHIFT_TOL)
    assert F2_BAND[0] <= mix_m[(2, 0)] <= F2_BAND[1], \
        "B=%.4f F'=2,m'=0 mixing = %+.4f not in [%.2f, %.2f]" % (B_MAGIC, mix_m[(2, 0)], F2_BAND[0], F2_BAND[1])
    assert abs(mix_m[(3, 0)]) < F3_ABS, \
        "B=%.4f F'=3,m'=0 |mixing| = %.4f, expected < %.2f" % (B_MAGIC, abs(mix_m[(3, 0)]), F3_ABS)
    return True


if __name__ == "__main__":
    print_table(B_COOL)
    verify(B_COOL)
    print("\n  fmix verify(): PASS")
