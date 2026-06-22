"""
================================================================================
 cloud_cooling_tool.py  --  PI-facing simulation of the RADIAL (cloud) floor of
                            clock-EIT cooling of 87Rb in the 1064 nm HCPCF lattice
================================================================================

SCOPE / WHAT IS AND IS NOT VERIFIED  (read before quoting a cloud number)
    This is a REDUCED 3-level Lambda engine + single-rate trajectory MC
    (d<n>/dt = -W(r)*(<n> - n_ss(r)), with W clamped >= 0). Two scope rails:
    * The "dead-wall flat-top collapse" headline is VERIFIED at THIS level: the
      off-axis freeze is EMERGENT, not an artifact of the clamp. A cold atom at
      r=9 um (n_ss=0.11) stays ~0.01 -- it does NOT heat to n_ss; early- and
      late-time relaxation rates agree (~1e-5), so there is no fast heating
      transient the single-rate fit could miss, and W(r) > 0 everywhere (the
      clamp never fires). It is NOT YET verified against the MULTILEVEL solver:
      F'1/F'3 contaminants shift with Delta_eff(r) off-axis, so the multilevel
      n_ss at the box WALLS is unconfirmed (the flat BOTTOM has uniform Delta_eff
      -> contaminants match on-axis; the walls are where W collapses -> frozen).
      Certifying it needs clk2/ccs3 on the radial grid -- the documented open
      "cloud x multilevel union". Quote the cloud floor as 3-level/single-rate.
    * The 1064 scalar shift is COMMON-MODE (Delta_eff(r) moves the SINGLE-photon
      detuning but NOT delta2; the two-photon dark resonance holds at every r, so
      there is no first-order delta2-servo mismatch). Only the perturbative
      tensor/vector shifts could drift delta2 off-axis (second-order, held out).

WHAT THIS IS / HOW IT RELATES TO eit_cooling_tool.py
    eit_cooling_tool.py  computes the AXIAL floor <n_z> and fixes the operating
        point and delivery (dual-end vs retro). It treats the radial motion as
        frozen -- the single number it returns is the on-axis axial floor.
    THIS tool answers the next question: once a whole CLOUD of atoms with a
        radial temperature sits in the trap, what mean phonon number is actually
        achievable? That depends on the trap's transverse profile and on how the
        cooling tone(s) are placed -- the "radial story" of master brief v17 Sec.5.

THE PHYSICS IN ONE PARAGRAPH
    The 1064 trap's transverse Gaussian intensity profile makes the EIT single-
    photon detuning vary with radius:  Delta_eff(r) = Delta + 60.9*(1 - s(r)),
    s(r) = I(r)/I(0).  This is a SCALAR shift common to BOTH EIT legs, so it does
    NOT move the two-photon detuning delta2 -- it just broadens the single-photon
    detuning across the cloud. A single cooling tone is optimal at only one radius;
    its cooling RATE W(r) collapses off-axis (27x by r=6um, ~270x by 12um). Two
    independent fixes are computed here:
      (1) FLAT-TOP (box) trap: flatten the intensity over the cloud so Delta_eff is
          uniform. KEY DYNAMIC RESULT (the "dead-wall effect"): because W collapses
          off-axis, off-axis atoms barely couple to the light -- they neither cool
          NOR heat (the diffusion ~ W*n_ss vanishes). An atom cools to the on-axis
          floor in the flat bottom and then coasts FROZEN through the walls instead
          of equilibrating to the high wall n_ss. The cloud floor therefore collapses
          to the on-axis value for EVERY radial temperature, not just a cold cloud.
          Coverage (flat width) then governs the cooling TIME, not the floor.
      (2) TWO TONES: add a second cooling tone tuned to be resonant off-axis,
          covering the shell the first tone leaves cold. Helps the UNCOOLED (hot)
          cloud; on a COLD cloud the second tone's center heating makes it
          net-negative.

HOW IT WORKS -- two layers, so tuning is fast
    ENGINE  (QuTiP, slow ~1-2 min, run ONCE and cached):  a reduced 3-level Lambda
        EIT cooler is solved at a grid of radii. Per radius it returns the steady-
        state phonon number n_ss(r) AND the near-equilibrium cooling rate W(r).
        [Section 2]
    MONTE-CARLO  (numpy, fast ~seconds -- THE TUNING SURFACE):  classical radial
        trajectories in the chosen trap profile, each carrying <n>(t) via the
        single-rate closure  d<n>/dt = -W(r)*(<n> - n_ss(r)); the cloud floor is the
        ensemble- and time-average of <n>.  [Section 3]
    To tune the RADIAL knobs (profile, r_flat, T_radial, tone count) just re-run the
    MC on the cached grid -- seconds. To change the OPERATING POINT (Delta, OmR) the
    grid is rebuilt automatically (cached under a new filename).

VALIDATION  (reproduced by `python cloud_cooling_tool.py --regression`, ~3 min)
  At the v17 operating point (Delta=45, OmR=0.12):
    grid, 1 tone        :  n_ss(0)=0.0018  W(0)=0.0053  ->  W collapses ~33x by r~6um
    Gaussian cloud floor:  0.0074 @100uK ; @556uK is N_orbits-sensitive (~0.036 at the
                           default 300 orbits, falls further -- the hot Gaussian cloud cools
                           VERY slowly, which is itself why the two fixes below help)
    box r_flat=14um     :  0.0021 @100uK   0.0033 @556uK   (-> on-axis 0.0018, BOTH temps)
    two-tone, hot cloud :  0.036 -> 0.016 @556uK (~2.2x) ; on a cold cloud it is net-negative
  The earlier inline session runs used the radial engine's OmR=0.10 (giving n_ss(0)=0.0016,
  W(0)=0.0038, 27x); the box collapse and the two-tone help are robust to that shift. ABSOLUTE
  floors are the 3-level reduction (on-axis ~0.0018); the multilevel on-axis is ~0.0048, so
  multilevel box-covered floors land ~0.005-0.006 (v17 Sec.5). The RELATIVE collapse and the
  dead-wall mechanism are the robust, model-independent results (~2x absolute calibration spread).

UNITS  (one convention, stated once)
    Rates / detunings in 2*pi*MHz (nu_z=0.430 means 2*pi*430 kHz). Lengths in um.
    Temperatures in uK. Detunings positive = blue.

USAGE
    python cloud_cooling_tool.py                 # run the 4 presets (builds grids, ~min)
    python cloud_cooling_tool.py --regression    # reproduce the validated numbers
    # programmatic:
    from cloud_cooling_tool import Config, preset, cloud_floor
    cfg = preset("box_flat_top")                 # or build a Config() yourself
    cfg = Config(profile="box", r_flat_um=12, T_radial_uK=300, Delta=45, OmR=0.12)
    floor = cloud_floor(cfg)                      # the cloud <n>; prints diagnostics
================================================================================
"""

