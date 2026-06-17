"""
eit_cooling_tool.py
===================

Steady-state and dynamics model of clock-EIT (electromagnetically-induced-
transparency) ground-state sideband cooling of 87Rb in a one-dimensional 1064 nm
optical lattice formed inside a kagome hollow-core photonic-crystal fibre (HCPCF).

OVERVIEW
    Given a single Config object specifying every experimentally adjustable
    parameter -- detunings, Rabi frequencies, the beam-delivery configuration, the
    phase-modulator settings, the repumpers, the trap, the magnetic field, and the
    initial temperatures -- the tool returns:
      (1) the explicit optical spectrum delivered to the atoms (every tone:
          frequency, Rabi frequency, polarization, propagation direction, and the
          nearest atomic resonance), with parasitic near-resonances flagged;
      (2) the steady-state mean axial phonon number <n_z> from a multilevel
          open-system (Lindblad) solver, with the populations and the true
          motional Fock distribution;
      (3) the cooling dynamics (asymptotic rate and time-to-cool from a given
          initial temperature) and a check of whether the operating point lies in
          the regime where this steady-state treatment is valid.
    Parameter sweeps, two-dimensional maps, the two-photon-detuning landscape, and
    a key-performance-indicator scan over any parameter are also provided.

PHYSICAL SYSTEM
    Atom            87Rb, D2 line (5S_1/2 -> 5P_3/2), Gamma = 2*pi*6.07 MHz.
    Cooling Lambda  the clock pair |F=1,m=-1> (probe, sigma+) and |F=2,m=+1>
                    (control, sigma-), both closing on |F'=2,m'=0>. Both ground
                    states have g_F m_F = +1/2, so the two-photon resonance is
                    magnetic-field insensitive at any field.
    Trap            axial (cooled) frequency  nu_z = 2*pi*430 kHz;
                    radial (spectator)        nu_r = 2*pi*5.42 kHz;
                    depth U0 ~ 1094 uK; axial Lamb-Dicke parameter eta_z = 0.094.
    Field           cooling at B = 1 G along the fibre axis; clock interrogation
                    at the magic field 3.2288 G (a separate phase, not modelled).

ARCHITECTURE
    Two logically distinct parts, both contained in this one file:
      * The beam-delivery / spectrum model (Section 3) maps the hardware knobs --
        phase-modulation depth and frequency, sideband orders, the tagging AOM and
        quarter-wave plate, the retro efficiency -- onto the explicit set of
        optical tones at the atoms. This is where the delivery architectures
        (dual-end, single-end tagged retro, ideal clean-Lambda) differ.
      * The atomic engine (Section 6) is a multilevel QuTiP steady-state solver
        (8-state Breit-Rabi ground manifold; tensor-diagonalized 5P_3/2, F'=0..3;
        Clebsch-Gordan dipole couplings; a breadth-first multi-rotating frame;
        m-resolved hyperfine decay; three-point photon recoil; the coherent
        |F'=3,0> control admixture). It is included verbatim from the solver
        validated during this study; the regression gate (Section 6b) reproduces
        the validated floors, so the numbers reported here are identical to the
        benchmarked ones.

TABLE OF CONTENTS
    Section 1   physical constants of 87Rb and electromagnetism
    Section 2   Config (all adjustable parameters) and named operating points
    Section 3   beam-delivery / optical-spectrum model
    Section 4   optical-spectrum table with resonance annotation
    Section 5   fast self-tests on the delivery model
    Section 6   multilevel atomic engine and Config adapter
    Section 6b  physics regression gate (reproduces the validated floors)
    Section 6c  cooling dynamics and regime/validity diagnostics
    Section 7   single operating-point report
    Section 8   parameter sweeps, maps, and KPI scans

UNITS  (fixed convention, stated once)
    * All optical frequencies, detunings and Rabi frequencies are ANGULAR,
      expressed as ordinary frequency in 2*pi*MHz  (i.e. a "5" means 2*pi*5 MHz).
    * Trap frequencies likewise (nu_z = 0.430 means 2*pi*430 kHz).
    * The single REFERENCE for every optical frequency is the bare
      |F=2> -> |F'=2> transition, defined as 0 MHz. "Bluer" = more positive.
      A field's detuning from any transition is (field frequency) - (transition
      frequency); the engine knows all transition frequencies, so this one
      reference fixes everything.

SIGN / KNOB CONVENTIONS
    * Delta > 0 is BLUE of |F'=2> (blue-detuned EIT cooling).
    * delta2 is the PRIMARY two-photon knob; the EOM drive f_mod is DERIVED from
      it per configuration (Section 3). A numeric f_mod overrides, and then
      delta2 is reported back as the derived value.

DETUNING REFERENCE  (subtle with the 1064 nm trap -- read before trusting a number)
    The engine carries BARE internal energies (Breit-Rabi grounds + tensor-
    diagonalized 5P3/2); it contains no 1064 Stark term. The 1064 shifts split
    into: ground scalar -U0 (the trap, common to both clock grounds); a common
    5P3/2 scalar ~+37 MHz; and an F'- and m'-dependent TENSOR part (exactly zero
    for F'=2, nonzero for F'=0,1,3 and dependent on the lattice polarization
    angle theta). Therefore:
      * delta2 (two-photon): referenced to the ground hyperfine splitting. The 5S
        scalar shift common to |1,-1> and |2,+1> CANCELS, so delta2 is trap-
        independent to leading order and delta2=0 is the dark resonance at every
        radius. The residual is the small F=1/F=2 differential scalar shift from
        the 6.835 GHz hyperfine splitting (~6e-5 of U0, ~1.4 kHz*(1-s)): the
        dominant 1064 nm clock light shift, but negligible for cooling (~1% of the
        cooling feature). For a linear lattice polarization the vector shift is
        zero. The radial walk is modelled in radial_inhomogeneity.py.
      * Delta (single-photon): referenced to the ACTUAL in-trap, on-axis
        (trap-bottom) |F'2,0> transition. The |F'2,0> scalar (+38) and ground
        (-U0) shifts are a common ~+61 MHz offset that cancels (the engine only
        uses Delta = laser - |F'2,0>), so the number you set IS the on-axis
        in-trap detuning. Radial variation Delta_eff(r)=Delta+61*(1-s) is added
        by the companion radial Monte-Carlo analysis. (Exact.)
      * Repump & contaminant detunings (current limitation): referenced to BARE
        5P3/2 hyperfine spacings; the differential TENSOR Stark shift of the
        target level vs |F'2,0> is OMITTED. ~0 for F'=2 targets (rep2 option C),
        but up to ~12-16 MHz for F'=1 (rep1, rep2 option A, dominant F'1
        contaminant) and theta-dependent. So Drep1=15 is 15 MHz from the BARE
        F=1->F'1 line, which can be ~2x off the actual in-trap detuning. This is
        addressed by the planned polarization-angle-aware Stark treatment that
        references every detuning to its in-trap on-axis transition (see ROADMAP).

VALIDATION
    The embedded engine reproduces the independently obtained steady-state floors
    (run with --regression): clean-Lambda recoil limit 0.0072; clean base 0.0014;
    with the F'=1 / F'=3 / F'=0 contaminants 0.0048 / 0.0024 / 0.0015; full
    dual-end 0.0048; full single-end 0.0075. The regression is evaluated at the
    magic field, at which those reference values were generated; the cooling floor
    is field-insensitive (|Delta<n_z>| <= 0.0003 between 1 G and 3.2288 G), so the
    1 G cooling default and the regression anchor agree.

ROADMAP
    * A polarization-angle-aware a.c.-Stark treatment that references the repumper
      and contaminant detunings to the in-trap on-axis transitions (the geometry
      is B = 1 G along the fibre axis, so the axial 1064 nm field is transversely
      polarized, theta = 90 deg).
    * Promotion of the currently-flagged parasitics (dual-end carrier leak;
      single-end down-shifted retro carrier) from spectrum flags to full coherent
      beams in the engine, re-validated against the present engine in the
      dual-end limit.

USAGE
    python eit_cooling_tool.py               spectrum tables + fast self-tests
    python eit_cooling_tool.py --report      full operating-point reports
    python eit_cooling_tool.py --regression  reproduce the validated floors
    python eit_cooling_tool.py --sweeps      write example sweep figures (PNG)
    python eit_cooling_tool.py --kpi         example KPI-vs-parameter scans (PNG)

    >>> from eit_cooling_tool import Config, preset, run, report, cooling_dynamics
    >>> nbar, delta2 = run(preset("dual_end_optimal"))
    >>> report(preset("dual_end_optimal"))

REQUIREMENTS
    Python 3.9+, numpy, scipy, qutip (>= 5), sympy; matplotlib for the figures.

AUTHORSHIP
    Author / maintainer:  Michelangelo Dondi, e-mail: michelangelo.dondi@unibo.it
    Cold-atoms group of Prof. F. Minardi, Department of Physics and Astronomy,
    University of Bologna.
    License:  MIT

REFERENCES
    [1] D. A. Steck, "Rubidium 87 D Line Data" (atomic-structure constants).
    [2] G. Morigi, J. Eschner, C. H. Keitel, Phys. Rev. Lett. 85, 4458 (2000)
        -- ground-state cooling via electromagnetically induced transparency.
    [3] G. Morigi, Phys. Rev. A 67, 033402 (2003) -- EIT cooling theory.
    [4] J. R. Johansson, P. D. Nation, F. Nori, Comput. Phys. Commun. 184, 1234
        (2013) -- QuTiP.
"""

from dataclasses import dataclass, replace
from typing import Optional, Union, List
import numpy as np
from scipy.special import jv          # Bessel J_n, for the phase-EOM sideband comb
from scipy.optimize import brentq     # used to invert beta <-> probe/control ratio
import qutip as qt                                            # engine (Section 6)
from sympy.physics.wigner import clebsch_gordan, wigner_6j    # CG and 6j (Section 6)
from sympy import S

__version__ = "0.3.0"
# CHANGELOG (bump on every physics/interface change; update README + report + regression too)
#   0.2.4  Documentation correction: the two-photon detuning delta2 is trap-independent only to
#          leading order. The 5S scalar shift common to both clock states cancels, but the small
#          F=1/F=2 differential scalar shift (6.835 GHz hyperfine dispersion, ~6e-5 of U0,
#          ~1.4 kHz*(1-s)) remains -- the dominant 1064 nm clock light shift, negligible for
#          cooling. The detuning-reference section is corrected accordingly; the radial walk of
#          both detunings is modelled in the companion radial_inhomogeneity.py. No code change.
#   0.2.3  Fix the cooling-rate (Liouvillian-gap) eigensolve. It used ARPACK shift-invert at
#          sigma=0, which coincides with the Liouvillian's exact zero (steady-state) eigenvalue
#          and is therefore singular -- yielding spurious near-zero modes and a non-reproducible
#          rate (occasionally wrong by ~100x). It now uses a small negative shift (sigma=-1e-5,
#          off the zero eigenvalue), a fixed start vector (deterministic, identical run-to-run),
#          and a rate floor that discards the steady-state mode. The steady-state floor and the
#          regression are unaffected (they never used this routine); only W, tau and the
#          time-to-cool estimates are affected, and they are now reproducible.
#   0.2.2  Documentation revision for external release: the module header is rewritten as a
#          standalone scientific document (overview, physical system, architecture, validation,
#          roadmap, usage, authorship, references) and the section banners and comments are
#          professionalized. No functional change -- the code, the validated floors and the
#          regression are byte-for-byte identical to 0.2.1.
#   0.2.1  default B_field -> 1 G (the COOLING field: vertical, || fiber axis), since the tool
#          computes the cooling phase; 3.2287 G (clock-magic) is interrogation-only. The cooling
#          dark pair |1,-1>/|2,+1> is field-insensitive, so the floor is essentially B-independent
#          -- verified |d<n_z>| <= 0.0003 between 1 G and 3.2287 G for dual- and single-end. The
#          regression is pinned at 3.2287 G to keep the validated baseline as an exact fidelity
#          anchor; report() now labels the field (cooling vs interrogation).
#   0.2.0  cooling dynamics & regime: initial axial/radial T knobs; cooling_dynamics()
#          (tau=1/gap via the validated delta_tau method; time-to-<n>=0.1 and to 2x floor
#          from T_axial_init); regime block in report() (Lamb-Dicke, EIT sideband
#          resolution & tuning, n_init-vs-Nf, radial trapping + Delta_eff inhomogeneity);
#          report() now uses the true P(n=0) from the Fock diagonal. Floor/regression
#          unchanged (initial T affects only time & regime, not the steady state).
#   0.1.0  spectrum/delivery layer; embedded validated engine + Config adapter;
#          regression gate; self-documenting report; sweeps/plots; kpi_scan.
#          KNOWN LIMITATION (-> v0.3.0): repump & contaminant detunings referenced to BARE
#          5P3/2 spacings -- differential TENSOR 1064 Stark shift omitted (~0 for F'=2; up
#          to ~12-16 MHz for F'=1, theta-dep). Delta & delta2 exact. See "DETUNING REFERENCE".


