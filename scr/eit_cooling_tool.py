"""
================================================================================
 eit_cooling_tool.py  --  interactive auditor for clock-EIT sideband cooling
                          of 87Rb in a 1064 nm axial lattice (kagome HCPCF)
================================================================================

PURPOSE
    A single, heavily-commented file to AUDIT and EXPLORE the cooling scheme:
    change detunings, intensities, the delivery configuration (dual-end /
    single-end tagged retro / ideal clean-Lambda), the EOM modulation depth and
    frequency, which sideband overtones are used, the tag-AOM shift, the retro
    efficiency, the lambda/4, and the repumpers -- and see (i) the explicit
    optical spectrum that arrives at the atoms and (ii) [from Turn 3 on] the
    steady-state axial <n_z> from the validated multilevel solver.

DESIGN
    Layered, all in this one file (table of contents below). The atomic engine
    (Turn 3) REUSES the multilevel QuTiP solver that already reproduces every
    number in our program, so the built-in self-tests are bit-for-bit
    meaningful. The piece BUILT IN THIS FILE FROM SCRATCH is the spectrum /
    delivery layer (Section 3): it makes beta, f_mod, overtones, dual/single,
    tag AOM and lambda/4 into REAL knobs instead of hard-coded assumptions.

    TABLE OF CONTENTS
      Section 1  -- physical constants  (FIXED; the PI cannot vary these)
      Section 2  -- CONFIG dataclass    (EVERY knob lives here) + presets
      Section 3  -- spectrum / delivery builder            [done]
      Section 4  -- pretty-printer for the optical field table   [done]
      Section 5  -- spectrum self-tests (fast)             [done]
      Section 6  -- atomic engine (embedded validated solver) + Config adapter
                    + physics regression gate              [done]
      Section 7  -- single-point report (model/assumptions/non-idealities) [done]
      Section 8  -- sweeps + plotting                      [done]

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

STATUS
    Feature-complete (Sections 1-8). The spectrum/delivery layer, the embedded
    validated engine wired through run(Config), the self-documenting single-point
    report, and the sweep/plot layer are all in place. `--regression` reproduces
    the audited floors exactly (clean base 0.0014; +F'1 0.0048 / +F'3 0.0024 /
    +F'0 0.0015; dual 0.0048; single 0.0075) at the correct servoed delta2.
    Modes: (default) tables + fast self-tests; --report; --regression; --sweeps.
================================================================================
"""

from dataclasses import dataclass, replace
from typing import Optional, Union, List
import numpy as np
from scipy.special import jv          # Bessel J_n, for the phase-EOM sideband comb
from scipy.optimize import brentq     # used to invert beta <-> probe/control ratio
import qutip as qt                                            # engine (Section 6)
from sympy.physics.wigner import clebsch_gordan, wigner_6j    # CG and 6j (Section 6)
from sympy import S


# =============================================================================
# SECTION 1 -- PHYSICAL CONSTANTS  (FIXED -- the PI cannot vary these)
# -----------------------------------------------------------------------------
# Properties of the 87Rb atom and of electromagnetism. NOT in CONFIG because no
# experiment can change them. (Apparatus settings such as the trap frequency or
# lattice depth ARE tunable and live in CONFIG instead.)
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
EM_REC = [(-1, 1/6), (0, 2/3), (1, 1/6)]   # used by the engine (Turn 3)

# Excited-state hyperfine DECAY branching BR[F'][F]  (engine, Turn 3):
#   F'=0 -> F=1 only;  F'=3 -> F=2 only;  F'=1,2 -> both.
BR = {0: {1: 1.0, 2: 0.0}, 1: {1: 5/6, 2: 1/6},
      2: {1: 1/2, 2: 1/2}, 3: {1: 0.0, 2: 1.0}}

J0_FIRST_ZERO = 2.4048255577   # first zero of J_0; the carrier-suppression depth.


