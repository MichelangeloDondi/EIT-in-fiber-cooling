"""Per-radius P_e(r) on the clk2 (full clock) engine -> TESTS the squeezer rate-rise channel.
   R_sq(r) ~ P_e(F'2)(r) [leak driver] * kernel(nu_z(r)) [FALLS off-axis].
   RESULT (2026-06-20): P_e FALLS off-axis (1.53->0.88e-5 over r=0-10um) -- the M3 shift is COMMON
   to both legs (delta2 unchanged, dark state preserved) and the weaker off-axis field dominates.
   The hypothesized off-axis rate-rise is DISPROVEN; R_sq falls to 0.32x at r=10 (kernel-falloff
   unopposed). Only the 1/W tail amplification remains, dwell-discounted."""
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "engines"))
import numpy as np, qutip as qt
from clk2 import (Eg, excited_energies, beams, build_frame, CGc, GAMMA, EM_REC, BR)
NU0, ETA0, C_M3, W0 = 0.430, 0.094, 60.9, 19.0
RHO_RATIO = 2.435                     # |alpha_e/alpha_g| inverted ratio (m'=0, r=-2.435)

def kernel(s):                        # per-excursion squeezer heat; omega_e = nu_z(r)*sqrt(rho)
    nu = NU0*np.sqrt(s); we = nu*np.sqrt(RHO_RATIO)
    pref = (np.sqrt(RHO_RATIO)+1/np.sqrt(RHO_RATIO))**2
    return pref*we**2/(2*(GAMMA**2-4*we**2))

def solve_radial(s, Dc0=80.0, OmR=0.25, Drep1=20.0, Drep2=5.0, Om_r=1.5, B=3.2287, Nf=8):
    nu=NU0*np.sqrt(s); eta=ETA0*s**(-0.25)
    Oc0=np.sqrt(4*Dc0*NU0)/np.sqrt(1+OmR**2); Oc=Oc0*np.sqrt(s); Op=OmR*Oc
    Dc=Dc0+C_M3*(1.0-s)
    gE={(F,mm):Eg(F,mm,B) for F in (1,2) for mm in (range(-1,2) if F==1 else range(-2,3))}
    eE=excited_energies(B); bm=beams('A',Dc,Drep1,Drep2,0.0,Oc,Op,Om_r)
    Gs=[(1,-1),(1,0),(1,1),(2,-2),(2,-1),(2,0),(2,1),(2,2)]; Es=list(Gs)
    nodes=[('g',g) for g in Gs]+[('e',e) for e in Es]; idx={n:i for i,n in enumerate(nodes)}; NA=len(nodes)
    ng,ne=set(Gs),set(Es)
    for b in bm: b['edges']=[(g,e,c) for (g,e,c) in b['edges'] if g in ng and e in ne]
    bm=[b for b in bm if b['edges'] and b['named'][0] in ng and b['named'][1] in ne]
    h,conf=build_frame(bm,gE,eE)
    for n in nodes:
        if n not in h: h[n]=0.0
    bas=[qt.basis(NA,i) for i in range(NA)]; P=lambda i,j: bas[i]*bas[j].dag()
    If=qt.qeye(Nf); aop=qt.destroy(Nf); Dsp=lambda x: qt.displace(Nf,1j*eta*x)
    H=nu*qt.tensor(qt.qeye(NA),aop.dag()*aop)
    for n in nodes: H+=h[n]*qt.tensor(P(idx[n],idx[n]),If)
    for b in bm:
        (gn,en)=b['named']; cn=[c for (g,e,c) in b['edges'] if g==gn and e==en][0]
        for (g,e,c) in b['edges']:
            O=b['Rabi']*(c/cn); i,j=idx[('g',g)],idx[('e',e)]
            H+=-(O/2)*(qt.tensor(P(j,i),Dsp(b['kdir']))+qt.tensor(P(i,j),Dsp(b['kdir']).dag()))
    legs=[(1,-1),(2,1)]; Gset=set(Gs); cops=[]
    for (Fp,mp) in Es:
        ch={}
        for Fg in (1,2):
            for mg in (mp-1,mp,mp+1):
                if abs(mg)>Fg: continue
                c=CGc(Fg,mg,mp-mg,Fp,mp)
                if abs(c)<1e-12: continue
                w=BR[Fp][Fg]*c**2
                if (Fg,mg) in Gset: ch[(Fg,mg)]=ch.get((Fg,mg),0)+w
                else:
                    lw=np.array([CGc(lf,lm,mp-lm,Fp,mp)**2 for (lf,lm) in legs])
                    lw=lw/lw.sum() if lw.sum()>0 else np.ones(len(legs))/len(legs)
                    for (lf,lm),ww in zip(legs,lw): ch[(lf,lm)]=ch.get((lf,lm),0)+w*ww
        tot=sum(ch.values())
        for (g,w) in ch.items():
            for (u,wem) in EM_REC:
                cops.append(np.sqrt(GAMMA*(w/tot)*wem)*qt.tensor(P(idx[('g',g)],idx[('e',(Fp,mp))]),Dsp(u)))
    L=qt.liouvillian(H,cops)
    try: rho=qt.steadystate(L,method='direct')
    except Exception: rho=qt.steadystate(L,method='eigen')
    N=qt.tensor(qt.qeye(NA),aop.dag()*aop)
    peF1=sum(qt.expect(qt.tensor(P(idx[('e',e)],idx[('e',e)]),If),rho) for e in Es if e[0]==1)
    peF2=sum(qt.expect(qt.tensor(P(idx[('e',e)],idx[('e',e)]),If),rho) for e in Es if e[0]==2)
    return float(qt.expect(N,rho)), float(peF1), float(peF2)

if __name__ == "__main__":
    print("r(um)  s       nbar     P_e(F'2)    P_e(F'1)   kernel    R_sq=peF2*kern   R_sq/R_sq(0)")
    rs=[0.0,1.0,2.0,2.9,4.0,5.0,5.74,7.0,8.7,10.0]   # sigma_r(100)=2.9, sigma_r(400)=5.74, 3sig(100)=8.7
    rows=[]
    for r in rs:
        s=np.exp(-2*r**2/W0**2) if r>0 else 1.0
        nb,p1,p2=solve_radial(s); k=kernel(s); Rsq=p2*k
        rows.append((r,s,nb,p2,p1,k,Rsq))
    R0=rows[0][6]
    for (r,s,nb,p2,p1,k,Rsq) in rows:
        print(" %4.1f  %.4f  %.5f  %.3e  %.3e  %.5f   %.3e      %.3f"%(r,s,nb,p2,p1,k,Rsq,Rsq/R0))
