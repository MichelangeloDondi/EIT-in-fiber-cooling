"""
radial_inhomogeneity.py
=======================

Radial (off-axis) inhomogeneity of the clock-EIT axial cooling floor for 87Rb in
the 1064 nm kagome-HCPCF lattice. Companion to eit_cooling_tool.py: that tool
computes the ON-AXIS steady-state <n_z>; this module averages it over the radial
thermal cloud in the FROZEN approximation -- radial motion is slow (nu_r << nu_z),
so each atom is treated at a fixed radius during axial cooling.

It REUSES the validated engine of eit_cooling_tool.py (run / Config) unchanged:
every local floor n_f(r) is a full multilevel steady-state solve. The only added
physics is (i) how the on-axis parameters map to radius r through the Gaussian
lattice/beam profile and (ii) the radial thermal average.

POSITION LAWS  (Gaussian lattice/beam of waist w; intensity fraction s(r)=exp(-2 r^2/w^2)):
    nu_z(r)      = nu_z(0) * sqrt(s)         trap frequency       (nu ~ sqrt(depth) ~ sqrt(I))
    eta_z(r)     = eta_z(0) * s^(-1/4)       Lamb-Dicke parameter (eta ~ nu^(-1/2))
    Omega(r)     = Omega(0) * sqrt(s)        drive Rabi           (beam attenuation, waist w)
    Delta_eff(r) = Delta(0) + c*(1 - s)      single-photon detuning WALK (see below)
    delta2(r)    = delta2(0) + d_clk*(1 - s) two-photon detuning: nearly trap-independent.
                                             The common 5S scalar cancels and (linear lattice
                                             polarization) the vector shift is zero, leaving only
                                             the small F=1/F=2 differential scalar shift d_clk.

DIFFERENTIAL-STARK DETUNING WALK
    The cooling transition |g> -> |F'2,0> has frequency E(F'2,0) - E(g); BOTH endpoints
    shift with the 1064 intensity and with OPPOSITE sign (the 5S ground is trapped, shifts
    down by U0*s; the 5P3/2 is anti-trapped, shifts up by (alpha_5P/alpha_5S)*U0*s), so the
    transition walks by their SUM:
        c = c_ground + c_excited,
        c_ground  = U0                          (5S ground scalar,  ~22.8 MHz at full depth)
        c_excited = (alpha_5P/alpha_5S)*U0       (5P3/2 scalar,      ~38.1 MHz at full depth)
    On axis (s=1) the laser is referenced to the in-trap transition, so Delta(0) is the set
    detuning and the walk is zero. Off axis (s<1) the transition moves blue by c*(1-s), which
    detunes the EIT cooling (the bright peak no longer sits on the red sideband). Both
    contributions are real and ADD; the booleans include_ground_stark / include_excited_stark
    isolate each. (Setting both False reproduces the no-walk model used by radial_frozen.py.)

    Note: the F=1 vs F=2 differential ground scalar polarizability (the clock light shift) is a
    SEPARATE, much smaller effect, included via delta2_eff (see below).

DIFFERENTIAL CLOCK SCALAR SHIFT  (the F=1/F=2 6.8 GHz differential)
    The 5S scalar polarizability differs very slightly between F=1 and F=2 because the optical
    transition frequencies from the two ground states differ by the 6.835 GHz hyperfine
    splitting (dispersion of the D1/D2 polarizability). This shifts the two-photon (clock)
    resonance with intensity:
        delta2_eff(r) = delta2(0) + d_clk*(1 - s),   d_clk = (dalpha/alpha)*U0,
    with (dalpha/alpha) = (alpha_F2 - alpha_F1)/alpha ~ 6.1e-5 computed from the D-line
    dispersion (clock_diff_ratio()), giving d_clk ~ 1.4 kHz at full depth. This is the dominant
    1064 nm CLOCK light shift, but it is ~1% of the cooling feature width, so its effect on the
    cooling floor is negligible (quantified in report()). Toggle with include_clock_diff_stark.

THERMAL CLOUD AVERAGE
    Frozen 2D-harmonic radial distribution P(r) ~ r*exp(-r^2/r_rms^2), r_rms = w*sqrt(T/(2 U0)).
    Reported: the local floor at the rms radius, the cloud-averaged <n_f>, and the fraction of
    the cloud cooled below a threshold. Valid while T << U0 (deeply bound, near-harmonic).

VALIDATION
    On axis (r=0, s=1) every model reduces to eit_cooling_tool.run() and reproduces its floor.

SCOPE / CAVEAT
    The per-atom solve uses the engine's Fock truncation (default Nf=6) and the Lamb-Dicke /
    steady-state picture. Where the local floor grows large (far off-axis, or hot clouds), both
    are stretched, so large n_f(r) values and the warm-cloud averages are INDICATIVE, not
    precise; the cooled-fraction and the T_rad <~ 100 uK cloud averages are the robust outputs.

USAGE
    python radial_inhomogeneity.py            # local-floor profile + cloud averages (slow)
    >>> from radial_inhomogeneity import report, radial_profile, cloud_average, setup
    >>> report()

AUTHORSHIP / LICENSE
    Michelangelo Dondi, michelangelo.dondi@unibo.it -- Cold-atoms group of Prof. F. Minardi,
    Department of Physics and Astronomy, University of Bologna. License: MIT.
"""
import numpy as np
from eit_cooling_tool import Config, preset, run, replace, SCALAR_RATIO_5P_5S, KB_OVER_H

