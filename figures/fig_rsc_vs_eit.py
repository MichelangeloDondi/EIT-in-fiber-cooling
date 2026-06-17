"""
fig_rsc_vs_eit.py  --  Paper T headline: the field-insensitivity / cooling-floor
trade-off.

Three floors, each computed from the project engines:
  * EIT, clock pair  |1,-1>/|2,+1>  (field-insensitive)  -> 0.0048   [tagged_solver]
  * RSC, clock pair  |1,-1>/|2,+1>  (field-insensitive)  -> >=0.0137  [raman_sbc, Nf=10
        LOWER BOUND: higher Fock cutoff does not converge within budget -> the
        steady state is hot/spread; the field-insensitive Dm=2 Raman is rank-2
        suppressed, so RSC barely cools this pair]
  * RSC, stretched pair |2,+2>/|2,+1> (FIELD-SENSITIVE) -> 0.00196   [raman_sbc]

Message: you can have field-insensitivity (EIT, ~0.005) OR RSC's best floor
(~0.002) -- but RSC's best needs a field-SENSITIVE pair that the inhomogeneous
radial bath dephases.  On the field-insensitive pair the experiment actually
needs, EIT beats RSC.

NOTE: the "0.45" clock-RSC floor carried in earlier notes was NOT reproduced by
the engine and is treated as unverified; the defensible claim is comparative.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# computed floors (see module docstring for provenance)
labels = ["EIT\nclock pair", "RSC\nclock pair", "RSC\nstretched pair"]
vals   = [0.0048, 0.0137, 0.00196]
lb     = [False,  True,    False]          # clock-RSC is a lower bound
field  = ["field-insensitive", "field-insensitive", "field-SENSITIVE"]
colors = ["#1565c0", "#7b8794", "#c0392b"]

x = np.arange(3)
fig, ax = plt.subplots(figsize=(8.8, 5.6))
ax.set_yscale("log")
bars = ax.bar(x, vals, width=0.60, color=colors, edgecolor="black", linewidth=0.8,
              zorder=3)
bars[1].set_hatch("////"); bars[1].set_alpha(0.85)

ax.axhspan(0.004, 0.006, color="#eafaf0", zorder=0)
ax.text(-0.52, 0.0049, "EIT target ~0.005", fontsize=8.5, color="#2e7d32",
        ha="left", va="center")

for xi, v, is_lb in zip(x, vals, lb):
    txt = (r"$\geq%.4f$" % v) if is_lb else ("%.4f" % v)
    ax.text(xi, v * 1.22, txt, ha="center", va="bottom", fontsize=11.5,
            fontweight="bold")
    if is_lb:
        ax.annotate("", xy=(xi, v * 2.35), xytext=(xi, v * 1.55),
                    arrowprops=dict(arrowstyle="-|>", color="black", lw=1.5))

# field-sensitivity as a colored sub-row BELOW the x tick labels
for xi, fl in zip(x, field):
    ax.text(xi, -0.205, fl, transform=ax.get_xaxis_transform(), ha="center",
            va="top", fontsize=9.2,
            color=("#c0392b" if "SENS" in fl else "#1b5e20"),
            fontweight="bold")

ax.text(1, 0.040,
        "rank-2 suppressed:\nhigher $N_f$ does not converge\n(hot distribution)",
        ha="center", va="bottom", fontsize=8.4, color="#5a5a5a")

ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=11)
ax.set_xlim(-0.65, 2.65)
ax.set_ylim(1.2e-3, 1.5e-1)
ax.set_ylabel(r"axial floor  $\langle n_z\rangle$", fontsize=12)
ax.set_title("Field-insensitivity vs cooling floor\n"
             "EIT cools the field-insensitive pair; RSC's best needs a "
             "field-sensitive pair", fontsize=12.5)
ax.grid(alpha=0.25, axis="y", which="both")
plt.subplots_adjust(bottom=0.20)
plt.savefig("fig_rsc_vs_eit.png", dpi=150, bbox_inches="tight")
print("wrote fig_rsc_vs_eit.png")