# =============================================================================
# SECTION 1 -- PHYSICAL CONSTANTS OF 87Rb AND ELECTROMAGNETISM
# -----------------------------------------------------------------------------
# Atomic-structure and electromagnetic constants. Apparatus-dependent quantities
# (trap frequencies, lattice depth, magnetic field, Lamb-Dicke parameter) are
# configurable and live in Config (Section 2). Atomic data follow Steck,
# "Rubidium 87 D Line Data" (reference [1] in the module header).
# =============================================================================

A_HFS = 6834.682610          # 87Rb 5S_1/2 ground hyperfine splitting (2pi MHz).
                             #   E(F=2) - E(F=1) = +A_HFS, i.e. F=2 lies ABOVE F=1,
                             #   so a transition FROM F=1 to a given F' is A_HFS
                             #   HIGHER in frequency than the same transition FROM F=2.

GAMMA_D2 = 6.07              # 5P_3/2 natural linewidth (2pi MHz).
GAMMA_D1 = 5.746             # 5P_1/2 (kept for reference; this tool is D2).

# Lande / nuclear constants for the ground-state Breit-Rabi energies (engine, Sec 6):
gJ_5S, gI_87, uB_MHzG, I_87 = 2.00233, -0.0009951, 1.399624, 1.5   # uB/h in MHz/G

# 5P_3/2 hyperfine CENTROID energies (2pi MHz), and spacings measured FROM F'=2.
EHF = {0: -302.07, 1: -229.85, 2: -72.91, 3: 193.74}
DF = {Fp: EHF[Fp] - EHF[2] for Fp in EHF}     # {0:-229.16, 1:-156.94, 2:0, 3:+266.65}

# Allowed electric-dipole F->F' transitions (Delta F = 0, +-1; +-2 forbidden):
#   from F=2 :  F'=1,2,3      from F=1 :  F'=0,1,2
# Frequency offset of each line from the reference (|F=2>->|F'=2> == 0):
#   F=2 -> F' :          DF[F']           F=1 -> F' :  A_HFS + DF[F']
LINE = {(2, 1): DF[1], (2, 2): DF[2], (2, 3): DF[3],
        (1, 0): A_HFS + DF[0], (1, 1): A_HFS + DF[1], (1, 2): A_HFS + DF[2]}

# Dipole spontaneous-emission recoil distribution over (delta-m, weight):
EM_REC = [(-1, 1/6), (0, 2/3), (1, 1/6)]   # used by the engine (Section 6)

# Excited-state hyperfine DECAY branching BR[F'][F]  (engine, Section 6):
#   F'=0 -> F=1 only;  F'=3 -> F=2 only;  F'=1,2 -> both.
BR = {0: {1: 1.0, 2: 0.0}, 1: {1: 5/6, 2: 1/6},
      2: {1: 1/2, 2: 1/2}, 3: {1: 0.0, 2: 1.0}}

J0_FIRST_ZERO = 2.4048255577   # first zero of J_0; the carrier-suppression depth.

# Temperature <-> frequency, and the 1064 nm differential-Stark coefficient used only for
# the radial-inhomogeneity ANNOTATION (the |F'2,0> on-axis differential; NOT the per-(F',m')
# v0.3.0 Stark fix). c_radial(U0) = (1 + |a0_5P/a0_5S|)*U0, since |F'2,0> is pure scalar.
KB_OVER_H = 0.0208366                 # k_B/h, MHz per uK
SCALAR_RATIO_5P_5S = 1149.0 / 687.3   # |a0(5P3/2)/a0(5S)| ~ 1.671 (Chen; Goncalves-Raithel)


# =============================================================================
# SECTION 2 -- CONFIG  (all adjustable parameters)
# -----------------------------------------------------------------------------
# Every experimentally adjustable parameter lives in this dataclass; the physical
# constants are in Section 1. Group (a)-(f) set the optical fields and delivery;
# (g) the trap; (h) the engine/field; (i) the initial temperatures. preset()
# returns the validated operating points.
# =============================================================================

@dataclass
class Config:
    # ---- (a) delivery configuration -----------------------------------------
    configuration: str = "dual_end"
    #   "dual_end"          -- two-ended, carrier-suppressed EOM (preferred)
    #   "single_end_tagged" -- one end, EOM + retro + tag AOM + lambda/4
    #   "clean_lambda"      -- ideal 3-field reference (no EOM/parasitics)

    # ---- (b) detunings (2pi MHz) --------------------------------------------
    Delta: float = 55.0          # single-photon detuning of control/probe, BLUE of |F'=2>
    delta2: float = 0.0          # PRIMARY two-photon (Raman) detuning. f_mod is derived
                                 #   from this per configuration (see Section 3).
    Drep1: float = 15.0          # repump-1 detuning, BLUE of |F=1>->|F'=1>
    Drep2: float = 5.0           # repump-2 detuning, BLUE of its line (see repump_option)

    # ---- (c) intensities / Rabi (2pi MHz) -----------------------------------
    OmR: float = 0.10            # probe/control Rabi ratio  Omega_p / Omega_c (key lever)
    Omega_rep: float = 3.0       # repump Rabi (each repumper)
    Omega_tot_abs: Optional[float] = None   # override the pinned Omega_tot if set
    #   Total Rabi pinned to EIT: Omega_tot = sqrt(4*Delta*nu_z);
    #   Omega_c = Omega_tot/sqrt(1+OmR^2), Omega_p = OmR*Omega_c.

    # ---- (d) EOM / sideband comb --------------------------------------------
    f_mod: Union[float, str] = "auto"   # EOM modulation frequency (2pi MHz), or "auto" to
                                 #   DERIVE from delta2 and the configuration (Section 3):
                                 #     dual:   probe_order*f_mod = A_HFS + delta2
                                 #     single: probe_order*f_mod = A_HFS + delta2 + 2*f_A
                                 #   A numeric value overrides; then delta2 is reported derived.
    beta: Union[float, str] = "auto"
    #   EOM phase-modulation depth. Numeric value, OR "auto":
    #     dual_end -> 2.4048... (first J0 zero => carrier suppressed)
    #     single   -> value giving the requested OmR for the chosen eta_dp & order
    probe_order: int = 1         # which sideband n is the probe (1 = fundamental; 2 = 2nd
                                 #   overtone with f_mod ~ A_HFS/2; etc.)
    keep_orders: tuple = (-2, -1, 0, 1, 2)   # sideband orders to include in the spectrum

    # ---- (e) retro / tag (single-end only) ----------------------------------
    tag_2fA: float = 300.0       # double-passed tag-AOM total shift 2*f_A (2pi MHz);
                                 #   the RETURN beam is DOWN-shifted by this amount.
    eta_dp: float = 0.5          # round-trip (double-pass) power efficiency of the retro
    quarter_wave: bool = True    # lambda/4 in the retro arm flips helicity (sigma+ <-> sigma-)

    # ---- (f) repumpers ------------------------------------------------------
    repump_option: str = "A"     # "A": rep2 drives F=2->F'1 (sigma+);  "C": F=2->F'2 (pi)
    #   rep1 always drives F=1->F'1 (sigma-).

    # ---- (g) trap parameters (lattice-dependent) ----------------------------
    nu_z: float = 0.430          # axial trap frequency (2pi MHz) -- the cooled (stiff) axis
    nu_r: float = 0.00542        # radial trap frequency (2pi MHz)
    U0_uK: float = 1094.0        # trap depth (uK)
    eta_z: float = 0.094         # axial Lamb-Dicke parameter (single photon)

    # ---- (h) atomic engine and magnetic field -------------------------------
    B_field: float = 1.0         # magnetic field (G). DEFAULT = the cooling field: 1 G,
                                 #   vertical, parallel to the fiber axis (this is the
                                 #   cooling phase). The clock-magic 3.2287 G is needed
                                 #   ONLY for clock interrogation, a separate phase. The
                                 #   cooling dark pair |1,-1>/|2,+1> is field-insensitive
                                 #   (both g_F m_F = +1/2), so the floor is essentially
                                 #   B-independent: verified |d<n_z>| <= 0.0003 between
                                 #   1 G and 3.2287 G for both dual- and single-end.
    N_f: int = 6                 # axial Fock-space truncation
    with_e0: bool = True         # include 5P3/2 F'=0 contaminant (probe-leg, negligible)
    with_e1: bool = True         # include F'=1 contaminant (COMMON level -- dominant)
    with_e3: bool = True         # include F'=3 contaminant (control-leg, secondary)
    servo_delta2: bool = True    # auto-servo delta2 to the dark resonance (else use delta2)
    radius_um: float = 0.0       # radial position (um); 0 = on-axis.

    # ---- (i) initial conditions  (cooling-time & regime ONLY; do NOT affect the floor) ----
    T_axial_init_uK: float = 50.0    # initial axial T: sets n_init and the time-to-cool
    T_radial_init_uK: float = 100.0  # initial radial T: regime/inhomogeneity only (radial
                                     #   motion is decoupled from the axial cooling rate)


def preset(name: str) -> Config:
    """Return a Config for a named, validated operating point."""
    if name == "dual_end_optimal":
        return Config(configuration="dual_end", Delta=45.0, OmR=0.12,
                      beta="auto", probe_order=1, repump_option="A",
                      Omega_rep=3.0, Drep1=15.0, Drep2=5.0)
    if name == "single_end_tagged":
        return Config(configuration="single_end_tagged", Delta=45.0, OmR=0.12,
                      beta="auto", tag_2fA=400.0, eta_dp=0.30, quarter_wave=True,
                      repump_option="A", Omega_rep=3.0, Drep1=15.0, Drep2=5.0)
    if name == "single_end_tagged_v14":
        # v14 retro-capped point: a 2f_A = 400 MHz tag makes the 20-40% retro
        # reflectivity (AOM double-pass x re-injection) non-binding -- the floor is
        # flat in eta_dp; the atom-frame point is unchanged, only EOM depth/launch
        # power scale. Delta=45 sits in the flat 40-55 optimum. See operating_point.md.
        return Config(configuration="single_end_tagged", Delta=45.0, OmR=0.12,
                      beta="auto", tag_2fA=400.0, eta_dp=0.30, quarter_wave=True,
                      repump_option="A", Omega_rep=3.0, Drep1=15.0, Drep2=5.0)
    if name == "clean_lambda":
        return Config(configuration="clean_lambda", Delta=45.0, OmR=0.12, delta2=0.0)
    raise ValueError(f"unknown preset {name!r}")


