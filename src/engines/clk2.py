"""
clk2.py -- clock_combined_solve.py + surgical hooks (swap / rep2mode / want_fock /
clearer). The engine behind the leg-swap DECIDING RUN and the EOM-Raman clearer test.

PROVENANCE: reconstructed onto the validated base clock_combined_solve.py (the base's
physics is byte-identical; `diff` shows the hooks are the only delta). The external
auditor's clk2.py was itself a reconstruction on this same base; this one is validated
NON-CIRCULARLY against the reported anchors of BOTH tests:

  DECIDING RUN (run `python clk2.py`) -- all reproduce:
    clean-Lambda config A (swap=F)         = 0.0072   [base anchor]
    clean-Lambda config B (swap=T)         = 0.0022   [validates the swap hook]
    full config A (swap=F, rep2=A, OmR=.25)= 0.0048   [hard-converged, frame-conflict 0]
    config B (swap=T, rep2=A) Fock tail     rises with Nf (-> ~1) = heating divergence
    config-B full <n> ~ 0.014-0.017 across the Drep grid (auditor 0.0173); VERDICT (A
    ~3.8x better, B divergent) is convention-robust.

  EOM-RAMAN CLEARER (clearer=dict(Om_L,Dr,dR2,scatter,lightshift)) -- all reproduce:
    config B clearer OFF                    = 0.0167  (auditor 0.0173)
    ideal rung (scatter+lightshift off)     = 0.0060  (auditor ~0.006) -- floors at ~A,
                                              NEVER clean-Lambda 0.0022 even at Om_L=90 (8xOc)
    + parasitic scatter (the killer)        = 0.055   (auditor 0.057) -- dark-state depletion
    => window empty: no (Om_L,Dr,dR2) where B converges below A. A holds vs the clearer too.
    NOTE on dR2: the two-photon resonance location is frame-convention-dependent (auditor's
    [O1]); here it optimizes near the frame-predicted +2.0, vs the auditor's empirical [-1,0].
    The FLOOR values match -- that is what carries the verdict.

------------------------------------------------------------------------------
clock_combined_solve.py -- the m'=0 (magic-clock) analogue of combined_solve.py,
wired to the locked clock configuration:

  cooling Lambda : |2,+1> sigma- / |1,-1> sigma+  ->  |F'2,0>   (Dc=80, AC-Stark
                   matched Oc^2/4Dc = nu_z, delta_2ph = 0 servo, B = 3.2287 G magic)
  repump1        : sigma- on F=1 -> F'1   (clears |1,0>->|F'1,-1>; |1,-1>->|F'1,-2|
                   FORBIDDEN -> probe clock leg DARK by edge rule)
  repump2 opt A  : sigma+ on F=2 -> F'1   (clears |2,-2>->|F'1,-1>; |2,+1>->|F'1,+2|
                   FORBIDDEN -> control clock leg DARK by edge rule); AXIAL recoil
  repump2 opt C  : pi     on F=2 -> F'2   (clears |2,-2>->|F'2,-2>; |2,0>->|F'2,0|
                   CG=0); TRANSVERSE absorption (no axial kick) but shares the F'2
                   manifold with the control -> a Dm Raman (|2,+2><->|2,+1> via
                   |F'2,+1>) that touches the control clock leg near Drep ~ +80.

MODEL
  internal : 8 grounds {F=1 m=-1..1 ; F=2 m=-2..2}  +  F'1(3) + F'2(5) excited
  motion   : axial Fock (Nf), Lamb-Dicke displacement D(i eta k) on every coupling
  frame    : EACH beam couples its ground manifold to ONE excited hyperfine manifold
             (RWA drops the ~157 MHz cross-F' tails). Every CG-allowed transition of
             each beam is kept (full ladders), so the secondary couplings that build
             the Dm Ramans are present. A static multi-rotating frame exists because
             the coherent graph is a FOREST (the |2,0>->|F'2,0> CG=0 null breaks the
             control/pi-rep F=2 ladder); it is built by BFS over the graph from the
             |2,+1> reference, assigning each diagonal as h[node] from real Breit-Rabi
             (ground) and tensor-diagonalized 5P3/2 (excited) energies, so off-resonant
             residuals and the Raman resonance positions come out automatically.
  decay    : full hyperfine branchings BR(F'1->F1)=5/6,(F'1->F2)=1/6,(F'2->F)=1/2 each,
             m-resolved by CG^2, axial emission recoil distribution (1/6,2/3,1/6).
             Every decay target is inside the 8-ground set -> exact closure, no redirect.

GATES
  A  repumps off + only the cooling Lambda kept -> clean clock-Lambda floor (recoil-ish).
  B  BFS frame is consistent (forest) AND the opt-C control-leg Raman appears at the
     line-referenced Drep* ~ +80 (frame-bookkeeping check).
"""
import numpy as np
import qutip as qt
from sympy.physics.wigner import clebsch_gordan
from sympy import S

