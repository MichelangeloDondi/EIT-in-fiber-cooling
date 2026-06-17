"""
operating_point.py  --  SINGLE SOURCE OF TRUTH (SSOT) for the clock-EIT program.

Every canonical number lives here ONCE: physical constants, the cooling
operating point, and the floor budget (solve -> +anti-trap/leak -> all-in, with
the model band).  Engines, figures, and docs should defer to this module; the
audit checker (audit/check.py) asserts that the rest of the repo agrees with it.

Conventions (stated once):
  * All optical detunings / Rabi frequencies are ANGULAR, quoted as ordinary
    frequency in 2*pi*MHz (a "45" means 2*pi*45 MHz).  Trap frequencies likewise
    (nu_z = 0.430 -> 2*pi*430 kHz).
  * Reference for optical frequencies: the bare |F=2> -> |F'=2> transition = 0 MHz;
    bluer = more positive.
  * delta2 SIGN CONVENTION = the tagged_solver convention: the servo set-point is
    a small POSITIVE offset from the bare two-photon resonance (the e3 admixture
    Stark-shifts |2,+1>, so the cooling optimum sits at +delta2).  Some prose docs
    historically wrote this negative; the positive convention here (matching the
    validated engine and the figures) is authoritative.

Tags used in comments: [V] computed/verified in-program, [I] inferred/estimate,
[O] open / bench-gated, [ASSERTED] stated but not reproduced by an engine.
"""
from __future__ import annotations
from dataclasses import dataclass, field

# =====================================================================
# 1. PHYSICAL CONSTANTS  (fixed; not knobs)
# =====================================================================
SPECIES        = "87Rb"
LINE           = "D2"
A_HFS_MHZ      = 6834.682610            # ground hyperfine splitting [V]
GAMMA_D2_MHZ   = 6.07                   # 2*pi*MHz, natural linewidth D2
GAMMA_D1_MHZ   = 5.746                  # 2*pi*MHz, natural linewidth D1
G_F2, G_F1     = +0.5, -0.5            # ground Lande g-factors
MAGIC_B_G      = 3.2288                 # clock magic field -- INTERROGATION ONLY, not cooling

# 5P3/2 hyperfine centroids relative to the line centroid (MHz) [V]
HF_5P32_MHZ    = {0: -302.07, 1: -229.85, 2: -72.91, 3: +193.74}
F3_ABOVE_F2_MHZ = 266.65

# trap (in-fibre 1064 nm axial lattice; kagome K19, 48 um core, w ~ 19 um)
NU_Z_MHZ       = 0.430                  # axial (stiff, cooled) = 2*pi*430 kHz  [I: w1064 inferred, O: measure directly]
NU_R_MHZ       = 0.00542               # radial (soft, degenerate, NOT cooled) = 2*pi*5.42 kHz
U0_MHZ         = 22.8                   # trap depth
U0_UK          = 1094.0                 # = U0 in temperature units
LATTICE_NM     = 532.0
ETA_780        = 0.094                  # Lamb-Dicke, single 780 photon, axial
ETA_RETRO_2K   = 0.187                  # effective Lamb-Dicke, retro (2k) -- the Raman/thermometry value
ETA_EM         = ETA_780 / 3**0.5      # emission Lamb-Dicke ~ 0.054
B_FICT_G_PER_CIRC = 0.336              # vector light shift = fictitious B per unit circular [V, Audit-C]

