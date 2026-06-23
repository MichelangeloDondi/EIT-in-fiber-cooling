"""
clock_branching_check.py -- the dark-leg spontaneous-decay branching that
decides the control/probe leg assignment, for BOTH cooling schemes.

WHY THIS EXISTS
  The leg-swap verdict turns on which dark leg the cooling excited state
  decays into: the dark state sits ~94% on the PROBE leg (|D> ~ Oc|g_probe>),
  so decays landing on the probe leg recycle into the dark state (good), and
  decays landing on the control/bright leg diffuse out (floor-raising). The
  optimal assignment seats the dark state on the high-decay leg.

  Stretched (m'=2, |F'2,2>) and clock (m'=0, |F'2,0>) have OPPOSITE dark-leg
  asymmetries -> the leg-swap verdict that holds for stretched INVERTS for the
  clock scheme we actually run.

GATE: |F'2,2> must reproduce verify_tagged_solve.py:32 ("e2 -> g1/g2 =
  0.75/0.25") -- validates the CG machinery before trusting the clock number.

REPRODUCES the load-bearing numbers in clock_leg_swap_finding.md.
numpy + sympy only (laptop).
"""
from sympy.physics.wigner import wigner_6j, clebsch_gordan
from sympy import S

Inuc = S(3) / 2                      # Rb-87 nuclear spin
JP_D2 = S(3) / 2                     # 5P3/2
CGx = lambda j1, m1, j2, m2, J, M: clebsch_gordan(
    S(j1), S(j2), S(J), S(m1), S(m2), S(M))


def m_branch(Jp, Fp, mp):
    """Exact {(F,m): fraction} for a D-line |F',m'> -> |F,m>, normalized over
    ALL accessible ground sublevels (hyperfine 6j x m-resolved CG^2)."""
    raw = {}
    for F in (1, 2):
        hf = (2 * F + 1) * (2 * Fp + 1) * wigner_6j(S(1) / 2, S(Jp), 1, Fp, F, Inuc) ** 2
        for m in range(-F, F + 1):
            q = mp - m                                   # emitted photon helicity
            if q in (-1, 0, 1):
                w = hf * CGx(F, m, 1, q, Fp, mp) ** 2
                if w != 0:
                    raw[(F, m)] = raw.get((F, m), S(0)) + w
    Z = sum(raw.values())
    return {k: v / Z for k, v in raw.items()}


def report(Fp, mp, dark_legs, label):
    b = m_branch(JP_D2, Fp, mp)
    print(f"\n{label}:  |F'2,m'={mp}>  ->")
    for k in sorted(b):
        tag = "  [DARK LEG]" if k in dark_legs else ""
        print(f"     |{k[0]},{k[1]:+d}> : {float(b[k]):.4f}{tag}")
    ds = sum(b.get(k, S(0)) for k in dark_legs)
    renorm = {k: float(b.get(k, S(0)) / ds) for k in dark_legs}
    leak = float(1 - sum(b.get(k, S(0)) for k in dark_legs))
    print(f"   renormalized over dark legs {dark_legs}: "
          + ", ".join(f"|{k[0]},{k[1]:+d}>={v:.2f}" for k, v in renorm.items()))
    print(f"   raw spectator/leak fraction: {leak:.3f}")
    return renorm


if __name__ == "__main__":
    # --- GATE: stretched must give 0.75/0.25 (verify_tagged_solve.py:32) ---
    s = report(2, 2, [(1, 1), (2, 1)], "STRETCHED (m'=2)")
    assert abs(s[(1, 1)] - 0.75) < 1e-6 and abs(s[(2, 1)] - 0.25) < 1e-6, \
        "GATE FAILED: m'=2 does not reproduce verify's 0.75/0.25"
    print("   GATE OK: matches verify_tagged_solve.py:32 (0.75/0.25)")

    # --- the clock number (what we run) ---
    c = report(2, 0, [(1, -1), (2, 1)], "CLOCK (m'=0)  [adopted]")
    print(f"\n==> dark-leg asymmetry FLIPS: stretched favors F=1 (0.75), "
          f"clock favors |2,+1> (0.{round(c[(2,1)]*100):.0f}).")
    print("    Current clock seats the dark state on |1,-1> (0.25 leg) "
          "= diffusion-SUBOPTIMAL.")
    print("    Diffusion-optimal clock choice = SWAP (dark on |2,+1>, "
          "control on |1,-1>); also kills the F'3 parasitic (F=1->F'3 forbidden).")