__version__ = "0.1.0"

WAIST_UM = 19.0     # lattice / cooling-beam waist (S1 position laws)

# D-line data for the F=1/F=2 differential scalar polarizability (the 1064 nm clock light shift).
# Frequencies in THz; reduced dipole matrix elements |<J||d||J'>|^2 in atomic units (Steck).
_LATTICE_THZ = 299792.458 / 1064.0
_A_HFS_THZ   = 6.834682610e-3                       # ground hyperfine splitting (6.835 GHz)
_DLINES = [(299792.458 / 794.978, 4.227**2),        # D1: 5S1/2 -> 5P1/2
           (299792.458 / 780.241, 5.977**2)]        # D2: 5S1/2 -> 5P3/2


def clock_diff_ratio():
    """(alpha_F2 - alpha_F1)/alpha for the 5S clock states at 1064 nm, from the D1/D2 dispersion.
       The optical transitions from F=1 lie A_HFS above those from F=2, so the scalar
       polarizabilities differ slightly; g(nu0)=nu0/(nu0^2 - nu_lattice^2)."""
    g = lambda n0: n0 / (n0**2 - _LATTICE_THZ**2)
    num = sum(d2 * (g(n0) - g(n0 + _A_HFS_THZ)) for n0, d2 in _DLINES)
    den = sum(d2 * g(n0) for n0, d2 in _DLINES)
    return num / den


def clock_diff_shift(base: Config):
    """Differential clock scalar shift at full trap depth (2pi MHz): (dalpha/alpha)*U0 (~1.4 kHz)."""
    return clock_diff_ratio() * base.U0_uK * KB_OVER_H


def _trapz(y, x):
    return (np.trapezoid if hasattr(np, "trapezoid") else np.trapz)(y, x)


def setup(base: Config = None):
    """On-axis anchor: servo delta2 once. Returns (base, delta2_star, Omega_tot0, n_axis)."""
    base = replace(preset("dual_end_optimal"), N_f=6) if base is None else base
    n0, d2star = run(base)
    Otot0 = np.sqrt(4.0 * base.Delta * base.nu_z) if base.Omega_tot_abs is None else base.Omega_tot_abs
    return base, d2star, Otot0, n0


def stark_coeff(base: Config, include_ground_stark=True, include_excited_stark=True):
    """Detuning-walk coefficient c (2pi MHz): c_ground + c_excited (each toggleable)."""
    U0 = base.U0_uK * KB_OVER_H
    return ((U0 if include_ground_stark else 0.0)
            + (SCALAR_RATIO_5P_5S * U0 if include_excited_stark else 0.0))


def local_floor(r_um, base, d2star, Otot0, include_ground_stark=True,
                include_excited_stark=True, include_clock_diff_stark=True, w=WAIST_UM):
    """Steady-state <n_z> for an atom frozen at radius r (one full engine solve).
       include_ground_stark / include_excited_stark toggle the single-photon detuning walk;
       include_clock_diff_stark toggles the F=1/F=2 differential clock shift (the delta2 walk)."""
    s = np.exp(-2.0 * r_um**2 / w**2)
    c = stark_coeff(base, include_ground_stark, include_excited_stark)
    d2 = d2star + (clock_diff_shift(base) * (1.0 - s) if include_clock_diff_stark else 0.0)
    cfg = replace(base, servo_delta2=False, delta2=d2,
                  nu_z=base.nu_z * np.sqrt(s), eta_z=base.eta_z * s**-0.25,
                  Omega_tot_abs=Otot0 * np.sqrt(s), Delta=base.Delta + c * (1.0 - s))
    return run(cfg)[0]


