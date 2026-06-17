"""
fig_retro_flatness.py  --  THE counterintuitive result: with a large AOM tag
(2fA = 400 MHz) the cooling floor is essentially INDEPENDENT of the retro
mirror reflectivity eta_dp, because the rejected (non-resonant) return fields
are pushed far off every D2 line.  With a small tag (2fA = 160 MHz) the
rejected forward-probe scatter (~ 1/eta_dp, only 160 MHz detuned) reheats the
dark state as eta_dp drops.  Floor is optimized over delta2 at each point.

Engine: ../src/tagged_solver.py (legs='swapped').
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import tagged_solver as ts

Delta, OmR, Nf = 45.0, 0.12, 14
eta_dp = np.array([0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50])
d2grid = np.linspace(0.10, 0.40, 7)   # fine enough to hit the +0.25 optimum

def floor_opt(twofA, e):
    n, _, _ = ts.d2min(d2grid, Delta=Delta, twofA=twofA, eta_dp=e,
                       OmR=OmR, Nf=Nf, legs="swapped")
    return n

print("computing floor(eta_dp) for 2fA = 400 and 160 ...")
f400 = np.array([floor_opt(400.0, e) for e in eta_dp])
f160 = np.array([floor_opt(160.0, e) for e in eta_dp])
for e, a, b in zip(eta_dp, f400, f160):
    print("  eta_dp=%.2f :  2fA=400 -> %.4f    2fA=160 -> %.4f" % (e, a, b))

fig, ax = plt.subplots(figsize=(8.2, 5.2))
ax.plot(eta_dp, f400, "o-", ms=7, lw=2.4, color="#1565c0",
        label=r"$2f_A=400$ MHz (adopted)  $-$  flat")
ax.plot(eta_dp, f160, "s--", ms=7, lw=2.0, color="#c0392b",
        label=r"$2f_A=160$ MHz  $-$  reheats at low reflectivity")
ax.axhspan(0.0, 0.006, color="#eafaf0", zorder=0)
ax.text(0.205, 0.0065, "$\\langle n_z\\rangle \\lesssim 0.006$ target band",
        fontsize=8.5, color="#2e7d32", va="bottom")

ax.set_xlabel(r"retro double-pass reflectivity  $\eta_{dp}$", fontsize=12)
ax.set_ylabel(r"axial floor  $\langle n_z\rangle$  (optimized over $\delta_2$)",
              fontsize=12)
ax.set_title("Large AOM tag makes the floor insensitive to retro reflectivity\n"
             r"($\Delta=45$, $\Omega_p/\Omega_c=0.12$, $\nu_z=2\pi\times430$ kHz)",
             fontsize=12.5)
ax.set_ylim(0, max(f160.max(), 0.02) * 1.15)
ax.legend(fontsize=10, loc="upper right", framealpha=0.95)
ax.grid(alpha=0.25)
plt.tight_layout()
plt.savefig("fig_retro_flatness.png", dpi=150, bbox_inches="tight")
print("wrote fig_retro_flatness.png")
