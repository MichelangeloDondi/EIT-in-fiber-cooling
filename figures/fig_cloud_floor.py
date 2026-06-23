"""
fig_cloud_floor.py  --  Cloud-averaged axial floor vs radial temperature.

The radial mode is shallow (nu_r ~ 5.4 kHz, NOT resolved-sideband), so the
cloud samples a spread of radial positions -> a spread of light shift and
two-photon detuning.  The field-insensitive dark pair keeps the cloud dark, so
the residual floor rise with radial T is modest (recoil/inhomogeneity-limited),
not catastrophic.  Curves: Boltzmann-column-averaged floor and an independent
Monte-Carlo trajectory floor; single-atom (turning-point) floor for reference.

Engine: ../src/engines/radial_floor_mc.py  (Dc0 = 45 cooling-rate grid; U0 = 1094 uK,
w_L = 19 um).
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "engines"))
import radial_floor_mc as rmc

n_g = rmc.d["n45"]; W_g = rmc.d["W45"]      # v14 operating cooling-rate grid
Ts = np.array([20, 40, 60, 80, 100, 120, 150], float)

frozen, floor_avg, mc_traj = [], [], []
for T in Ts:
    fr, fl, ra = rmc.spatial_avgs(n_g, W_g, T)
    _, m = rmc.mc_floor(n_g, W_g, T)
    frozen.append(fr); floor_avg.append(fl); mc_traj.append(m)
    print("T=%3duK : frozen=%.4f  column-avg=%.4f  MC=%.4f" % (T, fr, fl, m))
frozen = np.array(frozen); floor_avg = np.array(floor_avg); mc_traj = np.array(mc_traj)

i100 = int(np.where(Ts == 100)[0][0])

fig, ax = plt.subplots(figsize=(8.2, 5.2))
ax.plot(Ts, floor_avg, "o-", ms=6.5, lw=2.4, color="#1565c0",
        label="cloud floor (Boltzmann-column average)")
ax.plot(Ts, mc_traj, "^--", ms=6.5, lw=1.8, color="#7b2cbf",
        label="cloud floor (Monte-Carlo trajectory)")
ax.plot(Ts, frozen, "s:", ms=5.5, lw=1.6, color="#9aa0a6",
        label="single-atom floor (turning-point avg)")

ax.axvline(100, color="#c0392b", lw=0.9, ls="--", alpha=0.7)
ax.plot([100], [mc_traj[i100]], "*", ms=16, color="#c0392b", zorder=6)
ax.annotate("$100\\,\\mu$K:  MC $%.3f$,\nstatic-column $%.3f$"
            % (mc_traj[i100], floor_avg[i100]),
            xy=(100, mc_traj[i100]), xytext=(38, mc_traj[i100] + 0.014),
            fontsize=9.5, color="#c0392b",
            arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.0))

ax.set_xlabel(r"radial temperature  $T_r$  ($\mu$K)", fontsize=12)
ax.set_ylabel(r"axial floor  $\langle n_z\rangle$", fontsize=12)
ax.set_title("Cloud floor vs radial temperature  $-$  field-insensitive pair\n"
             r"keeps the rise modest (recoil/inhomogeneity-limited)", fontsize=12.5)
ax.set_ylim(0, max(floor_avg.max(), mc_traj.max()) * 1.2)
ax.legend(fontsize=9.5, loc="upper left", framealpha=0.95)
ax.grid(alpha=0.25)
plt.tight_layout()
plt.savefig("fig_cloud_floor.png", dpi=150, bbox_inches="tight")
print("wrote fig_cloud_floor.png")
