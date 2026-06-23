"""Red-team: is the m=0 clock transition |1,0>-|2,0> rank-2-obstructed, or an allowed
   vector Raman? Compute g_F' for the Dk=2k path and compare to the Dm=2 case."""
import sympy as sp
from sympy.physics.wigner import clebsch_gordan
J=sp.Rational(1,2); Jp=sp.Rational(3,2); I=sp.Rational(3,2)
Gamma=6.0666
dHFS={0:-302.07,1:-229.85,2:-72.91,3:193.74}   # 5P3/2 (87Rb), MHz vs centroid

def me(Fe,meF,Fg,mgF,q):
    tot=sp.Integer(0)
    for mI2 in (-3,-1,1,3):
        mI=sp.Rational(mI2,2)
        for mJ2 in (-1,1):
            mJ=sp.Rational(mJ2,2); mJp=mJ+q
            if abs(mJp)>sp.Rational(3,2): continue
            tot+=(clebsch_gordan(Jp,I,sp.Integer(Fe),mJp,mI,sp.Integer(meF))
                  *clebsch_gordan(J,I,sp.Integer(Fg),mJ,mI,sp.Integer(mgF))
                  *clebsch_gordan(J,1,Jp,mJ,sp.Integer(q),mJp))
    return sp.nsimplify(tot)

def analyze(name, gfun, c1fun, c2fun, Fps=(0,1,2,3)):
    g={Fp:sp.simplify(gfun(Fp)) for Fp in Fps}
    gn={k:float(v) for k,v in g.items()}
    c1={Fp:float(c1fun(Fp)) for Fp in Fps}; c2={Fp:float(c2fun(Fp)) for Fp in Fps}
    null=float(sp.simplify(sum(g.values())))
    G2=sum(gn[Fp]*dHFS[Fp] for Fp in Fps)
    def G(D): return sum(gn[Fp]/(D+dHFS[Fp]) for Fp in Fps)
    def Sig(D): return sum(c1[Fp]**2/(D+dHFS[Fp])**2+c2[Fp]**2/(D+dHFS[Fp])**2 for Fp in Fps)
    def FoM(D): return 2*abs(G(D))/(Gamma*Sig(D))
    print("="*64); print(" %s"%name); print("="*64)
    print("  g_F' :", {Fp:round(gn[Fp],4) for Fp in Fps})
    print("  sum_F' g = %.4e   (0 => rank-2 null/obstructed)"%null)
    print("  Delta*G  at 1,10,30 GHz: %.3f %.3f %.3f  (const => 1/Delta, ALLOWED)"
          %(1e3*G(1e3),1e4*G(1e4),3e4*G(3e4)))
    print("  Delta^2*G at 1,10,30GHz: %.1f %.1f %.1f  (const => 1/Delta^2, obstructed)"
          %(1e6*G(1e3),1e8*G(1e4),9e8*G(3e4)))
    print("  FoM at Delta=1,3,10,30 GHz: %.2f %.2f %.2f %.2f"
          %(FoM(1e3),FoM(3e3),FoM(1e4),FoM(3e4)))

# --- Dm=2 matched pair (the paper's case): |1,-1>-(s+)->|F',0>-(s+)->|2,+1>
analyze("Dm=2 matched-pair Raman  |1,-1> -> |2,+1>  (paper's claim)",
    gfun=lambda Fp: -me(Fp,0,2,1,-1)*me(Fp,0,1,-1,1),
    c1fun=lambda Fp: me(Fp,0,1,-1,1), c2fun=lambda Fp: me(Fp,0,2,1,-1))

# --- m=0 clock transition: |1,0>-(s+)->|F',+1>-(s+ emit)->|2,0>, Dk=2k
analyze("m=0 clock Raman  |1,0> -> |2,0>  (Dm=0, vector channel, Dk=2k)",
    gfun=lambda Fp: -me(Fp,1,2,0,1)*me(Fp,1,1,0,1),
    c1fun=lambda Fp: me(Fp,1,1,0,1), c2fun=lambda Fp: me(Fp,1,2,0,1))
