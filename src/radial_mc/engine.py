"""
engine.py -- thin reuse of eit_common's 3-level Lambda EIT physics, extended to
accept an explicit Otot (so guided beams Omega(r)=Omega0*sqrt(s) can be set).

Physics byte-identical to eit_common.eit_floor (same H, same emission recoil, same
dephasing); only the Otot computation is exposed and the Liouvillian is returned.

The authoritative export of this file is `_build_L` (used by grid_build.py and mc.py).

WARNING -- W extractor in solve():
  solve(...,want_W=True) returns a cooling rate from the n-content-selected slowest
  Liouvillian eigenvalue (shift-invert sigma=0). This was found UNRELIABLE here:
  ARPACK shift-invert returns spurious POSITIVE-real-part modes and the n-content
  pick is ambiguous near the dense small-|lambda| cluster (see audit notes). It is
  retained only to mirror radial_frozen.W_clock's method and to reproduce the
  eit_floor n_ss gate. ALL W(r) used in the MC come instead from grid_build.nss_and_W,
  which fits the slope of ln(<n>-n_ss) of a short expm_multiply relaxation from
  thermal(n_ss+dn) -- the near-equilibrium (small-deviation) rate. Do not use solve()'s
  W for production; use grid_build.
"""
import numpy as np, qutip as qt
from eit_common import GAMMA, NU_Z, ETA, B1_DEF, B2_DEF, _EM_REC

def _build_L(Delta, nu, eta, Otot, OmR, gphi, delta2, b1, b2, Nf):
    g1,g2,e = qt.basis(3,0),qt.basis(3,1),qt.basis(3,2)
    P=lambda a,b:a*b.dag(); If=qt.qeye(Nf); a=qt.destroy(Nf)
    Nop=qt.tensor(qt.qeye(3),a.dag()*a)
    Oc=Otot/np.sqrt(1.0+OmR**2); Op=OmR*Oc
    Dc=qt.displace(Nf,+1j*eta); Dp=qt.displace(Nf,-1j*eta)
    H=(-Delta)*qt.tensor(P(e,e),If)+nu*Nop+delta2*qt.tensor(P(g2,g2),If)
    H=H-(Oc/2.)*(qt.tensor(P(e,g2),Dc)+qt.tensor(P(g2,e),Dc.dag()))
    H=H-(Op/2.)*(qt.tensor(P(e,g1),Dp)+qt.tensor(P(g1,e),Dp.dag()))
    s=b1+b2; b1n,b2n=b1/s,b2/s; cops=[]
    for u,wg in _EM_REC:
        Ds=qt.displace(Nf,1j*eta*u)
        cops.append(np.sqrt(GAMMA*b1n*wg)*qt.tensor(P(g1,e),Ds))
        cops.append(np.sqrt(GAMMA*b2n*wg)*qt.tensor(P(g2,e),Ds))
    if gphi>0: cops.append(np.sqrt(gphi)*qt.tensor(P(g1,g1)-P(g2,g2),If))
    return qt.liouvillian(H,cops), Nop

def solve(Delta, nu=NU_Z, eta=ETA, Otot=None, OmR=0.25, gphi=0.0, delta2=0.0,
          b1=B1_DEF, b2=B2_DEF, Nf=24, want_W=True):
    if Otot is None: Otot=np.sqrt(4.0*Delta*nu)     # default = on-resonant cooling condition
    L,Nop=_build_L(Delta,nu,eta,Otot,OmR,gphi,delta2,b1,b2,Nf)
    try: rho=qt.steadystate(L,method='power')
    except Exception: rho=qt.steadystate(L,method='direct')
    nss=float(qt.expect(Nop,rho))
    if not want_W: return nss, None, None
    pe=float(qt.expect(qt.tensor(qt.basis(3,2)*qt.basis(3,2).dag(),qt.qeye(Nf)),rho))
    # cooling-mode gap: slowest nonzero Liouvillian eigenvalue with largest n-content
    import scipy.sparse.linalg as sla
    Lsc=L.data.as_scipy().tocsc(); dim=int(np.sqrt(Lsc.shape[0])); Nm=Nop.full()
    try:
        vals,vecs=sla.eigs(Lsc,k=8,sigma=0.0,which='LM')
    except Exception:
        return nss, None, pe
    best,bestnc=None,-1.0
    for k in range(len(vals)):
        if abs(vals[k].real)<1e-9: continue
        rmat=vecs[:,k].reshape(dim,dim); rs=(rmat+rmat.conj().T)/2
        trn=np.sum(np.abs(np.linalg.eigvals(rs)))
        nc=abs(np.trace(Nm@rmat))/(trn if trn>1e-12 else 1)
        if nc>bestnc: bestnc,best=nc,abs(vals[k].real)
    W=2*np.pi*best*1e3 if best is not None else None     # /ms
    return nss, W, pe

if __name__=='__main__':
    import time; t0=time.time()
    # GATE: reproduce eit_common defaults (Otot from cooling condition)
    from eit_common import eit_floor
    for D in (40.,45.,80.):
        n0=eit_floor(D,Nf=16); n1,W,pe=solve(D,Nf=16)
        print("Delta=%4.0f  eit_floor=%.4f  engine.solve=%.4f  W=%.1f/ms (%.2f kHz)  Pe=%.1e"
              %(D,n0,n1,W,W*1e3/(2*np.pi),pe))   # W reported /ms -> kHz: /ms = 1e3/s; kHz=1e3/s -> kHz=W
    print("elapsed %.1fs"%(time.time()-t0))