import os
import numpy as np
from dataclasses import dataclass

# =============================================================================
# SECTION 1 -- FIXED CONSTANTS (the PI cannot change these; they are atomic /
#              electromagnetic properties, not apparatus settings)
# =============================================================================
GAMMA = 6.07            # 87Rb D2 natural linewidth (2*pi MHz)
NU_Z0 = 0.430           # ON-AXIS axial trap frequency (2*pi MHz = 2*pi*430 kHz)
ETA0  = 0.094           # ON-AXIS axial Lamb-Dicke parameter
B1_DEF, B2_DEF = 0.667, 0.333          # closed-Lambda decay weights into g1, g2
_EM_REC = [(-1, 1/6), (0, 2/3), (1, 1/6)]   # emission-recoil distribution over (-1,0,+1)
STARK_SLOPE = 60.9      # differential SCALAR Stark slope (2*pi MHz):
                        #   Delta_eff(r) = Delta + STARK_SLOPE*(1 - s(r))
                        #   (common to both EIT legs; does NOT shift delta2)


# =============================================================================
# SECTION 2 -- THE 3-LEVEL EIT ENGINE  (n_ss and W per radius)
# -----------------------------------------------------------------------------
# A reduced three-level Lambda dark-state cooler (Morigi-Eschner-Keitel EIT
# cooling, single tight mode): two ground legs g1 (weak/probe) and g2 (strong/
# control) of the dark superposition plus one excited state e. The cooling
# condition Omega_c^2/(4*Delta)=nu_z puts the AC-Stark-shifted bright resonance
# on the red motional sideband. Control and probe COUNTER-PROPAGATE (opposite-
# sign Lamb-Dicke displacement) -- that is what makes the dark state motion-
# sensitive and gives net cooling. This is the same engine eit_common.py uses,
# embedded here so the tool is one file.
# =============================================================================