# =============================================================================
# SECTION 2 -- CONFIG  (EVERY tunable knob lives here)
# -----------------------------------------------------------------------------
# Fields marked [Turn 3+] are consumed by the atomic engine added later; they
# are present now so the config structure is complete and stable.
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

    # ---- (g) apparatus / trap (tunable: a different lattice changes these) ---
    nu_z: float = 0.430          # axial trap frequency (2pi MHz) -- the cooled (stiff) axis
    nu_r: float = 0.00542        # radial trap frequency (2pi MHz) [Turn 3+]
    U0_uK: float = 1094.0        # trap depth (uK) [Turn 3+, radial tool]
    eta_z: float = 0.094         # axial Lamb-Dicke parameter (single photon) [Turn 3+]

    # ---- (h) atomic engine knobs  [Turn 3+] ---------------------------------
    B_field: float = 3.2287      # magnetic field (G). Cooling works at any field; 3.229 G
                                 #   is clock-magic (only needed for interrogation).
    N_f: int = 6                 # axial Fock-space truncation
    with_e0: bool = True         # include 5P3/2 F'=0 contaminant (probe-leg, negligible)
    with_e1: bool = True         # include F'=1 contaminant (COMMON level -- dominant)
    with_e3: bool = True         # include F'=3 contaminant (control-leg, secondary)
    servo_delta2: bool = True    # auto-servo delta2 to the dark resonance (else use delta2)
    radius_um: float = 0.0       # radial position (um); 0 = on-axis. [Turn 3+]


def preset(name: str) -> Config:
    """Return a Config for a named operating point (audited values)."""
    if name == "dual_end_optimal":
        return Config(configuration="dual_end", Delta=55.0, OmR=0.10,
                      beta="auto", probe_order=1, repump_option="A",
                      Omega_rep=3.0, Drep1=15.0, Drep2=5.0)
    if name == "single_end_tagged":
        return Config(configuration="single_end_tagged", Delta=55.0, OmR=0.10,
                      beta="auto", tag_2fA=300.0, eta_dp=0.5, quarter_wave=True,
                      repump_option="A", Omega_rep=3.0, Drep1=15.0, Drep2=5.0)
    if name == "clean_lambda":
        return Config(configuration="clean_lambda", Delta=55.0, OmR=0.10, delta2=0.0)
    raise ValueError(f"unknown preset {name!r}")


# =============================================================================
# SECTION 3 -- SPECTRUM / DELIVERY BUILDER  (the new physics of this turn)
# -----------------------------------------------------------------------------
# Given a Config, return the explicit list of optical fields AT THE ATOMS. Each
# field is one tone: frequency, Rabi, polarization, propagation direction, and a
# label flagged INTENDED (control/probe) / REPUMP / PARASITIC (carrier leakage,
# rejected retro tones, unused overtones). This list is exactly what the engine
# (Turn 3) turns into Hamiltonian couplings.
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
# SECTION 5 -- self-tests  (regression targets the engine must later match)
# -----------------------------------------------------------------------------
# Detuning checks use the detuning from the SPECIFIC line each field addresses
# (freq - LINE[(F,F')]), matching the validated solver's convention (Dc, Dc+d2,
# Dc-2fA, Dc+d2+2fA). The nearest-line helper is for the display table only.
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
# SECTION 6 -- ATOMIC ENGINE  (embedded VERBATIM from the validated solver)
# -----------------------------------------------------------------------------
# This is the multilevel QuTiP steady-state engine that reproduces every number
# in our program (clock_tagged_solve.py / clock_combined_solve.py lineage):
# real 8-ground Breit-Rabi energies, tensor-diagonalized 5P3/2 (F'=0,1,2,3),
# full Clebsch-Gordan ladders, a BFS multi-rotating frame, full hyperfine decay
# branching, 3-point recoil, the coherent F'3 control admixture, and -- for the
# single-end configuration only -- the two rejected retro beams entered as
# linearized dissipators with their analytic AC-Stark shifts.
#
# It is copied unchanged on purpose: the audit value is that the floors are
# bit-for-bit the validated ones. The Config adapter `run()` below maps the
# user's knobs onto solve(); _regression() locks the audited floors.
#
# SCOPE NOTE (honest): solve() assumes perfect dual-end carrier suppression
# (no carrier-leak field) and treats the single-end rejected tones as linearized
# dissipators laddered to F'2/F'3 only. The spectrum table (Sec 3-4) already
# FLAGS what solve() does not yet fold into <n_z>: a carrier-leak field if
# beta != 2.4048, extra overtones, and the down-shifted retro carrier sitting
# ~88 MHz from F=2->F'1. Promoting those to full coherent beams is the planned
# next refinement, to be re-validated against this engine in the dual-end limit.
# =============================================================================