# =============================================================================
# SECTION 3 -- BEAM-DELIVERY / OPTICAL-SPECTRUM MODEL
# -----------------------------------------------------------------------------
# Given a Config, return the explicit list of optical fields at the atoms. Each
# field is one tone: frequency, Rabi frequency, polarization, propagation
# direction, and a label classifying it as INTENDED (control/probe), REPUMP, or
# PARASITIC (carrier leakage, rejected retro tones, unused overtones). This list
# is exactly what the engine (Section 6) turns into Hamiltonian couplings, so the
# phase-modulation depth, modulation frequency, sideband orders, tagging AOM and
# quarter-wave plate are genuine parameters rather than hard-coded assumptions.
# =============================================================================

@dataclass
class OpticalField:
    label: str            # human name, e.g. "control", "probe", "armB_carrier_leak"
    role: str             # "intended", "repump", or "parasitic"
    freq: float           # frequency offset from |F=2>->|F'=2|  (2pi MHz)
    q: int                # polarization: +1 sigma+, -1 sigma-, 0 pi
    kdir: int             # propagation: +1 forward, -1 retro/counter (sets recoil sign)
    rabi: float           # Rabi frequency on its reference transition (2pi MHz)
    groundF: Optional[int] = None   # ground hyperfine it primarily addresses (1, 2, or None)


def reference_rabis(cfg: Config):
    """Control and probe Rabi from the EIT pinning Omega_tot = sqrt(4*Delta*nu_z)."""
    Otot = cfg.Omega_tot_abs if cfg.Omega_tot_abs is not None \
        else np.sqrt(4.0 * cfg.Delta * cfg.nu_z)
    Oc = Otot / np.sqrt(1.0 + cfg.OmR**2)
    Op = cfg.OmR * Oc
    return Oc, Op


def beta_for_OmR(OmR: float, eta_dp: float, order: int = 1) -> float:
    """Single-end: depth beta so the RETURN order-`order` sideband gives Omega_p/Omega_c = OmR.
       Condition: (J_order/J0)*sqrt(eta_dp) = OmR. Solved below the first J0 zero, where the
       ratio rises monotonically from 0."""
    target = OmR / np.sqrt(eta_dp)
    g = lambda b: jv(order, b) / jv(0, b) - target
    return brentq(g, 1e-6, J0_FIRST_ZERO - 1e-3)


def resolve_beta(cfg: Config) -> float:
    """Turn cfg.beta ('auto' or a number) into a numeric depth for this configuration."""
    if cfg.beta != "auto":
        return float(cfg.beta)
    if cfg.configuration == "dual_end":
        return J0_FIRST_ZERO                                  # carrier suppression
    if cfg.configuration == "single_end_tagged":
        return beta_for_OmR(cfg.OmR, cfg.eta_dp, cfg.probe_order)
    return 0.0                                                # clean_lambda: no EOM


def resolve_fmod(cfg: Config) -> float:
    """Numeric EOM frequency. 'auto' derives it from delta2 so the probe lands correctly:
         dual:   probe_order*f_mod = A_HFS + delta2
         single: probe_order*f_mod = A_HFS + delta2 + 2*f_A   (return is down-shifted by 2fA)
       A numeric cfg.f_mod overrides (delta2 then follows; see *_fields for the realized value)."""
    if cfg.f_mod != "auto":
        return float(cfg.f_mod)
    n = cfg.probe_order
    if cfg.configuration == "single_end_tagged":
        return (A_HFS + cfg.delta2 + cfg.tag_2fA) / n
    return (A_HFS + cfg.delta2) / n        # dual_end (and a harmless default for clean)


def _repump_fields(cfg: Config) -> List[OpticalField]:
    """Two repumpers (separate tones). rep1: F=1->F'1 sigma-. rep2: option A/C."""
    f = [OpticalField("repump1", "repump", LINE[(1, 1)] + cfg.Drep1, q=-1, kdir=+1,
                      rabi=cfg.Omega_rep, groundF=1)]
    if cfg.repump_option == "A":
        f.append(OpticalField("repump2_A(F2->F'1,sig+)", "repump",
                              LINE[(2, 1)] + cfg.Drep2, q=+1, kdir=+1,
                              rabi=cfg.Omega_rep, groundF=2))
    elif cfg.repump_option == "C":
        f.append(OpticalField("repump2_C(F2->F'2,pi)", "repump",
                              LINE[(2, 2)] + cfg.Drep2, q=0, kdir=+1,
                              rabi=cfg.Omega_rep, groundF=2))
    else:
        raise ValueError(f"repump_option must be 'A' or 'C', got {cfg.repump_option!r}")
    return f


def _clean_lambda_fields(cfg: Config) -> List[OpticalField]:
    """Ideal reference: the two Lambda legs only, no EOM/parasitics/repumpers.
       Control sigma- on |F=2>->|F'=2>; probe sigma+ on |F=1>->|F'=2>; counter-propagating."""
    Oc, Op = reference_rabis(cfg)
    return [
        OpticalField("control", "intended", cfg.Delta, q=-1, kdir=+1, rabi=Oc, groundF=2),
        OpticalField("probe", "intended", LINE[(1, 2)] + cfg.Delta + cfg.delta2,
                     q=+1, kdir=-1, rabi=Op, groundF=1),
    ]


def _dual_end_fields(cfg: Config) -> List[OpticalField]:
    """Dual-end carrier-suppressed delivery.
       Arm A: clean control tone (sigma-, one end).
       Arm B: SAME master, phase-EOM at f_mod, injected the OTHER end (sigma+). With beta at
       the J0 zero the carrier vanishes; the probe is the chosen sideband (default upper J1).
       delta2 = probe_order*f_mod - A_HFS  (carrier sits at the control frequency)."""
    Oc, Op = reference_rabis(cfg)
    beta = resolve_beta(cfg)
    fmod = resolve_fmod(cfg)
    n_p = cfg.probe_order
    Jp = jv(n_p, beta)
    if abs(Jp) < 1e-9:
        raise ValueError(f"probe sideband order {n_p} ~ zero amplitude at beta={beta:.4f}")
    O_armB = Op / abs(Jp)                 # arm-B carrier amplitude so the probe sideband == Op

    fields = [OpticalField("control", "intended", cfg.Delta, q=-1, kdir=+1,
                           rabi=Oc, groundF=2)]
    for n in cfg.keep_orders:
        rabi = O_armB * abs(jv(n, beta))
        freq = cfg.Delta + n * fmod               # carrier at Delta; sideband n at +n*f_mod
        if n == n_p:
            fields.append(OpticalField("probe", "intended", freq, q=+1, kdir=-1,
                                       rabi=rabi, groundF=1))
        elif n == 0:
            fields.append(OpticalField("armB_carrier_leak", "parasitic", freq, q=+1,
                                       kdir=-1, rabi=rabi, groundF=2))
        else:
            fields.append(OpticalField(f"armB_sideband_{n:+d}", "parasitic", freq, q=+1,
                                       kdir=-1, rabi=rabi, groundF=None))
    fields[0]._meta = dict(beta=beta, fmod=fmod,                       # type: ignore
                           delta2_eff=n_p * fmod - A_HFS)
    return fields


def _single_end_fields(cfg: Config) -> List[OpticalField]:
    """Single-end tagged-retro delivery.
       Forward beam (one end, sigma-): carrier == control, plus the EOM sideband.
       A retro mirror sends it back; a double-passed tag AOM DOWN-shifts the return by 2*f_A,
       and a lambda/4 flips its helicity (sigma- -> sigma+).
         intended control       = forward carrier            (sigma-, kdir +1)
         intended probe          = RETURN order-n_p sideband  (sigma+, kdir -1, shifted -2fA)
         parasitic (rejected)    = forward sideband           (sigma-, kdir +1)   wrong helicity
         parasitic (rejected)    = return carrier             (sigma+, kdir -1, -2fA)
       Amplitudes: O_in*J0 = Oc ; return sideband = O_in*J_{n_p}*sqrt(eta_dp) = Op.
       delta2 = probe_order*f_mod - A_HFS - 2fA  (return sideband lands at the probe line)."""
    Oc, Op = reference_rabis(cfg)
    beta = resolve_beta(cfg)
    fmod = resolve_fmod(cfg)
    n_p = cfg.probe_order
    J0, Jp = jv(0, beta), jv(n_p, beta)
    O_in = Oc / J0                                  # forward-beam carrier amplitude
    twofA = cfg.tag_2fA
    q_ret = +1 if cfg.quarter_wave else -1          # helicity of the return (flipped by lambda/4)

    delta2_eff = n_p * fmod - A_HFS - twofA         # realized two-photon detuning
    OmR_eff = (Jp / J0) * np.sqrt(cfg.eta_dp)        # realized probe/control ratio

    fields = [
        OpticalField("control", "intended", cfg.Delta, q=-1, kdir=+1, rabi=Oc, groundF=2),
        OpticalField("probe", "intended", cfg.Delta + n_p * fmod - twofA, q=q_ret, kdir=-1,
                     rabi=O_in * Jp * np.sqrt(cfg.eta_dp), groundF=1),
        OpticalField("fwd_sideband_rejected", "parasitic", cfg.Delta + n_p * fmod, q=-1,
                     kdir=+1, rabi=O_in * Jp, groundF=1),
        OpticalField("retro_carrier_rejected", "parasitic", cfg.Delta - twofA, q=q_ret,
                     kdir=-1, rabi=Oc * np.sqrt(cfg.eta_dp), groundF=2),
    ]
    fields[0]._meta = dict(beta=beta, fmod=fmod, delta2_eff=delta2_eff,  # type: ignore
                           OmR_eff=OmR_eff)
    return fields


def build_spectrum(cfg: Config) -> List[OpticalField]:
    """Top-level: dispatch on cfg.configuration and append repumpers (except clean_lambda)."""
    if cfg.configuration == "clean_lambda":
        return _clean_lambda_fields(cfg)
    if cfg.configuration == "dual_end":
        return _dual_end_fields(cfg) + _repump_fields(cfg)
    if cfg.configuration == "single_end_tagged":
        return _single_end_fields(cfg) + _repump_fields(cfg)
    raise ValueError(f"unknown configuration {cfg.configuration!r}")


# =============================================================================
# SECTION 4 -- field-table printer + detuning annotation
# =============================================================================
def nearest_line(freq: float):
    """(label, signed_detuning) for the allowed F->F' line nearest `freq`."""
    best = None
    for (Fg, Fp), f0 in LINE.items():
        d = freq - f0
        if best is None or abs(d) < abs(best[1]):
            best = (f"F{Fg}->F'{Fp}", d)
    return best


def near_resonances(freq: float, threshold: float = 400.0):
    """All allowed lines within `threshold` MHz of `freq` (for parasitic warnings)."""
    return [(f"F{Fg}->F'{Fp}", freq - f0)
            for (Fg, Fp), f0 in LINE.items() if abs(freq - f0) < threshold]


POL = {+1: "sig+", -1: "sig-", 0: "pi  "}


def print_spectrum_table(cfg: Config, fields: List[OpticalField]):
    """Print the explicit optical spectrum at the atoms, with parasitic warnings."""
    print(f"\nCONFIGURATION: {cfg.configuration}   Delta={cfg.Delta:g}  OmR={cfg.OmR:g}  "
          f"f_mod={resolve_fmod(cfg):g}  beta={resolve_beta(cfg):.4f}")
    meta = getattr(fields[0], "_meta", None) if fields else None
    if meta:
        msg = f"   realized delta2={meta['delta2_eff']:+.3f}"
        if "OmR_eff" in meta:
            msg += f",  realized OmR={meta['OmR_eff']:.4f}  (eta_dp={cfg.eta_dp})"
        print(msg)
    print("-" * 96)
    print(f"{'field':26s} {'role':9s} {'freq[MHz]':>11s} {'pol':4s} {'kdir':>4s} "
          f"{'Rabi[MHz]':>10s}  nearest line (detuning)")
    print("-" * 96)
    for fl in fields:
        line, det = nearest_line(fl.freq)
        warn = ""
        if fl.role == "parasitic" and any(abs(d) < 150 for _, d in near_resonances(fl.freq)):
            warn = "  <-- within 150 MHz of a line"
        print(f"{fl.label:26s} {fl.role:9s} {fl.freq:11.2f} {POL[fl.q]:4s} {fl.kdir:>4d} "
              f"{fl.rabi:10.4f}  {line} ({det:+.1f}){warn}")
    print("-" * 96)


