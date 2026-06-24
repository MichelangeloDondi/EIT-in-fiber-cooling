"""
fig_cloud_floor_multilevel.py  --  the cloud axial floor, POST-RETRACTION (multilevel union).

Replaces the 3-level fig_cloud_floor in the master/authority: shows the CURRENT cloud story
with the retraction-era numbers and evidence tiers -- a Gaussian trap's floor rises with the
radial temperature T_r, while a flat-top box collapses it toward the on-axis single-atom floor
(the lever).  Designed from Cuddy's red-team-round figure; rebuilt as a baked repo script so it
is regenerable and carries its provenance.

DATA PROVENANCE (baked documented values; compute-free.  The multilevel union is a ~12-min/solve
cluster job, so this plots the documented SSOT, not a live scan -- matching the docs by construction):
  * Gaussian cloud floor (T_r-gated): INDEX §1b "cloud floor, Gaussian"  [I, cross-engine]
        T_r 25/100/400 uK -> 0.007 / 0.012 / 0.022
  * Flat-top box (cloud_multilevel_union = eit-tool coherent (x) Fock on the radial grid; INDEX §1b):
        cooled   100 uK -> 0.0072   [V, Nf-converged, +1.4% Nf6->Nf8]
        uncooled 556 uK -> >= 0.021 [O, non-converged lower bound, +79% Nf6->Nf8, cluster-pending]
        (the Nf=6 0.0118 once read off here is RETRACTED -- under-resolved)
  * single-atom solve floor band 0.0048-0.0072 [V] (dual-end / single-tagged)
  CAVEAT (disclosed): the Gaussian curve is the [I] cross-engine row; the WITHIN-union Gaussian is
        higher still (0.024 @100uK / 0.099 @556uK; INDEX §1b), so the lever shown vs the [I] Gaussian
        is CONSERVATIVE -- the true within-engine collapse is larger.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Gaussian cloud floor (T_r-gated) -- INDEX §1b [I, cross-engine]
Tg = np.array([25.0, 100.0, 400.0]);  fg = np.array([0.007, 0.012, 0.022])
# Flat-top box (multilevel union) -- INDEX §1b
T_cool, f_cool = 100.0, 0.0072      # [V]
T_hot,  f_hot  = 556.0, 0.021       # [O] lower bound

fig, ax = plt.subplots(figsize=(9.2, 5.4))

# single-atom solve-floor band
ax.axhspan(0.0048, 0.0072, color="#eef5ee", zorder=0)
ax.text(595, 0.0058, "single-atom solve floor\n0.0048–0.0072 [V]",
        fontsize=8, color="#3f7a3f", va="center", ha="right")

# Gaussian curve (rises with T_r)
ax.plot(Tg, fg, "o-", color="#c0392b", lw=2.4, ms=8,
        label=r"Gaussian trap — floor rises with $T_r$  [I]")
for t, f in zip(Tg, fg):
    ax.annotate(f"{f:.3f}", (t, f), textcoords="offset points", xytext=(6, 7),
                color="#c0392b", fontsize=8.5)

# flat-top box: cooled [V] and uncooled [O]
ax.plot(T_cool, f_cool, "s", color="#1565c0", ms=11, zorder=5,
        label=r"flat-top box, cooled  0.0072 [V]")
ax.annotate("0.0072", (T_cool, f_cool), textcoords="offset points", xytext=(8, -13),
            color="#1565c0", fontsize=8.5)
ax.plot(T_hot, f_hot, "^", color="#8e44ad", ms=12, zorder=5,
        label=r"flat-top box, uncooled  ≥0.021 [O]")
ax.annotate("≥0.021", (T_hot, f_hot), textcoords="offset points", xytext=(9, 1),
            color="#8e44ad", fontsize=8.5)
ax.annotate("", xy=(T_hot, f_hot + 0.0020), xytext=(T_hot, f_hot),
            arrowprops=dict(arrowstyle="->", color="#8e44ad", lw=1.0))   # lower-bound up-arrow

# the lever: hot Gaussian down to the cooled flat-top floor
ax.annotate("the lever:\nflat-top collapses\nthe cloud floor",
            xy=(T_cool, f_cool + 0.0004), xytext=(210, 0.0095),
            fontsize=8.6, color="#1565c0", ha="center",
            arrowprops=dict(arrowstyle="->", color="#1565c0", lw=0.9))

# retraction / convergence note
ax.text(0.015, 0.97,
        "Nf=6 flat-top floor 0.0118 RETRACTED (under-resolved);\n"
        "uncooled digit Nf-divergent → cluster-pending (INDEX §1b)",
        transform=ax.transAxes, fontsize=7.8, color="#555", va="top",
        bbox=dict(boxstyle="round,pad=0.4", fc="#fbf4f4", ec="#d8b0b0"))

ax.set_xlabel(r"radial temperature  $T_r$  (µK)", fontsize=11)
ax.set_ylabel(r"axial cloud floor  $\langle n_z\rangle$", fontsize=11)
ax.set_title("Cloud axial floor — a flat-top box collapses the $T_r$-driven Gaussian rise\n"
             "post-retraction (multilevel union): cooled 0.0072 [V] / uncooled ≥0.021 [O]",
             fontsize=10.5)
ax.set_ylim(0, 0.025);  ax.set_xlim(0, 620)
ax.legend(fontsize=8.5, loc="upper center", frameon=False, bbox_to_anchor=(0.62, 0.99))
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
plt.tight_layout()
plt.savefig("fig_cloud_floor_multilevel.png", dpi=150, bbox_inches="tight")
print("wrote fig_cloud_floor_multilevel.png")