CGc = lambda F, m, q, Fp, mp: float(clebsch_gordan(S(F), 1, S(Fp), S(m), S(q), S(mp)))

GAMMA, NU, ETA = 6.07, 0.430, 0.094
EM_REC = [(-1, 1/6), (0, 2/3), (1, 1/6)]          # axial emission recoil distribution
BR = {1: {1: 5/6, 2: 1/6}, 2: {1: 1/2, 2: 1/2}}   # BR(F'->F) for 5P3/2

# ---- real internal energies (MHz) -------------------------------------------
A_HFS, gJ, gI, uB, II = 6834.682610, 2.00233, -0.0009951, 1.399624, 1.5
def Eg(F, m, B):                                  # Breit-Rabi ground (rel. centroid)
    x = (gJ - gI)*uB*B/A_HFS; sgn = +1 if F == 2 else -1
    return -A_HFS/(2*(2*II+1)) + gI*uB*m*B + sgn*(A_HFS/2)*np.sqrt(1+4*m*x/(2*II+1)+x**2)

_EHF = {0: -302.07, 1: -229.85, 2: -72.91, 3: 193.74}
def excited_energies(B):
    """Dominant eigenvalue of each |F',m'> under hyperfine+Zeeman+perp tensor."""
    Ex = [(0, 0)] + [(1, m) for m in (-1, 0, 1)] + [(2, m) for m in range(-2, 3)] \
         + [(3, m) for m in range(-3, 4)]
    prod = [(1.5-a, 1.5-b) for a in range(4) for b in range(4)]
    U = np.zeros((16, 16))
    for ci, (Fp, mp) in enumerate(Ex):
        for pj, (mJ, mI) in enumerate(prod):
            if abs(mJ+mI-mp) < 1e-9:
                U[ci, pj] = float(clebsch_gordan(S(3)/2, S(3)/2, S(Fp), S(mJ), S(mI), S(mp)))
    sq3 = np.sqrt(3)
    Jx32 = 0.5*np.array([[0, sq3, 0, 0], [sq3, 0, 2, 0], [0, 2, 0, sq3], [0, 0, sq3, 0]])
    Jx = U @ np.kron(Jx32, np.eye(4)) @ U.T
    gFp = 2.0/3.0  # F'=2 ; F'=1 uses its own below
    def gF(Fp): return gJ*(Fp*(Fp+1))/(2*Fp*(Fp+1)) if Fp > 0 else 0.0
    H0 = np.diag([_EHF[Fp] + gF(Fp)*uB*B*mp for (Fp, mp) in Ex]).astype(float)
    w, v = np.linalg.eigh(H0 - 6.233*(3*Jx@Jx - 3.75*np.eye(16)))
    out = {}
    for (Fp, mp) in Ex:
        if Fp in (1, 2):
            out[(Fp, mp)] = w[np.argmax(np.abs(v[Ex.index((Fp, mp)), :])**2)]
    return out

