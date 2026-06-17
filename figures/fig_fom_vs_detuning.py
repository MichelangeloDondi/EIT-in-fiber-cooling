"""
fig_fom_vs_detuning.py -- Paper T Fig. 3.

The coherence-per-scatter FoM vs Raman detuning. The Dm=2 clock Raman (rank-2 limited) is
FLAT at ~5.6 -- you cannot detune out of trouble -- while an allowed Raman improves as
Delta/Gamma. Neither helps the Dm=2 case reach the FoM ~ 170 needed for ground-state cooling.

Curve and constants come from the verified core (src/paper_T_fom.py); stdlib + matplotlib only.
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import paper_T_fom as pt

GHZ = 1000.0
D_GHz = np.logspace(np.log10(0.5), np.log10(100.0), 300)
D_MHz = D_GHz * GHZ

fom_dm2     = np.array([pt.FoM(D) for D in D_MHz])          # computed, rank-2 limited
fom_allowed = D_MHz / pt.GAMMA                              # canonical allowed scaling, FoM ~ Delta/Gamma
THRESH = 170.0                                             # FoM needed for n_bar ~ 0.01 (rsc_floor_rate_eqn.py)

fig, ax = plt.subplots(figsize=(7.2, 5.0))
ax.loglog(D_GHz, fom_allowed, color="#9aa7b4", lw=2.2, ls="--",
          label=r"allowed Raman  $\propto\ \Delta/\Gamma$  (improvable)")
ax.loglog(D_GHz, fom_dm2, color="#b5341e", lw=3.0,
          label=r"$\Delta m{=}2$ clock Raman (rank-2 limited)")

# disqualification threshold
ax.axhline(THRESH, color="#1f6f4a", lw=1.6, ls=":")
ax.text(0.62, THRESH*1.15, r"FoM needed for ground-state cooling ($\bar n\lesssim0.01$)",
        color="#1f6f4a", fontsize=10, va="bottom")
# the pinned plateau
ax.axhline(pt.FOM_INF, color="#b5341e", lw=0.9, ls="-", alpha=0.35)
ax.text(60, pt.FOM_INF*0.62, r"FoM $\to %.1f$" % pt.FOM_INF, color="#b5341e",
        fontsize=10, ha="right", va="top")

# shaded "disqualified" band for the Dm=2 case
ax.axhspan(1e-2, THRESH, color="#b5341e", alpha=0.05)

ax.annotate("detuning does not help:\nsignal and scatter both fall as $1/\\Delta^2$",
            xy=(8, pt.FoM(8*GHZ)), xytext=(1.3, 0.9),
            fontsize=9.5, color="#7a241a",
            arrowprops=dict(arrowstyle="->", color="#7a241a", lw=1.2))

ax.set_xlabel(r"Raman one-photon detuning  $\Delta$  (GHz)", fontsize=12)
ax.set_ylabel(r"coherence per scattered photon,  FoM", fontsize=12)
ax.set_title(r"Why $\Delta m{=}2$ clock-qubit Raman cannot be detuned out of the rank-2 obstruction",
             fontsize=11.5)
ax.set_xlim(0.5, 100)
ax.set_ylim(3e-1, 3e4)
ax.grid(True, which="both", alpha=0.18)
ax.legend(loc="upper left", fontsize=10.5, framealpha=0.95)
fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fig_fom_vs_detuning.png")
fig.savefig(out, dpi=150)
print("wrote", out)
print("FoM(Delta=1 GHz)=%.2f  FoM(30 GHz)=%.2f  plateau=%.2f  (flat); allowed crosses %g at Delta=%.2f GHz"
      % (pt.FoM(1*GHZ), pt.FoM(30*GHZ), pt.FOM_INF, THRESH, THRESH*pt.GAMMA/GHZ))