# =============================================================================
# SECTION 5 -- fast self-tests on the delivery model
# -----------------------------------------------------------------------------
# Internal consistency checks on Section 3 (run in well under a second). Detuning
# checks use the detuning from the SPECIFIC line each field addresses
# (freq - LINE[(F,F')]), matching the engine's convention (Dc, Dc+d2, Dc-2fA,
# Dc+d2+2fA). The nearest-line helper is for the display table only.
# =============================================================================
def _selftests():
    n_ok = 0
    def check(name, cond):
        nonlocal n_ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
        assert cond, name
        n_ok += 1

    print("\nSELF-TESTS")

    # (1) Bessel energy conservation
    check("Bessel sum_n J_n^2 == 1",
          abs(sum(jv(n, 1.3)**2 for n in range(-30, 31)) - 1.0) < 1e-9)

    # (2-4) dual-end
    cfg = preset("dual_end_optimal")
    flds = build_spectrum(cfg)
    g = {f.label: f for f in flds}
    check("dual-end carrier leak ~ 0 at J0 zero", g["armB_carrier_leak"].rabi < 1e-6)
    check("dual-end control = sigma-, forward",
          g["control"].q == -1 and g["control"].kdir == +1)
    check("dual-end probe = sigma+, counter-prop",
          g["probe"].q == +1 and g["probe"].kdir == -1)
    dp = g["probe"].freq - LINE[(1, 2)]
    check("dual-end probe detuning == Delta + delta2", abs(dp - (cfg.Delta + cfg.delta2)) < 0.01)
    check("dual-end delta2 == probe_order*f_mod - A_HFS == cfg.delta2",
          abs((cfg.probe_order * resolve_fmod(cfg) - A_HFS) - cfg.delta2) < 1e-6)

    # (5) single-end: 2 intended + 2 parasitic; detunings match the solver's rejected set
    cfg2 = preset("single_end_tagged")
    f2 = build_spectrum(cfg2)
    g2 = {f.label: f for f in f2}
    twofA = cfg2.tag_2fA
    check("single-end has 2 intended fields",
          sum(f.role == "intended" for f in f2) == 2)
    check("single-end has 2 parasitic fields",
          sum(f.role == "parasitic" for f in f2) == 2)
    check("single-end control detuning == Delta",
          abs((g2["control"].freq - LINE[(2, 2)]) - cfg2.Delta) < 0.01)
    check("single-end probe detuning == Delta + delta2",
          abs((g2["probe"].freq - LINE[(1, 2)]) - (cfg2.Delta + cfg2.delta2)) < 0.01)
    check("single-end retro-carrier detuning == Delta - 2fA",
          abs((g2["retro_carrier_rejected"].freq - LINE[(2, 2)]) - (cfg2.Delta - twofA)) < 0.01)
    check("single-end fwd-sideband detuning == Delta + delta2 + 2fA",
          abs((g2["fwd_sideband_rejected"].freq - LINE[(1, 2)])
              - (cfg2.Delta + cfg2.delta2 + twofA)) < 0.01)

    # (6) single-end auto-beta realizes requested OmR
    bb = resolve_beta(cfg2)
    OmR_eff = (jv(cfg2.probe_order, bb) / jv(0, bb)) * np.sqrt(cfg2.eta_dp)
    check("single-end auto-beta realizes requested OmR", abs(OmR_eff - cfg2.OmR) < 1e-6)

    # (7) the table surfaces a parasitic near-resonance: down-shifted retro carrier sits
    #     ~88 MHz from F=2->F'1 (a channel the linearized solver only partly carried)
    d_to_F1 = dict(near_resonances(g2["retro_carrier_rejected"].freq)).get("F2->F'1")
    check("retro carrier flagged ~88 MHz from F=2->F'1",
          d_to_F1 is not None and abs(abs(d_to_F1) - 88.06) < 1.0)

    print(f"\n  {n_ok}/{n_ok} checks passed.")


# =============================================================================
# SECTION 6 -- MULTILEVEL ATOMIC ENGINE  (verbatim from the validated solver)
# -----------------------------------------------------------------------------
# Multilevel QuTiP steady-state solver for the cooling Lambda system: real
# 8-state Breit-Rabi ground manifold, tensor-diagonalized 5P_3/2 (F'=0,1,2,3),
# full Clebsch-Gordan dipole ladders, a breadth-first multi-rotating frame,
# m-resolved hyperfine decay branching, three-point photon recoil, the coherent
# |F'=3,0> control admixture and -- for the single-end configuration only -- the
# two rejected retro beams entered as linearized dissipators with their analytic
# a.c.-Stark shifts. It derives from the solver benchmarked during this study
# (clock_tagged_solve / clock_combined_solve) and is reproduced unchanged so that
# the floors reported here are identical to the independently validated values;
# the regression gate (Section 6b) enforces this. The Config adapter run() below
# maps the user parameters onto solve().
#
# SCOPE: solve() assumes perfect dual-end carrier suppression (no carrier-leak
# field) and treats the single-end rejected tones as linearized dissipators
# laddered to F'2/F'3 only. The spectrum table (Sections 3-4) flags what solve()
# does not yet fold into <n_z>: a carrier-leak field if beta != 2.4048, extra
# overtones, and the down-shifted retro carrier sitting ~88 MHz from F=2->F'1.
# Promoting those to full coherent beams is the planned refinement (see ROADMAP),
# to be re-validated against this engine in the dual-end limit.
# =============================================================================

# Aliases feeding the Section-1 constants (and the Config apparatus defaults) into the embedded
# engine. GAMMA, F3OFF, A_HFS_E and the g-factors are physical constants. NU and ETA are ONLY
# fallback defaults for a bare solve() call: the Config-driven path (run -> _engine_kwargs) always
# passes cfg.nu_z and cfg.eta_z, so these never shadow the Config. Bound to the Config defaults so
# there is a single source of truth (no duplicated literal that could drift).
GAMMA = GAMMA_D2
NU, ETA = Config.nu_z, Config.eta_z
F3OFF = DF[3]                                       # F'=3 above F'=2 (centroid)
A_HFS_E = A_HFS
gJ, gI, uB, II = gJ_5S, gI_87, uB_MHzG, I_87

CGc = lambda F, m, q, Fp, mp: float(clebsch_gordan(S(F), 1, S(Fp), S(m), S(q), S(mp)))
def Sfac(F, Fp):
    return (2*Fp+1)*float(wigner_6j(S(1)/2, S(3)/2, 1, S(Fp), S(F), S(3)/2))**2

def Eg(F, m, B):
    x = (gJ - gI)*uB*B/A_HFS; sgn = +1 if F == 2 else -1
    return -A_HFS/(2*(2*II+1)) + gI*uB*m*B + sgn*(A_HFS/2)*np.sqrt(1+4*m*x/(2*II+1)+x**2)

def excited_energies(B):
    Ex = [(0, 0)] + [(1, m) for m in (-1, 0, 1)] + [(2, m) for m in range(-2, 3)] \
         + [(3, m) for m in range(-3, 4)]
    prod = [(1.5-a, 1.5-b) for a in range(4) for b in range(4)]
    U = np.zeros((16, 16))
    for ci, (Fp, mp) in enumerate(Ex):
        for pj, (mJ, mI) in enumerate(prod):
            if abs(mJ+mI-mp) < 1e-9:
                U[ci, pj] = float(clebsch_gordan(S(3)/2, S(3)/2, S(Fp), S(mJ), S(mI), S(mp)))
    sq3 = np.sqrt(3)
    Jx32 = 0.5*np.array([[0, sq3, 0, 0], [sq3, 0, 2, 0], [0, 2, 0, sq3], [0, 0, sq3, 0]])
    Jx = U @ np.kron(Jx32, np.eye(4)) @ U.T
    def gF(Fp): return gJ*(Fp*(Fp+1))/(2*Fp*(Fp+1)) if Fp > 0 else 0.0
    H0 = np.diag([EHF[Fp] + gF(Fp)*uB*B*mp for (Fp, mp) in Ex]).astype(float)
    w, v = np.linalg.eigh(H0 - 6.233*(3*Jx@Jx - 3.75*np.eye(16)))
    out = {}
    for (Fp, mp) in Ex:
        if Fp in (0, 1, 2, 3):
            out[(Fp, mp)] = w[np.argmax(np.abs(v[Ex.index((Fp, mp)), :])**2)]
    return out

def beams(option, Dc, Drep1, Drep2, d2, Oc, Op, Om_r, with_e1=False, with_e0=False):
    def ladder(Fg, q, Fp):
        e = []
        for mg in ([-1, 0, 1] if Fg == 1 else [-2, -1, 0, 1, 2]):
            mp = mg + q
            if abs(mp) <= Fp:
                c = CGc(Fg, mg, q, Fp, mp)
                if abs(c) > 1e-9:
                    e.append(((Fg, mg), (Fp, mp), c))
        return e
    bm = []
    # control sigma- F=2 -> F'2, named |2,+1>->|F'2,0>; + coherent F'3 admixture
    ctrl_edges = ladder(2, -1, 2) + [((2, 1), (3, 0), CGc(2, 1, -1, 3, 0))]
    if with_e1: ctrl_edges = ctrl_edges + [((2, 1), (1, 0), CGc(2, 1, -1, 1, 0))]
    bm.append(dict(edges=ctrl_edges, named=((2, 1), (2, 0)), det=Dc,
                   Rabi=Oc, kdir=+1, tag='ctrl'))
    # probe sigma+ F=1 -> F'2, named |1,-1>->|F'2,0>
    pe = ladder(1, +1, 2) + ([((1, -1), (1, 0), CGc(1, -1, 1, 1, 0))] if with_e1 else [])
    if with_e0: pe = pe + [((1, -1), (0, 0), CGc(1, -1, 1, 0, 0))]
    bm.append(dict(edges=pe, named=((1, -1), (2, 0)), det=Dc + d2,
                   Rabi=Op, kdir=-1, tag='probe'))
    # repump1 sigma- F=1 -> F'1, named |1,0>->|F'1,-1>
    bm.append(dict(edges=ladder(1, -1, 1), named=((1, 0), (1, -1)), det=Drep1,
                   Rabi=Om_r, kdir=+1, tag='rep1'))
    if option == 'A':
        bm.append(dict(edges=ladder(2, +1, 1), named=((2, -2), (1, -1)), det=Drep2,
                       Rabi=Om_r, kdir=+1, tag='rep2'))
    elif option == 'C':
        bm.append(dict(edges=ladder(2, 0, 2), named=((2, -2), (2, -2)), det=Drep2,
                       Rabi=Om_r, kdir=0, tag='rep2'))
    return bm

def build_frame(bm, gE, eE):
    realE = {}
    for g in gE: realE[('g', g)] = gE[g]
    for e in eE: realE[('e', e)] = eE[e]
    for b in bm:
        (g, e), Dn = b['named'], b['det']
        b['nu'] = Dn + (realE[('e', e)] - realE[('g', g)])
    adj = {}
    def add(n1, n2, d):
        adj.setdefault(n1, []).append((n2, d)); adj.setdefault(n2, []).append((n1, -d))
    for b in bm:
        for (g, e, c) in b['edges']:
            det_ge = b['nu'] - (realE[('e', e)] - realE[('g', g)])
            add(('g', g), ('e', e), -det_ge)
    h = {}; max_conf = 0.0
    order = [('g', (2, 1))] + [n for n in adj if n != ('g', (2, 1))]
    for start in order:
        if start in h or start not in adj:
            continue
        h[start] = 0.0; stack = [start]
        while stack:
            n = stack.pop()
            for (m, d) in adj.get(n, []):
                hv = h[n] + d
                if m in h:
                    max_conf = max(max_conf, abs(h[m] - hv))
                else:
                    h[m] = hv; stack.append(m)
    return h, max_conf