# ---- beam definitions: ladders of (g, e) with CG, per polarization ----------
def beams(option, Dc, Drep1, Drep2, d2, Oc, Op, Om_r, swap=False, rep2mode=None):
    """Return list of beams; each beam = dict(edges, named, det, Rabi, kdir).
       edges: list of ((Fg,mg),(Fp,mp),CG).  named: (g,e) anchor.  det: anchor detuning.
       kdir: axial recoil direction (0 = transverse / no axial kick).

       HOOK swap (clk2): the control<->probe leg assignment.
         swap=False (config A): strong control = sigma- F2->F'2 on |2,+1>; weak probe =
              sigma+ F1->F'2 on |1,-1>.  Dark leg = |1,-1> (F=1 EDGE).
         swap=True  (config B): strong control = sigma+ F1->F'2 on |1,-1>; weak probe =
              sigma- F2->F'2 on |2,+1>.  Dark leg = |2,+1> (F=2 INTERIOR).
         Forward/strong keeps +k, retro/weak keeps -k, d2 servo rides the weak (probe)
         leg in both; only the launched helicity (and which leg is strong) flips.
       HOOK rep2mode (clk2): repump2 topology scan; None -> use `option` (A/C as base)."""
    def ladder(Fg, q, Fp):
        e = []
        for mg in ([-1, 0, 1] if Fg == 1 else [-2, -1, 0, 1, 2]):
            mp = mg + q
            if abs(mp) <= Fp:
                c = CGc(Fg, mg, q, Fp, mp)
                if abs(c) > 1e-9:
                    e.append(((Fg, mg), (Fp, mp), c))
        return e
    bm = []
    if not swap:
        # config A: control sigma- F2->F'2 strong on |2,+1>; probe sigma+ F1->F'2 weak on |1,-1>
        bm.append(dict(edges=ladder(2, -1, 2), named=((2, 1), (2, 0)), det=Dc,
                       Rabi=Oc, kdir=+1, tag='ctrl'))
        bm.append(dict(edges=ladder(1, +1, 2), named=((1, -1), (2, 0)), det=Dc + d2,
                       Rabi=Op, kdir=-1, tag='probe'))
    else:
        # config B (swap): control sigma+ F1->F'2 strong on |1,-1>; probe sigma- F2->F'2 weak on |2,+1>
        bm.append(dict(edges=ladder(1, +1, 2), named=((1, -1), (2, 0)), det=Dc,
                       Rabi=Oc, kdir=+1, tag='ctrl'))
        bm.append(dict(edges=ladder(2, -1, 2), named=((2, 1), (2, 0)), det=Dc + d2,
                       Rabi=Op, kdir=-1, tag='probe'))
    # repump1 sigma- on F=1 -> F'1 ; named |1,0>->|F'1,-1>, detuning Drep1
    bm.append(dict(edges=ladder(1, -1, 1), named=((1, 0), (1, -1)), det=Drep1,
                   Rabi=Om_r, kdir=+1, tag='rep1'))
    # repump2 -- rep2mode overrides option (topology scan); base options A/C preserved
    rm = rep2mode if rep2mode is not None else option
    if rm == 'A':       # sigma+ F2->F'1 ; named |2,-2>->|F'1,-1>  (the unique protector)
        bm.append(dict(edges=ladder(2, +1, 1), named=((2, -2), (1, -1)), det=Drep2,
                       Rabi=Om_r, kdir=+1, tag='rep2'))
    elif rm == 'C':     # pi F2->F'2 ; named |2,-2>->|F'2,-2> ; TRANSVERSE
        bm.append(dict(edges=ladder(2, 0, 2), named=((2, -2), (2, -2)), det=Drep2,
                       Rabi=Om_r, kdir=0, tag='rep2'))
    elif rm == 'spF2':  # sigma+ F2->F'2
        bm.append(dict(edges=ladder(2, +1, 2), named=((2, -2), (2, -1)), det=Drep2,
                       Rabi=Om_r, kdir=+1, tag='rep2'))
    elif rm == 'smF1':  # sigma- F2->F'1
        bm.append(dict(edges=ladder(2, -1, 1), named=((2, 0), (1, -1)), det=Drep2,
                       Rabi=Om_r, kdir=+1, tag='rep2'))
    elif rm == 'piF1':  # pi F2->F'1
        bm.append(dict(edges=ladder(2, 0, 1), named=((2, -1), (1, -1)), det=Drep2,
                       Rabi=Om_r, kdir=0, tag='rep2'))
    elif rm == 'smF2':  # sigma- F2->F'2
        bm.append(dict(edges=ladder(2, -1, 2), named=((2, 0), (2, -1)), det=Drep2,
                       Rabi=Om_r, kdir=+1, tag='rep2'))
    return bm

