#!/usr/bin/env python3
"""
cloud_multilevel_union.py -- the cloud x multilevel UNION (the run that retires the
"additive cloud" objection).

WHAT IT COMPUTES
  The radial cloud floor with the FULL multilevel atomic engine at every radius -- not the
  3-level single-rate proxy (cloud_cooling_tool.py) and not an additive scale-separation
  argument. For each radius r it evaluates the headline coherent all-contaminant engine
  (eit_cooling_tool: 8-state ground manifold, F'=0..3 as coherent ladder edges, recoil)
  under the GUIDED GEOMETRY -- Delta_eff(r), nu_z(r), eta(r), Omega_tot(r) all scaling with
  the local intensity s(r) per cloud_cooling_tool.radial_params -- giving n_ss(r) AND the
  near-equilibrium cooling rate W(r), then feeds (s, n_ss, W) into the SAME dead-wall
  trajectory MC the 3-level tool uses (cloud_cooling_tool.run_mc).

WHY IT CLOSES THE SEAM
  The 3-level cloud result (cloud floor ~= on-axis floor, because off-axis atoms hit the
  "dead wall" W(r)->0 and freeze cold rather than heat to the warmer off-axis n_ss) was the
  one piece still argued by SCALE SEPARATION rather than computed with the multilevel engine.
  This recomputes that result with the multilevel n_ss(r)/W(r), apples-to-apples (same
  radial_params, same W relaxation-fit definition, same MC) -- so the headline cloud number
  is COMPUTED, not assumed additive.

CONVENTIONS / CHOICES (documented, checkable)
  * delta2 = -0.10 (field convention, dual_end on-axis value) is held FIXED across radii: the
    two-photon dark resonance is set by the ground manifold, and the 1064 scalar shift is
    common-mode on both ground states, so delta2 is trap-independent to leading order. r=0 is
    a BUILT-IN CHECK -- it must reproduce the gate's on-axis dual floor (~0.0048 at Nf=6); if
    it does not, delta2 is wrong and must be re-servoed.
  * W is the relaxation-fit rate (slope of ln(<n>-n_ss) from a thermal perturbation),
    IDENTICAL to cloud_cooling_tool.nss_and_W -- NOT the slowest-eigenvalue/gap estimate, so
    the multilevel and 3-level W share one definition.
  * Nf=6 (the gate truncation). The dead-wall conclusion is the SHAPE W(r)/W(0), Nf-robust.

WHAT Nf=6 SETTLES vs WHAT NEEDS CONVERGENCE (the Mac-grade / cite-grade split)
  * SHAPE is Nf-robust: the n_ss(r) de-fang, the W(r) collapse, and the cloud/on-axis RATIO
    -- i.e. WHETHER the dead-wall survives -- are settled by the Nf=6 grid (Mac-grade verdict).
  * The ABSOLUTE floor off an Nf=6 grid is the same underconverged proxy that prints 0.0048
    instead of the converged 0.0059. Do NOT cite the Nf=6 absolute. The right convergence test
    is the FLOOR ITSELF across two Nf grids (`grid8` then `compare`), NOT a per-radius n_ss
    (`nf`): the floor is the W-WEIGHTED aggregate <W*n_ss>/<W>, and because W collapses ~250x
    off-axis while n_ss climbs, the floor down-weights exactly the high-n_ss radii where Nf=6
    bites -- so per-radius flatness neither implies nor is implied by floor robustness. Decide
    at 556 uK (hot -> max off-axis weight): small Nf6->Nf8 floor drift => Mac-citable; large
    drift => genuine cluster case (and the 'dead-wall collapses for all T_r' claim itself has an
    Nf component). A cold cloud is on-axis-dominated, so its floor trivially inherits the on-axis
    +4% and tests nothing.
  * CLOSURE is a NEW multilevel assumption: the dead-wall uses d<n>/dt=-W(<n>-n_ss), one rate.
    The 3-level cold-start test that earned "freeze, not heat" did not see F'1/F'3 internal
    modes. `closure <r>` two-rate-fits the multilevel relaxation at one off-axis radius to
    confirm early-rate ~= late-rate (one extra solve).

MODES
  python src/engines/cloud_multilevel_union.py            # the full Nf=6 radial grid + dead-wall MC (default)
  python src/engines/cloud_multilevel_union.py grid8      # the same grid at Nf=8 -> union_grid_nf8.npz
  python src/engines/cloud_multilevel_union.py compare    # citable-number test: floor drift Nf6->Nf8 (4 profiles)
  python src/engines/cloud_multilevel_union.py closure 9  # single-rate closure check at r=9um
  python src/engines/cloud_multilevel_union.py nf 9       # per-radius Nf=6/8/10 bound at r=9um (sanity, not the decider)
  python src/engines/cloud_multilevel_union.py defang 9   # isolated F'1 increment (with_e1 on/off) at r=9um (opt-in deliverable)

COST  ~11-25 min per radius (the multilevel sparse steady-state LU dominates; faster BLAS does
  NOT help -- it is the sparse solve, not dense matmul). An 8-radius grid is ~2-3 h. Run
  detached, ideally with a numpy<2 / OpenBLAS venv:
      .venv-np1/bin/python src/engines/cloud_multilevel_union.py
  Writes union_grid.npz (saved after EACH radius, so a kill leaves partial results) and prints
  one line per radius (multilevel vs 3-level) then the dead-wall floor comparison.
"""
import os
import sys
import time
import warnings

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import qutip as qt
import eit_cooling_tool as eit
import cloud_cooling_tool as cc

