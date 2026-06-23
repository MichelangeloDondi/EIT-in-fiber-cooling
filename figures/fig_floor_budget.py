"""
fig_floor_budget.py  --  The axial floor budget as a waterfall: how the dual-end
solve floor builds up from the clean-Lambda base, why F'=1 dominates, and the
once-only squeezer that takes it to the certified single-atom floor.
(Guide Ch 05; master §5 and §7.)

DATA PROVENANCE (baked documented values -- master §5/§7; compute-free):
  base (clean Lambda)      0.0014
  + F'=1   (DOMINANT)     +0.0034   -> 0.0048
  + F'=3                  +0.0010
  + F'=0                  +0.0001   -> ~0.0059 (converged dual; Nf=6 gate reads 0.0048, non-additive)
  + transient squeezer    +0.0030   (added ONCE, master §7)
  = certified single-atom  ~0.0089   (band 0.008-0.010)
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

labels = ["base\n(clean Λ)", "+ F′=1\n(dominant)", "+ F′=3", "+ F′=0",
          "solve floor\n(dual-end)", "+ squeezer\n(once)", "certified\nsingle-atom"]
incr   = [0.0014, 0.0034, 0.0010, 0.0001, None, 0.0030, None]   # None = total bar
is_tot = [False, False, False, False, True, False, True]
totcol = "#1565c0"
colors = ["#7f8c8d", "#c0392b", "#e67e22", "#f1c40f", totcol, "#16a085", "#27ae60"]

fig, ax = plt.subplots(figsize=(10.2, 5.4))
run = 0.0
for i, (lab, dv, tot, col) in enumerate(zip(labels, incr, is_tot, colors)):
    if tot:                                   # absolute total bar from 0
        h = 0.0059 if i == 4 else 0.0089
        ax.bar(i, h, color=col, edgecolor="black", lw=0.8, width=0.62, zorder=3)
        ax.text(i, h + 0.00025, f"{h:.4f}".rstrip("0"), ha="center", va="bottom",
                fontsize=9.5, fontweight="bold", color=col)
        run = h
    else:                                     # incremental (floating) bar
        ax.bar(i, dv, bottom=run, color=col, edgecolor="black", lw=0.8, width=0.62, zorder=3)
        tag = f"+{dv:.4f}".rstrip("0") if i else f"{dv:.4f}".rstrip("0")
        ax.text(i, run + dv + 0.00025, tag, ha="center", va="bottom", fontsize=9, color=col)
        if 0 < i < 4:                         # connector line for the waterfall
            ax.plot([i - 0.31, i + 0.31], [run, run], color="#999", lw=0.8, ls=":", zorder=2)
        run += dv

ax.axhspan(0.008, 0.010, color="#27ae60", alpha=0.10, zorder=0)
ax.text(6.0, 0.0102, "certified band\n0.008–0.010", fontsize=8.5, color="#27ae60",
        ha="center", va="bottom")
ax.annotate("F′=1 is the largest\ncontaminant (+0.0034):\ncommon, Λ-closing",
            xy=(1, 0.0014 + 0.0017), xytext=(1.7, 0.0085), fontsize=9, color="#c0392b",
            ha="center", arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.0))

ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels, fontsize=8.8)
ax.set_ylabel(r"axial floor  $\langle n_z\rangle$", fontsize=11)
ax.set_ylim(0, 0.0118)
ax.set_title("The axial floor budget — F′=1 dominates the contaminants; the squeezer is added once\n"
             "(dual-end, master §5/§7; increments are non-additive — the Nf=6 gate reads 0.0048)",
             fontsize=11, pad=8)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
plt.tight_layout()
plt.savefig("fig_floor_budget.png", dpi=150, bbox_inches="tight")
print("wrote fig_floor_budget.png")