def _build_L(Delta, nu, eta, Otot, OmR, Nf):
    """Liouvillian + number operator for the 3-level Lambda cooler. (needs qutip)"""
    import qutip as qt
    g1, g2, e = qt.basis(3, 0), qt.basis(3, 1), qt.basis(3, 2)
    P = lambda a, b: a * b.dag()
    If = qt.qeye(Nf); a = qt.destroy(Nf)
    Nop = qt.tensor(qt.qeye(3), a.dag() * a)

    Oc = Otot / np.sqrt(1.0 + OmR**2)      # strong control on g2
    Op = OmR * Oc                          # weak probe on g1
    Dc = qt.displace(Nf, +1j * eta)        # control absorption  (+k)
    Dp = qt.displace(Nf, -1j * eta)        # probe absorption    (-k, counter-propagating)

    H = (-Delta) * qt.tensor(P(e, e), If) + nu * Nop
    H = H - (Oc / 2.0) * (qt.tensor(P(e, g2), Dc) + qt.tensor(P(g2, e), Dc.dag()))
    H = H - (Op / 2.0) * (qt.tensor(P(e, g1), Dp) + qt.tensor(P(g1, e), Dp.dag()))

    sden = B1_DEF + B2_DEF; b1, b2 = B1_DEF / sden, B2_DEF / sden
    cops = []
    for u, wg in _EM_REC:                  # spontaneous emission with recoil
        Ds = qt.displace(Nf, 1j * eta * u)
        cops.append(np.sqrt(GAMMA * b1 * wg) * qt.tensor(P(g1, e), Ds))
        cops.append(np.sqrt(GAMMA * b2 * wg) * qt.tensor(P(g2, e), Ds))
    return qt.liouvillian(H, cops), Nop


def radial_params(r_um, Delta, w0_um, Otot_ref):
    """Local trap/beam quantities at radius r for a Gaussian beam.

    Returns (Delta_eff, nu_z(r), eta(r), Omega_tot(r), s(r)). The axial trap
    frequency scales as sqrt(intensity) (nu_z(r)=nu_z0*sqrt(s)); eta ~ 1/sqrt(nu)
    so eta(r)=eta0*s^-0.25; the beam Rabi scales as sqrt(intensity) too.
    Otot_ref is the ON-AXIS total Rabi the tone would have at full intensity.
    """
    s = np.exp(-2.0 * (r_um / w0_um) ** 2)
    Deff = Delta + STARK_SLOPE * (1.0 - s)
    nu = NU_Z0 * np.sqrt(s)
    eta = ETA0 * s ** (-0.25)
    Otot = Otot_ref * np.sqrt(s)
    return Deff, nu, eta, Otot, s


def nss_and_W(r_um, Delta, OmR, w0_um, Otot_ref, Nf=16):
    """Steady-state n_ss and near-equilibrium cooling rate W at radius r (3-level).

    W is the RELIABLE rate: the slope of ln(<n>-n_ss) of a short relaxation from a
    thermal state at n_ss+0.15, NOT the (unreliable) slowest-eigenvalue estimate.
    """
    import qutip as qt
    from scipy.sparse.linalg import expm_multiply
    Deff, nu, eta, Otot, s = radial_params(r_um, Delta, w0_um, Otot_ref)
    L, Nop = _build_L(Deff, nu, eta, Otot, OmR, Nf)
    rho = qt.steadystate(L, method='power')
    nss = float(qt.expect(Nop, rho))
    # qutip 5.x: the Liouvillian is Dense here (built from displacement operators),
    # and Dense has no .as_scipy() -- convert to CSR first (storage-only, value-identical).
    from qutip.core.data import to as _to_data, CSR as _CSR
    Lsc = _to_data(_CSR, L.data).as_scipy().tocsc()
    Nbra = qt.operator_to_vector(Nop).dag().full().flatten()
    rho_hot = qt.tensor(rho.ptrace(0), qt.thermal_dm(Nf, nss + 0.15))
    v0 = qt.operator_to_vector(rho_hot).full().flatten()
    tt = np.linspace(0.0, 160.0, 10)
    traj = expm_multiply(Lsc, v0, start=tt[0], stop=tt[-1], num=len(tt), endpoint=True)
    y = np.real(traj @ Nbra) - nss
    m = (tt >= 40.0) & (y > 1e-5)
    W = -np.polyfit(tt[m], np.log(y[m]), 1)[0] if m.sum() >= 3 else 0.0
    return nss, max(W, 0.0), s