def decay_branch(Fp, mp, Gset):
    """Normalized m-resolved decay branching of virtual |Fp,mp> into the grounds."""
    ch = {}
    for Fg in (1, 2):
        for mg in (mp-1, mp, mp+1):
            if abs(mg) > Fg:
                continue
            c = CGc(Fg, mg, mp-mg, Fp, mp)
            if abs(c) < 1e-12:
                continue
            ch[(Fg, mg)] = ch.get((Fg, mg), 0.0) + BR[Fp][Fg]*c**2
    s = sum(ch.values())
    return {g: w/s for g, w in ch.items()} if s > 0 else {}

def solve(option='A', Dc=80.0, twofA=220.0, eta_dp=0.5, Drep1=30.0, Drep2=5.0,
          d2=0.0, B=3.2287, Nf=8, OmR=0.25, Om_r=1.5, clean_lambda=False,
          with_e3=True, with_rejected=True, want_pops=False, oscale=1.0, with_e1=False, with_e0=False,
          nu_z=None, Otot_abs=None, eta_z=None, full=False):
    gE = {(F, m): Eg(F, m, B) for F in (1, 2)
          for m in (range(-1, 2) if F == 1 else range(-2, 3))}
    eE = excited_energies(B)
    nuz = nu_z if nu_z is not None else NU
    eta = eta_z if eta_z is not None else ETA
    Otot = Otot_abs if Otot_abs is not None else oscale*np.sqrt(4*Dc*nuz)
    Oc = Otot/np.sqrt(1+OmR**2); Op = OmR*Oc
    bm = beams(option, Dc, Drep1, Drep2, d2, Oc, Op, Om_r, with_e1=with_e1, with_e0=with_e0)
    if not with_e3:
        for b in bm:
            if b['tag'] == 'ctrl':
                b['edges'] = [(g, e, c) for (g, e, c) in b['edges'] if e[0] != 3]
    if clean_lambda:
        bm = [b for b in bm if b['tag'] in ('ctrl', 'probe')]
        for b in bm:                                   # drop F'3 for the clean gate
            b['edges'] = [(g, e, c) for (g, e, c) in b['edges'] if e[0] != 3]
        Gs = [(1, -1), (2, 1)]; Es = [(2, 0)]
    else:
        Gs = [(1, -1), (1, 0), (1, 1), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]
        Es = [(1, -1), (1, 0), (1, 1), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]
        if with_e3:
            Es = Es + [(3, 0)]
        if with_e0:
            Es = Es + [(0, 0)]
    nodes = [('g', g) for g in Gs] + [('e', e) for e in Es]
    idx = {n: i for i, n in enumerate(nodes)}
    NA = len(nodes)
    ng, ne = set(Gs), set(Es)
    for b in bm:
        b['edges'] = [(g, e, c) for (g, e, c) in b['edges'] if g in ng and e in ne]
    bm = [b for b in bm if b['edges'] and b['named'][0] in ng and b['named'][1] in ne]
    h, conf = build_frame(bm, gE, eE)
    for n in nodes:
        if n not in h: h[n] = 0.0

    bas = [qt.basis(NA, i) for i in range(NA)]
    P = lambda i, j: bas[i]*bas[j].dag()
    If = qt.qeye(Nf); aop = qt.destroy(Nf)
    Dsp = lambda s: qt.displace(Nf, 1j*eta*s)

    H = nuz*qt.tensor(qt.qeye(NA), aop.dag()*aop)
    for n in nodes:
        H += h[n]*qt.tensor(P(idx[n], idx[n]), If)
    for b in bm:
        (gn, en) = b['named']
        cnamed = [c for (g, e, c) in b['edges'] if g == gn and e == en][0]
        for (g, e, c) in b['edges']:
            ls = np.sqrt(Sfac(g[0], e[0])/Sfac(g[0], en[0])) if e[0] != en[0] else 1.0
            O = b['Rabi']*ls*(c/cnamed)
            i, j = idx[('g', g)], idx[('e', e)]
            H += -(O/2)*(qt.tensor(P(j, i), Dsp(b['kdir']))
                         + qt.tensor(P(i, j), Dsp(b['kdir']).dag()))

    legs = [(1, -1), (2, 1)]
    Gset = set(Gs)
    cops = []
    # real spontaneous decay
    for (Fp, mp) in Es:
        ch = {}
        for Fg in (1, 2):
            for mg in (mp-1, mp, mp+1):
                if abs(mg) > Fg:
                    continue
                c = CGc(Fg, mg, mp-mg, Fp, mp)
                if abs(c) < 1e-12:
                    continue
                w = BR[Fp][Fg]*c**2
                if (Fg, mg) in Gset:
                    ch[(Fg, mg)] = ch.get((Fg, mg), 0) + w
                else:
                    lw = np.array([CGc(lf, lm, mp-lm, Fp, mp)**2 for (lf, lm) in legs])
                    lw = lw/lw.sum() if lw.sum() > 0 else np.ones(len(legs))/len(legs)
                    for (lf, lm), ww in zip(legs, lw):
                        ch[(lf, lm)] = ch.get((lf, lm), 0) + w*ww
        tot = sum(ch.values())
        if tot <= 0:
            continue
        for (g, w) in ch.items():
            for (u, wem) in EM_REC:
                cops.append(np.sqrt(GAMMA*(w/tot)*wem)
                            * qt.tensor(P(idx[('g', g)], idx[('e', (Fp, mp))]), Dsp(u)))

    # linearized REJECTED dissipators (single-end / full system only)
    if with_rejected and not clean_lambda:
        cgC = CGc(2, 1, -1, 2, 0)                       # named control dipole CG
        cgP = CGc(1, -1, 1, 2, 0)                       # named probe   dipole CG
        rt = np.sqrt(Sfac(2, 3)/Sfac(2, 2))             # line-strength F'3/F'2 (F=2)
        Ocb = Oc*np.sqrt(eta_dp)                        # ret-carrier field
        Opb = Op/np.sqrt(eta_dp)                        # fwd-sideband field
        rej = [
            # (gsrc, kdir, Fp, mp, detuning, Rabi)
            ((2, 1), -1, 2, 2, Dc - twofA,
             Ocb*CGc(2, 1, 1, 2, 2)/cgC),
            ((2, 1), -1, 3, 2, Dc - twofA - F3OFF,
             Ocb*rt*CGc(2, 1, 1, 3, 2)/cgC),
            ((1, -1), +1, 2, -2, Dc + twofA,
             Opb*CGc(1, -1, -1, 2, -2)/cgP),
        ]
        acshift = {(2, 1): 0.0, (1, -1): 0.0}
        for (gsrc, kdir, Fp, mp, d, O) in rej:
            R = GAMMA*(O/2)**2/(d**2 + (GAMMA/2)**2)
            # coherent AC-Stark shift of the source ground (adiabatic elimination,
            # same sign convention as the resonant control: +(O/2)^2/d, d>0=blue).
            acshift[gsrc] = acshift.get(gsrc, 0.0) + (O/2)**2/d
            br = decay_branch(Fp, mp, Gset)
            for (g, w) in br.items():
                if g not in Gset:
                    continue
                for (u, wem) in EM_REC:
                    kick = Dsp(u)*Dsp(kdir)
                    cops.append(np.sqrt(R*w*wem)
                                * qt.tensor(P(idx[('g', g)], idx[('g', gsrc)]), kick))
        for (g, sh) in acshift.items():
            if g in ng:
                H += sh*qt.tensor(P(idx[('g', g)], idx[('g', g)]), If)

    L = qt.liouvillian(H, cops)
    try:
        rho = qt.steadystate(L, method='direct')
    except Exception:
        rho = qt.steadystate(L, method='svd')
    N = qt.tensor(qt.qeye(NA), aop.dag()*aop)
    nbar = float(np.real(qt.expect(N, rho)))
    if full or want_pops:
        pops = {g: float(np.real(qt.expect(qt.tensor(P(idx[('g', g)], idx[('g', g)]), If), rho)))
                for g in Gs}
    if full:
        # true motional Fock-diagonal P(n) read off the same steady state (no model change)
        fk = [qt.basis(Nf, k) for k in range(Nf)]
        motion = [float(np.real(qt.expect(qt.tensor(qt.qeye(NA), fk[k]*fk[k].dag()), rho)))
                  for k in range(Nf)]
        return dict(nbar=nbar, conf=conf, pops=pops, motion=motion, L=L, NA=NA)
    if want_pops:
        return nbar, conf, pops
    return nbar, conf

def d2min(grid, **kw):
    vals = [(solve(d2=d, **kw)[0], d) for d in grid]
    n, d = min(vals)
    return n, d, vals


# ---- Config -> engine adapter -----------------------------------------------
def _engine_kwargs(cfg: Config, Nf: int) -> dict:
    """Map a Config onto solve()'s arguments and pick the rejected/clean flags."""
    kw = dict(option=cfg.repump_option, Dc=cfg.Delta, twofA=cfg.tag_2fA, eta_dp=cfg.eta_dp,
              Drep1=cfg.Drep1, Drep2=cfg.Drep2, B=cfg.B_field, Nf=Nf, OmR=cfg.OmR,
              Om_r=cfg.Omega_rep, with_e1=cfg.with_e1, with_e0=cfg.with_e0, with_e3=cfg.with_e3,
              nu_z=cfg.nu_z, eta_z=cfg.eta_z, Otot_abs=cfg.Omega_tot_abs)
    if cfg.configuration == "clean_lambda":
        kw.update(clean_lambda=True, with_rejected=False)
    elif cfg.configuration == "dual_end":
        kw.update(clean_lambda=False, with_rejected=False)   # no rejected retro tones
    elif cfg.configuration == "single_end_tagged":
        kw.update(clean_lambda=False, with_rejected=True)
    else:
        raise ValueError(f"unknown configuration {cfg.configuration!r}")
    return kw


def run(cfg: Config, Nf: Optional[int] = None, servo_grid=None, want_pops=False, full=False):
    """Steady-state axial <n_z> for a Config, via the validated engine.
       Returns (nbar, delta2_used), or (nbar, delta2, pops) if want_pops, or -- if full --
       a dict {nbar, conf, pops, motion, delta2} with the true motional Fock distribution.
       If cfg.servo_delta2, delta2 is optimized on a grid (the dark resonance shifts with
       detuning/power/contaminants); otherwise cfg.delta2 is used as given."""
    Nf = Nf if Nf is not None else cfg.N_f
    kw = _engine_kwargs(cfg, Nf)
    if cfg.servo_delta2:
        grid = servo_grid if servo_grid is not None else np.round(np.arange(-0.40, 0.04, 0.03), 3)
        nbar, d2, _ = d2min(grid, **kw)
        if full:
            res = solve(d2=d2, full=True, **kw); res["delta2"] = d2; return res
        if want_pops:
            _, _, pops = solve(d2=d2, want_pops=True, **kw)
            return nbar, d2, pops
        return nbar, d2
    d2 = cfg.delta2
    if full:
        res = solve(d2=d2, full=True, **kw); res["delta2"] = d2; return res
    out = solve(d2=d2, want_pops=want_pops, **kw)
    return (out[0], d2, out[2]) if want_pops else (out[0], d2)