# aliases so the embedded engine uses the Section-1 physical constants
GAMMA, NU, ETA = GAMMA_D2, 0.430, 0.094
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
          nu_z=None, Otot_abs=None, eta_z=None):
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
    if want_pops:
        pops = {g: float(np.real(qt.expect(qt.tensor(P(idx[('g', g)], idx[('g', g)]), If), rho)))
                for g in Gs}
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


def run(cfg: Config, Nf: Optional[int] = None, servo_grid=None, want_pops=False):
    """Steady-state axial <n_z> for a Config, via the validated engine.
       Returns (nbar, delta2_used). If cfg.servo_delta2, delta2 is optimized on a grid
       (the dark resonance shifts with detuning/power/contaminants, so this is the
       realistic servo); otherwise cfg.delta2 is used as given."""
    Nf = Nf if Nf is not None else cfg.N_f
    kw = _engine_kwargs(cfg, Nf)
    if cfg.servo_delta2:
        grid = servo_grid if servo_grid is not None else np.round(np.arange(-0.40, 0.04, 0.03), 3)
        nbar, d2, _ = d2min(grid, **kw)
    else:
        d2 = cfg.delta2
        out = solve(d2=d2, want_pops=want_pops, **kw)
        return (out[0], d2, out[2]) if want_pops else (out[0], d2)
    if want_pops:
        _, _, pops = solve(d2=d2, want_pops=True, **kw)
        return nbar, d2, pops
    return nbar, d2


# =============================================================================
# SECTION 6b -- physics regression gate (reproduce the audited floors)
# -----------------------------------------------------------------------------
# Slow (servoed steady-state solves, ~1-2 min at Nf=6). Opt-in via --regression.
# These are the program's audited values; if a future edit changes them, this
# fails loudly. Increments over the clean base: +F'1 ~ +0.0034 (dominant),
# +F'3 ~ +0.0010, +F'0 ~ +0.0001 (negligible).
# =============================================================================
def _regression(Nf: int = 6):
    print(f"\nPHYSICS REGRESSION  (Nf={Nf}, delta2 servoed) -- reproduces audited floors")
    n_ok = 0
    def show(name, nbar, d2, expect, tol):
        nonlocal n_ok
        ok = abs(nbar - expect) <= tol
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:32s} <n_z>={nbar:.4f}  d2={d2:+.2f}"
              f"   (expect {expect:.4f} +-{tol:.4f})")
        assert ok, f"{name}: got {nbar:.4f}, expected {expect:.4f}+-{tol:.4f}"
        n_ok += 1

    def contam_off(c):
        c.with_e1 = c.with_e0 = c.with_e3 = False; return c

    # historical recoil-limit gate: clean Lambda at OmR=0.25
    c = Config(configuration="clean_lambda", Delta=80.0, OmR=0.25,
               servo_delta2=False, delta2=0.0, N_f=Nf)
    show("G0 clean-Lambda recoil (OmR.25)", run(c)[0], 0.0, 0.0072, 0.0012)

    # clean base (contaminants OFF), optimized repump
    c = contam_off(preset("dual_end_optimal")); c.N_f = Nf
    nb, d = run(c); show("clean base (contaminants off)", nb, d, 0.0014, 0.0005)

    # contaminant budget -- each contaminant toggled alone on the clean base
    for tag, flag, exp in [("budget +F'1 (dominant)", "with_e1", 0.0048),
                           ("budget +F'3 (control-leg)", "with_e3", 0.0024),
                           ("budget +F'0 (negligible)", "with_e0", 0.0015)]:
        c = contam_off(preset("dual_end_optimal")); setattr(c, flag, True); c.N_f = Nf
        nb, d = run(c); show(tag, nb, d, exp, 0.0006)

    # full configurations
    c = preset("dual_end_optimal"); c.N_f = Nf
    nb, d = run(c); show("dual-end full (preferred)", nb, d, 0.0048, 0.0007)
    c = preset("single_end_tagged"); c.N_f = Nf
    nb, d = run(c); show("single-end tagged full", nb, d, 0.0075, 0.0009)

    print(f"\n  {n_ok}/{n_ok} regression checks passed.")