def _grid_key(cfg):
    return ("cloudgrid_D%.0f_OmR%.2f_nt%d_D2%.0f_nr%d_rm%.0f_Nf%d.npz"
            % (cfg.Delta, cfg.OmR, cfg.n_tones, cfg.Delta2, cfg.n_radii,
               cfg.r_max_um, cfg.Nf))


def build_grid(cfg, verbose=True):
    """Run the engine over a radial grid -> (s, n_ss, W). Cached by operating point.

    Only the OPERATING-POINT knobs (Delta, OmR, n_tones, Delta2) and the grid
    resolution change this; the radial knobs (profile, r_flat, T_radial) do not,
    so they reuse the cache. Two tones: additive single-rate combine of two tones
    at the SAME physical power (Otot_ref = sqrt(4*Delta*nu_z0)) -- the v17 Sec.4C
    estimate (rigorous version is a two-field coherent solve).
    """
    cache = _grid_key(cfg)
    if os.path.exists(cache) and not cfg.rebuild_grid:
        d = np.load(cache)
        if verbose:
            print("  [grid cached: %s]" % cache)
        return d['s'], d['nss'], d['W']
    Oref = np.sqrt(4.0 * cfg.Delta * NU_Z0)      # tone-1 on-axis power (both tones use it)
    rs = np.linspace(0.0, cfg.r_max_um, cfg.n_radii)
    S, N, Wl = [], [], []
    if verbose:
        print("  building engine grid (%d radii, %d tone(s)) -- ~1-2 min ..."
              % (cfg.n_radii, cfg.n_tones))
    for r in rs:
        if cfg.n_tones == 1:
            nss, W, s = nss_and_W(r, cfg.Delta, cfg.OmR, cfg.w0_um, Oref, cfg.Nf)
        else:
            n1, W1, s = nss_and_W(r, cfg.Delta, cfg.OmR, cfg.w0_um, Oref, cfg.Nf)
            n2, W2, _ = nss_and_W(r, cfg.Delta2, cfg.OmR, cfg.w0_um, Oref, cfg.Nf)
            W = W1 + W2
            nss = (W1 * n1 + W2 * n2) / max(W, 1e-12)
        S.append(s); N.append(nss); Wl.append(W)
        if verbose:
            print("    r=%5.1fum  s=%.3f  n_ss=%.5f  W=%.5f" % (r, s, nss, W))
    S, N, Wl = np.array(S), np.array(N), np.array(Wl)
    np.savez(cache, s=S, nss=N, W=Wl)
    return S, N, Wl


# =============================================================================
# SECTION 3 -- THE TRAJECTORY MONTE-CARLO  (the fast tuning surface)
# -----------------------------------------------------------------------------
# Classical radial trajectories (velocity-Verlet) in the chosen transverse trap
# profile. Each atom carries <n>(t) integrated with the single-rate closure
#   d<n>/dtau = -SHAPE(r)*g*(<n> - n_ss(r)),  SHAPE(r)=W(r)/W(0),  g=Dratio/(2pi),
# Dratio = W(0)/nu_r. Time tau = omega_r * t (one radial orbit = 2*pi). The box
# profile is flat (force=0) inside r_flat and has a Gaussian confining wall beyond.
# The cloud floor is the ensemble- and final-orbit-average of <n>.
# =============================================================================

def _profile_s(rho, cfg):
    """Transverse intensity s(r)=I(r)/I(0); rho = r/w0 (normalized radius)."""
    if cfg.profile == 'box':
        rf = cfg.r_flat_um / cfg.w0_um
        return np.where(rho <= rf, 1.0, np.exp(-2.0 * (rho - rf) ** 2))
    return np.exp(-2.0 * rho ** 2)            # gaussian