# =============================================================================
# SECTION 6b -- physics regression gate (reproduces the validated floors)
# -----------------------------------------------------------------------------
# Slow (servoed steady-state solves, ~1-2 min at Nf=6). Opt-in via --regression.
# These are the independently validated values; any future edit that changes them
# fails this gate. Increments over the clean base: +F'1 ~ +0.0034 (dominant),
# +F'3 ~ +0.0010, +F'0 ~ +0.0001 (negligible).
# =============================================================================
def _regression(Nf: int = 6):
    print(f"\nPHYSICS REGRESSION  (Nf={Nf}, delta2 servoed) -- reproduces validated floors")
    n_ok = 0
    def show(name, nbar, d2, expect, tol):
        nonlocal n_ok
        ok = abs(nbar - expect) <= tol
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:32s} <n_z>={nbar:.4f}  d2={d2:+.2f}"
              f"   (expect {expect:.4f} +-{tol:.4f})")
        assert ok, f"{name}: got {nbar:.4f}, expected {expect:.4f}+-{tol:.4f}"
        n_ok += 1

    B_AUDIT = 3.2287   # the validated-solver numbers were generated at the clock-magic field;
                       # pin here so this fidelity gate stays the exact validated anchor regardless
                       # of the cooling-field default. (Floor is field-insensitive: |d<n_z>|<=0.0003
                       # between 1 G and 3.2287 G, verified for dual- and single-end.)

    def contam_off(c):
        c.with_e1 = c.with_e0 = c.with_e3 = False; c.B_field = B_AUDIT; c.N_f = Nf; return c

    # historical recoil-limit gate: clean Lambda at OmR=0.25
    c = Config(configuration="clean_lambda", Delta=80.0, OmR=0.25,
               servo_delta2=False, delta2=0.0, N_f=Nf, B_field=B_AUDIT)
    show("G0 clean-Lambda recoil (OmR.25)", run(c)[0], 0.0, 0.0072, 0.0012)

    # clean base (contaminants OFF), optimized repump
    c = contam_off(preset("dual_end_optimal"))
    nb, d = run(c); show("clean base (contaminants off)", nb, d, 0.0014, 0.0005)

    # contaminant budget -- each contaminant toggled alone on the clean base
    for tag, flag, exp in [("budget +F'1 (dominant)", "with_e1", 0.0048),
                           ("budget +F'3 (control-leg)", "with_e3", 0.0024),
                           ("budget +F'0 (negligible)", "with_e0", 0.0015)]:
        c = contam_off(preset("dual_end_optimal")); setattr(c, flag, True)
        nb, d = run(c); show(tag, nb, d, exp, 0.0006)

    # full configurations
    c = preset("dual_end_optimal"); c.N_f = Nf; c.B_field = B_AUDIT
    nb, d = run(c); show("dual-end full (preferred)", nb, d, 0.0048, 0.0007)
    c = preset("single_end_tagged"); c.N_f = Nf; c.B_field = B_AUDIT
    nb, d = run(c); show("single-end tagged full", nb, d, 0.0075, 0.0009)

    print(f"\n  {n_ok}/{n_ok} regression checks passed.")


# =============================================================================
# SECTION 6c -- cooling dynamics & regime diagnostics
# -----------------------------------------------------------------------------
# The steady-state floor AND the cooling RATE are both independent of the initial
# temperature (properties of the Liouvillian L). The initial AXIAL T sets only the
# time-to-cool (a logarithmic prefactor on 1/rate); with the initial RADIAL T it
# sets the cooling REGIME -- whether the start is inside the Lamb-Dicke /
# sideband-resolved / trapped window where this steady-state picture is valid.
# Cooling time uses the validated tau = 1/gap method (gap = slowest motional
# relaxation eigenvalue of L; cf. delta_tau.py). Radial motion is decoupled from
# the axial rate (k.v_r = 0); the radial T enters only as a regime annotation and
# feeds the companion radial_inhomogeneity.py for the cloud-averaged floor.
# =============================================================================

def n_thermal(T_uK, nu_MHz):
    """Mean phonon number of a 1D mode at temperature T (uK), trap freq nu (2pi MHz)."""
    return 1.0 / np.expm1(nu_MHz / (T_uK * KB_OVER_H))      # 1/(exp(h nu / kT) - 1)


def _liouvillian_gap(L, NA, Nf):
    """Asymptotic cooling rate W (2pi MHz): the slowest relaxation mode of L that couples to
       <n> (smallest |Re lambda| among modes with motional content), which governs the approach
       to the floor; tau_1e = 1/W. Implementation notes (both matter for correctness):
         * The slow eigenvalues are found by shift-invert (ARPACK) with a small NEGATIVE real
           shift sigma = -SHIFT, NOT 0. The Liouvillian has an exact zero eigenvalue (the steady
           state), so a shift of exactly 0 makes (L - sigma I) singular and ARPACK intermittently
           returns spurious near-zero "ghost" modes. The small offset removes the singularity
           while still targeting the modes nearest the imaginary axis.
         * A fixed start vector makes the result deterministic; with ARPACK's default random
           start the rate otherwise scatters run-to-run.
       The steady state (|Re lambda| ~ 0) is removed by a rate floor; among the remaining modes
       the slowest with motional content (nc > NC_MIN) is the asymptotic rate."""
    from scipy.sparse.linalg import eigs as speigs
    SHIFT, RATE_FLOOR, NC_MIN = 1e-5, 1e-6, 0.05
    A = L.data.as_scipy().tocsc(); D = NA * Nf
    Nm = qt.tensor(qt.qeye(NA), qt.destroy(Nf).dag() * qt.destroy(Nf)).full()
    v0 = np.ones(D * D) / np.sqrt(D * D)                 # fixed start vector -> deterministic
    try:
        vals, vecs = speigs(A, k=min(24, D * D - 2), sigma=-SHIFT, which="LM",
                            v0=v0, maxiter=20000, tol=0)
    except Exception:                                    # dense fallback (small systems only)
        vals, vecs = np.linalg.eig(A.toarray())
    cand = []
    for j in range(len(vals)):
        r = abs(vals[j].real)
        if r < RATE_FLOOR:                               # steady state and numerical near-zeros
            continue
        rho = vecs[:, j].reshape(D, D); rs = (rho + rho.conj().T) / 2
        trn = np.sum(np.abs(np.linalg.eigvals(rs)))
        nc = abs(np.trace(Nm @ rho)) / (trn if trn > 1e-12 else 1.0)
        cand.append((r, nc))
    motional = [r for (r, nc) in cand if nc > NC_MIN]    # modes that appear in <n>(t)
    if motional:
        return min(motional)                             # slowest such mode = asymptotic rate
    return min((r for (r, _) in cand), default=None)


def _cooling_from_res(res, cfg, Nf):
    """Cooling-dynamics KPIs from a full run() result (so the servo is not repeated)."""
    n_ss = res["nbar"]
    W = _liouvillian_gap(res["L"], res["NA"], Nf)
    n_init = n_thermal(cfg.T_axial_init_uK, cfg.nu_z)
    tau = 1e-3 / W if (W and W > 0) else float("inf")        # ms

    def t_to(target):                                        # n(t)=n_ss+(n_init-n_ss)exp(-Wt)
        if n_init <= target:
            return 0.0                                       # already below target
        if target <= n_ss:
            return float("inf")                              # below the floor: unreachable
        return tau * np.log((n_init - n_ss) / (target - n_ss))

    return dict(n_ss=n_ss, W=W, tau_1e_ms=tau, n_init=n_init,
                t_to_0p1_ms=t_to(0.1), t_to_2fl_ms=t_to(2.0 * n_ss), delta2=res["delta2"])


def cooling_dynamics(cfg: Config, Nf: Optional[int] = None):
    """Return cooling-dynamics KPIs for a Config (servoed operating point):
         n_ss, W (rate, 2pi MHz), tau_1e_ms (=1/W; init-independent),
         n_init (from T_axial_init), t_to_0p1_ms, t_to_2fl_ms.
       Times use the LD-exponential estimate t = ln[(n_init-n_ss)/(target-n_ss)]/W."""
    Nf = Nf if Nf is not None else cfg.N_f
    return _cooling_from_res(run(cfg, Nf=Nf, full=True), cfg, Nf)


def _regime_lines(cfg: Config):
    """Config-aware cooling-regime / validity annotations (initial-T dependent)."""
    Oc, _ = reference_rabis(cfg)
    Otot = cfg.Omega_tot_abs if cfg.Omega_tot_abs is not None else np.sqrt(4*cfg.Delta*cfg.nu_z)
    n_init = n_thermal(cfg.T_axial_init_uK, cfg.nu_z)
    ld = cfg.eta_z * np.sqrt(2 * n_init + 1)                 # LD parameter at the start
    feat = GAMMA_D2 * cfg.nu_z / cfg.Delta                   # EIT cooling-feature width ~Gamma*nu_z/Delta
    sb = cfg.Delta / GAMMA_D2                                # sideband resolution (EIT) = nu_z/feat
    tuned = np.sqrt(4 * cfg.Delta * cfg.nu_z)                # bright-peak-at-sideband Rabi
    c_rad = (1.0 + SCALAR_RATIO_5P_5S) * cfg.U0_uK * KB_OVER_H
    dmean = c_rad * (cfg.T_radial_init_uK / cfg.U0_uK)       # mean Delta_eff shift over radial cloud
    ax_bound = cfg.T_axial_init_uK * KB_OVER_H / (cfg.U0_uK * KB_OVER_H)   # = T_ax/U0
    return [
        "COOLING REGIME (initial-T dependent; validity of the steady-state LD-EIT picture)",
        f"  axial start: T_init={cfg.T_axial_init_uK:g} uK -> n_init={n_init:.2f};  "
        f"bound T_ax/U0={ax_bound:.3f} " + ("(trapped)" if ax_bound < 0.5 else "(near top!)"),
        f"  Lamb-Dicke: eta*sqrt(2n_init+1)={ld:.3f} "
        + ("(<<1, OK)" if ld < 0.3 else "(MARGINAL)" if ld < 1 else "(INVALID -- pre-cool first)"),
        f"  sideband resolution (EIT): Delta/Gamma={sb:.2f}  (feature ~Gamma*nu_z/Delta={feat:.3f} "
        f"MHz vs nu_z={cfg.nu_z:g}) " + ("(resolved)" if sb > 1 else "(UNRESOLVED)"),
        f"  EIT tuning: Omega_tot={Otot:.2f} vs sqrt(4*Delta*nu_z)={tuned:.2f} "
        + ("(on the bright-peak condition)" if abs(Otot - tuned) < 0.05 * tuned
           else "(OFF the bright-peak tuning)"),
        f"  n_init vs Nf={cfg.N_f}: "
        + ("ok (thermal tail within Fock space)" if n_init < 0.4 * cfg.N_f
           else "n_init not small vs Nf -- time-to-cool is a LOWER bound (hot dynamics slower)"),
        f"  radial: T_rad/U0={cfg.T_radial_init_uK/cfg.U0_uK:.3f} "
        + ("(deeply trapped)" if cfg.T_radial_init_uK/cfg.U0_uK < 0.3 else "(shallow -- loss risk)")
        + f"; mean Delta_eff shift over the radial cloud ~{dmean:.2f} MHz "
        "(inhomogeneity the on-axis number ignores; see the radial MC).",
    ]


# =============================================================================
# SECTION 7 -- single operating-point report
# -----------------------------------------------------------------------------
# One readable block: the parameters echoed, the explicit optical spectrum, the
# result (<n_z>, servoed delta2, populations, cooling dynamics), and -- for
# transparency -- an explicit statement of the PHYSICAL MODEL, its ASSUMPTIONS,
# and the NON-IDEALITIES, split into (i) those modelled here, (ii) those flagged
# in the spectrum but not yet folded into <n_z>, and (iii) those outside this
# engine's scope. The flags in (ii)/(iii) are configuration-aware.
# =============================================================================
LEAK_STATES = [(1, 0), (2, -2), (2, 2), (1, 1)]   # states dark to the cooler that can fill