# ---- BFS multi-rotating frame ----------------------------------------------
def build_frame(bm, gE, eE):
    """Assign h[node] (rotating-frame diagonal) by BFS. Returns (h, max_conflict)."""
    realE = {}
    for g in gE: realE[('g', g)] = gE[g]
    for e in eE: realE[('e', e)] = eE[e]
    # nu_b for each beam from its named transition
    for b in bm:
        (g, e), Dn = b['named'], b['det']
        b['nu'] = Dn + (realE[('e', e)] - realE[('g', g)])
    adj = {}                                          # node -> list of (other, h_delta)
    def add(n1, n2, d):
        adj.setdefault(n1, []).append((n2, d)); adj.setdefault(n2, []).append((n1, -d))
    for b in bm:
        for (g, e, c) in b['edges']:
            # static condition: h[('e',e)] - h[('g',g)] = -det_ge ;
            # det_ge = nu_b - (E_e - E_g) ; so h[e] = h[g] - det_ge
            det_ge = b['nu'] - (realE[('e', e)] - realE[('g', g)])
            add(('g', g), ('e', e), -det_ge)          # h[e] = h[g] + (-det_ge)
    # BFS over EVERY connected component (components are linked only by decay,
    # which is frame-invariant, so each gets its own arbitrary offset). Reference
    # |2,+1> kept at 0 for interpretability; other components anchored at 0 locally.
    h = {}; max_conf = 0.0
    order = [('g', (2, 1))] + [n for n in adj if n != ('g', (2, 1))]
    for start in order:
        if start in h or start not in adj:
            continue
        h[start] = 0.0; stack = [start]
        while stack:
            n = stack.pop()
            for (m, d) in adj.get(n, []):
                hv = h[n] + d
                if m in h:
                    max_conf = max(max_conf, abs(h[m] - hv))
                else:
                    h[m] = hv; stack.append(m)
    return h, max_conf

