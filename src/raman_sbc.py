"""
raman_sbc.py -- STANDARD resolved-sideband Raman cooling solver (built from
scratch; NOT a wrap of eit_common/combined_solve, which are dark-resonance
engines).  87Rb, 1064 nm kagome-HCPCF axial lattice.  v12 builder session.

MECHANISM (different from EIT/dRSC -- no dark state):
  A resolved red-sideband two-photon Raman drive on a SINGLE ground pair
  {|g_lo>,|g_hi>} removes one phonon (|g_lo,n> -> |g_hi,n-1>), alternated with
  optical pumping that resets |g_hi> -> |g_lo> with recoil.  The far-detuned
  excited state is adiabatically eliminated -> the Raman is an effective
  two-level coupling and the pump is a set of RATE Lindblads.  No inverted
  potential lives in the Fock basis (v11 sec8.1) so a truncated Fock(Nf) is
  safe and G4-convergent.

CONVENTION (pinned, gated):
  sigma_+ = |g_hi><g_lo| ; internal diagonal E_hi - E_lo = -delta_2 so the RED
  (cooling) sideband sits at delta_2 = -nu_z (G1/G3 verify).
  H = nu_z a^dag a - delta_2 P_hi
      - (Omega_R/2)[ |hi><lo| (x) D(i eta_eff(a+a^dag)) + h.c. ]
  D = qt.displace(Nf, i eta_eff) carries carrier + red + blue sidebands; nothing
  is dropped, so off-resonant heating (the A_+ term) is captured.
  Pump: |g_hi> (+ spectators) --rate--> excited(eliminated) --> grounds, with
  m-resolved CG branching (m_branch) and emission recoil EM_REC=(1/6,2/3,1/6) at
  kick eta, plus axial absorption recoil +eta on the pump leg.

PAIRS:
  'clock'    : g_lo=|1,-1>, g_hi=|2,+1>  (g_F m_F = +1/2 both -> 1st-order field
               insensitive).  Pump clears F=2 (sigma-) + repumps F=1 (sigma- on
               F'=1, leaving |1,-1> dark) -> MANY photons / return (high recoil).
  'stretched': g_lo=|2,+2>, g_hi=|2,+1>  (Zeeman pair, field-sensitive textbook
               baseline).  sigma+ pump on F'=2 (|2,+2> dark) + sigma+ F=1 repump
               -> near-cycling, FEW photons / return (low recoil).

Units: all frequencies in "MHz units" (=2pi*MHz cancels in ratios). A rate R in
these units is R*RATE_MHZ_TO_PER_MS per millisecond.
"""
import numpy as np
import qutip as qt
from functools import lru_cache
from sympy import S, Rational
from sympy.physics.wigner import clebsch_gordan, wigner_6j

# ---- constants (brief + project conventions) --------------------------------
A_HFS, gJ, gI, uB, II = 6834.682610, 2.00233, -0.0009951, 1.399624, 1.5
NU        = 0.430        # axial trap nu_z
ETA       = 0.094        # single-photon (780/D2) axial Lamb-Dicke
ETA_EFF   = 0.1838       # two-photon counter-prop Raman sideband LD
GAMMA_D2  = 6.07
GAMMA_D1  = 5.746
EM_REC    = [(-1, 1/6), (0, 2/3), (1, 1/6)]      # axial emission recoil; <u^2>=1/3 -> eta_em=eta/sqrt3
RATE_MHZ_TO_PER_MS = 6283.185                    # 2*pi*1e3 : MHz-units -> /ms

def R2(x): return Rational(int(round(2*x)), 2)
@lru_cache(None)
def CG(j1, m1, j2, m2, J, M):
    try: return float(clebsch_gordan(R2(j1), R2(j2), R2(J), R2(m1), R2(m2), R2(M)))
    except Exception: return 0.0

def E_Z(F, m, B):
    x = (gJ - gI)*uB*B/A_HFS; sgn = +1 if F == 2 else -1
    return -A_HFS/(2*(2*II+1)) + gI*uB*m*B + sgn*(A_HFS/2)*np.sqrt(1+4*m*x/(2*II+1)+x**2)

@lru_cache(None)
def m_branch(Jp2, Fp, mp):
    """Normalized m-resolved branching of excited |J',F',m'> (5P) to grounds F in
    (1,2). Jp2 = 2*J' (=3 for D2, =1 for D1)."""
    Jp = Rational(Jp2, 2); raw = {}
    for F in (1, 2):
        hf = (2*F+1)*(2*Fp+1)*float(wigner_6j(S(1)/2, Jp, 1, Fp, F, S(3)/2))**2
        for m in range(-F, F+1):
            q = mp - m
            if q in (-1, 0, 1):
                w = hf*CG(F, m, 1, q, Fp, mp)**2
                if w != 0: raw[(F, m)] = raw.get((F, m), 0.0) + w
    Z = sum(raw.values())
    return {k: v/Z for k, v in raw.items()}