def _model_lines(cfg: Config):
    """The physical model actually computed for this configuration."""
    L = [
        "PHYSICAL MODEL (what is computed)",
        "  internal: 8 ground sublevels from Breit-Rabi at B; 5P3/2 F'=0..3 from full",
        "    tensor diagonalization; clock Lambda = sigma- control |2,+1> and sigma+ probe",
        "    |1,-1> onto |F'2,0>, plus the coherent |F'3,0> control admixture (Om_F3/Oc=1.06).",
        "  contaminants (toggled): control/probe ladders into F'=1 (common level, dominant),",
        "    F'=3 (control leg), F'=0 (probe leg); plus two repumpers (option %s)." % cfg.repump_option,
        "  motion: ONE axial mode at nu_z; Lamb-Dicke displacement (eta_z); 3-point dipole",
        "    recoil on every absorption and emission. Steady state of the Liouvillian.",
        "  dissipation: full m-resolved hyperfine decay branching (F'->F=1,2).",
    ]
    if cfg.configuration == "single_end_tagged":
        L += [
            "  single-end: the two rejected retro tones (return carrier, forward sideband) are",
            "    entered as LINEARIZED dissipators with analytic AC-Stark shifts -- valid because",
            "    (Omega/2fA)^2 ~ 1e-3 and all rejected beats are >> Gamma, nu_z.",
        ]
    return L


def _assumption_lines(cfg: Config):
    L = [
        "ASSUMPTIONS",
        "  - steady state: no loading transient, finite pulse time, or atom loss.",
        "  - classical drive fields (no photon shot noise); rotating-wave per the BFS frame.",
        "  - radial motion frozen/decoupled: k.v_r = 0 by the axial geometry and nu_r << nu_z,",
        "    so the axial mode is treated alone (radial spread handled by the separate MC tool).",
        "  - Lamb-Dicke regime (eta_z = %.3f)." % cfg.eta_z,
        "  - detuning reference: Delta from the in-trap on-axis |F'2,0> (1064 scalar cancels),",
        "    delta2 from the near-Stark-immune ground splitting; BUT repump/contaminant detunings",
        "    use BARE 5P3/2 spacings -- see NON-IDEALITIES [v0.1.0].",
    ]
    if cfg.configuration == "dual_end":
        L.append("  - dual-end: PERFECT carrier suppression assumed (beta = 2.4048 exactly).")
    if cfg.servo_delta2:
        L.append("  - delta2 held at the servo optimum on grid [-0.40,+0.03] (assumes the lock attains it).")
    else:
        L.append("  - delta2 fixed at the supplied value (NOT servoed).")
    return L


def _nonideality_lines(cfg: Config):
    """(i) modeled, (ii) flagged-not-yet-in-<n_z>, (iii) out of scope. Config-aware."""
    fields = build_spectrum(cfg)
    flagged = []
    if cfg.configuration == "dual_end":
        beta = resolve_beta(cfg)
        if abs(beta - J0_FIRST_ZERO) > 1e-3:
            leak = next((f for f in fields if f.label == "armB_carrier_leak"), None)
            lr = leak.rabi if leak else 0.0
            flagged.append("carrier leak: beta=%.3f != 2.4048 leaves a sigma+ tone at the control"
                           " line (Rabi=%.3f); in the table, not in <n_z>." % (beta, lr))
    if cfg.configuration == "single_end_tagged":
        flagged.append("retro carrier sits ~88 MHz from F=2->F'1 (sigma+); the rejected tones are"
                       " laddered to F'2/F'3 only -- this F'1 path is flagged, not in <n_z>.")
    overt = [f for f in fields if f.role == "parasitic" and f.label.startswith("armB_sideband")
             and f.rabi > 1e-6 and any(abs(d) < 400 for _, d in near_resonances(f.freq))]
    if overt:
        flagged.append("an EOM overtone lands within 400 MHz of a line (see table); not in <n_z>.")
    if not flagged:
        flagged.append("none for this configuration (nominal beta, no near-resonant parasitics).")

    L = ["NON-IDEALITIES",
         "  modeled here: contaminant scatter F'=0/1/3; photon recoil heating; finite repump"]
    if cfg.configuration == "single_end_tagged":
        L[-1] += "; rejected retro tones (linearized)."
    else:
        L[-1] += "."
    L.append("  FLAGGED in the spectrum, NOT yet in <n_z>:")
    L += ["    - " + s for s in flagged]
    L += [
        "  ENGINE APPROXIMATION (detuning reference) [v0.1.0]:",
        "    - repump/contaminant detunings omit the differential tensor 1064 Stark shift of",
        "      the target level vs |F'2,0> (~0 for F'=2; up to ~12-16 MHz for F'=1, theta-dep).",
        "      So Drep1 is referenced to the BARE F=1->F'1 line, up to ~2x off the in-trap",
        "      value. Delta and delta2 references ARE exact. To be fixed in v0.3.0.",
        "  OUT OF SCOPE of this engine (bounded separately in the companion noise analyses):",
        "    - magnetic-field noise and Zeeman dephasing of the dark state;",
        "    - laser phase/frequency noise (finite linewidth) and relative control-probe phase",
        "      noise; intensity noise; polarization impurity;",
        "    - beam pointing / non-axiality (~0.08 kHz per degree); trap anharmonicity and",
        "      higher bands; radial-axial coupling beyond the frozen approximation;",
        "    - collisions / background-gas loss.",
    ]
    return L


def report(cfg: Config, Nf: Optional[int] = None):
    """Print the full single-point operating report for a Config."""
    Nf = Nf if Nf is not None else cfg.N_f
    Oc, Op = reference_rabis(cfg)
    Otot = cfg.Omega_tot_abs if cfg.Omega_tot_abs is not None else np.sqrt(4*cfg.Delta*cfg.nu_z)
    fields = build_spectrum(cfg)

    print("\n" + "=" * 96)
    print(f" OPERATING POINT REPORT  --  configuration: {cfg.configuration}")
    print("=" * 96)
    print("KNOBS")
    _btag = ("cooling field" if cfg.B_field < 2.0
             else "clock-magic interrogation field" if abs(cfg.B_field - 3.2288) < 0.05
             else "non-standard field")
    print(f"  Delta={cfg.Delta:g}  OmR={cfg.OmR:g}  B={cfg.B_field:g} G ({_btag})  Nf={Nf}  "
          f"repump={cfg.repump_option} (Om_rep={cfg.Omega_rep:g}, Drep1={cfg.Drep1:g}, "
          f"Drep2={cfg.Drep2:g})")
    if cfg.configuration == "single_end_tagged":
        print(f"  2fA={cfg.tag_2fA:g}  eta_dp={cfg.eta_dp:g}  lambda/4={'on' if cfg.quarter_wave else 'off'}")
    print(f"  EOM: f_mod={resolve_fmod(cfg):g}  beta={resolve_beta(cfg):.4f}  "
          f"probe_order={cfg.probe_order}")
    print(f"  realized Rabis (2pi MHz): Omega_tot={Otot:.3f}  Omega_c={Oc:.3f}  Omega_p={Op:.3f}")

    print("\nOPTICAL SPECTRUM AT THE ATOMS")
    print_spectrum_table(cfg, fields)

    res = run(cfg, Nf=Nf, full=True)
    nbar, d2, pops = res["nbar"], res["delta2"], res["pops"]
    gtot = sum(pops.values()); exc = 1.0 - gtot; P0 = res["motion"][0]
    print("RESULT")
    print(f"  <n_z> = {nbar:.4f}     servoed delta2 = {d2:+.3f}" if cfg.servo_delta2
          else f"  <n_z> = {nbar:.4f}     delta2 = {d2:+.3f} (fixed)")
    print(f"  motional ground-state fraction P(n=0) = {P0:.4f}  (true, from the Fock diagonal)")
    print(f"  internal: ground population {gtot:.4f}, excited (scatter load) {exc:.2e}")
    top = sorted(pops.items(), key=lambda kv: -kv[1])[:6]
    print("  where the ground population sits (top 6):")
    print("     " + "   ".join(f"|{F},{m:+d}>={p:.3f}" for (F, m), p in top))
    leak = [(s, pops.get(s, 0.0)) for s in LEAK_STATES if s in pops]
    if leak:
        print("  leak states (dark to the cooler): "
              + "  ".join(f"|{F},{m:+d}>={p:.2e}" for (F, m), p in leak))

    cd = _cooling_from_res(res, cfg, Nf)
    print("\nCOOLING DYNAMICS  (floor and rate are initial-T independent)")
    print(f"  asymptotic cooling rate W (slowest motional mode of L) = {cd['W']:.5f} (2pi MHz)")
    print(f"     -> tau_1e = {cd['tau_1e_ms']:.3f} ms  (approach to the floor)")
    print(f"  from T_axial_init={cfg.T_axial_init_uK:g} uK (n_init={cd['n_init']:.2f}), "
          f"LD-exponential estimate n(t)=n_ss+(n_init-n_ss)exp(-Wt):")
    print(f"     time to <n_z>=0.1         ~ {cd['t_to_0p1_ms']:.3f} ms  "
          f"(upper bound; multi-exponential early cooling is faster)")
    print(f"     time to 2x floor (={2*cd['n_ss']:.4f}) ~ {cd['t_to_2fl_ms']:.3f} ms")

    print()
    for line in (_regime_lines(cfg) + [""] + _model_lines(cfg) + [""]
                 + _assumption_lines(cfg) + [""] + _nonideality_lines(cfg)):
        print(line)
    print("=" * 96)


# =============================================================================
# SECTION 8 -- sweeps + plotting
# -----------------------------------------------------------------------------
# Scan any Config knob(s) and plot <n_z>, reusing run(). Two cost regimes:
#   * base cfg with servo_delta2=True  -> delta2 is re-optimized at every point
#     (faithful: the dark resonance moves with the swept knob), ~15x slower.
#   * base cfg with servo_delta2=False -> delta2 held fixed (fast scouting).
# delta2_landscape() instead scans delta2 itself (servo necessarily off) to show
# the cooling resonance and how tight the lock must be. Figures are written to
# PNG files in the current directory.
# =============================================================================

def sweep1d(cfg: Config, knob: str, values, Nf: Optional[int] = None, servo_grid=None):
    """Vary one knob; return (values, nbars, delta2s). Honours cfg.servo_delta2.
       servo_grid (optional) overrides the per-point delta2 search grid (coarser = faster)."""
    nb, d2 = [], []
    for v in values:
        n, d = run(replace(cfg, **{knob: v}), Nf=Nf, servo_grid=servo_grid)
        nb.append(n); d2.append(d)
    return np.asarray(values, float), np.asarray(nb), np.asarray(d2)


def sweep2d(cfg: Config, knobx: str, xvals, knoby: str, yvals,
            Nf: Optional[int] = None, servo_grid=None):
    """Vary two knobs; return (xvals, yvals, Z[ny,nx] of <n_z>). Honours cfg.servo_delta2."""
    Z = np.zeros((len(yvals), len(xvals)))
    for iy, vy in enumerate(yvals):
        for ix, vx in enumerate(xvals):
            Z[iy, ix] = run(replace(cfg, **{knobx: vx, knoby: vy}), Nf=Nf, servo_grid=servo_grid)[0]
    return np.asarray(xvals, float), np.asarray(yvals, float), Z


def delta2_landscape(cfg: Config, grid=None, Nf: Optional[int] = None):
    """Scan delta2 directly (servo OFF) -> (grid, nbars): the dark-resonance landscape."""
    Nf = Nf if Nf is not None else cfg.N_f
    grid = np.round(np.arange(-0.50, 0.31, 0.02), 3) if grid is None else np.asarray(grid, float)
    kw = _engine_kwargs(cfg, Nf)
    nb = np.array([solve(d2=float(d), **kw)[0] for d in grid])
    return grid, nb


