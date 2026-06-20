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
    # ==================================================================
    # CONVENTION (certified 2026-06-20, two-instance audit). The headline
    # all-in is NOT "solve + a lumped increment" -- that double-counted the
    # clean floor (lower edge 0.007) AND the bare recoil (upper edge 0.012).
    # The fix:
    #   solve = clk2 steady state = TRAFFIC-IN / POTENTIAL-OUT (clk2.py:234
    #     puts ONE ground frequency NU on all 16 internal states; excited
    #     manifolds get NO inverted potential) = the "no-squeezer" quantity
    #     AT clk2's (low) repump dwell.
    #   The ONLY honest addition is the anti-trap SQUEEZER HEAT
    #     = faithful_bulk - no_squeezer_bulk, counted ONCE.
    #   NEVER add 0.012 (= eta^2 + eta_em^2 bare recoil, ALREADY in solve via
    #     the Lamb-Dicke displacement + 1/6,2/3,1/6 emission distribution) nor
    #     0.007 (= no-squeezer bulk ~= solve itself). Both double-count.
    # ==================================================================

    # (a) solve floor [V, traffic-in / potential-out, AT LOW DWELL]
    solve_clean_lambda:  float = 0.0032
    solve_dual_end:      float = 0.0048
    solve_single_tagged: float = 0.0072      # ~= low-dwell no-squeezer bulk 0.0069 -> clean subtraction
    solve_model_band:    tuple = (0.002, 0.0076)   # recycler-model spread (~2x)

    # (b) anti-trap SQUEEZER increment = faithful - no_squeezer, ONCE
    #     [I, low-dwell, grid->clk2 transfer]. Grid (ANTITRAP_RESOLUTION.md):
    #     faithful 0.0095 - no_squeezer 0.0069 = 0.0026 ~ 0.003. Transferred onto
    #     clk2 solve because no_squeezer_grid 0.0069 ~= clk2_clean 0.0072 -- a MODEL
    #     TRANSFER, not an identity. (eta_em^2 ~ 0.003 is an INDEPENDENT cross-check,
    #     DIFFERENT physics -- do NOT tie the increment to axial_recoil_bound.)
    squeezer_increment_lowdwell: float = 0.003

    # (c) HIGH-DWELL all-in = an explicitly UNCONVERGED BRACKET, NOT a bulk. [O]
    #     Grid: no_squeezer 0.026 <= faithful <= contaminated 0.053, where the 0.053
    #     upper IS the same Fock/grid truncation artifact discarded at low dwell ->
    #     the true faithful sits BELOW it. And the grid is a REDUCED anti-trap model
    #     (no clk2 tagged-extra / multilevel structure) with no low-dwell-style
    #     cross-check at high dwell. So the honest high-dwell all-in is the clk2
    #     RE-SOLVE at the physical F'=1 dwell; this bracket is a placeholder only.
    highdwell_grid_bracket: tuple = (0.026, 0.053)  # (no-squeezer lower ; contaminated-Fock upper = ARTIFACT)
    highdwell_all_in: str = "[RETIRED, scheme is low-dwell: clk2 config-A P_e(F'1)=8.4e-6 << 4e-5 ref] grid bracket 0.026-0.053 does NOT apply; certified low-dwell floor stands. [workstation re-solve only if the dwell proxy is contested]"

    # (d) per-radius cooling floor over the radial cloud [I, traffic-in/potential-out]
    #     clk2 CLOCK-UNIT QUASI-STATIC = Boltzmann avg of nbar(r) (2026-06-20, grid_avg2.py):
    cloud_qs_clk2: tuple = (0.0056, 0.0169, 0.130)   # T_r=25/100/400uK (conservative CEILING)
    #     -> SUPERSEDES the unverified semiclassical 0.0094 as the clock-unit quasi-static @100uK
    #        (which sits below it, consistent with the MC: realized < quasi-static).
    #        MC (3-level) suppression ~0.77/0.53/0.14 => clk2 REALIZED cooling cloud ~0.004/0.009/0.019
    #        [I, cross-engine suppression]; + squeezer ~0.003 (de-risked) => cloud all-in ~0.007/0.012/0.022.
    #        STRONGLY T_r-dependent (400uK only ~53% trapped) -> the in-fiber radial T gates the cloud.
    cloud_mc_100uK:       float = 0.0094   # legacy unverified semiclassical (driver absent); see cloud_qs_clk2
    cloud_frozen_ceiling: float = 0.0126   # S2 frozen bound @100uK -- SUPERSEDED as a realized ceiling
                                           #   (dynamic MC: realized cooling floor sits BELOW quasi-static)
    # CLOUD ALL-IN = cooling(r) + squeezer integral. BOTH halves now favor the cold center:
    #   * cooling half CHARACTERIZED (dynamic MC, 2026-06-20): W(r) peaks at the cold center,
    #     anti-correlated with n_ss(r), so the limit cycle is cooling-rate-weighted -> realized sits
    #     BELOW quasi-static (frozen 0.0126 superseded; dynamics benign). 3-LEVEL ENGINE => RATIO
    #     result (suppression ~1.2x/3.0x/7.4x at 25/100/400uK in its own bracket), NOT the clock floor;
    #     clock magnitude = clk2 per-radius re-run [O].
    #   * squeezer half DE-RISKED (radial_pe.py, 2026-06-20): P_e(F'2) FALLS off-axis (1.53->0.88e-5
    #     over r=0-10um) because the M3 shift is COMMON to both legs (delta2 unchanged, dark state
    #     PRESERVED) and the field weakens -> heat rate R_sq = P_e*kernel FALLS to 0.32x at r=10. The
    #     off-axis RATE-RISE is DISPROVEN (was the feared adverse half); only the 1/W tail amplification
    #     remains, which the dwell-weighting defeats (as it did for cooling). Magnitude confirm = MC
    #     dwell-weighted integral [O, not sign-deciding].
    #   (provenance: the 0.0085 semiclassical-MC driver asserted [V] in clock_EIT_consolidated.md:99
    #    was NOT in the file set; cloud_qs_clk2 above is the verified clock-engine quasi-static ceiling.)
    cloud_all_in: str = "[I, cross-engine] cooling(r) [MC: benign, below quasi-static] + squeezer ~0.003 [de-risked: P_e falls off-axis, rate-rise disproven] => ~0.007/0.012/0.022 at T_r=25/100/400uK, STRONGLY T_r-gated. Cloud ~= single-atom if radial-cooled to ~100uK. Do NOT enter a flat 0.012/0.016."

    # repump dwell status -- MEASURED 2026-06-20 (was [O])
    repump_dwell_status: str = "[I, MEASURED] clk2 config-A F'=1 dwell P_e(F'1)=8.4e-6 -- 5x BELOW the low-dwell ref 4e-5 => firmly LOW-dwell; high-dwell branch RETIRED. Proxy: clk2 pe_F1 ~ grid P_e_rep [I, auditor to vet]; F'2 residual 1.8e-5 cross-checks dark-state ~4e-5. Squeezer increment 0.003 (at the 4e-5 ref) is thus CONSERVATIVE."

    # legacy single-photon-recoil bound (kept for CROSS-CHECK only; NOT the increment)
    axial_recoil_bound: float = round(ETA_EM**2, 4)   # ~0.003 -- numerically near squeezer, different physics

    @property
    def all_in_single_atom_lowdwell(self) -> tuple:
        """CERTIFIED low-dwell single-atom floor = solve + squeezer heat, ONCE.
        [I, low-dwell, grid->clk2 squeezer transfer]. ~ (0.008, 0.010).
        This is the ONLY certified all-in number. High-dwell and cloud are [O]
        (see highdwell_all_in / cloud_all_in). Do NOT headline a Gaussian-cloud
        band until the radial squeezer integral lands."""
        lo = self.solve_dual_end + self.squeezer_increment_lowdwell
        hi = self.solve_single_tagged + self.squeezer_increment_lowdwell
        return (round(lo, 4), round(hi, 4))      # ~ (0.008, 0.010)

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
# clock-pair RSC: DISQUALIFIED by the rank-2 obstruction (audit_C_rank2.py, verified 3 ways;
# see docs/clock_RSC_resolution.md).  The Dm=+2 clock Raman has a bounded coherence-per-scatter
# FoM (~4, detuning- & field-proof): the rank-2 electronic operator vanishes in J=1/2
# [triangle(1/2,2,1/2) fails], the coupling runs only via excited I.J (prop Delta_HFS/Delta^2),
# and the mirror-ladder geometry forces one beam onto the dark state -> off-resonant scatter
# beats the slow LD cooling 11-23:1.  raman_sbc('clock')=0.0137 is the OBSTRUCTION-FREE
# idealization (free OmR, ~0 scatter), NOT the physical floor.
RSC_CLOCK_FLOOR     = 0.45              # physical floor [FoM; DISQUALIFIED, robust to x3 scatter]
RSC_CLOCK_IDEALIZED = 0.0137            # raman_sbc('clock') Nf=10: idealized, NOT the floor
RSC_CLOCK_STATUS    = "DISQUALIFIED (rank-2 obstruction)"   # Paper T rests on this -- UNBLOCKED

