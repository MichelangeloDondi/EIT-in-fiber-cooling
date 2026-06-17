#!/usr/bin/env python3
"""
audit/check.py  --  repository consistency gate.

Run from the repo root:   python3 audit/check.py

HARD checks (exit code 1 on any failure) -- these define a self-consistent repo:
  * the SSOT (src/operating_point.py) is internally consistent
  * the validated engine reproduces its documented anchors
  * no superseded operating point survives in code presets
  * the master doc carries no stale floor numbers
  * the README headlines the all-in floor, not the bare solve floor

SOFT checks (reported, non-fatal) -- the remaining reconciliation sweep, tracked
so it can be closed file-by-file without blocking.
"""
import os, sys, re, glob, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "src")
DOCS = os.path.join(ROOT, "docs")
sys.path.insert(0, SRC)
SLOW = "--slow" in sys.argv

fails, warns = [], []
def check(name, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + name + (("\n          " + detail) if (detail and not ok) else ""))
    if not ok:
        fails.append(name)

def soft(name, hits):
    if hits:
        print("  TODO  %s  (%d)" % (name, len(hits)))
        for h in hits[:12]:
            print("          " + h)
        warns.append(name)
    else:
        print("  ok    %s" % name)

def scan(paths, pattern, exempt=()):
    rx = re.compile(pattern)
    ex = [re.compile(e) for e in exempt]
    out = []
    for f in paths:
        for i, l in enumerate(open(f, encoding="utf-8", errors="ignore"), 1):
            if rx.search(l) and not any(e.search(l) for e in ex):
                out.append("%s:%d  %s" % (os.path.relpath(f, ROOT), i, l.strip()[:90]))
    return out

print("=" * 72)
print(" REPOSITORY CONSISTENCY GATE")
print("=" * 72)

# ---------- 1. SSOT internal consistency ----------
print("\n[1] SSOT self-consistency")
import operating_point as op
fb, P = op.FLOOR, op.OP
check("all_in[0] = solve_dual + increment_lo",
      abs(fb.all_in_single_atom[0] - (fb.solve_dual_end + fb.antitrap_leak_increment[0])) < 1e-9)
check("OmR = Omega_p / Omega_c",
      abs(P.OmR - P.Omega_p_MHz / P.Omega_c_MHz) < 0.01,
      "OmR=%.3f vs ratio=%.3f" % (P.OmR, P.Omega_p_MHz / P.Omega_c_MHz))
check("eta_em = eta_780/sqrt(3)", abs(op.ETA_EM - op.ETA_780 / 3 ** 0.5) < 1e-9)
check("axial_recoil_bound = eta_em^2", abs(fb.axial_recoil_bound - round(op.ETA_EM ** 2, 4)) < 1e-9)
check("radial n(100uK) ~ 384 (units sane)", abs(op.n_radial(100.0) - 384) < 5,
      "got %.1f" % op.n_radial(100.0))

# ---------- 2. engine <-> SSOT constant agreement (fast) + optional full solve ----------
print("\n[2] engine constants vs SSOT" + ("  (+ full regression via --slow)" if SLOW else "  (fast; pass --slow for the solve)"))
def engine_constants():
    """Read tagged_solver's constants; fall back to regex if qutip isn't installed (CI)."""
    try:
        import tagged_solver as ts
        return dict(GAMMA=ts.GAMMA, NU=ts.NU, ETA=ts.ETA, F3=ts.F3), "import"
    except Exception:
        src = open(os.path.join(SRC, "tagged_solver.py"), encoding="utf-8", errors="ignore").read()
        m = re.search(r"GAMMA,\s*NU,\s*ETA\s*=\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)", src)
        f = re.search(r"\bF3\s*=\s*([\d.]+)", src)
        return dict(GAMMA=float(m.group(1)), NU=float(m.group(2)),
                    ETA=float(m.group(3)), F3=float(f.group(1))), "regex (qutip absent)"
