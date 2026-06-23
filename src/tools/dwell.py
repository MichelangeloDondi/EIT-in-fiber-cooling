"""Measure clk2's physical F'=1 repump dwell -> decide low- vs high-dwell regime.
   ANTITRAP_RESOLUTION thresholds: low-dwell P_e_rep ~ 4e-5 -> anti-trap ~0.01;
   high-dwell ~3.5e-4 -> ~0.03-0.05. F'=2 residual should be ~4e-5 (dark-state, sanity)."""
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "engines"))
import clk2 as m
# config A (settled), validated full floor ~0.0048; defaults Dc=80, Drep1=30, Drep2=5, OmR=0.25
for Nf in (8, 10):
    nbar, conf, pops, (peF1, peF2) = m.solve(option='A', Dc=80.0, Nf=Nf, want_pops=True)
    print("Nf=%2d  nbar=%.5f  frame_conf=%.1e  |  P_e(F'1 repump dwell)=%.3e  P_e(F'2 cooling residual)=%.3e"
          % (Nf, nbar, conf, peF1, peF2))
print()
print("gate: nbar ~ 0.0048 (validated config-A full floor)")
print("verdict: F'1 dwell vs thresholds  low~4e-5 / high~3.5e-4")