# ---- pair / pump-scheme presets ---------------------------------------------
# Each preset: lo, hi, line (Jp2), grounds, clear legs, repump legs.
# A leg = (Fg, mg, q, Fp): pump ground (Fg,mg) with polarization q via excited F'.
PRESETS = {
    'stretched': dict(
        lo=(2, 2), hi=(2, 1), Jp2=3,
        grounds=[(2, 2), (2, 1), (2, 0), (1, 1), (1, 0), (1, -1)],
        clear=[(2, 1, +1, 2), (2, 0, +1, 2)],            # sigma+ on F'=2 ; |2,+2> dark (m'=3 none)
        repump=[(1, 1, +1, 2), (1, 0, +1, 2), (1, -1, +1, 2)],   # sigma+ F=1 -> F'=2
        pump_axial=+1,
    ),
    'clock': dict(
        lo=(1, -1), hi=(2, 1), Jp2=3,
        grounds=[(2, 2), (2, 1), (2, 0), (2, -1), (2, -2), (1, 1), (1, 0), (1, -1)],
        # multi-polarization clear F=2 -> F'=2 (no single-pol Zeeman dark trap);
        clear=[(F, m, q, 2) for F in (2,) for m in (-2, -1, 0, 1, 2) for q in (-1, 0, 1)
               if abs(m+q) <= 2],
        repump=[(1, 1, -1, 1), (1, 0, -1, 1)],   # sigma- F=1 -> F'=1 ; |1,-1> dark (m'=-2 none)
        pump_axial=+1,
    ),
}

def field_resonance(pair, B):
    p = PRESETS[pair]; (Fl, ml), (Fh, mh) = p['lo'], p['hi']
    f = E_Z(Fh, mh, B) - E_Z(Fl, ml, B)
    df = (E_Z(Fh, mh, B+1e-3) - E_Z(Fl, ml, B+1e-3) - f)/1e-3
    return f, df   # two-photon resonance (MHz), d/dB (MHz/G)

# ============================================================================
def _build(pair, B, Nf, OmR, R_p, R_r, delta2, eta_eff,
           incl_carrier=True, incl_pump_recoil=True, gphi=0.0):
    """Return (H, cops, chan, idx, Nf, lo, hi). delta2 default handled by caller."""
    p = PRESETS[pair]; Jp2 = p['Jp2']
    lo, hi = p['lo'], p['hi']
    G = p['grounds']
    idx = {g: i for i, g in enumerate(G)}; NA = len(G)
    bas = [qt.basis(NA, i) for i in range(NA)]
    P = lambda i, j: bas[i]*bas[j].dag()
    If = qt.qeye(Nf); a = qt.destroy(Nf)
    # coherent Raman displacement (full operator: carrier+red+blue). If carrier
    # is to be excluded, subtract its n-diagonal expectation (gate G3 uses incl).
    Dsb = qt.displace(Nf, 1j*eta_eff)
    if not incl_carrier:
        # remove the Delta n = 0 (carrier) part: project out diagonal of Dsb
        M = Dsb.full(); M = M - np.diag(np.diag(M)); Dsb = qt.Qobj(M)

    H = NU*qt.tensor(qt.qeye(NA), a.dag()*a)
    # internal diagonal: only hi carries the two-photon detuning (E_hi-E_lo=-delta2)
    H += (-delta2)*qt.tensor(P(idx[hi], idx[hi]), If)
    # Raman coupling lo<->hi
    H += -(OmR/2)*(qt.tensor(P(idx[hi], idx[lo]), Dsb)
                   + qt.tensor(P(idx[lo], idx[hi]), Dsb.dag()))

    cops = []; chan = {}
    def add(tag, rate, gout, gin, Dmot):
        if rate <= 0 or gout not in idx or gin not in idx: return
        cops.append(np.sqrt(rate)*qt.tensor(P(idx[gout], idx[gin]), Dmot))
        chan.setdefault(tag, []).append(cops[-1])

    Dabs = qt.displace(Nf, 1j*ETA*p['pump_axial']) if incl_pump_recoil else If
    Dem = {u: (qt.displace(Nf, 1j*ETA*u) if incl_pump_recoil else If) for u, _ in EM_REC}

    def legs(leglist, rate0, tag):
        for (Fg, mg, q, Fp) in leglist:
            mp = mg + q
            if abs(mp) > Fp: continue
            wabs = CG(Fg, mg, 1, q, Fp, mp)**2
            if wabs <= 0: continue
            for (Ft, mt), br in m_branch(Jp2, Fp, mp).items():
                if (Ft, mt) not in idx: continue
                for (u, wem) in EM_REC:
                    add(tag, rate0*wabs*br*wem, (Ft, mt), (Fg, mg), Dem[u]*Dabs)

    legs(p['clear'], R_p, 'clear')
    legs(p['repump'], R_r, 'repump')

    # optional Raman-pair dephasing Lindblad sqrt(gphi)*(P_hi - P_lo)  (T4 hook)
    if gphi > 0:
        deph = qt.tensor(P(idx[hi], idx[hi]) - P(idx[lo], idx[lo]), If)
        cops.append(np.sqrt(gphi)*deph); chan.setdefault('deph', []).append(cops[-1])
    return H, cops, chan, idx, Nf, lo, hi

