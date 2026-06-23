"""
fig_radial_efficiency.py  --  The dead-wall: cooling rate W(r) collapses off-axis
while the local floor n_ss(r) climbs, so off-axis atoms FREEZE cold rather than
equilibrate to the warm n_ss. This is the mechanism behind the flat-top cloud
collapse (Guide Ch 06, master Section 8).

DATA PROVENANCE: the multilevel n_ss(r), W(r) below are the output of
    python src/engines/cloud_multilevel_union.py grid       # -> union_grid.npz (Nf=6)
(the headline coherent eit_cooling_tool engine on the radial grid; W is the
relaxation-fit rate, identical to cloud_cooling_tool.nss_and_W). They are baked
in as literals because the grid .npz is gitignored (regenerated, not shipped)
and recomputing it is the ~hours multilevel solve. The SHAPE shown here is
Nf-robust; the high-r n_ss magnitude is a non-converged lower bound (INDEX 1b).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- union_grid.npz (Nf=6), multilevel engine -------------------------------
r      = np.array([0.0, 3.0, 6.0, 9.0, 12.0, 15.0, 18.0, 21.0])
nss_ml = np.array([0.0057, 0.0118, 0.0736, 0.2711, 0.656, 1.1518, 1.538, 1.4835])
W_ml   = np.array([3.6068e-3, 1.3264e-3, 1.6792e-4, 4.0932e-5, 1.6795e-5, 0.0, 0.0, 0.0])

Wfloor = 8e-6                       # plot floor for the "W below resolution -> 0" points
Wp = np.where(W_ml > 0, W_ml, Wfloor)
nz = W_ml > 0                       # radii with a resolvable rate
ratio = W_ml[0] / W_ml[4]          # r=0 -> r=12 collapse

fig, axL = plt.subplots(figsize=(9.2, 5.6))
axR = axL.twinx()

# cooling rate W(r) (left, log) -- collapses
lW, = axL.plot(r[nz], Wp[nz], "o-", color="#1565c0", lw=2.4, ms=7, zorder=4,
               label=r"cooling rate $W(r)$")
axL.plot(r[~nz], Wp[~nz], "v", color="#1565c0", ms=8, alpha=0.5, zorder=4)   # W->0 markers
axL.set_yscale("log")
axL.set_ylabel(r"cooling rate  $W(r)$  (2$\pi$·MHz)", color="#1565c0", fontsize=11)
axL.tick_params(axis="y", labelcolor="#1565c0")
axL.set_ylim(5e-6, 6e-3)

# local floor n_ss(r) (right, log) -- climbs
lN, = axR.plot(r, nss_ml, "s-", color="#c0392b", lw=2.4, ms=7, zorder=4,
               label=r"local floor $n_{\rm ss}(r)$")
axR.axhline(1.0, color="#c0392b", lw=0.8, ls=":", alpha=0.5)
axR.set_yscale("log")
axR.set_ylabel(r"local steady-state floor  $n_{\rm ss}(r)$", color="#c0392b", fontsize=11)
axR.tick_params(axis="y", labelcolor="#c0392b")
axR.set_ylim(3e-3, 3.0)

# the dead-wall zone (W collapsed)
axL.axvspan(13.5, 21.5, color="#bbbbbb", alpha=0.18, zorder=0)
axL.text(17.3, 2.2e-3, "dead wall\n$W\\to0$:\natoms freeze\n(don't reach $n_{\\rm ss}$)",
         fontsize=9.0, color="#555", ha="center", va="center")

# annotate the collapse
axL.annotate(f"$W$ collapses ~{ratio:.0f}× by r=12 µm",
             xy=(12, W_ml[4]), xytext=(5.2, 3.0e-5),
             fontsize=9.5, color="#1565c0",
             arrowprops=dict(arrowstyle="->", color="#1565c0", lw=1.0))
axR.annotate(r"$n_{\rm ss}$ would be warm off-axis…",
             xy=(12, nss_ml[4]), xytext=(2.0, 0.9),
             fontsize=9.5, color="#c0392b",
             arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.0))

axL.set_xlabel("radius  r  (µm)", fontsize=11)
axL.set_xlim(-0.7, 21.7)
axL.set_title("The dead-wall mechanism — off-axis the cooling rate collapses faster than the floor climbs\n"
              "(multilevel engine, Nf=6 shape; high-r $n_{\\rm ss}$ is a non-converged lower bound — INDEX §1b)",
              fontsize=11, pad=10)
axL.legend([lW, lN], [lW.get_label(), lN.get_label()], loc="lower left",
           fontsize=9.5, frameon=True, framealpha=0.9)
for s in ("top",):
    axL.spines[s].set_visible(False)
plt.tight_layout()
plt.savefig("fig_radial_efficiency.png", dpi=150, bbox_inches="tight")
print("wrote fig_radial_efficiency.png  (W collapse %.0fx r=0->12)" % ratio)