# Engine outputs (union grids) go to outputs/, NOT the repo root (see .gitignore); created on demand.
_OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "outputs")
os.makedirs(_OUTDIR, exist_ok=True)

# --- operating point (matches the v17 dual_end preset + the cloud tool's geometry) -----------
DELTA, OMR, NF = 45.0, 0.12, 6
D2_FIXED = -0.10                              # field-convention dual on-axis delta2 (held fixed)
W0_UM = 19.0                                  # 1064 beam waist (cloud_cooling_tool default)
OREF = float(np.sqrt(4.0 * DELTA * cc.NU_Z0))   # on-axis total Rabi = the engine's pinned Omega_tot
RADII = np.array([0.0, 3.0, 6.0, 9.0, 12.0, 15.0, 18.0, 21.0])   # s = 1.0 .. ~0.09


def W_relaxfit(L, rho, NA, Nf, nss):
    """Near-equilibrium cooling rate W = -slope of ln(<n>-n_ss) from a thermal perturbation.
       IDENTICAL definition to cloud_cooling_tool.nss_and_W (apples-to-apples)."""
    from qutip.core.data import to as _to, CSR as _CSR
    from scipy.sparse.linalg import expm_multiply
    Lsc = _to(_CSR, L.data).as_scipy().tocsc()
    Nop = qt.tensor(qt.qeye(NA), qt.destroy(Nf).dag() * qt.destroy(Nf))
    Nbra = qt.operator_to_vector(Nop).dag().full().flatten()
    rho_hot = qt.tensor(rho.ptrace(0), qt.thermal_dm(Nf, nss + 0.15))
    v0 = qt.operator_to_vector(rho_hot).full().flatten()
    tt = np.linspace(0.0, 160.0, 10)
    traj = expm_multiply(Lsc, v0, start=tt[0], stop=tt[-1], num=len(tt), endpoint=True)
    y = np.real(traj @ Nbra) - nss
    m = (tt >= 40.0) & (y > 1e-5)
    return float(-np.polyfit(tt[m], np.log(y[m]), 1)[0]) if m.sum() >= 3 else 0.0


def _solve_radius(r, Nf):
    """Solve the headline coherent engine at radius r under the guided geometry -> (res, s, Deff).
       res is the full dict {nbar, L, NA, rho, ...}."""
    Deff, nu, eta, Otot, s = cc.radial_params(r, DELTA, W0_UM, OREF)
    # explicit dual_end Config (replicates eit.preset('dual_end')) + the radial overrides
    cfg = eit.Config(configuration="dual_end", Delta=Deff, OmR=OMR, beta="auto",
                     probe_order=1, repump_option="A", Omega_rep=3.0, Drep1=15.0, Drep2=5.0,
                     nu_z=nu, eta_z=eta, Omega_tot_abs=Otot,
                     delta2=D2_FIXED, servo_delta2=False, N_f=Nf)
    res = eit.run(cfg, Nf=Nf, full=True)
    return res, s, Deff


