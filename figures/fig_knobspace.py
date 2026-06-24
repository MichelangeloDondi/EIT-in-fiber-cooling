"""
fig_knobspace.py  --  Operating-point knob space: the two levers that set the
axial floor and the cooling speed (Guide Ch 04; operating_point.md; master §3/§5/§6).

Left  (FLOOR lever): <n_z> vs probe ratio OmR -- the weaker-probe lever. Lowering
      the probe lowers the floor while the cooling RATE saturates, so the optimum
      is at weak probe (bounded below only by the cooling-time budget).
Right (SPEED lever): cooling time tau vs detuning Delta -- lower Delta cools
      faster; the floor is flat across 40-55, so operate at the low end.

DATA PROVENANCE (baked documented values -- compute-free, reproducible, and matching
the canonical docs by construction; each multilevel solve is ~10 min on this Mac,
so a live scan is a cluster job -- see INDEX numpy-pin note):
  * floor vs OmR @ Delta=80 (dual-end): operating_point.md §2 line 29 labels this curve
        the "dual-end floor vs Omega_p/Omega_c": OmR 0.10/0.15/0.25 -> 0.0041/0.0072/0.0166.
        NOT clk2 -- clk2 config-A at Dc=80/OmR=0.25 is 0.0048 (clk2.py header, line 13), a
        different solver/recycler; do not relabel this curve "clk2". (op §2 line 16's
        "0.0166 -> 0.0048" is the tagged-solver Delta80->Delta45 improvement, a separate
        fact from this curve's label -- citing it here before was muddled; Cuddy caught it.)
  * floor vs OmR @ Delta=45 (eit_cooling_tool): master §5     0.10/0.12 -> 0.0051/0.0059
  * cooling time tau vs Delta (dual-end, OmR=0.10): master §6  45/60/80 -> 0.14/0.30/0.69 ms
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- floor vs OmR (the weaker-probe lever) ------------------------------------
omr80, fl80 = [0.10, 0.15, 0.25], [0.0041, 0.0072, 0.0166]      # Delta=80, dual-end (tagged_solver, op_point.md §2)
omr45, fl45 = [0.10, 0.12], [0.0051, 0.0059]                    # Delta=45, eit-tool
# --- cooling time vs Delta (the speed lever) ----------------------------------
dz, tau = [45.0, 60.0, 80.0], [0.14, 0.30, 0.69]               # ms, dual-end OmR=0.10

fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.0, 4.6))

# LEFT: floor vs OmR
axL.plot(omr80, fl80, "o-", color="#1565c0", lw=2.4, ms=7, label=r"$\Delta=80$ (dual-end)")
axL.plot(omr45, fl45, "s--", color="#2e7d32", lw=2.2, ms=7, label=r"$\Delta=45$ (eit-tool)")
axL.plot(0.12, 0.0059, "*", color="#c0392b", ms=17, zorder=5)
axL.annotate("operating point\nΔ=45, OmR=0.12\n(~1.4× faster than 0.10)",
             xy=(0.12, 0.0059), xytext=(0.135, 0.0125), fontsize=8.3, color="#c0392b",
             arrowprops=dict(arrowstyle="->", color="#c0392b", lw=0.9))
axL.annotate("weaker probe → lower floor\n(rate saturates)", xy=(0.10, 0.0041),
             xytext=(0.105, 0.0098), fontsize=9, color="#1565c0",
             arrowprops=dict(arrowstyle="->", color="#1565c0", lw=0.9))
axL.set_xlabel(r"probe/control ratio  $\Omega_p/\Omega_c$  (OmR)", fontsize=10.5)
axL.set_ylabel(r"axial floor  $\langle n_z\rangle$", fontsize=10.5)
axL.set_title("FLOOR lever — the weaker probe", fontsize=10.5)
axL.set_ylim(0, 0.018); axL.set_xlim(0.08, 0.27)
axL.legend(fontsize=8.5, loc="upper left", frameon=False)

# RIGHT: cooling time vs Delta
axR.plot(dz, tau, "o-", color="#8e44ad", lw=2.4, ms=8)
axR.axvspan(40, 55, color="#1565c0", alpha=0.10)
axR.text(47.5, 0.62, "floor flat\n40–55 MHz\n(master §3)", fontsize=8.6, color="#1565c0",
         ha="center", va="top")
axR.plot(45, 0.14, "*", color="#c0392b", ms=17, zorder=5)
axR.annotate("operating point\nΔ=45: 0.14 ms", xy=(45, 0.14), xytext=(52, 0.05),
             fontsize=8.3, color="#c0392b",
             arrowprops=dict(arrowstyle="->", color="#c0392b", lw=0.9))
axR.annotate("higher Δ → slower cooling", xy=(80, 0.69), xytext=(56, 0.60),
             fontsize=9, color="#8e44ad",
             arrowprops=dict(arrowstyle="->", color="#8e44ad", lw=0.9))
axR.set_xlabel(r"single-photon detuning  $\Delta$  (2$\pi$·MHz)", fontsize=10.5)
axR.set_ylabel(r"cooling time  $\tau=1/W$  (ms)", fontsize=10.5)
axR.set_title("SPEED lever — the detuning", fontsize=10.5)
axR.set_ylim(0, 0.78); axR.set_xlim(38, 84)

for a in (axL, axR):
    for s in ("top", "right"):
        a.spines[s].set_visible(False)
fig.suptitle("Operating-point knob space — pick the probe by the floor, the detuning by the speed",
             fontsize=11.5)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("fig_knobspace.png", dpi=150, bbox_inches="tight")
print("wrote fig_knobspace.png")