# ---- assemble and solve -----------------------------------------------------
def solve(option='C', Dc=80.0, Drep1=30.0, Drep2=5.0, d2=0.0, B=3.2287,
          Nf=8, OmR=0.25, Om_r=1.5, with_rep=True, clean_lambda=False,
          want_pops=False, swap=False, rep2mode=None, want_fock=False, clearer=None):
    gE = {(F, m): Eg(F, m, B) for F in (1, 2) for m in (range(-1, 2) if F == 1 else range(-2, 3))}
    eE = excited_energies(B)
    Otot = np.sqrt(4*Dc*NU); Oc = Otot/np.sqrt(1+OmR**2); Op = OmR*Oc
    bm = beams(option, Dc, Drep1, Drep2, d2, Oc, Op, Om_r, swap=swap, rep2mode=rep2mode)
    if clean_lambda:
        bm = [b for b in bm if b['tag'] in ('ctrl', 'probe')]
    elif not with_rep:
        bm = [b for b in bm if b['tag'] in ('ctrl', 'probe')]

    if clean_lambda:
        Gs = [(1, -1), (2, 1)]; Es = [(2, 0)]            # closed clock Lambda (redirect decay)
    else:
        Gs = [(1, -1), (1, 0), (1, 1), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]
        Es = [(1, -1), (1, 0), (1, 1), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]
    nodes = [('g', g) for g in Gs] + [('e', e) for e in Es]
    idx = {n: i for i, n in enumerate(nodes)}
    NA = len(nodes)
    # keep only edges within the active node set (matters for the reduced clean gate)
    ng, ne = set(Gs), set(Es)
    for b in bm:
        b['edges'] = [(g, e, c) for (g, e, c) in b['edges'] if g in ng and e in ne]
    bm = [b for b in bm if b['edges']
          and b['named'][0] in ng and b['named'][1] in ne]
    h, conf = build_frame(bm, gE, eE)
    # any node not reached by BFS (disconnected) -> put at its real energy offset 0
    for n in nodes:
        if n not in h: h[n] = 0.0

    bas = [qt.basis(NA, i) for i in range(NA)]
    P = lambda i, j: bas[i]*bas[j].dag()
    If = qt.qeye(Nf); aop = qt.destroy(Nf)
    Dsp = lambda s: qt.displace(Nf, 1j*ETA*s)

    H = NU*qt.tensor(qt.qeye(NA), aop.dag()*aop)
    for n in nodes:
        H += h[n]*qt.tensor(P(idx[n], idx[n]), If)
    # coherent couplings (Rabi scaled within beam by CG/CG_named)
    for b in bm:
        (gn, en), cnamed = b['named'], None
        cnamed = [c for (g, e, c) in b['edges'] if g == gn and e == en][0]
        for (g, e, c) in b['edges']:
            O = b['Rabi']*(c/cnamed)
            i, j = idx[('g', g)], idx[('e', e)]
            H += -(O/2)*(qt.tensor(P(j, i), Dsp(b['kdir']))
                         + qt.tensor(P(i, j), Dsp(b['kdir']).dag()))
    # spontaneous decay: full branchings, axial emission recoil.
    # Out-of-set targets (only in the closed-Lambda gate) are redirected to the
    # clock legs weighted by their own decay CG^2 (instant recycle, dm2 convention);
    # in the full 8-ground system every target is in-set -> exact closure, no redirect.
    legs = [(1, -1), (2, 1)]
    Gset = idx_keys(Gs)
    cops = []
    for (Fp, mp) in Es:
        ch = {}
        for Fg in (1, 2):
            for mg in (mp-1, mp, mp+1):
                if abs(mg) > Fg:
                    continue
                c = CGc(Fg, mg, mp-mg, Fp, mp)
                if abs(c) < 1e-12:
                    continue
                w = BR[Fp][Fg]*c**2
                if (Fg, mg) in Gset:
                    ch[(Fg, mg)] = ch.get((Fg, mg), 0) + w
                else:
                    lw = np.array([CGc(lf, lm, mp-lm, Fp, mp)**2 for (lf, lm) in legs])
                    lw = lw/lw.sum() if lw.sum() > 0 else np.ones(len(legs))/len(legs)
                    for (lf, lm), ww in zip(legs, lw):
                        ch[(lf, lm)] = ch.get((lf, lm), 0) + w*ww
        tot = sum(ch.values())
        for (g, w) in ch.items():
            for (u, wem) in EM_REC:
                cops.append(np.sqrt(GAMMA*(w/tot)*wem)
                            * qt.tensor(P(idx[('g', g)], idx[('e', (Fp, mp))]), Dsp(u)))

    # HOOK clearer (clk2): the EOM-Raman |2,+2> -> |1,+1> clearer (second EOM tone).
    # clearer = dict(Om_L=per-leg single-photon Rabi, Dr=intermediate detuning,
    #                dR2=two-photon detuning [pinned numerically], scatter=True,
    #                lightshift=True). Models, after adiabatic elimination of F'2:
    #   - coherent rung O2ph = Om_L^2 CG1 CG2 / (2 Dr)  (recoil-free, co-prop legs)
    #   - AC-Stark dLS = (Om_L CG_g)^2 / (4 Dr) on each touched ground
    #   - parasitic single-photon scatter R(g) = Gamma (Om_L CG_g)^2 / (4 Dr^2) on every
    #     F=2 sublevel (incl. the 93.5%-occupied dark leg |2,+1>), KH-branched over final
    #     grounds with absorption(+1 axial)+emission recoil. This scatter is the killer.
    if clearer is not None and not clean_lambda:
        OmL = clearer['Om_L']; Dr = clearer['Dr']; dR2 = clearer.get('dR2', 0.0)
        g22 = ('g', (2, 2)); g11 = ('g', (1, 1))
        CG1 = abs(CGc(2, 2, 0, 2, 2))            # leg1 pi  |2,+2>->|F'2,+2>
        CG2 = abs(CGc(1, 1, 1, 2, 2))            # leg2 sig+ |1,+1>->|F'2,+2>
        if g22 in idx and g11 in idx:
            O2ph = OmL**2 * CG1 * CG2 / (2*Dr)
            i22, i11 = idx[g22], idx[g11]
            # recoil-free coherent rung |2,+2> <-> |1,+1>
            H += -(O2ph/2)*(qt.tensor(P(i22, i11), If) + qt.tensor(P(i11, i22), If))
            # two-photon detuning (pinned numerically; small -> ~faithful on rep1's off-res |1,+1>)
            H += dR2*qt.tensor(P(i11, i11), If)
            if clearer.get('lightshift', True):
                for (Fg, mg) in Gs:
                    if Fg == 2:
                        cg = CGc(2, mg, 0, 2, mg)               # pi leg on F=2
                        if abs(cg) > 1e-9:
                            H += ((OmL*cg)**2/(4*Dr))*qt.tensor(
                                P(idx[('g', (Fg, mg))], idx[('g', (Fg, mg))]), If)
                H += ((OmL*CG2)**2/(4*Dr))*qt.tensor(P(i11, i11), If)
            if clearer.get('scatter', True):
                for (Fg, mg) in Gs:
                    if Fg != 2:
                        continue
                    cg = CGc(2, mg, 0, 2, mg)                    # pi excitation |2,mg>->|F'2,mg>
                    if abs(cg) < 1e-9:
                        continue
                    Rg = GAMMA*(OmL*cg)**2/(4*Dr**2)            # single-photon scatter rate
                    Fp, mp = 2, mg
                    ch = {}
                    for Ff in (1, 2):
                        for mf in (mp-1, mp, mp+1):
                            if abs(mf) > Ff or ('g', (Ff, mf)) not in idx:
                                continue
                            cc = CGc(Ff, mf, mp-mf, Fp, mp)
                            if abs(cc) < 1e-12:
                                continue
                            ch[(Ff, mf)] = ch.get((Ff, mf), 0) + BR[Fp][Ff]*cc**2
                    tot = sum(ch.values())
                    if tot <= 0:
                        continue
                    for (gf, w) in ch.items():
                        for (u, wem) in EM_REC:                  # absorption(+1)+emission(u) recoil
                            cops.append(np.sqrt(Rg*(w/tot)*wem)
                                        * qt.tensor(P(idx[('g', gf)], idx[('g', (2, mg))]),
                                                    Dsp(1 + u)))

    L = qt.liouvillian(H, cops)
    try:
        rho = qt.steadystate(L, method='direct')
    except Exception:
        rho = qt.steadystate(L, method='svd')
    N = qt.tensor(qt.qeye(NA), aop.dag()*aop)
    nbar = qt.expect(N, rho)
    if want_fock:
        # HOOK want_fock (clk2): partial-trace to the motional (Fock) subsystem and
        # return P(n) + the top-of-ladder ratio P(n+1)/P(n). A near-flat tail
        # (ratio -> ~1) is the heating-divergence signature; a damped tail (ratio << 1)
        # is a robust floor. tailmax = max ratio over the top three rungs.
        rho_f = rho.ptrace(1)
        Pn = np.real(np.diag(rho_f.full()))
        ratios = [Pn[k+1]/Pn[k] for k in range(Nf-1) if Pn[k] > 1e-14]
        tailmax = max(ratios[-3:]) if len(ratios) >= 3 else (max(ratios) if ratios else 0.0)
        return nbar, conf, Pn, tailmax
    if want_pops:
        pops = {g: qt.expect(qt.tensor(P(idx[('g', g)], idx[('g', g)]), If), rho) for g in Gs}
        pe = sum(qt.expect(qt.tensor(P(idx[('e', e)], idx[('e', e)]), If), rho) for e in Es)
        return nbar, conf, pops, pe
    return nbar, conf


