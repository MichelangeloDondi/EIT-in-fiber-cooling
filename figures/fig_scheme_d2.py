"""
fig_scheme_d2.py  --  Correct v14 cooling scheme (87Rb D2), clean layout.

Field-insensitive clock pair  |1,-1> (probe sigma+) / |2,+1> (control sigma-)
-> |F'=2, m'=0>.  Both ground legs g_F*m_F = +1/2 => first-order B-insensitive
at any field (defining choice; the m'=2 stretched pair was abandoned as
field-SENSITIVE).  One EIT window at delta2=0; F'=1 perturbs it (+0.0034);
F'=0, F'=3 are single-leg off-resonant scatterers.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

HF = {3: 266.65, 2: 0.0, 1: -156.95, 0: -229.17}     # 5P3/2 offsets re F'=2 (MHz)
MP = {3: range(-3, 4), 2: range(-2, 3), 1: range(-1, 2), 0: range(0, 1)}
YC, DIV = 5.2, 210.0
def yE(Fp): return YC + HF[Fp] / DIV
YF2, YF1 = 1.1, 0.0
LW = 0.30
ROLE = {3: "(scatterer)", 2: "(EIT level)", 1: "(perturbs window)", 0: "(scatterer)"}

fig, ax = plt.subplots(figsize=(11.0, 8.6))

# excited manifold
for Fp, ms in MP.items():
    y = yE(Fp)
    for m in ms:
        common = (Fp in (1, 2) and m == 0)
        col = ("#c0392b" if Fp == 1 else "#111") if common else "#333"
        ax.plot([m - LW, m + LW], [y, y], color=col,
                lw=2.8 if common else 1.5, solid_capstyle="round", zorder=3)
    ax.text(3.55, y, r"$F'=%d$" % Fp, va="center", ha="left", fontsize=12, color="#333")
    ax.text(3.55, y - 0.20, ROLE[Fp], va="center", ha="left", fontsize=8.2,
            color="#c0392b" if Fp == 1 else "#999")

ax.annotate(r"$|F'2,0\rangle$", xy=(0, yE(2)), xytext=(0.9, yE(2) + 0.45),
            fontsize=11, color="#111",
            arrowprops=dict(arrowstyle="-", color="#999", lw=0.8))

# ground manifold
for (F, y, ms) in [(2, YF2, range(-2, 3)), (1, YF1, range(-1, 2))]:
    for m in ms:
        ax.plot([m - LW, m + LW], [y, y], color="#111", lw=1.6,
                solid_capstyle="round", zorder=3)
    ax.text(3.55, y, r"$F=%d$" % F, va="center", ha="left", fontsize=12, color="#333")

ax.plot(-1, YF1, "o", ms=12, color="#2e7d32", zorder=5)
ax.plot(+1, YF2, "o", ms=12, color="#1565c0", zorder=5)
ax.text(-1, YF1 - 0.30, r"$|1,-1\rangle$" + "\ndark-dominant ~94%",
        ha="center", va="top", fontsize=10, color="#2e7d32")
ax.text(+1, YF2 - 0.30, r"$|2,+1\rangle$" + "\n~6%",
        ha="center", va="top", fontsize=10, color="#1565c0")

# 6.835 GHz splitting (far left)
ax.annotate("", xy=(-3.1, YF2), xytext=(-3.1, YF1),
            arrowprops=dict(arrowstyle="<->", color="#aaa", lw=1.0))
ax.text(-3.22, (YF1 + YF2) / 2, "6.835 GHz", rotation=90, va="center", ha="right",
        fontsize=9.5, color="#777")
ax.text(-3.22, YF2 + 0.55, "(gap not to scale)", rotation=90, va="bottom",
        ha="right", fontsize=7.5, color="#bbb")

# cooling legs
ax.add_patch(FancyArrowPatch((-1, YF1), (0, yE(2)), arrowstyle="-|>",
             mutation_scale=18, lw=2.6, color="#2e7d32", zorder=4, shrinkA=7, shrinkB=7))
ax.add_patch(FancyArrowPatch((+1, YF2), (0, yE(2)), arrowstyle="-|>",
             mutation_scale=18, lw=2.6, color="#1565c0", zorder=4, shrinkA=7, shrinkB=7))
ax.text(-1.15, 3.0, r"PROBE $\sigma^+$" + "\n(retro $-z$)", color="#2e7d32",
        fontsize=11, ha="center", va="center", fontweight="bold")
ax.text(1.18, 3.2, r"CONTROL $\sigma^-$" + "\n(forward $+z$)", color="#1565c0",
        fontsize=11, ha="center", va="center", fontweight="bold")

# residual coupling to F'=1 (the perturbation), faint
for g, yg in [(-1, YF1), (+1, YF2)]:
    ax.add_patch(FancyArrowPatch((g, yg), (0, yE(1)), arrowstyle="-",
                 lw=1.0, color="#c0392b", ls=(0, (4, 3)), zorder=2,
                 shrinkA=7, shrinkB=4, alpha=0.6))
ax.text(-2.3, yE(1) + 0.05, "$-0.31$ residual\n$\\to +0.0034$", fontsize=8.5,
        color="#c0392b", va="center", ha="center")

# repumpers (schematic), right of the control beam, clear of boxes
ax.add_patch(FancyArrowPatch((1.7, YF2), (1.7, yE(2) - 0.04), arrowstyle="-|>",
             mutation_scale=12, lw=1.6, color="#e67e22", ls=(0, (2, 2)),
             zorder=2, shrinkA=4, shrinkB=4))
ax.text(1.85, 3.1, "repumpers\n($\\times 2$)", fontsize=9, color="#e67e22",
        va="center", ha="left")

# Delta marker (blue detuning above F'=2)
ax.annotate("", xy=(0.42, yE(2)), xytext=(0.42, yE(2) + 0.5),
            arrowprops=dict(arrowstyle="<->", color="#444", lw=1.0))
ax.text(0.5, yE(2) + 0.25, r"$\Delta\approx45$ (blue)", fontsize=9, va="center",
        ha="left", color="#444")

# ---- bottom annotation boxes (clear of all levels/beams) ----
b1 = ("Both legs  $g_F m_F=+\\frac{1}{2}$  $\\Rightarrow$  dark pair is first-order\n"
      "$B$-insensitive at ANY field  $-$  immune to the radial $B$/trap spread\n"
      "the shallow degenerate trap imposes on the cloud.")
ax.add_patch(FancyBboxPatch((-3.95, -1.95), 4.05, 1.05, boxstyle="round,pad=0.1",
             linewidth=1.1, edgecolor="#2e7d32", facecolor="#eafaf0", zorder=6))
ax.text(-1.93, -1.42, b1, fontsize=9.0, va="center", ha="center", color="#1b5e20", zorder=7)

b2 = ("Single-end tagged delivery:  control $\\sigma^-$ forward, probe $\\sigma^+$\n"
      "on the $\\lambda/4$ retro.  Double-passed AOM tag $2f_A=400$ MHz down-shifts\n"
      "the return so exactly one fwd$\\times$ret pair is two-photon resonant.")
ax.add_patch(FancyBboxPatch((0.35, -1.95), 4.45, 1.05, boxstyle="round,pad=0.1",
             linewidth=1.1, edgecolor="#1565c0", facecolor="#eaf1fb", zorder=6))
ax.text(2.575, -1.42, b2, fontsize=8.8, va="center", ha="center", color="#0d3c78", zorder=7)

ax.set_xlim(-4.0, 4.95)
ax.set_ylim(-2.05, 7.25)
ax.set_xlabel(r"$m_F$", fontsize=13)
ax.set_xticks(range(-3, 4))
ax.set_yticks([])
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.set_title(r"$^{87}$Rb D2 cooling scheme $-$ field-insensitive clock pair "
             r"$|1,-1\rangle/|2,+1\rangle \to |F'2,0\rangle$", fontsize=13.5, pad=10)
plt.tight_layout()
plt.savefig("fig_scheme_d2.png", dpi=150, bbox_inches="tight")
print("wrote fig_scheme_d2.png")