# =====================================================================
# 2. OPERATING POINT  (v14; supersedes the Delta=80/OmR=0.25 memo AND the
#    Delta=55/OmR=0.10 v12 point)
# =====================================================================
@dataclass(frozen=True)
class OperatingPoint:
    Delta_MHz: float = 45.0            # single-photon, blue of F'=2; flat optimum 40-55 [V]
    OmR: float = 0.12                  # Omega_p / Omega_c (the weaker-probe lever) [V]
    Omega_c_MHz: float = 8.74          # pinned to EIT condition Omega_tot = sqrt(4*Delta*nu_z)
    Omega_p_MHz: float = 1.05
    delta2_setpoint_MHz: float = +0.25  # servoed to the dark resonance; POSITIVE convention (see header)
    B_cool_G: tuple = (1.0, 1.5)       # cooling field range (field-insensitive pair -> any B works)
    twofA_tag_MHz: float = 400.0       # single-ended tagged retro: 200 MHz AOM double-passed (down-shift)
    eta_dp_range: tuple = (0.20, 0.50) # retro double-pass reflectivity -- floor flat across this range

OP = OperatingPoint()

# two-photon coherence budget [V, audit_brief_v12_noise]: the clock-EIT floor DOUBLES at this
# two-photon (NOT laser) linewidth.  Sub-100 Hz target => ~2.6x margin only.
TWO_PHOTON_DOUBLE_KHZ = 0.26

# =====================================================================
# 3. FLOOR BUDGET  -- the headline must be the ALL-IN floor, not the solve floor
# =====================================================================
@dataclass(frozen=True)
class FloorBudget:
    # (a) axial cooling-physics floor from the multilevel tagged solver
    #     (delta2-optimized, N_f-stable, tagged-extra-inclusive)  [V]
    solve_clean_lambda: float = 0.0032
    solve_dual_end:     float = 0.0048
    solve_single_tagged: float = 0.0072      # at 2fA=400, OmR=0.12
    solve_model_band:   tuple = (0.002, 0.0076)  # recycler-model spread (~2x): 3-level/multilevel/full
    # (b) separately-budgeted increment added for the ALL-IN system floor [I]
    antitrap_leak_increment: tuple = (0.007, 0.012)
    # (c) radial-inhomogeneity cloud floor @100 uK, Delta=45 (semiclassical MC) [I]
    cloud_floor_100uK: float = 0.0094
    # (d) fundamental axial single-photon-recoil bound
    axial_recoil_bound: float = round(ETA_EM**2, 4)   # ~0.003

    @property
    def all_in_single_atom(self) -> tuple:
        """ALL-IN single-atom floor = solve (dual..single) + anti-trap/leak increment.
        This is the number that should be headlined, NOT the bare solve floor."""
        lo = self.solve_dual_end + self.antitrap_leak_increment[0]
        hi = self.solve_single_tagged + self.antitrap_leak_increment[1]
        return (round(lo, 4), round(hi, 4))      # ~ (0.012, 0.019)

FLOOR = FloorBudget()

# =====================================================================
# 4. RADIAL STATE  -- the scheme does NOT cool this mode (1D cooler)
# =====================================================================
HBAR_NU_R_OVER_KB_UK = NU_R_MHZ * 1e6 * 4.79924e-5  # ℏν_r/k_B in uK  (h/k_B = 4.79924e-5 uK/Hz)

def n_thermal(T_uK: float, nu_MHz: float) -> float:
    """Mean occupation of a mode of frequency nu_MHz (2*pi*MHz) at temperature T_uK."""
    x = (nu_MHz * 1e6 * 4.79924e-5) / T_uK     # ℏν/k_BT
    import math
    return 1.0 / (math.exp(x) - 1.0)

def n_radial(T_uK: float) -> float:
    return n_thermal(T_uK, NU_R_MHZ)

def p0_3d(nbar_z: float, T_radial_uK: float) -> float:
    """3D ground-state fraction = P0(axial) * P0(radial)^2 for a thermal state."""
    nz, nr = nbar_z, n_radial(T_radial_uK)
    return (1.0/(nz+1.0)) * (1.0/(nr+1.0))**2

