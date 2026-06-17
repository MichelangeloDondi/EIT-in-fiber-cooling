"""
fig_level_scheme.py -- Paper T Fig. 1.

(a) Level scheme of the Dm=2 field-insensitive clock-pair Raman in 87Rb:
    |1,-1> --sigma+--> |F',0> (5P3/2) --sigma- --> |2,+1>, both legs through m'=0.
    The two contributing excited levels F'=1,2 carry opposite-sign amplitudes
    (g1 = -g2), i.e. the rank-2 null sum_F' g = 0.
(b) Mirror-ladder geometry: guided sigma- control + retro sigma+ probe along the
    trap axis -> a single Dm=+2 two-photon kick.

Pure matplotlib (stdlib); writes fig_level_scheme.pdf (vector, for the manuscript).
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Ellipse

BLUE = "#1f5fb5"   # sigma+
RED  = "#b5341e"   # sigma-
GREY = "#9aa7b4"
DK   = "#222222"
HL1  = "#c8772a"   # F'=1 highlight
HL2  = "#1f6f4a"   # F'=2 highlight

fig = plt.figure(figsize=(3.6, 4.5))
gs = fig.add_gridspec(2, 1, height_ratios=[2.7, 1.0], hspace=0.28)
axA = fig.add_subplot(gs[0]); axB = fig.add_subplot(gs[1])
for ax in (axA, axB):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

# ---------------- panel (a): level scheme ----------------
axA.set_xlim(-2.6, 2.8); axA.set_ylim(-0.5, 6.6)

def level(ax, xc, y, c=DK, lw=2.2, half=0.34):
    ax.plot([xc-half, xc+half], [y, y], color=c, lw=lw, solid_capstyle="round")

# ground 5S1/2: F=1 (y=0) and F=2 (y=1.05), hyperfine gap broken
yF1, yF2 = 0.0, 1.05
for m in (-1, 0, 1):
    level(axA, m, yF1, c=GREY, lw=1.6)
for m in (-2, -1, 0, 1, 2):
    level(axA, m, yF2, c=GREY, lw=1.6)
# the two clock states, emphasized
level(axA, -1, yF1, c=DK, lw=3.0)
level(axA, +1, yF2, c=DK, lw=3.0)
axA.plot(-1, yF1, "o", color=BLUE, ms=6, zorder=5)
axA.plot(+1, yF2, "o", color=RED, ms=6, zorder=5)
axA.text(-1, yF1-0.42, r"$|1,-1\rangle$", ha="center", va="top", fontsize=8.5, color=DK)
axA.text(+1, yF2+0.16, r"$|2,+1\rangle$", ha="center", va="bottom", fontsize=8.5, color=DK)
axA.text(2.55, yF1, r"$F{=}1$", ha="left", va="center", fontsize=7.5, color=GREY)
axA.text(2.55, yF2, r"$F{=}2$", ha="left", va="center", fontsize=7.5, color=GREY)
# hyperfine gap marker
axA.annotate("", xy=(-2.25, yF2), xytext=(-2.25, yF1),
             arrowprops=dict(arrowstyle="<->", color=GREY, lw=0.9))
axA.text(-2.33, 0.5*(yF1+yF2), r"6.835 GHz", ha="right", va="center",
         fontsize=6.8, color=GREY, rotation=90)
axA.text(-1.7, -0.30, r"$5S_{1/2}$", ha="center", va="top", fontsize=8, color=DK)

# excited 5P3/2: F'=0,1,2,3 at relative spacings (-302,-230,-73,+194 MHz, scaled)
y0, dstep = 4.95, 0.32        # even visual spacing (schematic; not to scale)
ylev = {Fp: y0 + Fp * dstep for Fp in (0, 1, 2, 3)}
colF = {0: GREY, 1: HL1, 2: HL2, 3: GREY}
for Fp in (0, 1, 2, 3):
    lw = 2.6 if Fp in (1, 2) else 1.5
    level(axA, 0, ylev[Fp], c=colF[Fp], lw=lw, half=0.5)
    axA.text(0.58, ylev[Fp], r"$F'{=}%d$" % Fp, ha="left", va="center",
             fontsize=6.6, color=colF[Fp])
axA.text(-1.35, ylev[3]+0.12, r"$5P_{3/2}\ |F',0\rangle$", ha="center", va="bottom", fontsize=7.6, color=DK)
axA.text(0.58, ylev[0]-0.30, r"(not to scale)", ha="left", va="top", fontsize=5.6, color=GREY, style="italic")

# two Raman legs through m'=0 (meet at the F'=1/2 manifold, ~ylev[1..2])
ymid = 0.5*(ylev[1] + ylev[2])
axA.add_patch(FancyArrowPatch((-1, yF1+0.05), (-0.06, ymid-0.04),
              arrowstyle="-|>", mutation_scale=11, lw=1.8, color=BLUE, shrinkA=0, shrinkB=0))
axA.add_patch(FancyArrowPatch((0.0, ymid-0.04), (1, yF2+0.05),
              arrowstyle="-|>", mutation_scale=11, lw=1.8, color=RED, shrinkA=0, shrinkB=0))
axA.text(-0.95, 2.9, r"$\sigma^+$", color=BLUE, fontsize=10, ha="right")
axA.text(0.95, 2.9, r"$\sigma^-$", color=RED, fontsize=10, ha="left")

# detuning Delta: dashed virtual line below the manifold
yv = ylev[0] - 0.55
axA.plot([-0.5, 0.5], [yv, yv], ls=(0, (4, 3)), color=DK, lw=1.0)
axA.annotate("", xy=(0.0, yv), xytext=(0.0, ylev[1]),
             arrowprops=dict(arrowstyle="<->", color=DK, lw=0.8))
axA.text(0.12, 0.5*(yv+ylev[1]), r"$\Delta$", fontsize=8.5, va="center")

# rank-2 null annotation
axA.text(2.78, ymid+0.05,
         "$g_{F'=1}=-g_{F'=2}$\n" r"$\Rightarrow\ \sum_{F'} g_{F'}=0$" "\n(rank-2 null)",
         ha="right", va="center", fontsize=7.0, color=DK,
         bbox=dict(boxstyle="round,pad=0.3", fc="#f4f1ea", ec="#cbb9a0", lw=0.7))
axA.text(-2.5, 6.45, r"(a)", fontsize=10, fontweight="bold", ha="left", va="top")
axA.text(0, -0.5, r"$m_F$", fontsize=8, ha="center", va="top")

# ---------------- panel (b): mirror-ladder geometry ----------------
axB.set_xlim(0, 10); axB.set_ylim(0, 3)
# fibre core (rounded bar)
axB.add_patch(FancyBboxPatch((1.2, 1.15), 7.6, 0.7,
              boxstyle="round,pad=0.02,rounding_size=0.18",
              fc="#eef2f6", ec=GREY, lw=1.0))
# axial lattice ticks
for xx in [i*0.5 for i in range(5, 16)]:
    axB.plot([xx, xx], [1.25, 1.75], color=GREY, lw=0.6, alpha=0.6)
# atom
axB.add_patch(Ellipse((5.0, 1.5), 0.34, 0.5, fc=DK, ec="none", zorder=5))
# guided sigma- control (forward, from left)
axB.add_patch(FancyArrowPatch((1.6, 2.45), (4.6, 2.45), arrowstyle="-|>",
              mutation_scale=12, lw=2.0, color=RED))
axB.text(1.5, 2.62, r"control $\sigma^-$ (guided)", color=RED, fontsize=7.0, ha="left", va="bottom")
# retro sigma+ probe (backward, from right)
axB.add_patch(FancyArrowPatch((8.4, 0.55), (5.4, 0.55), arrowstyle="-|>",
              mutation_scale=12, lw=2.0, color=BLUE))
axB.text(8.5, 0.40, r"retro $\sigma^+$ probe ($\lambda/4$)", color=BLUE, fontsize=7.0, ha="right", va="top")
# mirror at right
axB.plot([9.15, 9.15], [0.95, 2.05], color=DK, lw=2.6)
axB.add_patch(plt.Rectangle((9.18, 0.95), 0.13, 1.1, fc="none", ec="none"))
for yy in [1.05, 1.25, 1.45, 1.65, 1.85]:
    axB.plot([9.15, 9.42], [yy, yy-0.18], color=DK, lw=0.8)
axB.text(5.0, 0.95, r"$\Delta m=+2$", ha="center", va="top", fontsize=8.0, color=DK)
axB.text(0.15, 2.9, r"(b)", fontsize=10, fontweight="bold", ha="left", va="top")

fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fig_level_scheme.pdf")
fig.savefig(out, bbox_inches="tight")
fig.savefig(out.replace(".pdf", ".png"), dpi=160, bbox_inches="tight")
print("wrote", out, "and .png")