# =============================================================================
# SECTION 7 -- single-point operating report
# -----------------------------------------------------------------------------
# One readable block: knobs echoed, the explicit optical spectrum, the result
# (<n_z>, servoed delta2, populations), and -- per the audit requirement -- an
# explicit statement of the PHYSICAL MODEL, its ASSUMPTIONS, and the
# NON-IDEALITIES, split into (i) those modeled here, (ii) those FLAGGED in the
# spectrum but not yet folded into <n_z>, and (iii) those outside this engine's
# scope. The flags in (ii)/(iii) are config-aware.
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
        "  OUT OF SCOPE of this engine (bound separately in the program's noise studies):",
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
    print(f"  Delta={cfg.Delta:g}  OmR={cfg.OmR:g}  B={cfg.B_field:g} G  Nf={Nf}  "
          f"repump={cfg.repump_option} (Om_rep={cfg.Omega_rep:g}, Drep1={cfg.Drep1:g}, "
          f"Drep2={cfg.Drep2:g})")
    if cfg.configuration == "single_end_tagged":
        print(f"  2fA={cfg.tag_2fA:g}  eta_dp={cfg.eta_dp:g}  lambda/4={'on' if cfg.quarter_wave else 'off'}")
    print(f"  EOM: f_mod={resolve_fmod(cfg):g}  beta={resolve_beta(cfg):.4f}  "
          f"probe_order={cfg.probe_order}")
    print(f"  realized Rabis (2pi MHz): Omega_tot={Otot:.3f}  Omega_c={Oc:.3f}  Omega_p={Op:.3f}")

    print("\nOPTICAL SPECTRUM AT THE ATOMS")
    print_spectrum_table(cfg, fields)

    nbar, d2, pops = run(cfg, Nf=Nf, want_pops=True)
    gtot = sum(pops.values()); exc = 1.0 - gtot; P0 = 1.0/(1.0 + nbar)
    print("RESULT")
    print(f"  <n_z> = {nbar:.4f}     servoed delta2 = {d2:+.3f}" if cfg.servo_delta2
          else f"  <n_z> = {nbar:.4f}     delta2 = {d2:+.3f} (fixed)")
    print(f"  motional ground-state fraction P(n=0) ~ {P0:.3f}  (thermal estimate 1/(1+<n>))")
    print(f"  internal: ground population {gtot:.4f}, excited (scatter load) {exc:.2e}")
    top = sorted(pops.items(), key=lambda kv: -kv[1])[:6]
    print("  where the ground population sits (top 6):")
    print("     " + "   ".join(f"|{F},{m:+d}>={p:.3f}" for (F, m), p in top))
    leak = [(s, pops.get(s, 0.0)) for s in LEAK_STATES if s in pops]
    if leak:
        print("  leak states (dark to the cooler): "
              + "  ".join(f"|{F},{m:+d}>={p:.2e}" for (F, m), p in leak))

    print()
    for line in _model_lines(cfg) + [""] + _assumption_lines(cfg) + [""] + _nonideality_lines(cfg):
        print(line)
    print("=" * 96)


# =============================================================================
# SECTION 8 -- sweeps + plotting
# -----------------------------------------------------------------------------
# Scan any Config knob(s) and plot <n_z>, reusing run(). Two cost regimes:
#   * base cfg with servo_delta2=True  -> delta2 is re-optimized at every point
#     (honest: the dark resonance moves with the swept knob), ~15x slower.
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
#   python eit_cooling_tool.py --regression   # reproduce the audited floors (slow)
#   python eit_cooling_tool.py --sweeps       # write example sweep figures (slow)
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
    else:
        for nm in ("dual_end_optimal", "single_end_tagged", "clean_lambda"):
            c = preset(nm)
            print_spectrum_table(c, build_spectrum(c))
        _selftests()