# =====================================================================
# 5. RSC COMPARISON FLOORS  (for Paper T)
# =====================================================================
RSC_STRETCHED = 0.00196                 # field-SENSITIVE pair [V, engine self-test]
# clock-pair RSC: UNRESOLVED.  scheme_comparison.md asserts ~0.45 (analytic rank-2 depumping);
# raman_sbc.py engine returns 0.0137 (Nf=10, won't converge higher).  DO NOT headline either.
RSC_CLOCK_DOC_ASSERTED = 0.45           # [ASSERTED, not reproduced]
RSC_CLOCK_ENGINE_NF10  = 0.0137         # [V at Nf=10, lower bound]
RSC_CLOCK_STATUS = "OPEN"               # gate Paper T on the high-Nf recompute

# =====================================================================
# 6. SCOPE  -- the model's domain; quantities outside it are tracked, never headlined
# =====================================================================
SCOPE = {
    "dimensionality": "1D (axial only); radial mode is NOT cooled",
    "atom_picture":   "single-atom / column-averaged; ensemble OD + collisions are separate",
    "trap":           "nu_z inferred from radial freq, NOT directly measured [O]",
    "detection":      "in-fibre F2->F'3 cycling assumed; SNR budget not closed [O]",
}

def print_summary():
    fb = FLOOR
    print("="*70)
    print(" SSOT  --  clock-EIT cooling of %s (%s), v14 operating point" % (SPECIES, LINE))
    print("="*70)
    print(" OPERATING POINT:  Delta=%.0f  OmR=%.2f  (Om_c=%.2f, Om_p=%.2f)  delta2=%+.2f"
          % (OP.Delta_MHz, OP.OmR, OP.Omega_c_MHz, OP.Omega_p_MHz, OP.delta2_setpoint_MHz))
    print("                   2fA_tag=%.0f MHz   B_cool=%s G   eta_dp flat over %s"
          % (OP.twofA_tag_MHz, OP.B_cool_G, OP.eta_dp_range))
    print(" TRAP:  nu_z=%.3f (2pi MHz)  nu_r=%.5f  U0=%.1f MHz=%.0f uK  eta_780=%.3f  eta_2k=%.3f"
          % (NU_Z_MHZ, NU_R_MHZ, U0_MHZ, U0_UK, ETA_780, ETA_RETRO_2K))
    print("-"*70)
    print(" FLOOR BUDGET (axial <n_z>):")
    print("   solve (cooling physics):  clean %.4f | dual %.4f | single-tagged %.4f"
          % (fb.solve_clean_lambda, fb.solve_dual_end, fb.solve_single_tagged))
    print("   + anti-trap/leak increment:  +%.3f..%.3f" % fb.antitrap_leak_increment)
    print("   => ALL-IN single-atom floor (HEADLINE):  %.3f .. %.3f" % fb.all_in_single_atom)
    print("   cloud inhomogeneity @100uK (Delta=45):   %.4f" % fb.cloud_floor_100uK)
    print("   axial recoil bound (eta_em^2):           %.4f" % fb.axial_recoil_bound)
    print("   model band on solve floor (~2x):         %s" % (fb.solve_model_band,))
    print("-"*70)
    print(" RADIAL STATE (NOT cooled):")
    for T in (100.0, 25.0, 2.5):
        print("   T_r=%6.1f uK -> n_radial=%6.1f  | 3D ground fraction(n_z=%.3f) = %.2e"
              % (T, n_radial(T), fb.all_in_single_atom[0], p0_3d(fb.all_in_single_atom[0], T)))
    print("-"*70)
    print(" 2-photon coherence: floor doubles at %.2f kHz (sub-100 Hz => ~2.6x margin)"
          % TWO_PHOTON_DOUBLE_KHZ)
    print(" RSC (Paper T):  stretched %.5f [V] | clock-RSC %s (doc %.2f / engine %.4f)"
          % (RSC_STRETCHED, RSC_CLOCK_STATUS, RSC_CLOCK_DOC_ASSERTED, RSC_CLOCK_ENGINE_NF10))
    print(" SCOPE:  " + " | ".join("%s: %s" % (k, v) for k, v in SCOPE.items()))
    print("="*70)

if __name__ == "__main__":
    print_summary()
