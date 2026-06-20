"""
grid_build.py -- per-radius n_ss(r) and small-deviation cooling rate W(r) on the
3-level Lambda engine, at the S3 operating point:
   Delta0=45, OmR=0.10, GUIDED beams Omega(r)=Omega0*sqrt(s), M3 detuning shift
   Delta_eff(r)=Delta0 + c*(1-s) with c=60.9, delta2=0 (fixed, on-axis / HEADLINE).
Radial laws (S1/S3):
   s(r)=exp(-2 r^2/w0^2), w0=19 um
   nu_z(r)=nu0*sqrt(s)        (nu0=0.430)
   eta(r)=eta0*s^(-1/4)       (eta0=0.094)
   Omega(r)=Omega0*sqrt(s)    (guided): Otot(r)=Otot0*sqrt(s), Otot0=sqrt(4*45*nu0)
W(r): evolve thermal(n_ss+dn0) under L (expm_multiply), fit slope of ln(<n>-n_ss)
      over a post-internal-transient window -> near-equilibrium (small-deviation) rate /t_H.
Usage:  python3 grid_build.py  r1 r2 r3 ...    (appends to grid_cache.npz)
"""
import sys, warnings, time
warnings.filterwarnings('ignore')
import numpy as np, qutip as qt
import scipy.sparse.linalg as sla
from engine import _build_L
from eit_common import NU_Z, ETA, B1_DEF, B2_DEF

w0   = 19.0
nu0  = NU_Z          # 0.430
eta0 = ETA           # 0.094
D0   = 45.0
cM3  = 60.9
OmR  = 0.10
Otot0 = np.sqrt(4*D0*nu0)
CACHE = 'grid_cache.npz'

def s_of_r(r):    return np.exp(-2*r**2/w0**2)
def params(r):
    s = s_of_r(r)
    D   = D0 + cM3*(1-s)
    nu  = nu0*np.sqrt(s)
    eta = eta0*s**(-0.25)
    Ot  = Otot0*np.sqrt(s)
    return D, nu, eta, Ot, s

def nss_and_W(r, Nf=16, dn0=0.15, twin=(40.,160.), npts=10):
    D,nu,eta,Ot,s = params(r)
    L,Nop = _build_L(D,nu,eta,Ot,OmR,0.0,0.0,B1_DEF,B2_DEF,Nf)
    rho = qt.steadystate(L,method='power'); nss=float(qt.expect(Nop,rho))
    Lsc = L.data.as_scipy().tocsc()
    Nbra = qt.operator_to_vector(Nop).dag().full().flatten()
    rho_hot = qt.tensor(rho.ptrace(0), qt.thermal_dm(Nf, nss+dn0))
    v0 = qt.operator_to_vector(rho_hot).full().flatten()
    tt = np.linspace(0.0, twin[1], npts)
    traj = sla.expm_multiply(Lsc, v0, start=tt[0], stop=tt[-1], num=len(tt), endpoint=True)
    n_t = np.real(traj@Nbra); y = n_t-nss
    m = (tt>=twin[0]) & (y>1e-5)
    lam = -np.polyfit(tt[m], np.log(y[m]), 1)[0] if m.sum()>=3 else np.nan
    # also a Pe (excited pop) for diagnostics
    pe = float(qt.expect(qt.tensor(qt.basis(3,2)*qt.basis(3,2).dag(),qt.qeye(Nf)),rho))
    return nss, lam, s, pe

def load():
    try:
        d = np.load(CACHE)
        return dict(r=list(d['r']), nss=list(d['nss']), lam=list(d['lam']),
                    s=list(d['s']), pe=list(d['pe']), Nf=list(d['Nf']))
    except Exception:
        return dict(r=[], nss=[], lam=[], s=[], pe=[], Nf=[])

def save(db):
    np.savez(CACHE, **{k:np.array(v) for k,v in db.items()})

if __name__=='__main__':
    Nf = 16
    radii = [float(x) for x in sys.argv[1:]]
    db = load()
    for r in radii:
        t0=time.time()
        nss,lam,s,pe = nss_and_W(r, Nf=Nf)
        db['r'].append(r); db['nss'].append(nss); db['lam'].append(lam)
        db['s'].append(s); db['pe'].append(pe); db['Nf'].append(Nf)
        save(db)
        print('r=%5.2f s=%.4f nss=%.5f W=%.4e/t_H pe=%.2e (%.1fs)'%(r,s,nss,lam,pe,time.time()-t0),flush=True)
    print('saved %d radii to %s'%(len(db['r']),CACHE),flush=True)