# ---- main entry -------------------------------------------------------------
def solve(pair='stretched', B=1.5, Nf=15, OmR=0.02, R_p=0.05, R_r=2.0,
          delta2=None, eta_eff=ETA_EFF, regime='CW',
          incl_carrier=True, incl_pump_recoil=True, gphi=0.0,
          want_detail=False, cw_method=None):
    if delta2 is None: delta2 = -NU            # red (cooling) sideband
    H, cops, chan, idx, Nf, lo, hi = _build(
        pair, B, Nf, OmR, R_p, R_r, delta2, eta_eff,
        incl_carrier, incl_pump_recoil, gphi)
    NA = H.dims[0][0]
    N = qt.tensor(qt.qeye(NA), qt.destroy(Nf).dag()*qt.destroy(Nf))

    if regime == 'CW':
        if cw_method is None:
            cw_method = 'mesolve' if NA*Nf > 90 else 'direct'
        if cw_method == 'mesolve':
            rho = _cw_evolve(H, cops, idx, lo, Nf, pair, R_p, OmR, eta_eff, delta2)
        else:
            L = qt.liouvillian(H, cops)
            try:    rho = qt.steadystate(L, method='direct')
            except Exception: rho = qt.steadystate(L, method='svd')
    elif regime == 'pulsed':
        rho = _pulsed_fixed_point(H, cops, idx, lo, hi, Nf, OmR, eta_eff, delta2)
    else:
        raise ValueError(regime)

    nbar = float(np.real(qt.expect(N, rho)))
    if not want_detail:
        return nbar, None
    bas = [qt.basis(NA, i) for i in range(NA)]
    P = lambda i, j: bas[i]*bas[j].dag(); If = qt.qeye(Nf)
    pops = {g: float(np.real(qt.expect(qt.tensor(P(i, i), If), rho))) for g, i in idx.items()}
    Rs = {t: float(sum(np.real(qt.expect(c.dag()*c, rho)) for c in cs)) for t, cs in chan.items()}
    out = dict(nbar=nbar, pops=pops, Rscatter=Rs, R_total=sum(Rs.values()),
               Plo=pops[lo], Phi=pops[hi], lo=lo, hi=hi, idx=idx, Nf=Nf,
               H=H, cops=cops, N=N, rho=rho, delta2=delta2)
    return nbar, out

def _cw_evolve(H, cops, idx, lo, Nf, pair, R_p, OmR, eta_eff, delta2):
    """Memory-light CW steady state: propagate (H,cops) to long time and confirm
    <N> has converged. Avoids the dense Liouvillian LU (4 GB cap)."""
    NA = H.dims[0][0]; N = qt.tensor(qt.qeye(NA), qt.destroy(Nf).dag()*qt.destroy(Nf))
    Ge = gamma_eff_of(pair, R_p)
    W = max(W_analytic(OmR, Ge, delta2, eta_eff)['W'], 1e-3)
    rho0 = qt.tensor(qt.basis(NA, idx[lo])*qt.basis(NA, idx[lo]).dag(), qt.thermal_dm(Nf, 1.0))
    opts = {'nsteps': 20000, 'atol': 1e-9, 'rtol': 1e-7}
    tprev, rho = None, rho0
    for span in (8.0, 8.0, 16.0):                 # extend until converged
        ts = np.linspace(0, span/W, 40)
        res = qt.mesolve(H, rho, ts, cops, options=opts)
        rho = res.states[-1]
        n_now = float(np.real(qt.expect(N, rho)))
        if tprev is not None and abs(n_now - tprev) < 1e-4:
            break
        tprev = n_now
    return rho