def radial_profile(rgrid, base, d2star, Otot0, **stark):
    return np.array([local_floor(r, base, d2star, Otot0, **stark) for r in rgrid])


def r_rms(T_uK, base, w=WAIST_UM):
    """2D-harmonic radial rms radius of a thermal cloud at temperature T_uK."""
    return w * np.sqrt(T_uK / (2.0 * base.U0_uK))


def cloud_average(rgrid, nf, T_uK, base, thr=0.1, w=WAIST_UM):
    """Frozen thermal average of n_f(r) over the radial cloud.
       Returns {r_rms, nf_at_rms, nf_cloud, cooled_frac}."""
    rr = r_rms(T_uK, base, w)
    x = np.linspace(0.0, min(4.0 * rr, rgrid[-1]), 800)
    P = x * np.exp(-x**2 / rr**2); P /= _trapz(P, x)
    nfi = np.interp(x, rgrid, nf)
    return dict(r_rms=float(rr), nf_at_rms=float(np.interp(rr, rgrid, nf)),
                nf_cloud=float(_trapz(P * nfi, x)),
                cooled_frac=float(_trapz(P * (nfi < thr), x)))


def report(base=None, rgrid=None, temps=(25.0, 100.0, 400.0)):
    """Local-floor profile and cloud averages for the three Stark-walk models."""
    base, d2star, Otot0, n0 = setup(base)
    rgrid = np.array([0, 1.5, 3, 4.5, 6, 7.5, 9, 10.5, 12.0]) if rgrid is None \
        else np.asarray(rgrid, float)
    models = [("none (c=0)", dict(include_ground_stark=False, include_excited_stark=False,
                                  include_clock_diff_stark=False)),
              ("excited-only", dict(include_ground_stark=False, include_excited_stark=True,
                                    include_clock_diff_stark=False)),
              ("full ground+excited", dict(include_ground_stark=True, include_excited_stark=True,
                                           include_clock_diff_stark=False))]
    NF = {nm: radial_profile(rgrid, base, d2star, Otot0, **kw) for nm, kw in models}
    cg, ce = stark_coeff(base, True, False), stark_coeff(base, False, True)
    d_clk = clock_diff_shift(base)

    print("=" * 80)
    print(" RADIAL INHOMOGENEITY OF THE COOLING FLOOR  (frozen thermal cloud)")
    print("=" * 80)
    print("on-axis floor=%.5f  servo delta2*=%+.3f   c_ground=%.1f  c_excited=%.1f  c_full=%.1f MHz"
          % (n0, d2star, cg, ce, cg + ce))
    print("F=1/F=2 differential scalar (6.8 GHz): (da/a)=%.2e -> d_clk=%.4f kHz (delta2 walk) at full depth"
          % (clock_diff_ratio(), d_clk * 1e3))
    print("\nLOCAL FLOOR n_f(r)  [single-photon detuning walk; delta2 fixed]:")
    print("  r (um)        " + "  ".join("%7.1f" % r for r in rgrid))
    for nm, _ in models:
        print("  %-20s " % nm + "  ".join("%7.4f" % v for v in NF[nm]))
    print("\nCLOUD AVERAGES (cooled fraction = P(n_f < 0.1)):")
    for T in temps:
        print("  T_rad = %4.0f uK:" % T)
        for nm, _ in models:
            c = cloud_average(rgrid, NF[nm], T, base)
            print("     %-20s r_rms=%4.2f um  n_f(r_rms)=%.4f  <n_f>_cloud=%.4f  cooled=%3.0f%%"
                  % (nm, c["r_rms"], c["nf_at_rms"], c["nf_cloud"], 100 * c["cooled_frac"]))

    # Effect of the F=1/F=2 differential clock shift (delta2 walk), on top of the full walk:
    nf_clk = radial_profile(rgrid, base, d2star, Otot0, include_ground_stark=True,
                            include_excited_stark=True, include_clock_diff_stark=True)
    print("\nF=1/F=2 DIFFERENTIAL CLOCK SHIFT -- effect on the cooled floor (added to the full walk):")
    for T in temps:
        a = cloud_average(rgrid, NF["full ground+excited"], T, base)["nf_cloud"]
        b = cloud_average(rgrid, nf_clk, T, base)["nf_cloud"]
        print("     T_rad=%4.0f uK:  <n_f>_cloud %.5f -> %.5f   (change %+.2e, %+.2f%%)"
              % (T, a, b, b - a, 100 * (b - a) / a if a else 0.0))
    print("=" * 80)


if __name__ == "__main__":
    report()
