#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
thermometry.py -- asymmetric-sideband thermometry for the m'=0 clock-EIT scheme.

SUPERSEDES thermometry_sim.py (which modeled the earlier *swapped m'=2* scheme:
cool in a field-sensitive pair, park in |1,+1>, then a microwave Dm=-1 carrier
pi-pulse transferred |1,+1>->|1,0> to read on the clock pair |1,0><->|2,0>).

In the CURRENT m'=0 scheme the cooling pair |1,-1><->|2,+1> *is* the
field-insensitive pair (both g_F m_F = +1/2), so thermometry reads the SAME pair
directly -- no park->read transfer (the old [I5] step is gone). The two-level x
Fock sideband physics is otherwise identical, so the validated coherent core of
thermometry_sim.py is reused verbatim and only re-labelled.

WHAT THIS ADDS over the old sim (to resolve the laser-architecture question):
  (1) a spontaneous-SCATTER model tied to the single-photon detuning Delta, for a
      *sideband*-pi probe (the realistic full-transfer probe), and a demonstration
      that uniform scatter cancels in the red/blue ratio R;
  (2) the R-vs-<n> CALIBRATION curve with Blackman shaping  -> Q1 of
      laser_architecture_comparison.md;
  (3) a blue-sideband Rabi-flop + fit to recover P0           -> Q2.

MODEL  (dimensionless: energies/Rabis in units of nu_z; delta = two-photon
detuning in units of nu_z; tau = nu_z * t):
  internal g=|1,-1>, e=|2,+1>; shared axial oscillator; 2k Raman -> displacement
  D(i*ETA_R), ETA_R = 2*eta_z.
      H/nu_z = a^dag a - delta |e><e| + (s/2)[ |e><g| D^dag + |g><e| D ]
  resonances: carrier delta=0, blue (n->n+1) delta=+1, red (n->n-1) delta=-1.
  s = Omega0/nu_z is the carrier two-photon Rabi as a fraction of the trap freq.
OBSERVABLE: R = A_red/A_blue -> <n>_meas = R/(1-R).