def idx_keys(Gs):
    return set(Gs)


if __name__ == '__main__':
    print("=== clk2.py GATE: base-physics anchors (unchanged from clock_combined_solve) ===")
    print("clean closed clock-Lambda floor (repumps off), config A:")
    for Nf in (6, 8, 10):
        nb, cf = solve(clean_lambda=True, Nf=Nf, swap=False)
        print("   Nf=%2d  <n>=%.4f   frame-conflict=%.2e   [expect ~0.0072]" % (Nf, nb, cf))

    print("\n=== clk2.py DECIDING RUN: config A vs config B (swap) ===")
    print("clean-Lambda, config A (swap=F) vs config B (swap=T):")
    nbA, cfA = solve(clean_lambda=True, Nf=8, swap=False)
    nbB, cfB = solve(clean_lambda=True, Nf=8, swap=True)
    print("   A  <n>=%.4f  cf=%.1e   [expect ~0.0072]" % (nbA, cfA))
    print("   B  <n>=%.4f  cf=%.1e   [expect ~0.0022]" % (nbB, cfB))

    print("\nFULL repumped, config A (swap=F, rep2=A, Drep1=20, Drep2=5, OmR=0.25):")
    nbAf, cfAf = solve(option='A', swap=False, Drep1=20, Drep2=5, OmR=0.25, Nf=8)
    print("   A  <n>=%.4f  cf=%.1e   [expect ~0.0048 hard-converged]" % (nbAf, cfAf))

    print("\nFULL repumped, config B (swap=T, rep2=A forced, Drep2=20, OmR=0.25) -- Nf scan:")
    for Nf in (6, 8, 10):  # Nf=12 exceeds RAM budget; 3-point trend is sufficient
        nb, cf, Pn, tail = solve(swap=True, rep2mode='A', Drep1=20, Drep2=20,
                                 OmR=0.25, Nf=Nf, want_fock=True)
        print("   Nf=%2d  <n>=%.4f  tail=%.3f  cf=%.1e   [expect rising <n>, tail->~1]"
              % (Nf, nb, tail, cf))