def multilevel_point(r, Nf=NF):
    """(n_ss, W, s, Delta_eff) from the headline coherent engine under the guided geometry."""
    res, s, Deff = _solve_radius(r, Nf)
    nss = float(res["nbar"])
    W = W_relaxfit(res["L"], res["rho"], res["NA"], Nf, nss)
    return nss, W, s, Deff


def two_rate_check(r, Nf=NF):
    """CLOSURE CHECK (Cuddy red-team point): confirm the multilevel relaxation is single-rate
       (early-rate ~= late-rate), validating the dead-wall closure d<n>/dt = -W(<n>-n_ss).

    The 3-level cold-start test that earned "freeze, not heat" ran on the 3-level engine; the
    MULTILEVEL adds F'1/F'3 internal modes, so a fast contaminant-driven transient would show
    as early-rate >> late-rate and break the single-rate assumption. We propagate from BOTH a
    hot (n_ss+0.30) and a cold (0.3*n_ss, below the floor) start and compare the early vs late
    slope of ln|<n>-n_ss|. early ~= late (both starts) => one dominant axial rate => closure holds.
    """
    from qutip.core.data import to as _to, CSR as _CSR
    from scipy.sparse.linalg import expm_multiply
    res, s, Deff = _solve_radius(r, Nf)
    L, rho, NA = res["L"], res["rho"], res["NA"]
    nss = float(res["nbar"])
    Lsc = _to(_CSR, L.data).as_scipy().tocsc()
    Nop = qt.tensor(qt.qeye(NA), qt.destroy(Nf).dag() * qt.destroy(Nf))
    Nbra = qt.operator_to_vector(Nop).dag().full().flatten()
    # AUTO-SCALE the window to ~4/W so the slow off-axis relaxation is actually resolved. A FIXED
    # window under-resolves it: at r=9, W~4e-5, a 0-400 window relaxes only 1.6% -> the early/late
    # slopes are fit-noise, not a measurement. The resolved fraction is printed so under-resolution
    # is never silent again. Run where W is large + the floor weight lives (r=0-3); deep dead-wall
    # radii (r>=6) have ~zero floor weight and a 1/W too large to propagate.
    West = W_relaxfit(L, rho, NA, Nf, nss)
    Tmax = 4.0 / West if (West and West > 0) else 400.0
    print("two-rate closure: r=%.1f Nf=%d s=%.3f n_ss=%.5f  W=%.2e  Tmax=%.0f (resolves %.0f%%)"
          % (r, Nf, s, nss, West, Tmax, 100.0 * (1.0 - np.exp(-min(West * Tmax, 50.0)))), flush=True)
    ok = True
    for label, n0 in [("hot", nss + 0.30), ("cold", max(nss * 0.3, 1e-4))]:
        rho0 = qt.tensor(rho.ptrace(0), qt.thermal_dm(Nf, n0))
        v0 = qt.operator_to_vector(rho0).full().flatten()
        tt = np.linspace(0.0, Tmax, 60)
        traj = expm_multiply(Lsc, v0, start=0.0, stop=Tmax, num=60, endpoint=True)
        y = np.abs(np.real(traj @ Nbra) - nss)

        def slope(lo, hi):
            m = (tt >= lo) & (tt <= hi) & (y > 1e-7)
            return float(-np.polyfit(tt[m], np.log(y[m]), 1)[0]) if m.sum() >= 3 else float('nan')
        early, late = slope(0.05 * Tmax, 0.35 * Tmax), slope(0.55 * Tmax, Tmax)
        ratio = early / late if (late and late == late) else float('nan')
        ok = ok and (late == late and abs(ratio - 1.0) < 0.30)
        print("  %-4s start n0=%.4f -> early-rate=%.3e  late-rate=%.3e  early/late=%.2f"
              % (label, n0, early, late, ratio), flush=True)
    print("  => single-rate closure %s (early~=late within 30%% on both starts)"
          % ("HOLDS" if ok else "CHECK -- multi-rate transient present"), flush=True)
    return ok


