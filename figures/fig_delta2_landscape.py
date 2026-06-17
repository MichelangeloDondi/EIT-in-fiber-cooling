"""
fig_delta2_landscape.py  --  Axial floor <n_z> vs two-photon detuning delta2,
computed from the validated QuTiP tagged steady-state solver at the v14
operating point.  Shows the EIT cooling resonance and the servo set-point
(the e3 admixture Stark-shifts g2 by ~ -0.2 MHz, so the optimum sits at a
small POSITIVE delta2 offset, not at 0).

Engine: ../src/tagged_solver.py  (legs='swapped' = adopted; e3 + rejected
tagged fields included).
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import tagged_solver as ts

# ---- v14 operating point ----
Delta, OmR, twofA, eta_dp, Nf = 45.0, 0.12, 400.0, 0.30, 14

d2 = np.linspace(-0.6, 0.9, 31)
full = np.array([ts.solve(Delta=Delta, twofA=twofA, eta_dp=eta_dp, d2=x,
                          OmR=OmR, Nf=Nf, legs="swapped") for x in d2])
# clean reference (no rejected tagged fields): the intrinsic EIT floor
clean = np.array([ts.solve(Delta=Delta, twofA=twofA, eta_dp=eta_dp, d2=x,
                           OmR=OmR, Nf=Nf, legs="swapped",
                           with_rejected=False) for x in d2])

imin = int(np.argmin(full)); d2_opt, f_opt = d2[imin], full[imin]
jmin = int(np.argmin(clean)); f_clean = clean[jmin]
print("operating delta2 = %+.3f MHz   floor(full) = %.4f   floor(clean) = %.4f"
      % (d2_opt, f_opt, f_clean))

fig, ax = plt.subplots(figsize=(8.8, 5.3))
ax.set_yscale("log")
ax.plot(d2, clean, "o-", ms=4, color="#9aa0a6", lw=1.6,
        label="intrinsic EIT (F'=2 + F'=1 + F'=3 coherent)")
ax.plot(d2, full, "o-", ms=4.5, color="#1565c0", lw=2.2,
        label=r"with tagged rejected fields ($2f_A=400$, $\eta_{dp}=0.30$)")
ax.set_ylim(3e-3, 3e1)

# cooling / heating guide
ax.axvspan(d2[0], -0.18, color="#fdecea", alpha=0.7, zorder=0)
ax.text(-0.42, 9.0, "heating\n(red of resonance)", fontsize=9, color="#c0392b",
        ha="center", va="center")
ax.text(0.45, 9.0, "cooling band", fontsize=9.5, color="#1565c0", ha="center", va="center")

# operating point
ax.axvline(d2_opt, color="#c0392b", lw=1.0, ls="--")
ax.axhline(f_opt, color="#c0392b", lw=0.7, ls=":", alpha=0.6)
ax.plot([d2_opt], [f_opt], "*", ms=17, color="#c0392b", zorder=6)
ax.annotate("servo set-point\n$\\delta_2=%+.2f$ MHz\n$\\langle n_z\\rangle=%.4f$"
            % (d2_opt, f_opt), xy=(d2_opt, f_opt),
            xytext=(d2_opt + 0.07, 0.018), fontsize=9.5, color="#c0392b",
            ha="left", arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.0))

ax.set_xlabel(r"two-photon detuning  $\delta_2$  (MHz)", fontsize=12)
ax.set_ylabel(r"steady-state axial $\langle n_z\rangle$", fontsize=12)
ax.set_title("EIT cooling resonance from the validated tagged solver\n"
             r"($\Delta=45$, $\Omega_p/\Omega_c=0.12$, $2f_A=400$, $\nu_z=2\pi\times430$ kHz)",
             fontsize=12.5)
ax.legend(fontsize=9.3, loc="upper center", framealpha=0.95)
ax.grid(alpha=0.25, which="both")
plt.tight_layout()
plt.savefig("fig_delta2_landscape.png", dpi=150, bbox_inches="tight")
print("wrote fig_delta2_landscape.png")
