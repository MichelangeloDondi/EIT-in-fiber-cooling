"""
verify_tagged_solve.py -- full steady-state verification of the AOM-tagged
architecture's cooling floor, replacing the incoherent rejected-field
estimator of tagged_operating_point.py.  [brief Sec. 9A.6 item (1)]

MODEL (4 levels x axial Fock)
  g1=|1,+1>, g2=|2,+1>, e2=|F'2,2>, e3=|F'3,2>.
  Coherent H (rotating frame of the resonant pair):
    nu a'a + (-Delta)|e2><e2| + (F3-Delta)|e3><e3| + d2|g2><g2|
    - (Oc/2)(|e2><g2| D(+i eta) + h.c.)          fwd-control (resonant leg)
    - (Op/2)(|e2><g1| D(-i eta) + h.c.)          ret-probe   (resonant leg)
    - (Oc3/2)(|e3><g2| D(+i eta) + h.c.)         fwd-control on F'3
                                                  (same frequency -> coherent;
                                                   Oc3 = Oc*sqrt(2.857))
  Rejected fields (different frequencies by +-2fA -> all cross terms beat at
  >= 220 MHz >> Gamma, nu; secular bound (Omega/2fA)^2 ~ 1e-3) enter as
  LINEARIZED DISSIPATORS: scatter rate R = Gamma (O/2)^2 / (d^2 + (Gamma/2)^2)
  from the source ground state, with absorption recoil D(+-i eta) by beam
  direction, 3-point emission kernel, and e2/e3 branchings. Saturation
  (O/2d)^2 <= 3e-4 -> linearization excellent.
    ret-control via e2 : d = Delta - 2fA          (-180), kick D(-i eta)
    ret-control via e3 : d = Delta - 2fA - F3     (-447), kick D(-i eta)
    fwd-probe   via e2 : d = Delta + 2fA          (+260), kick D(+i eta)
  Powers: ret-control O^2 = Oc^2 * eta_dp; fwd-probe O^2 = Op^2 / eta_dp.

  delta2 IS SCANNED and the minimum reported -- this is the servo. The e3
  admixture Stark-shifts g2 by ~ -0.21 MHz (half a sideband); fixing d2 = 0
  would repeat the uncompensated-m'=0 mistake. The minimum's LOCATION is a
  cross-check against the shift budget (eit_beam_shift_budget.py: -245 kHz
  set-point offset, sign per convention below: compensation at d2 = +shift).

BRANCHINGS: e2 -> g1/g2 = 0.75/0.25 (renormalized, leak budgeted separately);
  e3 -> g2 = 1 (true 2/3 to |2,1>, 1/3 to the |2,2> leak; renormalized --
  same convention as the 3-level engine; the leak increment +0.007-0.012 is
  the separately validated budget line and is NOT in this number).

GATES: rejected+e3 OFF reproduces clean 0.0085; final number Nf-stable.
OUTPUT: clean -> +F'3 coherent (dual-end baseline) -> full tagged, each
  d2-optimized; the verified tagged-extra and the estimator calibration.
"""
import numpy as np
import qutip as qt

GAMMA, NU, ETA = 6.07, 0.430, 0.094
F3 = 266.65
B1, B2 = 0.75, 0.25