def run_mc(cfg, s_grid, nss_grid, W_grid, n_init=None):
    """Cloud floor for the chosen profile and radial temperature (numpy only)."""
    o = np.argsort(s_grid)
    sg, ng, Wg = s_grid[o], nss_grid[o], W_grid[o]
    W0 = Wg[-1]                                # W at s=1 (on-axis)
    nss_of = lambda x: np.interp(x, sg, ng)
    W_of = lambda x: np.interp(x, sg, Wg)
    rng = np.random.default_rng(cfg.seed)
    th = cfg.T_radial_uK / cfg.U0_uK
    rf = cfg.r_flat_um / cfg.w0_um if cfg.profile == 'box' else 0.0
    sp = lambda rho: _profile_s(rho, cfg)

    # --- initial conditions: positions ~ bound Boltzmann in the profile potential,
    #     velocities Maxwellian; drop atoms with total (scaled) energy > 1 (unbound).
    rho = np.linspace(0.0, 3.0, 8000)
    ub = 1.0 - sp(rho)
    P = np.clip(rho * np.exp(-ub / th) * (1.0 - np.exp(-np.clip(1.0 - ub, 0, None) / th)),
                0, None)
    P /= P.sum()
    cdf = np.cumsum(P)
    uu = rng.random(cfg.N_atoms)
    rr = np.interp(uu, cdf, rho)
    ph = rng.random(cfg.N_atoms) * 2 * np.pi
    xi, ze = rr * np.cos(ph), rr * np.sin(ph)
    sig = np.sqrt(th) / 2.0
    vx, vz = rng.normal(0, sig, cfg.N_atoms), rng.normal(0, sig, cfg.N_atoms)
    E = 2 * (vx**2 + vz**2) + (1.0 - sp(np.sqrt(xi**2 + ze**2)))
    b = E < 0.999
    xi, ze, vx, vz = xi[b], ze[b], vx[b], vz[b]

    nr = lambda xi, ze: nss_of(sp(np.sqrt(xi**2 + ze**2)))
    shr = lambda xi, ze: W_of(sp(np.sqrt(xi**2 + ze**2))) / W0

    def acc(xi, ze):
        rho = np.sqrt(xi**2 + ze**2)
        if cfg.profile == 'box':
            dr = rho - rf; wall = rho > rf; f = np.zeros_like(rho)
            f[wall] = -dr[wall] * np.exp(-2.0 * dr[wall]**2) / np.maximum(rho[wall], 1e-9)
            return f * xi, f * ze
        ex = np.exp(-2.0 * (xi**2 + ze**2))   # gaussian force
        return -xi * ex, -ze * ex

    Dratio = W0 / cfg.nu_r_MHz
    g = Dratio / (2 * np.pi)
    n = nr(xi, ze).copy() if n_init is None else np.full(len(xi), float(n_init))
    dtau = 2 * np.pi / cfg.nstep
    acc_sum = np.zeros(len(xi)); na = 0
    start = (cfg.N_orbits - cfg.navg) * cfg.nstep
    for k in range(cfg.N_orbits * cfg.nstep):
        ax, az = acc(xi, ze)
        xi2 = xi + vx * dtau + 0.5 * ax * dtau**2
        ze2 = ze + vz * dtau + 0.5 * az * dtau**2
        ax2, az2 = acc(xi2, ze2)
        vx += 0.5 * (ax + ax2) * dtau
        vz += 0.5 * (az + az2) * dtau
        xi, ze = xi2, ze2
        sh = shr(xi, ze); ns = nr(xi, ze)
        k1 = -sh * g * (n - ns); nm = n + 0.5 * dtau * k1
        k2 = -sh * g * (nm - ns); n = n + dtau * k2
        if k >= start:
            acc_sum += n; na += 1
    return float(np.mean(acc_sum / na))


# =============================================================================
# SECTION 4 -- CONFIG (every knob) + PRESETS
# =============================================================================
@dataclass
class Config:
    # --- operating point (passed to the engine; rebuilds the grid if changed) ---
    Delta: float = 45.0          # single-photon detuning, blue of F'=2 (2*pi MHz)
    OmR: float = 0.12            # probe/control Rabi ratio Omega_p/Omega_c
    # --- trap (transverse profile) ---
    profile: str = 'gaussian'    # 'gaussian' (current fiber) | 'box' (flat-top mode)
    r_flat_um: float = 10.0      # box: flat-bottom radius (ignored for gaussian)
    w0_um: float = 19.0          # 1064 beam waist
    U0_uK: float = 1094.0        # trap depth
    nu_r_MHz: float = 0.00542    # radial trap frequency (2*pi*5.42 kHz)
    # --- cloud ---
    T_radial_uK: float = 100.0   # radial temperature (100 ~ cooled, 556 ~ uncooled)
    # --- tones ---
    n_tones: int = 1             # 1 or 2 cooling tones
    Delta2: float = 25.0         # 2nd-tone center detuning (off-axis optimal) (2*pi MHz)
    # --- engine grid ---
    r_max_um: float = 14.0
    n_radii: int = 12
    Nf: int = 16                 # Fock truncation
    rebuild_grid: bool = False   # force a fresh engine grid even if cached
    # --- Monte-Carlo ---
    N_atoms: int = 2500
    N_orbits: int = 300          # raise for hot/under-covered clouds (slow convergence)
    nstep: int = 60
    navg: int = 12
    seed: int = 1