def nf_sweep(r, Nfs=(6, 8, 10)):
    """Nf-CONVERGENCE BOUND (Cuddy red-team point): the SHAPE/ratio is Nf-robust but the ABSOLUTE
       floor off an Nf=6 grid is the same underconverged proxy that reads 0.0048 vs 0.0059. Quote
       the corrected number: this prints n_ss(r), W(r) vs Nf so the Nf=6->converged gap is bounded
       (run at a couple of radii to confirm the correction is ~radius-flat -> the cloud/on-axis
       ratio carries the converged on-axis to a citable cloud floor without a full converged grid)."""
    import time
    print("Nf-convergence bound at r=%.1f:" % r, flush=True)
    t0 = time.time()
    for Nf in Nfs:
        nss, W, s, Deff = multilevel_point(r, Nf)
        print("  Nf=%-2d  n_ss=%.5f  W=%.5f   (%.0fs)" % (Nf, nss, W, time.time() - t0), flush=True)


def defang_check(r, Nf=NF):
    """ISOLATED F'1 de-fang at radius r (Cuddy red-team precision): n_ss with `with_e1` on vs off,
       per radius. The ML/3-level ratio (3.22->2.77->2.42 over r=0,3,6) SHOWS the de-fang but
       CONFLATES it with the other multilevel-clean-vs-proxy differences (the 8-ground recycle, the
       F'2 structure). This toggle is the clean F'1 increment; its off-axis/on-axis ratio is the
       isolated de-fang (cf. the analytic ~x0.81). Two solves per radius -- opt-in deliverable, NOT
       the floor path (the floor needs only n_ss(r), which carries F'1 regardless)."""
    Deff, nu, eta, Otot, s = cc.radial_params(r, DELTA, W0_UM, OREF)

    def nss_e1(flag):
        cfg = eit.Config(configuration="dual_end", Delta=Deff, OmR=OMR, beta="auto",
                         probe_order=1, repump_option="A", Omega_rep=3.0, Drep1=15.0, Drep2=5.0,
                         nu_z=nu, eta_z=eta, Omega_tot_abs=Otot,
                         delta2=D2_FIXED, servo_delta2=False, N_f=Nf, with_e1=flag)
        return float(eit.run(cfg, Nf=Nf)[0])
    n_on, n_off = nss_e1(True), nss_e1(False)
    print("  r=%.1f s=%.3f: n_ss(F'1 on)=%.5f  n_ss(F'1 off)=%.5f  F'1 increment=%.5f"
          % (r, s, n_on, n_off, n_on - n_off), flush=True)
    return n_on, n_off


DEADWALL_CASES = [('gaussian', 100.0, None), ('gaussian', 556.0, None),
                  ('box', 100.0, 14.0), ('box', 556.0, 14.0)]


def _floor(S, NSS, W, prof, T, rf):
    """Dead-wall MC cloud floor for one (profile, T_radial) case, given a radial grid."""
    kw = dict(profile=prof, T_radial_uK=T, Delta=DELTA, OmR=OMR)
    if rf is not None:
        kw['r_flat_um'] = rf
    return cc.run_mc(cc.Config(**kw), np.asarray(S), np.asarray(NSS), np.asarray(W))


