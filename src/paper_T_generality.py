"""
paper_T_generality.py -- Paper T section 7: the obstruction across the alkalis.

The rank-2 null is universal: any J=1/2 ground manifold supports no rank-2 tensor, so the
leading (degenerate-excited) Dm=2 amplitude vanishes -- sum_F' g_F' = 0 -- for EVERY alkali.
The field-insensitive clock pair is always |F=I-1/2, m=-1> / |F=I+1/2, m=+1> (matched g_F m_F),
and only the two excited levels F'=I-1/2, I+1/2 carry the surviving amplitude, so

    FoM = 2|G2|/(Gamma*Sigma) = 2 |g_lo| * Delta_split / (Gamma * Sigma_inf),

where g_lo and Sigma_inf are pure angular factors (functions of I only, computed here) and
Delta_split = (F'=I-1/2)<->(F'=I+1/2) excited-state hyperfine interval, Gamma = D2 linewidth.

Excited-state nP3/2 hyperfine constants (A,B) and D2 linewidths are standard tabulated values
(Steck Rb-87/Na/Cs data; Tiecke K; Steck/Gehm Li); the intervals are computed from the Casimir
formula and cross-checked (Cs 151/201/251 MHz, Rb 72/157/267 MHz). The species constants are
[I] (tabulated, +/-few%); the null and the angular factors are [V] (exact).
"""
import sympy as sp
from sympy.physics.wigner import clebsch_gordan

Jg = sp.Rational(1, 2)   # ground 5S/6S... J = 1/2  (the universal feature)
Je = sp.Rational(3, 2)   # excited nP3/2 (D2)

def angular(I):
    """Pure angular factors for the Dm=2 clock pair |I-1/2,-1>/|I+1/2,+1> via J'=3/2.
    Returns (Flo, Fhi, g_dict, |g_lo|, Sigma_inf, null=sum g)."""
    I = sp.nsimplify(I)
    Flo, Fhi = I - sp.Rational(1, 2), I + sp.Rational(1, 2)
    def me(Fe, meF, Fg, mgF, q):
        tot = sp.Integer(0)
        nI = int(2 * I) + 1
        for kk in range(nI):
            mI = -I + kk
            for mJ2 in (-1, 1):
                mJ = sp.Rational(mJ2, 2)
                mJp = mJ + q
                if abs(mJp) > sp.Rational(3, 2):
                    continue
                tot += (clebsch_gordan(Je, I, Fe, mJp, mI, meF)
                        * clebsch_gordan(Jg, I, Fg, mJ, mI, mgF)
                        * clebsch_gordan(Jg, 1, Je, mJ, sp.Integer(q), mJp))
        return sp.nsimplify(tot)
    Fps = [I + sp.Rational(d, 2) for d in (-3, -1, 1, 3) if I + sp.Rational(d, 2) >= 0]
    g, c1, c2 = {}, {}, {}
    for Fp in Fps:
        a = me(Fp, 0, Flo, -1, +1)     # <F',0| d+ |Flo,-1>
        b = me(Fp, 0, Fhi,  1, -1)     # <F',0| d- |Fhi, 1>
        c1[Fp], c2[Fp] = a, b
        g[Fp] = sp.simplify(-b * a)
    null = float(sp.simplify(sum(g.values())))
    Sigma = float(sum(c1[Fp]**2 + c2[Fp]**2 for Fp in Fps))
    return Flo, Fhi, {str(k): float(v) for k, v in g.items()}, abs(float(g[Flo])), Sigma, null

# species: I, F'=(I-1/2)<->(I+1/2) excited interval (MHz), D2 linewidth Gamma/2pi (MHz), excited (A,B)
SPECIES = [
    ("Rb-87",  sp.Rational(3,2), 156.94, 6.0666, "5P3/2  A=84.72, B=12.50"),
    ("Cs-133", sp.Rational(7,2), 201.29, 5.22,   "6P3/2  A=50.29, B=-0.49"),
    ("Na-23",  sp.Rational(3,2),  34.34, 9.79,   "3P3/2  A=18.53, B= 2.72"),
    ("K-39",   sp.Rational(3,2),   9.40, 6.035,  "4P3/2  A= 6.09, B= 2.79"),
    ("Li-7",   sp.Rational(3,2),   5.89, 5.87,   "2P3/2  A=-3.06, B=-0.22"),
]

print("="*78)
print(" Dm=2 FIELD-INSENSITIVE CLOCK RAMAN -- FoM across the alkalis (J=1/2 ground)")
print("="*78)
print(" null check (sum_F' g_F' must be 0 for all; the rank-2 obstruction is universal):")
ang_cache = {}
for name, I, split, Gamma, note in SPECIES:
    Flo, Fhi, gd, glo, Sigma, null = angular(I)
    ang_cache[name] = (Flo, Fhi, glo, Sigma)
    print("   %-7s I=%-3s  clock pair |%s,-1>/|%s,+1>  F'=%s,%s  |g_lo|=%.4f  Sigma=%.3f  null=%.1e"
          % (name, str(I), str(Flo), str(Fhi), str(Flo), str(Fhi), glo, Sigma, null))
print("-"*78)
print(" FoM = 2|g_lo|*Delta_split/(Gamma*Sigma)   (radians of 2-photon rotation per scattered photon)")
print(" %-7s | %-22s | split(MHz) | Gamma | FoM   | per-pi scatter | verdict" % ("atom", "excited nP3/2"))
print(" "+"-"*92)
for name, I, split, Gamma, note in SPECIES:
    Flo, Fhi, glo, Sigma = ang_cache[name]
    fom = 2 * glo * split / (Gamma * Sigma)
    per_pi = 3.14159 / fom
    verdict = "DISQUALIFIED" + (" (sub-unity!)" if fom < 1 else "")
    print(" %-7s | %-22s | %8.1f   | %5.2f | %5.2f | %5.2f photons  | %s"
          % (name, note, split, Gamma, fom, per_pi, verdict))
print(" "+"-"*92)
print(" threshold for ground-state cooling (n<=0.01, from rsc_floor_rate_eqn.py):  FoM >= ~170")
print("="*78)
print(" RESULT: sum g=0 for every alkali (universal rank-2 null). The FoM ceiling Delta_HFS/Gamma")
print(" runs from ~0.2 (Li, K -- SUB-UNITY: >1 photon scattered per radian) to ~5-6 (Rb, Cs);")
print(" NONE approaches the ~170 needed. Dm=2 Raman sideband cooling of the field-insensitive")
print(" clock qubit is obstructed for the whole alkali series -- worst for the light alkalis.")
print(" EIT (near-resonant) is the field-insensitive route for all.   [null,angular: V; const: I]")
print("="*78)