def _pulsed_fixed_point(H, cops, idx, lo, hi, Nf, OmR, eta_eff, delta2,
                        dt=None, max_steps=4000, tol=1e-7):
    """Regime B: STROBOSCOPIC (interleaved) propagation of the SAME generator as
    regime A, found as the fixed point of the Lie-Trotter split map
        rho  ->  exp(L_diss dt) [ U rho U^dag ],   U = exp(-i H dt),
    where L_diss = pure pump dissipator and H carries trap+detuning+Raman. As the
    stroboscopic period dt -> 0 (fine-slice = fast-pump limit) the split map's
    fixed point equals the CW steady state -- this is exactly the agreement G5
    tests, via an independent numerical route (iterated split map vs. sparse-LU
    steadystate). Memory-light (4 GB cap): U is a SMALL Hilbert-space unitary and
    the dissipative half-step uses scipy expm_multiply on the vectorized state, so
    no dense Liouvillian propagator is ever formed.

    dt is auto-set small vs the drive and the recoil-weighted trap-dissipator
    non-commutation scale (NOT vs the bare trap nu*Nf, which lives inside the exact
    unitary U and contributes no leading Trotter error)."""
    from scipy.sparse.linalg import expm_multiply
    NA = H.dims[0][0]
    N = qt.tensor(qt.qeye(NA), qt.destroy(Nf).dag()*qt.destroy(Nf))
    bas = [qt.basis(NA, i) for i in range(NA)]
    Gtot = sum(float(np.real((c.dag()*c).tr()))/(NA*Nf) for c in cops)
    if dt is None:
        # leading Trotter error ~ dt*||[H, L_diss]|| ; drive sets OmR, recoil-weighted
        # trap sets ETA*NU, pump sets Gtot. Keep dt small vs all of these.
        scale = max(OmR, Gtot, ETA*NU, 1e-3)
        dt = 0.3/scale
    U = (-1j*H*dt).expm()
    Ld = qt.liouvillian(0*H, cops)
    Lsp = (Ld.data_as('csr_matrix') if hasattr(Ld, 'data_as') else
           __import__('scipy.sparse', fromlist=['csr_matrix']).csr_matrix(Ld.full()))*dt
    rho = qt.tensor(bas[idx[lo]]*bas[idx[lo]].dag(), qt.thermal_dm(Nf, 0.5))
    vtmpl = qt.operator_to_vector(rho)
    last = 1e9
    for k in range(max_steps):
        rho = U*rho*U.dag()                                  # coherent slice (Hilbert)
        v = expm_multiply(Lsp, qt.operator_to_vector(rho).full().flatten())  # dissipative slice
        rho = qt.vector_to_operator(qt.Qobj(v.reshape(-1, 1), dims=vtmpl.dims))
        rho = (rho + rho.dag())/2.0; rho = rho/rho.tr()
        if k % 25 == 0:
            n = float(np.real(qt.expect(N, rho)))
            if abs(n - last) < tol:
                break
            last = n
    return rho

# ============================================================================
# COOLING RATE W -- three independent methods
# ============================================================================
def W_analytic(OmR, R_p_eff, delta2=None, eta_eff=ETA_EFF):
    """W1: resolved-sideband golden rule. Gamma_eff = effective optical-pumping
    linewidth of |g_hi> (= total pump rate out of hi). Returns A_-, A_+, W, n_min."""
    if delta2 is None: delta2 = -NU
    Ge = R_p_eff
    def A(sign):  # sign=+1 -> (delta2+nu) [cooling res at delta2=-nu]; -1 -> heating
        return eta_eff**2*OmR**2*Ge/4 / ((delta2 + sign*NU)**2 + (Ge/2)**2)
    Am, Ap = A(+1), A(-1)
    W = Am - Ap
    n_min = Ap/(Am - Ap) if (Am - Ap) > 0 else np.inf
    return dict(Aminus=Am, Aplus=Ap, W=W, n_min=n_min, Gamma_eff=Ge)

def gamma_eff_of(pair, R_p):
    """Total optical-pumping rate out of |g_hi> for this pair/scheme (sets W1)."""
    p = PRESETS[pair]; hi = p['hi']
    tot = 0.0
    for (Fg, mg, q, Fp) in p['clear']:
        if (Fg, mg) == hi:
            mp = mg + q
            if abs(mp) <= Fp:
                tot += R_p*CG(Fg, mg, 1, q, Fp, mp)**2
    return tot