GATES (carried from thermometry_sim.py): (1) weak-probe recovers <n>; (2) Nf-stable.
NEW gate (3): uniform scatter leaves R invariant.
"""

import numpy as np
from numpy import pi
from scipy.linalg import expm

# ----------------- physical constants (from the tool where available) -----------
try:
    from eit_cooling_tool import GAMMA_D2 as GAMMA_MHz, A_HFS  # noqa: F401
    from eit_cooling_tool import Config as _Cfg
    NU_Z  = _Cfg.nu_z      # 0.430  (2pi MHz)  axial (cooled) trap frequency
    ETA_Z = _Cfg.eta_z     # 0.094  single-photon axial Lamb-Dicke
except Exception:                                    # pragma: no cover
    GAMMA_MHz, NU_Z, ETA_Z = 6.07, 0.430, 0.094

ETA_R = 0.187                       # 2k counter-prop Raman LD (= eta_eff ~= 2*eta_z)
DW0   = np.exp(-ETA_R**2 / 2.0)     # carrier Debye-Waller on |0>
NU_Z_HZ = NU_Z * 1e6                # Hz
GAMMA_OVER_NU = GAMMA_MHz / NU_Z    # ~14.1

__version__ = "0.2.0"
# CHANGELOG
#   0.1.0  reuse of the validated coherent core (make_ops/H_block/_Pe/measure),
#          scatter model, R-vs-<n> calibration (Q1), BSB-flop fit (Q2),
#          radial broadening; gates 1-4.
#   0.2.0  branching-resolved scatter RE-ENTRY: scatter_branching (CG line
#          strengths + m-resolved decay), recoil_heating_per_scatter, and a
#          master-equation pedestal (reentry_pedestal) + reentry_summary.
#          Finding: the re-entry pedestal is a near-constant offset on R that
#          CALIBRATION absorbs (naive R/(1-R) is biased ~3x at 0.8 GHz, and
#          off-sideband subtraction OVER-subtracts) -> SNR cost, not bias.


# ============================== coherent core ===================================
# (reused from thermometry_sim.py; validated in thermometry_audit.md)
def make_ops(Nf, eta):
    a    = np.diag(np.sqrt(np.arange(1, Nf)), 1).astype(complex)
    adag = a.conj().T
    ncol = adag @ a
    D    = expm(1j * eta * (a + adag))            # == qt.displace(Nf, 1j*eta)
    return a, adag, ncol, D


def thermal_pops(nbar, Nf):
    n = np.arange(Nf)
    p = (nbar ** n) / ((1.0 + nbar) ** (n + 1))
    return p / p.sum()


def H_block(delta, s, Nf, ncol, D, carrier_only=False, loss=0.0):
    """2*Nf Hamiltonian. loss = uniform non-Hermitian decay (Gamma_sc/nu_z) on
    BOTH internal states (scatter out of the clock pair)."""
    Dc = np.diag(np.diag(D)) if carrier_only else D
    I  = np.eye(Nf, dtype=complex)
    Hgg = ncol.astype(complex) - 0.5j * loss * I
    Hee = ncol - delta * I - 0.5j * loss * I
    Hge = (s / 2.0) * Dc.conj().T
    Heg = (s / 2.0) * Dc
    return np.block([[Hgg, Hge], [Heg, Hee]])


def _blackman(M):
    k = np.arange(M)
    return 0.42 - 0.5 * np.cos(2 * pi * k / (M - 1)) + 0.08 * np.cos(4 * pi * k / (M - 1))


def _Pe(delta, s, T, Nf, ncol, D, pops, shape='square', carrier_only=False,
        loss=0.0, M=120):
    """Excited population after a pulse of dimensionless duration T, AREA pi
    (calibrated on the driven resonance via the caller's choice of T).
    shape='square' or 'blackman'. Returns scalar P_e on the mixture `pops`."""
    if shape == 'square':
        U = expm(-1j * H_block(delta, s, Nf, ncol, D, carrier_only, loss) * T)
    elif shape == 'blackman':
        w = _blackman(M); dt = T / M
        s_pk = s * (M) / np.sum(w)               # keep the SAME pulse area as square
        U = np.eye(2 * Nf, dtype=complex)
        for j in range(M):
            U = expm(-1j * H_block(delta, s_pk * w[j], Nf, ncol, D, carrier_only, loss) * dt) @ U
    else:
        raise ValueError(shape)
    Ue = U[Nf:2 * Nf, :Nf]
    col_pe = np.sum(np.abs(Ue) ** 2, axis=0)
    return float(np.dot(pops, col_pe))


def invert(R):
    return R / (1.0 - R)


# ============================== probe / measurement =============================
def _Tpulse(s, probe):
    """Dimensionless duration (tau = 2*pi*nu_z*t) for an area-pi pulse on |0>."""
    if probe == 'carrier':      # carrier-pi DURATION (weak sideband probe; old sim)
        return pi / (s * DW0)
    if probe == 'sideband':     # sideband-pi: full n=0<->1 transfer (realistic probe)
        return pi / (s * ETA_R * DW0)
    raise ValueError(probe)


def tpi_us(s, probe='sideband'):
    """Physical pi-pulse duration in microseconds (t = tau / (2*pi*nu_z))."""
    return _Tpulse(s, probe) / (2 * pi * NU_Z_HZ) * 1e6


def measure(nbar, s, Nf=18, shape='blackman', probe='sideband', loss=0.0, M=120,
            pops=None):
    """Drive RSB (delta=-1) and BSB (delta=+1); return red/blue amplitudes, the raw
    and carrier-pedestal-subtracted R, and the inferred <n>."""
    _, _, ncol, D = make_ops(Nf, ETA_R)
    p = thermal_pops(nbar, Nf) if pops is None else pops
    T = _Tpulse(s, probe)
    Ar = _Pe(-1.0, s, T, Nf, ncol, D, p, shape, False, loss, M)
    Ab = _Pe(+1.0, s, T, Nf, ncol, D, p, shape, False, loss, M)
    wr = _Pe(-1.0, s, T, Nf, ncol, D, p, shape, True,  loss, M)   # carrier wing (red)
    wb = _Pe(+1.0, s, T, Nf, ncol, D, p, shape, True,  loss, M)   # carrier wing (blue)
    Rraw = Ar / Ab
    Rsub = max(Ar - wr, 0.0) / max(Ab - wb, 1e-30)
    return dict(Ar=Ar, Ab=Ab, wing_r=wr, wing_b=wb, wing_frac=wb / Ab,
                R_raw=Rraw, n_raw=invert(Rraw), R_sub=Rsub, n_sub=invert(Rsub), T=T)


# ============================== scatter model ===================================
def scatter_per_pulse(Delta_MHz, probe='sideband'):
    """Spontaneous-scatter probability per area-pi pulse, balanced Raman beams.
       carrier-pi : pi*Gamma/Delta ;  sideband-pi : (pi*Gamma/Delta)/ETA_R
    (the sideband pulse is 1/ETA_R longer, so it scatters that much more)."""
    base = pi * GAMMA_MHz / Delta_MHz
    return base / ETA_R if probe == 'sideband' else base


def loss_dimensionless(Delta_MHz, probe='sideband'):
    """Uniform decay rate Gamma_sc/nu_z to feed H_block(loss=...), set so that the
    integrated loss over the area-pi pulse equals scatter_per_pulse(Delta)."""
    Nsc = scatter_per_pulse(Delta_MHz, probe)
    T = _Tpulse(0.10, probe)             # T scales as 1/s; Gamma_sc*T is s-independent here
    # Gamma_sc * t = (loss)*T  (dimensionless) = Nsc  ->  loss = Nsc/T, but we want a
    # rate independent of s: use Gamma_sc/nu_z = Nsc / (T at this s) is s-dependent; instead
    # return Gamma_sc/nu_z directly = GAMMA_OVER_NU * Omega0/Delta with Omega0=s*nu_z folded
    # in by the caller. Simpler: caller passes s; see scatter_loss_for(s,Delta).
    return Nsc, T


def scatter_loss_for(s, Delta_MHz, probe='sideband'):
    """Gamma_sc/nu_z for given carrier-Rabi fraction s and detuning (balanced beams,
       Gamma_sc = Gamma * Omega0/Delta)."""
    return GAMMA_OVER_NU * (s * NU_Z) / Delta_MHz       # = (Gamma/nu_z)*(Omega0/Delta)


# ============================== calibration (Q1) ================================
def calibration_curve(s=0.10, shape='blackman', probe='sideband',
                      nbar_list=(0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0),
                      Delta_MHz=800.0, Nf=24):
    """R-vs-<n> with the chosen pulse, with scatter loss for Delta folded in.
    Returns list of (nbar_in, n_raw, n_sub)."""
    loss = scatter_loss_for(s, Delta_MHz, probe)
    out = []
    for nb in nbar_list:
        m = measure(nb, s=s, Nf=Nf, shape=shape, probe=probe, loss=loss)
        out.append((nb, m['n_raw'], m['n_sub']))
    return out


# ============================== BSB Rabi flop + fit (Q2) ========================
def bsb_flop(pops, s=0.10, areas=None, Nf=24, shape='square', loss=0.0):
    """Blue-sideband excited population vs pulse area (multiples of the n=0->1 pi)."""
    if areas is None:
        areas = np.linspace(0.0, 4.0, 41)            # in units of the n0->1 pi-area
    _, _, ncol, D = make_ops(Nf, ETA_R)
    T1 = _Tpulse(s, 'sideband')                      # n=0->1 pi duration
    Pe = []
    for am in areas:
        Pe.append(_Pe(+1.0, s, am * T1, Nf, ncol, D, pops, shape, False, loss))
    return np.array(areas), np.array(Pe)


def fit_P0_from_bsb(nbar_true=0.0047, s=0.10, Delta_MHz=800.0, Nf=24,
                    M_shots=2000, seed=0, nmax_fit=4):
    """Simulate a noisy BSB flop at <n>=nbar_true and Delta, then fit the Fock
    populations and return the recovered P0 vs the true P0."""
    rng = np.random.default_rng(seed)
    pops = thermal_pops(nbar_true, Nf)
    loss = scatter_loss_for(s, Delta_MHz, 'sideband')
    areas, Pe = bsb_flop(pops, s=s, Nf=Nf, shape='square', loss=loss)
    # projection noise
    Pe_noisy = Pe + rng.normal(0, np.sqrt(np.clip(Pe, 1e-6, 1) * (1 - np.clip(Pe, 1e-6, 1)) / M_shots))
    # model: sum_n q_n sin^2(sqrt(n+1) * theta/2) * exp(-gamma*theta), theta=area*pi
    from scipy.optimize import curve_fit

    def model(area, *q):
        q = np.array(q)
        th = area * pi
        damp = np.exp(-q[-1] * th)
        s_ = np.zeros_like(area)
        for n in range(len(q) - 1):
            s_ = s_ + q[n] * np.sin(np.sqrt(n + 1) * th / 2.0) ** 2
        return s_ * damp
    p0 = [0.9] + [0.05] * (nmax_fit - 1) + [0.05]
    try:
        popt, _ = curve_fit(model, areas, Pe_noisy, p0=p0, maxfev=20000)
        q = np.clip(popt[:-1], 0, None); q = q / q.sum()
        return dict(P0_true=pops[0], P0_fit=q[0], ok=abs(q[0] - pops[0]) < 0.10)
    except Exception as e:                                   # pragma: no cover
        return dict(P0_true=pops[0], P0_fit=np.nan, ok=False, err=str(e))


# ============================== branching-resolved re-entry =====================
def scatter_branching(Delta_MHz):
    """Branching of ONE spontaneous-scatter event during the far-detuned Raman
    pulse, from the tool's CG line strengths + m-resolved decay. The drive takes
    |g>=|1,-1> (sig+) and |e>=|2,+1> (sig-) to |F',0> virtual states; the atom
    then decays. Returns relative scatter-rate factors and probabilities to land
    back in g, in e (the DETECTED state), or lost."""
    from eit_cooling_tool import CGc, Sfac, decay_branch, DF

    def _bf(Fg, mg, q, Fps):
        w = {}
        for Fp in Fps:
            mp = mg + q
            if abs(mp) > Fp:
                continue
            det = Delta_MHz - DF[Fp]
            w[Fp] = CGc(Fg, mg, q, Fp, mp) ** 2 * Sfac(Fg, Fp) / det ** 2
        tot = sum(w.values()); dest = {}
        for Fp, wi in w.items():
            for gg, p in decay_branch(Fp, 0, None).items():
                dest[gg] = dest.get(gg, 0.0) + (wi / tot) * p
        return tot, dest

    rg, dg = _bf(1, -1, +1, [0, 1, 2])
    re_, de = _bf(2, +1, -1, [1, 2, 3])
    return dict(rate_g=rg, rate_e=re_,
                g_to_g=dg.get((1, -1), 0.0), g_to_e=dg.get((2, 1), 0.0),
                g_to_lost=1 - dg.get((1, -1), 0.0) - dg.get((2, 1), 0.0),
                e_to_g=de.get((1, -1), 0.0), e_to_e=de.get((2, 1), 0.0),
                e_to_lost=1 - de.get((1, -1), 0.0) - de.get((2, 1), 0.0))


def recoil_heating_per_scatter():
    """Axial <dn> per scatter: absorption (eta_z) + emission (3-pt, var 1/3)."""
    return ETA_Z ** 2 * (1.0 + 1.0 / 3.0)


def reentry_pedestal(Delta_MHz, nbar=0.0047, s=0.12, Nf=10, shape='blackman',
                     backgrounds=True):
    """Master-equation pedestal: solve the sideband pulse with scatter modeled as
    branching-resolved collapse operators (to g / e / lost) and report the
    red/blue excited population, the raw inferred <n>, and (optionally) the
    OFF-SIDEBAND-background-subtracted <n>. Recoil omitted in the collapse motion
    (the pedestal counts |e> at ALL n); recoil heating reported separately."""
    import qutip as qt
    wz = 2 * pi * NU_Z                                  # rad/us
    Om0 = s * wz
    T = tpi_us(s, 'sideband')                           # us
    Nsc = scatter_per_pulse(Delta_MHz, 'sideband')
    br = scatter_branching(Delta_MHz)
    ravg = 0.5 * (br['rate_g'] + br['rate_e'])
    Gg = (Nsc / T) * (br['rate_g'] / ravg)
    Ge = (Nsc / T) * (br['rate_e'] / ravg)

    g, e, dk = qt.basis(3, 0), qt.basis(3, 1), qt.basis(3, 2)
    sgg, see = g * g.dag(), e * e.dag()
    seg, sge = e * g.dag(), g * e.dag()
    sdg, sde = dk * g.dag(), dk * e.dag()
    a = qt.destroy(Nf); ncol = a.dag() * a; Im = qt.qeye(Nf)
    D = qt.displace(Nf, 1j * ETA_R)
    ts = np.linspace(0, T, 200); wbk = _blackman(200); amp = 200.0 / np.sum(wbk)

    def run_delta(delta):
        Hc = (Om0 / 2.0) * (qt.tensor(seg, D) + qt.tensor(sge, D.dag()))
        Hs = wz * qt.tensor(sgg + see, ncol) - delta * wz * qt.tensor(see, Im)
        if shape == 'blackman':
            H = [Hs, [Hc, qt.coefficient(lambda t, args: amp * np.interp(t, ts, wbk))]]
        else:
            H = Hs + Hc
        c = [np.sqrt(Gg * br['g_to_g']) * qt.tensor(sgg, Im),
             np.sqrt(Gg * br['g_to_e']) * qt.tensor(seg, Im),
             np.sqrt(Gg * br['g_to_lost']) * qt.tensor(sdg, Im),
             np.sqrt(Ge * br['e_to_g']) * qt.tensor(sge, Im),
             np.sqrt(Ge * br['e_to_e']) * qt.tensor(see, Im),
             np.sqrt(Ge * br['e_to_lost']) * qt.tensor(sde, Im)]
        rho0 = qt.tensor(g * g.dag(), qt.Qobj(np.diag(thermal_pops(nbar, Nf))))
        out = qt.mesolve(H, rho0, np.linspace(0, T, 30), c_ops=c,
                         e_ops=[qt.tensor(see, Im)], options={'nsteps': 40000})
        return float(out.expect[0][-1])

    Ar, Ab = run_delta(-1.0), run_delta(+1.0)
    R_raw = Ar / Ab
    if backgrounds:
        bg_r, bg_b = run_delta(-0.5), run_delta(+0.5)
        R_sub = max(Ar - bg_r, 0.0) / max(Ab - bg_b, 1e-30)
    else:
        bg_r = bg_b = np.nan
        R_sub = np.nan
    return dict(A_red=Ar, A_blue=Ab, bg_red=bg_r, bg_blue=bg_b,
                R_raw=R_raw, ped_red=bg_r, sig_red=Ar - bg_r,
                n_raw=invert(R_raw), n_sub=invert(R_sub),
                Nsc=Nsc, P_g_to_e=br['g_to_e'])


# ============================== radial contrast =================================
def radial_sideband_broadening(T_radial_uK, w_um=19.0):
    """Axial sideband frequency spread across the cloud: nu_z(r)=nu_z*sqrt(s(r)),
    s=exp(-2 r^2/w^2). r_rms for a 2D harmonic radial cloud = w*sqrt(T/(2*U0)).
    Returns (r_rms_um, dnu_z_kHz at r_rms)."""
    U0_uK = 1094.0                                    # axial well depth (project value)
    r_rms = w_um * np.sqrt(T_radial_uK / (2.0 * U0_uK))
    s_r = np.exp(-2.0 * r_rms ** 2 / w_um ** 2)
    dnu = NU_Z * (1.0 - np.sqrt(s_r)) * 1e3           # kHz
    return r_rms, dnu


# ============================== cooled distribution (lazy) ======================
def cooled_distribution(preset_name='dual_end_optimal', Nf=6):
    """Fetch the actual m'=0 cooled Fock distribution from the tool (slow: runs a
    servoed solve). Returned padded to length Nf."""
    from eit_cooling_tool import run, preset
    res = run(preset(preset_name), full=True)
    m = np.array(res['motion'])
    if len(m) < Nf:
        m = np.concatenate([m, np.zeros(Nf - len(m))])
    return res['nbar'], m[:Nf] / m[:Nf].sum()


# ============================== self-tests ======================================
def _selftests():
    print("thermometry.py self-tests (ETA_R=%.3f, nu_z=%g kHz, Gamma=%g MHz)"
          % (ETA_R, NU_Z * 1e3, GAMMA_MHz))
    ok = True

    # GATE 1: weak-probe, pedestal-subtracted <n> recovers input
    g1 = True
    for nb in (0.02, 0.05, 0.10):
        m = measure(nb, s=0.02, Nf=20, shape='square', probe='carrier')
        g1 &= abs(m['n_sub'] - nb) < 3e-3
    print("  [1] weak-probe recovery (sub):           ", "PASS" if g1 else "FAIL")
    ok &= g1

    # GATE 2: Nf-stability of the raw inference at the operating point
    vals = [measure(0.0047, s=0.05, Nf=N, shape='square', probe='carrier')['n_raw']
            for N in (12, 16, 20, 24)]
    g2 = (max(vals) - min(vals) < 5e-4)
    print("  [2] Nf-stability (spread %.1e):          " % (max(vals) - min(vals)),
          "PASS" if g2 else "FAIL")
    ok &= g2

    # GATE 3: uniform scatter leaves R invariant (cancels in the ratio)
    m0 = measure(0.05, s=0.10, Nf=20, shape='square', probe='sideband', loss=0.0)
    m1 = measure(0.05, s=0.10, Nf=20, shape='square', probe='sideband', loss=0.30)
    g3 = abs(m0['R_raw'] - m1['R_raw']) < 1e-9
    print("  [3] scatter cancels in R (|dR|=%.1e):  " % abs(m0['R_raw'] - m1['R_raw']),
          "PASS" if g3 else "FAIL")
    ok &= g3

    # GATE 4: Blackman suppresses the carrier wing far below the signal at the floor
    sq = measure(0.0047, s=0.12, Nf=22, shape='square',   probe='sideband')
    bl = measure(0.0047, s=0.12, Nf=22, shape='blackman', probe='sideband')
    g4 = (bl['wing_frac'] < sq['wing_frac'] / 50.0)
    print("  [4] Blackman wing/Ab %.1e vs square %.1e: " % (bl['wing_frac'], sq['wing_frac']),
          "PASS" if g4 else "FAIL")
    ok &= g4

    print("  OVERALL:", "PASS" if ok else "FAIL")
    return ok


# ============================== re-entry summary ================================
def reentry_summary(Deltas=(800.0, 4000.0), s=0.12, Nf=9,
                    calib_n=(0.005, 0.05, 0.2)):
    """Branching-resolved scatter re-entry: the branching, the recoil heating, the
    master-equation pedestal (raw + the failed off-sideband subtraction), and a
    short calibration showing R stays monotonic with a ~constant offset."""
    line = "=" * 74
    print(line)
    print("Branching-resolved scatter RE-ENTRY (thermometry.py v%s)" % __version__)
    print(line)
    print("Recoil heating per scatter event: <dn> = %.4f phonons" % recoil_heating_per_scatter())

    print("\n1) Branching of one scatter event (CG line strengths + m-resolved decay):")
    print("   Delta[MHz]   src   ->g(=|1,-1>)  ->e(=|2,+1>,DETECTED)   ->lost   rate(rel)")
    for D in Deltas:
        b = scatter_branching(D)
        rg, re_ = b['rate_g'], b['rate_e']
        print("   %6d       g     %.3f         %.3f                  %.3f    %.2f"
              % (D, b['g_to_g'], b['g_to_e'], b['g_to_lost'], rg / (0.5 * (rg + re_))))
        print("   %6s       e     %.3f         %.3f                  %.3f    %.2f"
              % ("", b['e_to_g'], b['e_to_e'], b['e_to_lost'], re_ / (0.5 * (rg + re_))))
    print("   -> a scatter from |g> lands in the DETECTED state |e> ~10%% of the time;")
    print("      with N_sc per pulse this is an incoherent pedestal on the tiny red signal.")

    print("\n2) Master-equation pedestal at the floor (<n>=0.0047, Blackman sideband-pi):")
    print("   Delta[MHz]  N_sc    A_red    off-sb bg   <n>_raw   <n>_sub(off-sb)   [true 0.0047]")
    for D in Deltas:
        r = reentry_pedestal(D, nbar=0.0047, s=s, Nf=Nf, backgrounds=True)
        print("   %6d      %4.1f%%  %.5f  %.5f     %.4f    %.4f"
              % (D, 100 * r['Nsc'], r['A_red'], r['bg_red'], r['n_raw'], r['n_sub']))
    print("   -> naive R/(1-R) is biased (pedestal ~3x signal at 0.8 GHz); the off-sideband")
    print("      background OVER-subtracts (it is undepleted, the on-resonance pedestal is")
    print("      depleted by re-driving) -> neither raw nor subtraction is correct.")

    print("\n3) CALIBRATION absorbs the pedestal (Delta=%g MHz): R is monotonic in <n>" % Deltas[0])
    print("   <n>_in    R(ideal,no scatter)   R(mesolve,w/pedestal)   offset")
    for nb in calib_n:
        Rid = measure(nb, s=s, Nf=Nf + 3, shape='blackman', probe='sideband')['R_raw']
        rm = reentry_pedestal(Deltas[0], nbar=nb, s=s, Nf=Nf, backgrounds=False)['R_raw']
        print("   %.3f     %.4f                %.4f                  %+.4f" % (nb, Rid, rm, rm - Rid))
    print("   -> ~constant offset, slope dR/d<n> preserved: calibrate R vs known <n>")
    print("      (never naive R/(1-R)). Pedestal is an SNR cost (~2-3x shots at 0.8 GHz,")
    print("      ~1.3x at 4 GHz); higher Delta is an SNR upgrade, not a bias fix.")
    print(line)


# ============================== report (architecture) ===========================
def report(Delta_lo=800.0, Delta_hi=4000.0, s=0.12):
    line = "=" * 74
    print(line)
    print("Asymmetric-sideband thermometry (m'=0 clock pair |1,-1><->|2,+1>)")
    print("  ETA_R=%.3f  nu_z=%g kHz" % (ETA_R, NU_Z * 1e3))
    print("  sideband-pi duration vs probe strength s (Blackman decouples carrier leak,")
    print("  so larger s -> shorter pulse is allowed):")
    print("     s        " + "  ".join("%.2f" % x for x in (0.12, 0.2, 0.3, 0.5)))
    print("     t_pi[us] " + "  ".join("%.1f" % tpi_us(x) for x in (0.12, 0.2, 0.3, 0.5)))
    print(line)

    print("\nSCATTER per area-pi pulse (the cost of a low single-photon detuning):")
    print("   Delta[MHz]   carrier-pi   sideband-pi (the realistic probe)")
    for D in (300, 800, 1000, 2000, 4000):
        print("   %6d       %6.1f%%      %6.1f%%"
              % (D, 100 * scatter_per_pulse(D, 'carrier'), 100 * scatter_per_pulse(D, 'sideband')))
    print("   -> uniform scatter CANCELS in R = A_red/A_blue (self-test [3]); it costs")
    print("      atom survival / SNR, not bias.")

    print("\nQ1  R-vs-<n> CALIBRATION (sideband-pi, scatter for Delta folded in):")
    for D in (Delta_lo, Delta_hi):
        print("   --- Delta = %g MHz (sideband scatter %.1f%%) ---"
              % (D, 100 * scatter_per_pulse(D, 'sideband')))
        print("     <n>_in   square n_raw   Blackman n_raw   Blackman n_sub")
        for nb in (0.005, 0.02, 0.05, 0.2, 0.5):
            sq = measure(nb, s=s, Nf=24, shape='square',   probe='sideband',
                         loss=scatter_loss_for(s, D, 'sideband'))
            bl = measure(nb, s=s, Nf=24, shape='blackman', probe='sideband',
                         loss=scatter_loss_for(s, D, 'sideband'))
            print("     %.3f    %+.4f        %+.4f          %+.4f"
                  % (nb, sq['n_raw'], bl['n_raw'], bl['n_sub']))

    print("\nQ2  BSB Rabi-flop fit of P0 at the floor (<n>=0.0047, ~2000 shots):")
    print("     Delta[MHz]   P0_true   P0_fit    within +-10%?")
    for D in (300, 800, 2000, 4000):
        r = fit_P0_from_bsb(0.0047, s=s, Delta_MHz=D, M_shots=2000, seed=1)
        print("     %6d       %.4f    %.4f    %s"
              % (D, r['P0_true'], r['P0_fit'], "yes" if r['ok'] else "NO"))

    print("\nRADIAL contrast (axial sideband spread across the cloud):")
    print("     T_radial[uK]   r_rms[um]   d(nu_z) at r_rms [kHz]")
    for Tr in (20, 50, 100, 200):
        rr, dn = radial_sideband_broadening(Tr)
        print("     %6d         %.2f        %.1f" % (Tr, rr, dn))
    print(line)


if __name__ == "__main__":
    import sys
    np.set_printoptions(precision=4, suppress=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "test"
    if mode == "test":
        _selftests()
    elif mode == "report":
        report()
    elif mode == "reentry":
        reentry_summary()
    elif mode == "calib":
        for nb, nr, ns in calibration_curve():
            print("  <n>_in=%.3f  n_raw=%+.4f  n_sub=%+.4f" % (nb, nr, ns))
    else:
        print("usage: thermometry.py [test|report|reentry|calib]")
