"""
fig_thermometry.py  --  Asymmetric-sideband (Raman) thermometry for the m'=0
clock pair |1,-1> <-> |2,+1>, at the v14 operating floor n_bar ~ 0.005.

Panel A : the spectrum.  A sideband-pi probe drives the blue sideband (n->n+1,
          delta=+1) to near-full transfer while the red sideband (n->n-1,
          delta=-1) is starved (needs n>=1).  The red/blue area ratio
          R = A_red/A_blue gives <n> = R/(1-R) directly.  Log-y so the tiny red
          peak is visible; the carrier-only "pedestal" (Blackman-shaped) shows
          how little carrier leaks onto the sidebands.
Panel B : calibration.  Inferred <n> vs true <n>.  The raw ratio is biased high
          at the floor (the carrier wing contaminates the tiny red signal); the
          pedestal-subtracted estimate recovers the diagonal.

Engine: ../src/thermometry.py  (validated coherent core; ETA_R=0.187,
nu_z=2pi x 430 kHz).
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import thermometry as th

NBAR = 0.0048          # v14 operating floor (matches the tagged-solver landscape)

# -------- Panel A: spectrum at the floor --------
NfA, s = 18, 0.12
_, _, ncol, D = th.make_ops(NfA, th.ETA_R)
popsA = th.thermal_pops(NBAR, NfA)
Tsb = th._Tpulse(s, "sideband")
dels = np.linspace(-1.6, 1.6, 170)
print("computing sideband spectrum (Blackman) ...")
Pe = np.array([th._Pe(d, s, Tsb, NfA, ncol, D, popsA, shape="blackman", M=70)
               for d in dels])
ped = np.array([th._Pe(d, s, Tsb, NfA, ncol, D, popsA, shape="blackman",
                       carrier_only=True, M=70) for d in dels])
m = th.measure(NBAR, s=s, Nf=22, shape="blackman", probe="sideband")
print("  A_red=%.4e  A_blue=%.4e  R=%.4e  n_sub=%.4f"
      % (m["Ar"], m["Ab"], m["R_raw"], m["n_sub"]))

# -------- Panel B: calibration --------
n_in = np.logspace(np.log10(0.004), np.log10(0.5), 11)
n_raw, n_sub = [], []
for nb in n_in:
    mm = th.measure(nb, s=0.10, Nf=24, shape="square", probe="sideband")
    n_raw.append(mm["n_raw"]); n_sub.append(mm["n_sub"])
n_raw = np.array(n_raw); n_sub = np.array(n_sub)

fig, (axA, axB) = plt.subplots(1, 2, figsize=(12.4, 5.0))

# Panel A
axA.set_yscale("log")
axA.plot(dels, np.clip(Pe, 1e-6, None), color="#1565c0", lw=2.0,
         label="full pulse  $P_e(\\delta)$")
axA.plot(dels, np.clip(ped, 1e-6, None), color="#9467bd", lw=1.3, ls="--",
         label="carrier-only pedestal")
axA.axvline(+1, color="#1565c0", lw=0.7, ls=":")
axA.axvline(-1, color="#c0392b", lw=0.7, ls=":")
axA.annotate("blue SB\n$A_{blue}=%.2f$" % m["Ab"], xy=(1, m["Ab"]),
             xytext=(1.05, 0.30), fontsize=9, color="#1565c0", ha="left",
             arrowprops=dict(arrowstyle="->", color="#1565c0", lw=0.9))
axA.annotate("red SB (starved)\n$A_{red}=%.1e$" % m["Ar"], xy=(-1, m["Ar"]),
             xytext=(-1.55, 2e-3), fontsize=9, color="#c0392b", ha="left",
             arrowprops=dict(arrowstyle="->", color="#c0392b", lw=0.9))
axA.text(0.0, 4e-5, "carrier\n($\\delta=0$)", fontsize=8.5, color="#666",
         ha="center", va="bottom")
axA.set_ylim(1e-5, 2.0)
axA.set_xlabel(r"two-photon detuning  $\delta/\nu_z$", fontsize=11.5)
axA.set_ylabel(r"excited population  $P_e$", fontsize=11.5)
axA.set_title("(A)  Sideband spectrum at $\\bar n=%.4f$\n"
              "$R=A_{red}/A_{blue}\\Rightarrow\\bar n_{meas}=%.4f$"
              % (NBAR, m["n_sub"]), fontsize=11.5)
axA.legend(fontsize=9, loc="upper left", framealpha=0.95)
axA.grid(alpha=0.25, which="both")

# Panel B
axB.set_xscale("log"); axB.set_yscale("log")
lo, hi = 3e-3, 6e-1
axB.plot([lo, hi], [lo, hi], color="#999", lw=1.2, ls="--", label="ideal (truth)")
axB.plot(n_in, n_raw, "o-", ms=6, color="#c0392b", lw=1.8,
         label="raw ratio  $R/(1-R)$  (biased at floor)")
axB.plot(n_in, n_sub, "s-", ms=6, color="#0b6e4f", lw=2.0,
         label="pedestal-subtracted (recovers truth)")
axB.axvline(NBAR, color="#1565c0", lw=0.8, ls=":")
axB.text(NBAR * 1.07, 0.30, "operating\nfloor", fontsize=8.5, color="#1565c0",
         va="top")
axB.set_xlim(lo, hi); axB.set_ylim(lo, hi)
axB.set_xlabel(r"true  $\bar n$", fontsize=11.5)
axB.set_ylabel(r"inferred  $\bar n_{meas}$", fontsize=11.5)
axB.set_title("(B)  Calibration: subtraction removes the\ncarrier-wing bias at the floor",
              fontsize=11.5)
axB.legend(fontsize=8.8, loc="upper left", framealpha=0.95)
axB.grid(alpha=0.25, which="both")

plt.tight_layout()
plt.savefig("fig_thermometry.png", dpi=150, bbox_inches="tight")
print("wrote fig_thermometry.png")