def solve(Delta=40.0, twofA=220.0, eta_dp=0.5, d2=0.0, Nf=18,
          with_e3=True, with_rejected=True, OmR=0.25, legs="swapped",
          OtotScale=1.0):
    """legs='swapped'  : strong control on g2 (b=0.25 leg) -- THE ADOPTED
                         SCHEME; dark state ~94% on g1 (b=0.75). Clean floor
                         0.0034 (cross-validates the prior 4-level Omega_r=0
                         result).
       legs='unswapped': strong control on g1 (b=0.75 leg) -- the ORIGINAL
                         pre-swap assignment used by the legacy 3-level
                         engine; reproduces its canonical 0.0085. The 2.5x
                         difference is repump-diffusion: swapped decays land
                         mostly in the dark-dominant state."""
    g1, g2, e2, e3 = (qt.basis(4, i) for i in range(4))
    P = lambda a, b: a * b.dag()
    If = qt.qeye(Nf); aop = qt.destroy(Nf)
    Dp_ = lambda s: qt.displace(Nf, 1j*ETA*s)
    Otot = OtotScale*np.sqrt(4*Delta*NU); Oc = Otot/np.sqrt(1+OmR**2); Op = OmR*Oc
    Oc3 = Oc*np.sqrt(2.857)
    gc, gp = (g2, g1) if legs == "swapped" else (g1, g2)   # control/probe leg

    H = NU*qt.tensor(qt.qeye(4), aop.dag()*aop) \
        + (-Delta)*qt.tensor(P(e2, e2), If) + d2*qt.tensor(P(g2, g2), If) \
        - (Oc/2)*(qt.tensor(P(e2, gc), Dp_(+1)) + qt.tensor(P(gc, e2), Dp_(+1).dag())) \
        - (Op/2)*(qt.tensor(P(e2, gp), Dp_(-1)) + qt.tensor(P(gp, e2), Dp_(-1).dag()))
    if with_e3:
        H += (F3 - Delta)*qt.tensor(P(e3, e3), If) \
            - (Oc3/2)*(qt.tensor(P(e3, gc), Dp_(+1)) + qt.tensor(P(gc, e3), Dp_(+1).dag()))

    cops = []
    for u, wem in [(-1, 1/6), (0, 2/3), (1, 1/6)]:
        # e2 decay (renormalized branchings); e3 decay ALWAYS present so the
        # level never forms a disconnected (singular) subspace when unused
        cops += [np.sqrt(GAMMA*B1*wem)*qt.tensor(P(g1, e2), Dp_(u)),
                 np.sqrt(GAMMA*B2*wem)*qt.tensor(P(g2, e2), Dp_(u)),
                 np.sqrt(GAMMA*wem)*qt.tensor(P(g2, e3), Dp_(u))]
    if with_rejected:
        chans = [(gc, Oc*np.sqrt(eta_dp),  Delta-twofA,      -1, (B1, B2)),
                 (gc, Oc3*np.sqrt(eta_dp), Delta-twofA-F3,   -1, (0.0, 1.0)),
                 (gp, Op/np.sqrt(eta_dp),  Delta+twofA,      +1, (B1, B2))]
        for gsrc, O, d, kdir, (bf1, bf2) in chans:
            R = GAMMA*(O/2)**2/(d**2 + (GAMMA/2)**2)
            for u, wem in [(-1, 1/6), (0, 2/3), (1, 1/6)]:
                kick = Dp_(u)*Dp_(kdir)
                if bf1 > 0: cops.append(np.sqrt(R*bf1*wem)*qt.tensor(P(g1, gsrc), kick))
                if bf2 > 0: cops.append(np.sqrt(R*bf2*wem)*qt.tensor(P(g2, gsrc), kick))
    Nop = qt.tensor(qt.qeye(4), aop.dag()*aop)
    return float(np.real(qt.expect(Nop, qt.steadystate(H, cops))))


def d2min(grid, **kw):
    vals = [(solve(d2=d, **kw), d) for d in grid]
    n, d = min(vals)
    return n, d, vals


if __name__ == "__main__":
    nA = solve(with_e3=False, with_rejected=False, legs="swapped")
    nB = solve(with_e3=False, with_rejected=False, legs="unswapped")
    print("GATE A  clean, SWAPPED legs (adopted scheme) = %.4f  "
          "(expect 0.0034 = prior 4-level Omega_r=0)" % nA)
    print("GATE B  clean, UNSWAPPED legs (legacy engine) = %.4f  "
          "(expect 0.0085 = legacy anchor)" % nB)
    assert abs(nA - 0.0034) < 5e-4 and abs(nB - 0.0085) < 6e-4
    print("-> the legacy/adopted floor difference is ENTIRELY the leg "
          "assignment (repump diffusion);\n   all numbers below are the "
          "adopted SWAPPED scheme.\n")

    g = np.arange(-0.10, 0.351, 0.05)
    nb, db, _ = d2min(g, with_rejected=False)
    print("dual-end baseline + coherent F'3 : min %.4f at d2 = %+.2f MHz"
          % (nb, db))
    nt, dt, vals = d2min(g)
    print("FULL TAGGED (2fA=220, eta_dp=0.5): min %.4f at d2 = %+.2f MHz"
          % (nt, dt))
    print("  d2 scan: " + "  ".join("%+.2f:%.4f" % (d, n) for n, d in vals))
    for Nf in (16, 22):
        print("  Nf=%d: %.4f" % (Nf, solve(d2=dt, Nf=Nf)))
    n3, d3, _ = d2min(g, twofA=300.0)
    print("alt 150 MHz AOM (2fA=300): min %.4f at d2 = %+.2f" % (n3, d3))
    print("\nVERIFIED tagged-extra over the F'3 baseline: %+.4f (220) / %+.4f"
          " (300)" % (nt - nb, n3 - nb))
    print("add the separately validated leak/anti-trap increment +0.007-0.012")
    print("for the system floor.")
