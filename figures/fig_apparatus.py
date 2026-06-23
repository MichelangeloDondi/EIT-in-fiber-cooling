"""
fig_apparatus.py  --  Apparatus / trap schematic (hand-drawn, no engine).

The kagome hollow-core PCF, the 1064 nm axial lattice threaded through the core,
atoms in the antinodes, and the dual-end cooling beams. The right panel conveys
the trap ANISOTROPY (stiff axial nu_z vs shallow degenerate radial nu_r, ~80x)
that drives the radial-cloud program (Guide Ch 06).

Numbers: master Section 1 (48 um core, w ~ 19 um, nu_z=2pi*430 kHz,
nu_r=2pi*5.42 kHz, 532 nm spacing, U0 = 1094 uK).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, FancyBboxPatch

fig = plt.figure(figsize=(12.6, 5.8))
gs = fig.add_gridspec(2, 2, width_ratios=[3.45, 1.0], height_ratios=[1, 1],
                      wspace=0.05, hspace=0.12)
ax = fig.add_subplot(gs[:, 0])          # schematic, full height (left)
axi = fig.add_subplot(gs[0, 1])         # anisotropy, top-right

# ---- the fibre: cladding bands + hollow core ----------------------------------
CORE_LO, CORE_HI = 1.30, 3.10
XL, XR = 0.6, 9.4
for (lo, hi) in [(0.55, CORE_LO), (CORE_HI, 3.85)]:            # cladding top & bottom
    ax.add_patch(Rectangle((XL, lo), XR - XL, hi - lo, facecolor="#eef2f7",
                 edgecolor="#9fb0c3", lw=1.0, hatch="......", zorder=1))
ax.text(XL + 0.08, 3.70, "kagome photonic-crystal cladding", fontsize=8.5,
        color="#7488a0", va="top", ha="left", style="italic", zorder=2)
ax.add_patch(Rectangle((XL, CORE_LO), XR - XL, CORE_HI - CORE_LO,        # hollow core
             facecolor="#ffffff", edgecolor="#9fb0c3", lw=1.2, zorder=1))

# ---- the 1064 nm standing-wave lattice in the core ----------------------------
yc = 0.5 * (CORE_LO + CORE_HI)
xs = np.linspace(XL + 0.5, XR - 0.5, 600)
period, env = 0.62, 0.60
inten = env * np.cos(2 * np.pi * (xs - xs[0]) / period) ** 2
ax.fill_between(xs, yc - inten, yc + inten, color="#cfe3f7", alpha=0.85, zorder=2)
anti = xs[0] + period * np.arange(0, int((xs[-1] - xs[0]) / period) + 1)
rng = np.random.default_rng(7)
for i, xa in enumerate(anti):
    if xa > xs[-1] - 0.1:
        continue
    ax.plot(xa, yc, "o", ms=8.5, color="#c0392b", zorder=5)                # on-axis
    if i % 3 == 1:                                                          # a few cloud atoms
        for dy in rng.uniform(0.22, 0.52, size=2) * rng.choice([-1, 1], 2):
            ax.plot(xa, yc + dy, "o", ms=4.2, color="#e8a0a0", zorder=4)

# ---- dual-end beams (opposite injection) --------------------------------------
ax.add_patch(FancyArrowPatch((XL - 0.55, yc), (XL + 0.45, yc), arrowstyle="-|>",
             mutation_scale=20, lw=3.0, color="#1565c0", zorder=6))
ax.text(XL - 0.55, yc + 0.42, r"control $\sigma^-$", color="#1565c0",
        fontsize=11, ha="left", va="bottom", fontweight="bold")
ax.text(XL - 0.55, yc - 0.42, "arm A, one end", color="#1565c0", fontsize=8, ha="left", va="top")
ax.add_patch(FancyArrowPatch((XR + 0.55, yc), (XR - 0.45, yc), arrowstyle="-|>",
             mutation_scale=20, lw=3.0, color="#2e7d32", zorder=6))
ax.text(XR + 0.55, yc + 0.42, r"probe $\sigma^+$", color="#2e7d32",
        fontsize=11, ha="right", va="bottom", fontweight="bold")
ax.text(XR + 0.55, yc - 0.42, "arm B, opposite end", color="#2e7d32", fontsize=8, ha="right", va="top")

# ---- core-size marker ---------------------------------------------------------
ax.annotate("", xy=(XR - 0.25, CORE_LO - 0.10), xytext=(XR - 0.25, CORE_HI + 0.10),
            arrowprops=dict(arrowstyle="<->", color="#888", lw=1.0))
ax.text(XR - 0.40, yc, "48 µm core\n($w\\approx$19 µm)", fontsize=8.3, color="#666",
        va="center", ha="right")

# ---- axes indicator (z axial, r radial) — clear lower-right -------------------
ox, oy = 6.85, 0.34
ax.add_patch(FancyArrowPatch((ox, oy), (ox + 0.95, oy), arrowstyle="-|>",
             mutation_scale=13, lw=1.8, color="#333", zorder=6))
ax.text(ox + 1.02, oy, r"$z$  axial (stiff)", fontsize=9, va="center", ha="left", color="#333")
ax.add_patch(FancyArrowPatch((ox, oy), (ox, oy + 0.66), arrowstyle="-|>",
             mutation_scale=13, lw=1.8, color="#333", zorder=6))
ax.text(ox + 0.06, oy + 0.70, r"$r$  radial (shallow)", fontsize=9, va="bottom", ha="left", color="#333")

# ---- label box (lower-left) ---------------------------------------------------
lab = ("1064 nm intra-fibre lattice:  532 nm spacing,  $U_0=1094$ µK.\n"
       "Atoms sit in the antinodes; a real cloud spreads radially (faint).")
ax.add_patch(FancyBboxPatch((XL + 0.05, 0.06), 5.55, 0.56, boxstyle="round,pad=0.08",
             linewidth=1.0, edgecolor="#9fb0c3", facecolor="#f7fafd", zorder=7))
ax.text(XL + 0.20, 0.34, lab, fontsize=8.5, va="center", ha="left", color="#445", zorder=8)

ax.set_xlim(XL - 1.45, XR + 1.45)
ax.set_ylim(-0.05, 4.05)
ax.axis("off")
ax.set_title("In-fibre apparatus — ⁸⁷Rb in a 1064 nm kagome-HCPCF lattice",
             fontsize=12.5, loc="left", pad=8)

# ---- right panel: the trap anisotropy ----------------------------------------
zz = np.linspace(-1, 1, 400)
axi.plot(zz, zz**2, color="#1565c0", lw=2.4, label=r"axial $\nu_z=2\pi\!\cdot\!430$ kHz")
axi.plot(zz, 0.0157 * zz**2, color="#2e7d32", lw=2.4, label=r"radial $\nu_r=2\pi\!\cdot\!5.42$ kHz")
axi.set_title("trap anisotropy (~80×)", fontsize=9.5)
axi.set_xlabel("displacement", fontsize=8)
axi.set_ylabel("potential", fontsize=8)
axi.set_xticks([]); axi.set_yticks([]); axi.set_ylim(-0.05, 1.05)
axi.legend(fontsize=7.0, loc="upper center", frameon=False)
for s in ("top", "right"):
    axi.spines[s].set_visible(False)

plt.savefig("fig_apparatus.png", dpi=150, bbox_inches="tight")
print("wrote fig_apparatus.png")
