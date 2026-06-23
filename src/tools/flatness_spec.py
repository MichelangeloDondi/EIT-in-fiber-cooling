"""Flat-top flatness spec: per-radial-depth floor on the validated config-A engine.
Maps fractional intensity variation DU/U over the cloud to floor degradation, to
back out the flatness tolerance XLIM needs. Uses clk2's validated building blocks."""
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "engines"))
import numpy as np, qutip as qt
import clk2 as m   # validated engine (config A = 0.00485, clean-Lambda 0.0072)
from clk2 import Eg, excited_energies, beams, build_frame, CGc, GAMMA, EM_REC, BR

NU0, ETA0 = 0.430, 0.094          # on-axis nu_z (MHz), eta  (clk2 globals)
C_M3 = 60.9                        # M3 radial detuning sensitivity (MHz per unit (1-s))
W0 = 19.0                          # beam waist (um)

def solve_radial(s, Dc0=80.0, OmR=0.25, Drep1=20.0, Drep2=5.0, Om_r=1.5,
                 B=3.2287, Nf=8):
    """Steady-state axial floor at fractional lattice depth s = U(r)/U0.
       Scales nu_z ~ sqrt(s), eta ~ s^-1/4, Oc(field) ~ sqrt(s), Dc -> Dc + C_M3*(1-s).
       Repumps held (sub-dominant). At s=1 reduces to validated config A (Dc0=80)."""
    nu  = NU0*np.sqrt(s)
    eta = ETA0*s**(-0.25)
    Oc0 = np.sqrt(4*Dc0*NU0)/np.sqrt(1+OmR**2)
    Oc  = Oc0*np.sqrt(s)
    Op  = OmR*Oc
    Dc  = Dc0 + C_M3*(1.0-s)
    gE = {(F,mm): Eg(F,mm,B) for F in (1,2) for mm in (range(-1,2) if F==1 else range(-2,3))}
    eE = excited_energies(B)
    bm = beams('A', Dc, Drep1, Drep2, 0.0, Oc, Op, Om_r)   # config A, no swap/clearer
    Gs = [(1,-1),(1,0),(1,1),(2,-2),(2,-1),(2,0),(2,1),(2,2)]
    Es = [(1,-1),(1,0),(1,1),(2,-2),(2,-1),(2,0),(2,1),(2,2)]
    nodes = [('g',g) for g in Gs] + [('e',e) for e in Es]
    idx = {n:i for i,n in enumerate(nodes)}; NA=len(nodes)
    ng, ne = set(Gs), set(Es)
    for b in bm:
        b['edges'] = [(g,e,c) for (g,e,c) in b['edges'] if g in ng and e in ne]
    bm = [b for b in bm if b['edges'] and b['named'][0] in ng and b['named'][1] in ne]
    h, conf = build_frame(bm, gE, eE)
    for n in nodes:
        if n not in h: h[n]=0.0
    bas=[qt.basis(NA,i) for i in range(NA)]; P=lambda i,j: bas[i]*bas[j].dag()
    If=qt.qeye(Nf); aop=qt.destroy(Nf); Dsp=lambda x: qt.displace(Nf,1j*eta*x)
    H = nu*qt.tensor(qt.qeye(NA), aop.dag()*aop)
    for n in nodes: H += h[n]*qt.tensor(P(idx[n],idx[n]), If)
    for b in bm:
        (gn,en)=b['named']; cn=[c for (g,e,c) in b['edges'] if g==gn and e==en][0]
        for (g,e,c) in b['edges']:
            O=b['Rabi']*(c/cn); i,j=idx[('g',g)],idx[('e',e)]
            H += -(O/2)*(qt.tensor(P(j,i),Dsp(b['kdir']))+qt.tensor(P(i,j),Dsp(b['kdir']).dag()))
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
    return float(qt.expect(N,rho))

# --- gate: s=1 must reproduce validated config A ---
n1 = solve_radial(1.0)
print("GATE: s=1 floor = %.5f  [validated config A = 0.00485]" % n1)
print()
print("per-depth floor scan (Dc0=80):")
print(" s      DU/U     r(um)    n_z       dn vs axis")
sgrid = [1.0,0.99,0.98,0.97,0.95,0.93,0.90,0.85,0.80]
rows=[]
for s in sgrid:
    n = solve_radial(s)
    DUoU = 1.0-s
    r = W0*np.sqrt(-np.log(s)/2.0) if s<1 else 0.0
    rows.append((s,DUoU,r,n,n-n1))
    print("  %.2f   %5.1f%%   %5.2f    %.5f   %+.5f" % (s, 100*DUoU, r, n, n-n1))
print()
# --- back out the flatness spec for floor-degradation budgets ---
print("FLATNESS SPEC (largest DU/U keeping worst in-cloud floor within budget of on-axis):")
for budget,lbl in [(0.0005,"+0.0005"),(0.001,"+0.001"),(0.002,"+0.002")]:
    ok = [r for r in rows if r[3] <= n1+budget]
    DUmax = max(r[1] for r in ok)
    print("  budget %s : DU/U <= %.1f%%   (detuning spread <= %.1f MHz, cloud radius <= %.1f um)"
          % (lbl, 100*DUmax, C_M3*DUmax, max(r[2] for r in ok)))