# =====================================================================
# 6. SCOPE  -- the model's domain; quantities outside it are tracked, never headlined
# =====================================================================
SCOPE = {
    "dimensionality": "1D (axial only); radial mode is NOT cooled",
    "atom_picture":   "single-atom / column-averaged; ensemble OD + collisions are separate",
    "trap":           "nu_z inferred from radial freq, NOT directly measured [O]",
    "detection":      "in-fibre F2->F'3 cycling; SNR/readout tier per CLAIMS D-series (NOT re-assessed in this floor model -- do not infer a tier here)",
    "survival":       "trap lifetime / loss tier per CLAIMS S-series (NOT re-assessed in this floor model)",
}

def print_summary():
    fb = FLOOR
    print("="*70)
    print(" SSOT  --  clock-EIT cooling of %s (%s), v15 floor convention (2026-06-20 correction)" % (SPECIES, LINE))
    print("="*70)
    print(" OPERATING POINT:  Delta=%.0f  OmR=%.2f  (Om_c=%.2f, Om_p=%.2f)  delta2=%+.2f"
          % (OP.Delta_MHz, OP.OmR, OP.Omega_c_MHz, OP.Omega_p_MHz, OP.delta2_setpoint_MHz))
    print("                   2fA_tag=%.0f MHz   B_cool=%s G   eta_dp flat over %s"
          % (OP.twofA_tag_MHz, OP.B_cool_G, OP.eta_dp_range))
    print(" TRAP:  nu_z=%.3f (2pi MHz)  nu_r=%.5f  U0=%.1f MHz=%.0f uK  eta_780=%.3f  eta_2k=%.3f"
          % (NU_Z_MHZ, NU_R_MHZ, U0_MHZ, U0_UK, ETA_780, ETA_RETRO_2K))
    print("-"*70)
    print(" FLOOR BUDGET (axial <n_z>) -- convention: solve [traffic-in/potential-out] + squeezer ONCE")
    print("   solve (cooling, low-dwell):  clean %.4f | dual %.4f | single-tagged %.4f"
          % (fb.solve_clean_lambda, fb.solve_dual_end, fb.solve_single_tagged))
    print("   + anti-trap SQUEEZER (faithful-no_squeezer, low-dwell):  +%.3f  [I, grid->clk2 transfer]"
          % fb.squeezer_increment_lowdwell)
    print("   => CERTIFIED low-dwell single-atom floor:  %.3f .. %.3f  [I, low-dwell]"
          % fb.all_in_single_atom_lowdwell)
    print("   high-dwell all-in:  %s" % fb.highdwell_all_in)
    print("   cloud all-in:       %s" % fb.cloud_all_in)
    print("   repump dwell:       %s" % fb.repump_dwell_status)
    print("   model band on solve (~2x):  %s" % (fb.solve_model_band,))
    print("   [NEVER add 0.012=eta^2+eta_em^2 (already in solve) nor 0.007=no-squeezer bulk (=solve)]")
    print("-"*70)
    print(" RADIAL STATE (NOT cooled):")
    for T in (100.0, 25.0, 2.5):
        print("   T_r=%6.1f uK -> n_radial=%6.1f  | 3D ground fraction(n_z=%.3f) = %.2e"
              % (T, n_radial(T), fb.all_in_single_atom_lowdwell[0], p0_3d(fb.all_in_single_atom_lowdwell[0], T)))
    print("-"*70)
    print(" 2-photon coherence: floor doubles at %.2f kHz (sub-100 Hz => ~2.6x margin)"
          % TWO_PHOTON_DOUBLE_KHZ)
    print(" RSC (Paper T):  stretched %.5f [V] | clock-RSC %s" % (RSC_STRETCHED, RSC_CLOCK_STATUS))
    print("                 floor ~%.2f (rank-2 obstruction); %.4f is the obstruction-free idealization, not the floor"
          % (RSC_CLOCK_FLOOR, RSC_CLOCK_IDEALIZED))
    print(" SCOPE:  " + " | ".join("%s: %s" % (k, v) for k, v in SCOPE.items()))
    print("="*70)

if __name__ == "__main__":
    print_summary()