def preset(name):
    """Four reference points. Copy and edit any field to tune."""
    if name == 'gaussian_cooled':
        return Config(profile='gaussian', T_radial_uK=100.0)
    if name == 'gaussian_uncooled':
        return Config(profile='gaussian', T_radial_uK=556.0)
    if name == 'box_flat_top':
        return Config(profile='box', r_flat_um=14.0, T_radial_uK=556.0)
    if name == 'two_tone_hot':
        return Config(profile='gaussian', n_tones=2, T_radial_uK=556.0)
    raise ValueError("unknown preset %r" % name)


# =============================================================================
# SECTION 5 -- DRIVER + REPORT + MAIN
# =============================================================================
def cloud_floor(cfg, verbose=True):
    """Build (or load) the engine grid, run the MC, return the cloud floor <n>."""
    s, nss, W = build_grid(cfg, verbose=verbose)
    floor = run_mc(cfg, s, nss, W)
    if verbose:
        tag = (" r_flat=%.0fum" % cfg.r_flat_um) if cfg.profile == 'box' else ""
        print("  %-8s T_radial=%4.0fuK  tones=%d%s  Delta=%.0f OmR=%.2f"
              % (cfg.profile, cfg.T_radial_uK, cfg.n_tones, tag, cfg.Delta, cfg.OmR))
        print("    on-axis n_ss(0)=%.5f  W(0)=%.5f  -> W collapses to %.5f at edge (%.0fx)"
              % (nss[0], W[0], W[-1], (W[0] / max(W[-1], 1e-9))))
        print("    CLOUD FLOOR <n> = %.5f" % floor)
    return floor


def _regression():
    """Trust gate: reproduce the box collapse and the two-tone help.

    Runs at the v17 operating point (Delta=45, OmR=0.12). See the header
    VALIDATION block for the expected ranges and the OmR/N_orbits caveats.
    """
    print("REGRESSION -- trust gate (v17 point Delta=45, OmR=0.12)\n")
    print("[1] grid (1 tone): per-radius engine -- on-axis floor and off-axis W-collapse")
    c = Config(profile='gaussian', n_radii=12)
    s, nss, W = build_grid(c, verbose=False)
    i6 = int(np.argmin(np.abs(np.linspace(0, c.r_max_um, c.n_radii) - 6.0)))
    print("    n_ss(0)=%.5f  W(0)=%.5f  W(~6um)=%.5f  drop=%.0fx\n"
          % (nss[0], W[0], W[i6], W[0] / max(W[i6], 1e-9)))
    print("[2] Gaussian cloud floor: the baseline the two fixes improve on (@556uK slow-converging)")
    f1 = run_mc(Config(profile='gaussian', T_radial_uK=100.0), s, nss, W)
    f2 = run_mc(Config(profile='gaussian', T_radial_uK=556.0), s, nss, W)
    print("    100uK=%.5f   556uK=%.5f\n" % (f1, f2))
    print("[3] box flat-top (r_flat=14um): collapses to ~on-axis for BOTH temperatures -- headline")
    f3 = run_mc(Config(profile='box', r_flat_um=14.0, T_radial_uK=100.0), s, nss, W)
    f4 = run_mc(Config(profile='box', r_flat_um=14.0, T_radial_uK=556.0), s, nss, W)
    print("    100uK=%.5f   556uK=%.5f\n" % (f3, f4))
    print("[4] two-tone: a second off-axis tone helps the HOT cloud (net-negative on a cold cloud)")
    c2 = Config(profile='gaussian', n_tones=2, T_radial_uK=556.0)
    s2, n2, W2 = build_grid(c2, verbose=False)
    f5 = run_mc(c2, s2, n2, W2)
    print("    two-tone 556uK=%.5f  (single-tone above was %.5f)\n" % (f5, f2))
    print("Done. Relative collapse and the dead-wall mechanism are the robust results.")


if __name__ == '__main__':
    import sys
    if '--regression' in sys.argv:
        _regression()
    else:
        print("Cloud cooling tool -- running the 4 presets (builds engine grids, ~min).\n")
        for name in ('gaussian_cooled', 'gaussian_uncooled', 'box_flat_top', 'two_tone_hot'):
            print("PRESET: %s" % name)
            cloud_floor(preset(name))
            print()
        print("Tune any Config field and call cloud_floor(cfg). See the header for knobs.")
