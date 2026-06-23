"""
paper_T_fom.py -- the theoretical core of Paper T, computed explicitly.

Dm=+2 clock Raman g1=|F=1,m=-1> -> |F',m'=0> -> g2=|F=2,m=+1> in 87Rb via 5P3/2.
Both beams drive the intermediate m'=0 (mirror-ladder: sigma+ guided, sigma- retro).

Shows: (1) NULL  sum_F' g_F' = 0 (rank-2 electronic null, concretely);
       (2) SCALING  surviving amplitude prop Delta_HFS/Delta^2;
       (3) FoM = |Omega_2ph|/R_scatter prop Delta_HFS/Gamma -- detuning-INDEPENDENT, ~few.

Every dipole element is built from the |m_J,m_I> product basis (dipole acts on m_J only,
Delta m_I=0), so there is no hyperfine reduced-element convention to get wrong; <J'||d||J>
is common to all elements and cancels in every ratio. The null is the oracle.

Importable: gF/gnum, c1n/c2n, G2, G_of(D), Sigma(D), FoM(D), FOM_INF, SIGMA_INF, NULL.
Run as a script for the full printed report.
"""
import os, sys
import sympy as sp
from sympy.physics.wigner import clebsch_gordan
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import operating_point as op

J  = sp.Rational(1, 2)   # 5S1/2
Jp = sp.Rational(3, 2)   # 5P3/2
Inuc = sp.Rational(3, 2) # 87Rb
GAMMA = op.GAMMA_D2_MHZ
dHFS = op.HF_5P32_MHZ

def _cg(j1, m1, j2, m2, J3, M3):
    return clebsch_gordan(j1, j2, J3, m1, m2, M3)

def me(Fe, meF, Fg, mgF, q):
    """<excited Fe,meF | d_q | ground Fg,mgF> / <J'||d||J>, via |m_J,m_I>."""
    tot = sp.Integer(0)
    for mI2 in (-3, -1, 1, 3):
        mI = sp.Rational(mI2, 2)
        for mJ2 in (-1, 1):
            mJ = sp.Rational(mJ2, 2)
            mJp = mJ + q
            if abs(mJp) > sp.Rational(3, 2):
                continue
            tot += (_cg(Jp, mJp, Inuc, mI, sp.Integer(Fe), sp.Integer(meF))
                    * _cg(J, mJ, Inuc, mI, sp.Integer(Fg), sp.Integer(mgF))
                    * _cg(J, mJ, 1, sp.Integer(q), Jp, mJp))
    return sp.nsimplify(tot)

# ---- path amplitudes g_F' and scatter line-strengths c1,c2 ----
# g_F' = <2,1|d+|F',0><F',0|d+|1,-1> ; <2,1|d+|F',0> = -<F',0|d-|2,1> (conjugation)
gF, _c1, _c2 = {}, {}, {}
for Fp in (0, 1, 2, 3):
    a = me(Fp, 0, 1, -1, +1)     # <F',0| d+ |1,-1>  (excite g1, sigma+)
    b = me(Fp, 0, 2,  1, -1)     # <F',0| d- |2, 1>  (excite g2, sigma-)
    _c1[Fp], _c2[Fp] = a, b
    gF[Fp] = sp.simplify(-b * a) # = <2,1|d+|F',0><F',0|d+|1,-1>

gnum = {k: float(v) for k, v in gF.items()}
c1n  = {k: float(v) for k, v in _c1.items()}
c2n  = {k: float(v) for k, v in _c2.items()}
NULL = float(sp.simplify(sum(gF.values())))
G2   = float(sum(gF[Fp] * dHFS[Fp] for Fp in (0, 1, 2, 3)))

def G_of(D):
    return sum(gnum[Fp] / (D + dHFS[Fp]) for Fp in (0, 1, 2, 3))
def Sigma(D):  # scatter line-strength: both beams excite their ground state to m'=0
    return sum(c1n[Fp]**2 / (D + dHFS[Fp])**2 for Fp in (0,1,2,3)) \
         + sum(c2n[Fp]**2 / (D + dHFS[Fp])**2 for Fp in (0,1,2,3))
def FoM(D):
    return 2*abs(G_of(D)) / (GAMMA * Sigma(D))

SIGMA_INF = sum(c1n[Fp]**2 for Fp in (0,1,2,3)) + sum(c2n[Fp]**2 for Fp in (0,1,2,3))
FOM_INF   = 2*abs(G2) / (GAMMA * SIGMA_INF)

if __name__ == "__main__":
    print("="*72)
    print(" Dm=2 CLOCK RAMAN -- explicit angular computation (87Rb, via 5P3/2)")
    print("="*72)
    print(" path amplitudes g_F' (units of <J'||d||J>^2):")
    for Fp in (0, 1, 2, 3):
        print("    F'=%d : g = %+.6f" % (Fp, gnum[Fp]))
    print(" NULL CHECK  sum_F' g_F' = %s  -> %.2e   [rank-2 electronic null]"
          % (sp.simplify(sum(gF.values())), NULL))
    print("-"*72)
    print(" SURVIVING amplitude: G2 = sum g_F' * dHFS = %.4f MHz  (prop to F'=1,2 splitting %.2f MHz)"
          % (G2, dHFS[1] - dHFS[2]))
    print("    Delta^2 * G(Delta) -> -G2 :")
    for D in (1e3, 1e4, 1e5):
        print("       Delta=%8.0f :  Delta^2*G = %+.4f   (-G2 = %+.4f)" % (D, D*D*G_of(D), -G2))
    print("-"*72)
    print(" FoM = 2|G(Delta)|/(Gamma*Sigma(Delta))  -- flat in Delta:")
    for D in (300., 1000., 3000., 10000., 30000.):
        print("       Delta=%8.0f :  FoM = %.3f" % (D, FoM(D)))
    print("    FoM_infinity = %.3f   (Sigma_inf=%.4f, Gamma=%.2f)" % (FOM_INF, SIGMA_INF, GAMMA))
    print("="*72)
    print(" RESULT: sum g_F'=0 (rank-2 null); survivor ~ Delta_HFS/Delta^2; FoM ~ %.1f pinned by" % FOM_INF)
    print(" Delta_HFS/Gamma, detuning-INDEPENDENT. An allowed Raman would give FoM ~ Delta/Gamma.")
    print("="*72)