ec, how = engine_constants()
print("        constants read via %s" % how)
check("tagged_solver GAMMA == SSOT D2 linewidth", ec["GAMMA"] == op.GAMMA_D2_MHZ, "%s vs %s" % (ec["GAMMA"], op.GAMMA_D2_MHZ))
check("tagged_solver NU == SSOT nu_z",            ec["NU"] == op.NU_Z_MHZ,        "%s vs %s" % (ec["NU"], op.NU_Z_MHZ))
check("tagged_solver ETA == SSOT eta_780",        ec["ETA"] == op.ETA_780,        "%s vs %s" % (ec["ETA"], op.ETA_780))
check("tagged_solver F3 == SSOT F3-above-F2",     ec["F3"] == op.F3_ABOVE_F2_MHZ, "%s vs %s" % (ec["F3"], op.F3_ABOVE_F2_MHZ))
if SLOW:
    try:
        r = subprocess.run([sys.executable, os.path.join(SRC, "tagged_solver.py")],
                           cwd=SRC, capture_output=True, text=True, timeout=600)
        tail = (r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "nonzero exit")
        check("tagged_solver full self-test (anchors 0.0034/0.0085)", r.returncode == 0, tail)
    except subprocess.TimeoutExpired:
        check("tagged_solver full self-test", False, "timed out >600s -- needs a fast-regression mode")

# ---------- 3. HARD stale-value checks ----------
print("\n[3] HARD: no superseded values in code / master doc")
tool = [f for f in glob.glob(os.path.join(SRC, "*.py")) if os.path.basename(f) != "operating_point.py"]
stale_presets = scan(tool, r"Delta\s*=\s*55(\.0)?\b", exempt=(r"#",))
stale_presets = [h for h in stale_presets if "Config(" in h or "preset" in h.lower()]
check("no Delta=55 in code Config presets", len(stale_presets) == 0, "; ".join(stale_presets))

cons = [os.path.join(DOCS, "clock_EIT_consolidated.md")]
check("master doc: no stale single-ended 0.0092",
      len(scan(cons, r"0\.0092")) == 0, "; ".join(scan(cons, r"0\.0092")))
check("master doc: no 0.0085 mislabeled as cloud floor",
      len(scan(cons, r"0\.0085\s*\(.?\u0394?=?45")) == 0,
      "; ".join(scan(cons, r"0\.0085\s*\(")))
check("master doc: operating point not stated as Delta=55, OmR=0.10",
      len(scan(cons, r"\u0394=55,\s*OmR=0\.10")) == 0,
      "; ".join(scan(cons, r"\u0394=55,\s*OmR=0\.10")))

readme = os.path.join(ROOT, "README.md")
allin_lo = "%.3f" % fb.all_in_single_atom[0]
has_allin = (os.path.exists(readme) and
             (allin_lo in open(readme, encoding="utf-8", errors="ignore").read()
              or "all-in" in open(readme, encoding="utf-8", errors="ignore").read().lower()))
check("README headlines the all-in floor (%s..%.3f)" % (allin_lo, fb.all_in_single_atom[1]), has_allin)

# ---------- 4. SOFT reconciliation sweep ----------
print("\n[4] SOFT: remaining reconciliation sweep (non-fatal)")
prose = [f for f in glob.glob(os.path.join(DOCS, "*.md"))]
hist = (r"was\b", r"stale", r"abandon", r"superseded", r"legacy", r"historical",
        r"earlier", r"\bv9\b", r"\bv1[0-3]\b", r"memo", r"~55 MHz", r"55.80", r"40.55",
        r"reference", r"scan at")
soft("docs still stating Delta=55 / OmR=0.10 operating point",
     scan(prose, r"\u0394\s*=?\s*55|Delta\s*=\s*55|OmR\s*=\s*0\.10", exempt=hist))
soft("docs with negative delta2 set-point (sign convention)",
     scan(prose, r"\u03b4\u2082[^.]{0,30}[\u2212-]0\.(1[0-9]|2[0-9])", exempt=hist))

# ---------- verdict ----------
print("\n" + "=" * 72)
if fails:
    print(" RESULT: FAIL  (%d hard check(s))  -- %s" % (len(fails), "; ".join(fails)))
    print("=" * 72)
    sys.exit(1)
print(" RESULT: PASS" + ("  (%d soft TODO group(s) remain)" % len(warns) if warns else ""))
print("=" * 72)
sys.exit(0)