def _mpl():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return plt


def plot_sweep1d(values, nbars, knob, path, d2s=None, servoed=True, logy=True):
    """Line plot of <n_z> vs a knob; marks the optimum; optional second axis for servoed delta2."""
    plt = _mpl()
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    ax.plot(values, nbars, "o-", color="C0", label="<n_z>")
    if logy and np.all(nbars > 0):
        ax.set_yscale("log")
    i = int(np.argmin(nbars))
    ax.plot(values[i], nbars[i], "r*", ms=14, zorder=5)
    ax.set_xlabel(knob); ax.set_ylabel("<n_z>"); ax.grid(True, which="both", alpha=0.3)
    note = "delta2 servoed per point" if servoed else "delta2 fixed"
    ax.set_title(f"{knob} sweep  ({note})\nmin <n_z>={nbars[i]:.4f} at {knob}={values[i]:g}")
    if d2s is not None and servoed:
        ax2 = ax.twinx()
        ax2.plot(values, d2s, "s--", color="C1", alpha=0.6, ms=4, label="servo delta2")
        ax2.set_ylabel("servo delta2 (2pi MHz)", color="C1")
        ax2.tick_params(axis="y", labelcolor="C1")
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)
    return path


def plot_sweep2d(xvals, yvals, Z, knobx, knoby, path):
    """Heatmap of <n_z> over two knobs (log color), marking the minimum cell."""
    plt = _mpl()
    from matplotlib.colors import LogNorm
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    Zp = np.clip(Z, max(Z[Z > 0].min() if np.any(Z > 0) else 1e-4, 1e-6), None)
    im = ax.pcolormesh(xvals, yvals, Zp, norm=LogNorm(), shading="auto", cmap="viridis")
    fig.colorbar(im, ax=ax, label="<n_z>")
    iy, ix = np.unravel_index(np.argmin(Z), Z.shape)
    ax.plot(xvals[ix], yvals[iy], "r*", ms=16)
    ax.set_xlabel(knobx); ax.set_ylabel(knoby)
    ax.set_title(f"<n_z> over ({knobx}, {knoby})\nmin {Z[iy,ix]:.4f} at "
                 f"{knobx}={xvals[ix]:g}, {knoby}={yvals[iy]:g}")
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)
    return path


def plot_delta2(grid, nbars, path, cfg=None):
    """The delta2 cooling landscape; marks the optimum (the servo lock point)."""
    plt = _mpl()
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    ax.plot(grid, nbars, "o-", color="C2", ms=4)
    if np.all(nbars > 0):
        ax.set_yscale("log")
    i = int(np.argmin(nbars))
    ax.plot(grid[i], nbars[i], "r*", ms=14, zorder=5)
    ax.set_xlabel("delta2 (2pi MHz)"); ax.set_ylabel("<n_z>")
    ax.grid(True, which="both", alpha=0.3)
    cfgname = f"{cfg.configuration}, Delta={cfg.Delta:g}, OmR={cfg.OmR:g}" if cfg else ""
    ax.set_title(f"delta2 cooling landscape  ({cfgname})\noptimum delta2={grid[i]:+.3f}, "
                 f"<n_z>={nbars[i]:.4f}")
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)
    return path


def _trend(y):
    """One-word classification of a KPI sequence for the report."""
    y = np.asarray(y, float)
    if np.ptp(y) < 0.05 * max(abs(y).max(), 1e-12):
        return "flat"
    d = np.diff(y)
    if np.all(d >= 0):
        return "monotonic increasing"
    if np.all(d <= 0):
        return "monotonic decreasing"
    i = int(np.argmin(y))
    return "non-monotonic (best at endpoint)" if i in (0, len(y) - 1) \
        else "non-monotonic (interior minimum)"


def kpi_scan(cfg: Config, param: str, vmin: float, vmax: float, n: int = 9,
             Nf: Optional[int] = None, servo_grid=None, plot_path=None):
    """Scan one Config knob from vmin to vmax and print a short KPI report.

    KPIs per point (all read off the same steady state):
      * <n_z>            -- mean axial phonon number (the headline)
      * P(n=0)           -- TRUE motional ground-state fraction (Fock diagonal)
      * excited pop      -- total excited-state population ~ photon-scatter load
      * delta2           -- the two-photon detuning used (servoed optimum, unless fixed)

    Reuses run(); honours cfg.servo_delta2, EXCEPT when param=='delta2' (the servo is
    then disabled so the scanned value is the one used -- i.e. the delta2 landscape,
    now reported with KPIs). Integer knobs (e.g. N_f) are scanned on integers.
    Returns a dict of arrays; writes a 3-panel figure if plot_path is given.
    """
    Nf = Nf if Nf is not None else cfg.N_f
    is_int = isinstance(getattr(cfg, param), int) and not isinstance(getattr(cfg, param), bool)
    raw = np.linspace(vmin, vmax, n)
    values = [int(round(v)) for v in raw] if is_int else [float(v) for v in raw]
    scan_d2 = (param == "delta2")

    nbar, P0, scat, d2s = [], [], [], []
    for v in values:
        c = replace(cfg, **{param: v})
        if scan_d2:
            c = replace(c, servo_delta2=False)
        r = run(c, Nf=Nf, servo_grid=servo_grid, full=True)
        nbar.append(r["nbar"]); P0.append(r["motion"][0])
        scat.append(1.0 - sum(r["pops"].values())); d2s.append(r["delta2"])
    nbar, P0, scat, d2s = (np.asarray(a, float) for a in (nbar, P0, scat, d2s))

    note = ("delta2 scanned (servo off)" if scan_d2 else
            ("delta2 servoed per point" if cfg.servo_delta2 else "delta2 fixed"))
    print(f"\nKPI SCAN  --  {param} : {vmin:g} -> {vmax:g}   "
          f"({n} pts, config={cfg.configuration}, {note}, Nf={Nf})")
    print("-" * 74)
    print(f"  {param:>12s}      <n_z>    P(n=0)    excited    {'delta2':>8s}")
    print("-" * 74)
    for i, v in enumerate(values):
        vv = f"{v:12d}" if is_int else f"{v:12.3f}"
        print(f"  {vv}    {nbar[i]:8.4f}   {P0[i]:7.4f}   {scat[i]:.2e}   {d2s[i]:+8.3f}")
    print("-" * 74)
    io = int(np.argmin(nbar))
    vopt = f"{values[io]:d}" if is_int else f"{values[io]:.3f}"
    print(f"OPTIMUM   <n_z>={nbar[io]:.4f} at {param}={vopt}"
          f"   (P(n=0)={P0[io]:.4f}, excited={scat[io]:.1e})")
    print(f"TREND     <n_z>: {_trend(nbar)};  P(n=0) {P0.min():.4f}->{P0.max():.4f};  "
          f"excited {scat.min():.1e}->{scat.max():.1e}")
    if not scan_d2 and cfg.servo_delta2:
        print(f"          servo delta2 drifts {d2s[0]:+.3f} -> {d2s[-1]:+.3f} across the scan")
    print("NOTES     KPIs from the steady state; excited pop ~ scatter load. Model/assumptions"
          " as in report().")
    out = dict(param=param, values=values, nbar=nbar, P0=P0, excited=scat, delta2=d2s)
    if plot_path:
        plot_kpi_scan(out, cfg, plot_path); print("FIGURE   ", plot_path)
    return out


def plot_kpi_scan(scan, cfg: Config, path):
    """3-panel figure for a kpi_scan: <n_z> (log), P(n=0), and delta2 (or excited for delta2 scans)."""
    plt = _mpl()
    v = np.asarray(scan["values"], float); p = scan["param"]
    fig, ax = plt.subplots(3, 1, figsize=(6.4, 7.4), sharex=True)
    ax[0].plot(v, scan["nbar"], "o-", color="C0")
    if np.all(scan["nbar"] > 0):
        ax[0].set_yscale("log")
    i = int(np.argmin(scan["nbar"])); ax[0].plot(v[i], scan["nbar"][i], "r*", ms=14, zorder=5)
    ax[0].set_ylabel("<n_z>"); ax[0].grid(True, which="both", alpha=0.3)
    ax[0].set_title(f"KPI scan vs {p}   ({cfg.configuration})\n"
                    f"optimum <n_z>={scan['nbar'][i]:.4f} at {p}={scan['values'][i]}")
    ax[1].plot(v, scan["P0"], "o-", color="C2"); ax[1].set_ylabel("P(n=0)")
    ax[1].grid(True, alpha=0.3)
    if p == "delta2":
        ax[2].plot(v, scan["excited"], "s-", color="C3"); ax[2].set_ylabel("excited pop")
        ax[2].set_yscale("log")
    else:
        ax[2].plot(v, scan["delta2"], "s-", color="C1"); ax[2].set_ylabel("servo delta2")
    ax[2].set_xlabel(p); ax[2].grid(True, alpha=0.3)
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)
    return path


def _demo_sweeps(Nf: int = 6):
    """Produce a representative figure set (saved as PNGs). ~3 min at Nf=6.
       Uses a coarse delta2 servo grid for speed; tighten it for publication numbers."""
    base = replace(preset("dual_end_optimal"), N_f=Nf)
    cg = np.round(np.arange(-0.34, 0.02, 0.04), 3)     # coarse per-point servo grid
    paths = []
    print("  delta2 landscape (dual-end, servo off) ...")
    g, nb = delta2_landscape(base, grid=np.round(np.arange(-0.45, 0.26, 0.03), 3))
    paths.append(plot_delta2(g, nb, "fig_delta2_landscape.png", cfg=base))
    print("  Delta scan (servoed, coarse grid) ...")
    v, nb, d2 = sweep1d(base, "Delta", [45, 55, 65, 80], servo_grid=cg)
    paths.append(plot_sweep1d(v, nb, "Delta", "fig_delta_scan.png", d2s=d2, servoed=True))
    print("  OmR scan (servoed) -- the weaker-probe lever ...")
    v, nb, d2 = sweep1d(base, "OmR", [0.06, 0.10, 0.14, 0.18, 0.22], servo_grid=cg)
    paths.append(plot_sweep1d(v, nb, "OmR", "fig_omR_scan.png", d2s=d2, servoed=True))
    print("  figures written:", ", ".join(paths))
    return paths


# =============================================================================
# main: see the modes below
#   python eit_cooling_tool.py                # spectrum tables + fast self-tests
#   python eit_cooling_tool.py --report       # full operating-point reports (slow)
#   python eit_cooling_tool.py --regression   # reproduce the validated floors (slow)
#   python eit_cooling_tool.py --sweeps       # write example sweep figures (slow)
#   python eit_cooling_tool.py --kpi          # example KPI-vs-parameter scans (slow)
# =============================================================================
if __name__ == "__main__":
    import sys
    if "--report" in sys.argv:
        _selftests()
        report(preset("dual_end_optimal"))
        report(preset("single_end_tagged"))
    elif "--regression" in sys.argv:
        _selftests()
        _regression(Nf=6)
    elif "--sweeps" in sys.argv:
        _selftests()
        print("\nSWEEPS")
        _demo_sweeps(Nf=6)
    elif "--kpi" in sys.argv:
        _selftests()
        base = preset("dual_end_optimal")
        kpi_scan(base, "delta2", -0.45, 0.25, n=18, plot_path="fig_kpi_delta2.png")
        kpi_scan(base, "Delta", 45, 80, n=6,
                 servo_grid=np.round(np.arange(-0.34, 0.02, 0.04), 3),
                 plot_path="fig_kpi_delta.png")
    else:
        for nm in ("dual_end_optimal", "single_end_tagged", "clean_lambda"):
            c = preset(nm)
            print_spectrum_table(c, build_spectrum(c))
        _selftests()