def W_timedomain(pair, B, Nf, OmR, R_p, R_r, n0=3.0, tmax=None, npts=200, **kw):
    """W2: time-domain relaxation of <N>(t) from a thermal state, fit
    <N>(t)=n_ss+(n0-n_ss)exp(-W t). The trajectory is computed with scipy
    expm_multiply in interval mode (stiff-robust: the pump/cooling timescale ratio
    is ~1e3 and defeats an explicit mesolve integrator's step size)."""
    from scipy.sparse.linalg import expm_multiply
    H, cops, chan, idx, Nf, lo, hi = _build(pair, B, Nf, OmR, R_p, R_r,
                                            kw.get('delta2', -NU), kw.get('eta_eff', ETA_EFF),
                                            kw.get('incl_carrier', True),
                                            kw.get('incl_pump_recoil', True), 0.0)
    NA = H.dims[0][0]; N = qt.tensor(qt.qeye(NA), qt.destroy(Nf).dag()*qt.destroy(Nf))
    rho0 = qt.tensor(qt.basis(NA, idx[lo])*qt.basis(NA, idx[lo]).dag(), qt.thermal_dm(Nf, n0))
    Ge = gamma_eff_of(pair, R_p)
    Wg = W_analytic(OmR, Ge, kw.get('delta2', -NU), kw.get('eta_eff', ETA_EFF))['W']
    if tmax is None: tmax = 5.0/max(Wg, 1e-5)
    Lsp = qt.liouvillian(H, cops).data_as('csr_matrix')
    vec0 = qt.operator_to_vector(rho0).full().flatten()
    Nvec = qt.operator_to_vector(N).full().flatten()
    traj = expm_multiply(Lsp, vec0, start=0.0, stop=tmax, num=npts, endpoint=True)
    y = np.real(traj @ Nvec.conj())                # <N>(t_j) = <<N|rho_j>>
    ts = np.linspace(0.0, tmax, npts)
    n_ss = y[-1]
    z = y - n_ss; mask = z > 1e-4*max(abs(z[0]), 1e-9)
    if mask.sum() > 5:
        W2 = -np.polyfit(ts[mask], np.log(z[mask]), 1)[0]
    else:
        W2 = np.nan
    return dict(W=W2, n_ss=n_ss, ts=ts, y=y)

def W_spectral(pair, B, Nf, OmR, R_p, R_r, **kw):
    """W3: the cooling eigenmode of the Liouvillian -- the (near-real) mode whose
    right-eigenvector, as an operator, has the largest overlap with N=a^dag a. This
    is NOT the raw spectral gap: a slow internal-state coherence can sit below the
    cooling mode and the bare gap then mis-reports the rate by ~100x (the artifact
    that broke the dark-resonance solvers). Cooling is overdamped, so the mode is
    near-real; absolute N-overlaps are diluted by the eigenvector's coherence
    content, so selection uses the *largest* overlap among near-real modes (a
    relative criterion), not an absolute threshold."""
    H, cops, chan, idx, Nf, lo, hi = _build(pair, B, Nf, OmR, R_p, R_r,
                                            kw.get('delta2', -NU), kw.get('eta_eff', ETA_EFF),
                                            kw.get('incl_carrier', True),
                                            kw.get('incl_pump_recoil', True), 0.0)
    NA = H.dims[0][0]; N = qt.tensor(qt.qeye(NA), qt.destroy(Nf).dag()*qt.destroy(Nf))
    from scipy.sparse.linalg import eigs
    L = qt.liouvillian(H, cops)
    Lsp = L.data_as('csr_matrix') if hasattr(L, 'data_as') else L.full()
    Nvec = qt.operator_to_vector(N).full().flatten(); Nvec /= np.linalg.norm(Nvec)
    try:
        evals, evecs = eigs(Lsp, k=min(40, Lsp.shape[0]-2), sigma=0.0, which='LM')
    except Exception:
        M = L.full(); evals, evecs = np.linalg.eig(M)
    cand = []
    for k in range(len(evals)):
        lam = evals[k]; rate = -lam.real
        if rate < 1e-9:                      # skip steady state / null space
            continue
        v = evecs[:, k]; v = v/np.linalg.norm(v)
        ov = abs(np.vdot(Nvec, v))
        near_real = abs(lam.imag) <= max(rate, 1e-6)   # cooling mode is overdamped
        cand.append((rate, ov, lam, near_real))
    real_modes = [c for c in cand if c[3]] or cand
    pick = max(real_modes, key=lambda c: c[1])         # largest N-overlap = cooling mode
    return dict(W=pick[0], overlap=pick[1], lam=pick[2])


if __name__ == '__main__':
    np.set_printoptions(precision=4, suppress=True)
    print("smoke test:", solve('stretched', Nf=12)[0])