def main(Nf=NF, npz=os.path.join(_OUTDIR, "union_grid.npz")):
    print("cloud x multilevel UNION -- headline coherent engine on the radial grid", flush=True)
    print("Delta=%.0f OmR=%.2f Nf=%d delta2=%.2f(fixed)  Oref=%.4f  w0=%.0fum"
          % (DELTA, OMR, Nf, D2_FIXED, OREF, W0_UM), flush=True)
    print("\n  r(um)  Deff    s       ML n_ss    ML W       3lvl n_ss  3lvl W     (elapsed)", flush=True)
    S, NSS, W, N3, W3 = [], [], [], [], []
    t0 = time.time()
    for r in RADII:
        try:
            nss, w, s, Deff = multilevel_point(float(r), Nf)
            n3, w3, _ = cc.nss_and_W(float(r), DELTA, OMR, W0_UM, OREF, Nf=16)
        except Exception as e:                          # one bad radius must not lose the rest
            print("  %5.1f  ERROR: %s" % (r, e), flush=True)
            continue
        S.append(s); NSS.append(nss); W.append(w); N3.append(n3); W3.append(w3)
        print("  %5.1f  %5.1f  %.4f  %.5f   %.5f   %.5f   %.5f   (%.0fs)"
              % (r, Deff, s, nss, w, n3, w3, time.time() - t0), flush=True)
        np.savez(npz, r=RADII[:len(S)], s=np.array(S), nss_ml=np.array(NSS),
                 W_ml=np.array(W), nss_3=np.array(N3), W_3=np.array(W3))
    S, NSS, W = np.array(S), np.array(NSS), np.array(W)
    N3, W3 = np.array(N3), np.array(W3)
    if len(S) < 2:
        print("\n(too few radii for the MC -- stopping)", flush=True)
        return

    print("\n=== dead-wall cloud floor: 3-level grid vs MULTILEVEL grid (identical MC) ===", flush=True)
    print("    on-axis: 3lvl n_ss=%.5f   ML n_ss=%.5f" % (N3[0], NSS[0]), flush=True)
    for prof, T, rf in DEADWALL_CASES:
        f_ml = _floor(S, NSS, W, prof, T, rf)
        f_3 = _floor(S, N3, W3, prof, T, rf)
        tag = ('r_flat=%g' % rf) if rf is not None else ''
        print("  %-9s T=%4.0fuK %-10s: 3lvl=%.5f   ML=%.5f" % (prof, T, tag, f_3, f_ml), flush=True)
    print("\nDONE  (saved %s)" % npz, flush=True)


def compare(npz6=os.path.join(_OUTDIR, "union_grid.npz"), npz8=os.path.join(_OUTDIR, "union_grid_nf8.npz")):
    """CITABLE-NUMBER TEST (Cuddy red-team): the Nf=6->converged correction that would license the
       Mac-derivable shortcut is a property of the W-WEIGHTED FLOOR, not a single per-radius n_ss --
       so test the FLOOR directly across two Nf grids. The hot (556uK) row is decisive: it puts the
       most weight off-axis, where the high-n_ss points (worst Nf=6 truncation) sit, AND is where
       the 'dead-wall collapses for all T_r' claim is most stressed. Small drift there => the citable
       floor is Mac-grade; large drift => genuine cluster case (and the dead-wall claim has an Nf
       component worth knowing before the thesis)."""
    d6, d8 = np.load(npz6), np.load(npz8)
    print("=== citable-number test: dead-wall floor, Nf=6 grid vs Nf=8 grid ===", flush=True)
    print("  (the hot 556uK row is decisive; small drift => Mac-citable)", flush=True)
    for prof, T, rf in DEADWALL_CASES:
        f6 = _floor(d6['s'], d6['nss_ml'], d6['W_ml'], prof, T, rf)
        f8 = _floor(d8['s'], d8['nss_ml'], d8['W_ml'], prof, T, rf)
        drift = (f8 / f6 - 1.0) * 100 if f6 else float('nan')
        tag = ('r_flat=%g' % rf) if rf is not None else ''
        print("  %-9s T=%4.0fuK %-10s: Nf6=%.5f  Nf8=%.5f  drift=%+.1f%%"
              % (prof, T, tag, f6, f8, drift), flush=True)
    print("  on-axis n_ss: Nf6=%.5f  Nf8=%.5f  (%+.1f%% reference)"
          % (d6['nss_ml'][0], d8['nss_ml'][0], (d8['nss_ml'][0] / d6['nss_ml'][0] - 1.0) * 100), flush=True)


if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) >= 2 else ""
    if mode == "closure" and len(sys.argv) >= 3:
        two_rate_check(float(sys.argv[2]))            # `... closure 9`  single-rate closure check
    elif mode == "nf" and len(sys.argv) >= 3:
        nf_sweep(float(sys.argv[2]))                  # `... nf 9`       per-radius Nf bound (sanity)
    elif mode == "defang" and len(sys.argv) >= 3:
        defang_check(float(sys.argv[2]))              # `... defang 9`   isolated F'1 increment (opt-in)
    elif mode == "grid8":
        main(Nf=8, npz=os.path.join(_OUTDIR, "union_grid_nf8.npz"))   # `... grid8`  Nf=8 grid (for compare)
    elif mode == "compare":
        compare()                                     # `... compare`    citable-number floor test
    else:
        main()                                        # default: the full Nf=6 grid + dead-wall MC
