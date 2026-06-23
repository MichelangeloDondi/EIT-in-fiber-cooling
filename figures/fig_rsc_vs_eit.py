"""
fig_rsc_vs_eit.py  --  Paper T headline: on the field-insensitive clock pair,
EIT cools but RSC is rank-2 DISQUALIFIED.

All floors are imported from the SSOT (src/engines/operating_point.py) so the figure
cannot drift from the canonical numbers:
  * EIT,  clock pair |1,-1>/|2,+1>  (field-insensitive)  -> 0.0048  [solve, dual-end]
  * RSC,  clock pair |1,-1>/|2,+1>  (field-insensitive)  -> ~0.45   DISQUALIFIED
        by the rank-2 obstruction: the Dm=+2 Raman vanishes in J=1/2 (rank-2
        electronic null; runs only via excited I.J ~ Delta_HFS/Delta^2), and the
        mirror-ladder geometry forces one beam onto the dark state -> bounded
        coherence-per-scatter (~4) -> off-resonant scatter beats the slow LD
        cooling 11-23:1.  The 0.0137 from raman_sbc is the OBSTRUCTION-FREE
        idealization (free Raman Rabi, ~0 scatter), NOT the physical floor.
        See docs/clock_RSC_resolution.md.
  * RSC,  stretched pair |2,+2>/|2,+1> (FIELD-SENSITIVE) -> 0.00196

Message: the experiment needs a FIELD-INSENSITIVE pair (the radial bath dephases
a field-sensitive one).  On that pair EIT reaches ~0.005 while RSC is rank-2
disqualified at ~0.45.  RSC's low floor (0.00196) exists only on a field-SENSITIVE
pair.  So for field-insensitive cooling the answer is EIT.
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "engines"))
import operating_point as op

EIT_CLOCK   = op.FLOOR.solve_dual_end       # 0.0048
RSC_CLOCK   = op.RSC_CLOCK_FLOOR            # 0.45   (rank-2 limited)
RSC_IDEAL   = op.RSC_CLOCK_IDEALIZED        # 0.0137 (obstruction-free idealization)
RSC_STRETCH = op.RSC_STRETCHED             # 0.00196
RECOIL      = op.FLOOR.axial_recoil_bound   # ~0.003
lift        = round(RSC_CLOCK / RSC_IDEAL)  # ~33x

labels = ["EIT\nclock pair", "RSC\nclock pair", "RSC\nstretched pair"]
vals   = [EIT_CLOCK, RSC_CLOCK, RSC_STRETCH]
field  = ["field-insensitive", "field-insensitive", "field-SENSITIVE"]
status = ["RECOMMENDED", "DISQUALIFIED (rank-2)", "lowest floor"]
colors = ["#1565c0", "#8a9199", "#c0392b"]

x = np.arange(3)
fig, ax = plt.subplots(figsize=(9.4, 6.3))
ax.set_yscale("log")
ax.set_ylim(1.2e-3, 1.4)

bars = ax.bar(x, vals, width=0.56, color=colors, edgecolor="black", linewidth=0.9, zorder=3)
bars[1].set_hatch("////"); bars[1].set_alpha(0.80)

# reference lines
ax.axhline(RECOIL, ls=":", color="#999", lw=1.0, zorder=1)
ax.text(2.62, RECOIL * 1.04, r"axial recoil bound $\eta_{em}^2$", fontsize=7.8,
        color="#999", va="bottom", ha="right")
ax.axhspan(0.004, 0.006, color="#eafaf0", zorder=0)

def fmt(v):
    return ("%.4f" % v) if v < 0.02 else ("%.2f" % v)
for xi, v in zip(x, vals):
    ax.text(xi, v * 1.30, fmt(v), ha="center", va="bottom", fontsize=13, fontweight="bold")

# status + field-sensitivity sub-rows below the tick labels
for xi, st in zip(x, status):
    col = "#1b5e20" if st.startswith("REC") else ("#b71c1c" if "rank" in st else "#c0392b")
    ax.text(xi, -0.125, st, transform=ax.get_xaxis_transform(), ha="center", va="top",
            fontsize=9.3, fontweight="bold", color=col)
for xi, fl in zip(x, field):
    ax.text(xi, -0.195, fl, transform=ax.get_xaxis_transform(), ha="center", va="top",
            fontsize=8.6, color=("#c0392b" if "SENS" in fl else "#1b5e20"))

# clock-RSC: where the obstruction-free engine put it, and the rank-2 lift
ax.plot([1], [RSC_IDEAL], marker="o", ms=9, mfc="white", mec="#555", mew=1.6, zorder=5)
ax.text(1.0, RSC_IDEAL * 0.66, "raman_sbc\nidealized %.4f" % RSC_IDEAL,
        ha="center", va="top", fontsize=7.8, color="#555", zorder=6,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#cccccc", alpha=0.95))
ax.annotate("", xy=(1, RSC_CLOCK * 0.82), xytext=(1, RSC_IDEAL * 1.32),
            arrowprops=dict(arrowstyle="-|>", color="#b71c1c", lw=2.0, ls=(0, (4, 2))))
ax.text(1.31, np.sqrt(RSC_IDEAL * RSC_CLOCK), "rank-2\nobstruction\n" + r"$\times%d$" % lift,
        ha="left", va="center", fontsize=8.8, color="#b71c1c", fontweight="bold")

# mechanism box (upper-left; the EIT bar is short, so no collision)
ax.text(0.015, 0.975,
        "Field-insensitive cooling must use the clock pair\n"
        "(a field-sensitive pair is dephased by the radial bath).\n"
        r"There the $\Delta m{=}{+}2$ Raman vanishes in $J{=}\frac{1}{2}$" + "\n"
        r"(rank-2; only via $\Delta_{HFS}/\Delta^2$) $\Rightarrow$ bounded" + "\n"
        r"coherence/scatter $\Rightarrow$ scatter beats cooling 11–23:1.",
        transform=ax.transAxes, ha="left", va="top", fontsize=8.3, color="#333",
        bbox=dict(boxstyle="round,pad=0.4", fc="#f7f7f7", ec="#cccccc"))

ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=11.5)
ax.set_xlim(-0.62, 2.74)
ax.set_ylabel(r"axial cooling-floor  $\langle n_z\rangle$  (solve)", fontsize=12)
ax.set_title("On the field-insensitive clock pair, EIT cools — RSC is rank-2 disqualified",
             fontsize=12.5, pad=12)
ax.grid(alpha=0.25, axis="y", which="both")
plt.subplots_adjust(bottom=0.22)

fig.text(0.5, 0.004,
         "0.0137 is the obstruction-free idealization (raman_sbc: free Raman Rabi, ~0 scatter) — not the physical floor.  "
         "See docs/clock_RSC_resolution.md.",
         ha="center", va="bottom", fontsize=7.6, color="#777")

plt.savefig("fig_rsc_vs_eit.png", dpi=150, bbox_inches="tight")
print("wrote fig_rsc_vs_eit.png  (EIT %.4f | clock-RSC %.2f DISQ rank-2 | stretched %.5f)"
      % (EIT_CLOCK, RSC_CLOCK, RSC_STRETCH))
