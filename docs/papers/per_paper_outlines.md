# Per-paper outlines — T / P1 / P2 / P3

Expands `paper_planning_memo.md` into draft skeletons. Same universal flags apply (repeated at the end). `[V]` = computed/verified in the program; `[bench]` = needs the apparatus. Authorship lines are **suggestions — PI decisions**. Backing scripts/docs are in this repo (canonical) or the working archive.

---

## Paper T — Rank-2 obstruction to clock-qubit Raman cooling  ·  **DEMOTED → P1 motivation (not standalone)**

> **Status update 2026-06-17 — see `novelty_findings.md`.** The central result is **prior art**
> (Naber–Spreeuw, PRA 94, 013427 (2016)): same magic pair, same Δm=2 σ⁺/σ⁻ geometry, same
> destructive-interference null, same "cannot detune away spontaneous emission" conclusion. The
> rank-2 *framing*, cooling floor, and alkali generalization are re-packaging/corollary. Scope is
> also narrower than claimed: the m=0 clock transition is a Δm=0 vector Raman that **is** coolable
> (FoM rises with detuning), so "EIT is *the* route" overclaims — the obstruction is specific to the
> **Δm=2 matched pairs (m≠0)**. **Do not submit standalone.** Retained below as P1's design rationale,
> cited to Naber–Spreeuw.

**Working title:** *Why EIT — not Raman — sideband cooling reaches the ground state of a field-insensitive clock qubit.* (alt: *A rank-2 selection-rule obstruction to Raman sideband cooling on field-insensitive clock transitions.*)

**Thesis (one line):** On a first-order field-insensitive clock pair (both g_F m_F = +½) the cooling Raman is Δm = 2, hence HFS-(rank-2)-enabled; this pins the coherence-per-scatter and lifts the achievable RSC floor to n̄ ≈ 0.45, whereas near-detuned EIT cooling is structurally immune — so clock-qubit ground-state cooling needs EIT, not Raman.

**Type / venue:** short theory paper / Letter — PRA, or PRL if framed as a clock-qubit-cooling selection rule. Atom-general (alkali hyperfine and, by extension, alkaline-earth(-like) clock qubits).

**Status:** **DEMOTED to P1 motivation (cited).** Not a standalone preprint — central result published (Naber–Spreeuw 2016). The verified core (null, FoM-pinning, floor) is reused as P1's design-rationale section.

**Authorship (suggested):** Dondi (first), Minardi; consider Prevedelli.

**Figures (~3):**
1. The field-insensitive clock pair: the Δm = 2 Raman path (rank-2 coupling highlighted) vs the EIT dark-state path.
2. Floor vs the rank-2 coupling / FoM-pinning: RSC → ≈0.45, EIT → ≈0.005.
3. The three independent verifications converging (or a table).

**Outline:** (i) clock qubits want field-insensitivity *and* the motional ground state — does the standard RSC toolbox deliver the latter on the former? (ii) selection-rule argument: equal g·m forces Δm = 2 → rank-2 → HFS-enabled → coherence-per-scatter pinned → FoM bound → floor ≈ 0.45; (iii) why EIT is immune (dark/bright set by one-photon detunings, not the rank-2 tensor); (iv) verification — three methods (rate-equation FoM, two-manifold diagonalisation, full solver) all give ≈0.45 RSC vs ≈0.005 EIT; (v) generality + implication. **Sharpen the contrast:** *stretched* RSC reaches the ground state (≈0.0020) but is field-sensitive; the obstruction is specific to the field-insensitive clock pair — so the choice is EIT.

**In hand [V]:** complete, verified 3 ways. **Needs bench:** nothing.

**Novelty/framing:** the physics is correct and verified, but **not novel** — the core (destructive-interference suppression of the Δm=2 magic-pair Raman, detuning-independent) is Naber–Spreeuw, PRA 94, 013427 (2016). Value is as P1's *why-EIT* motivation, cited; not a discovery.

**Positioning (Lan/Yb):** the *content* (cited) supports the why-EIT narrative; it is **not** a standalone demonstration-of-depth preprint (prior art). The demonstration of depth is P1.

**Backing:** `src/engines/tagged_solver.py`; `rank2_verify.py`, `audit_C_rank2.py` (archive).

---

## Paper P1 — Flagship: field-insensitive EIT-SC to the ground state in HCPCF  ·  **BENCH-GATED**

**Working title:** *Field-insensitive EIT sideband cooling of ⁸⁷Rb to the motional ground state in a hollow-core fibre.*

**Thesis:** EIT sideband cooling on a first-order field-insensitive clock pair brings fibre-guided ⁸⁷Rb to **n̄_z ≈ 0.005–0.007 (P₀ ≈ 99%)** — the cooled state *is* the field-insensitive clock state — confirmed by sideband thermometry: the enabling cold, field-insensitive source for the temperature-limited in-fibre platform.

**Type / venue:** flagship experimental — PRL / PRX Quantum. The thesis core.

**Status:** **bench-gated. Go/no-go = the as-built 6.835 GHz two-photon linewidth (sub-100 Hz).**

**Authorship:** Dondi (first), the experimental team (Minardi, Prevedelli, Marchesini, …), XLIM (fibre).

**Figures (~4):** (1) scheme + apparatus, single-EOM common-mode delivery (`d2_scheme.png`); (2) cooling result — sideband spectra before/after, red/blue asymmetry → n̄_z, approach to floor; (3) thermometry calibration + extracted n̄_z; (4) field-insensitivity (cooling vs B) and/or the floor budget.

**Outline:** (i) the in-fibre platform is temperature/inhomogeneity-limited; a cold field-insensitive source unlocks it; prior fibre cooling is RSC (Leong), EIT-SC not done in HCPCF nor on a field-insensitive clock pair in a guided geometry; (ii) scheme + operating point (Δ≈45, OmR≈0.10–0.12); (iii) methods (MOT→molasses→conveyor→in-fibre, single-EOM drive, thermometry); (iv) results — the two-photon linewidth, cooling to n̄_z≈0.005–0.007, field-insensitivity, model agreement; (v) limits (load-in, OD) and the route to 3D (P4).

**In hand [V]:** operating point, floor budget (≈0.005 dual-end / 0.0072 single-ended tagged), field-insensitivity, thermometry method, scheme survey, retro-cap result. **Needs bench:** EOM coherence **(gating)**; gray molasses → n_r≈9; in-fibre n̄_z; calibrated sideband-asymmetry; delivery (η_dp).

**Novelty/framing:** defensible firsts — "EIT-SC in HCPCF" + "field-insensitive clock-pair cooling in a guided geometry." **Novelty lit-check before the abstract** (Chiu 2025 EIT-SC in tweezers; Pache 2025 Cs ONF EIT-SC — guided/tweezer EIT-SC exists). **Do not** claim "first cooling in a fibre."

**Positioning (Lan/Yb):** this is the result Lan cares about — the cold field-insensitive source for his in-fibre platform.

**Backing:** `src/engines/eit_cooling_tool.py`, `src/engines/thermometry.py`, `docs/operating_point.md`, `docs/reference/delivery/architecture_delivery_thermometry.md`.

---

## Paper P2 — Methods: single-1560-EOM, OPLL-free common-mode delivery  ·  **BENCH-GATED (shares P1's measurement)**

**Working title:** *A single telecom-EOM, OPLL-free architecture for two-colour cooling in a guided geometry.*

**Thesis:** One 1560 nm seed + one EOM generates both EIT colours; sharing the laser phase makes the two-photon coherence **passively common-mode (sub-100 Hz, no OPLL** / slave laser / filter cavity); RF-only phase switching reconfigures the sequence (incl. EIT→thermometry); the carrier-suppressed dual-end and single-ended tagged-retro realizations reach the same atomic operating point, and the **retro reflectivity is non-binding**.

**Type / venue:** methods/apparatus — Optics Express / Rev. Sci. Instrum. / PR Applied.

**Status:** bench-gated; the two-photon linewidth is **the same measurement as P1's go/no-go**. Merge-vs-standalone is a PI call (default standalone).

**Authorship:** Dondi (first), Marchesini (apparatus lineage), Minardi/Prevedelli.

**Figures (~3):** (1) architecture — seed→EOM→colours, the common-mode cancellation, dual-end vs single-ended-tagged; (2) spurious-comb / intermod audit (2.4×10⁻⁷) + the EIT→thermometry RF switch; (3) the measured two-photon linewidth + the retro-cap β/power table.

**Outline:** (i) two-colour cooling/EIT usually needs an OPLL or microwave-locked pair — a single-EOM common-mode approach is simpler and telecom-leveraged; (ii) architecture + common-mode argument + the two delivery options + retro-cap non-binding; (iii) the comb/intermod budget + RF switching + EOM depth/power; (iv) results — measured two-photon linewidth, demonstrated switching/cleanliness; (v) where it helps (guided, fibre-integrated, transportable) — honest scope: clean engineering, not a breakthrough.

**In hand [V]:** architecture, spurious-comb audit, EIT→thermometry switch, retro-cap. **Needs bench:** measured two-photon linewidth; demonstrated switching + comb cleanliness.

**Novelty/framing:** economical, citable engineering — *not* a breakthrough (OPLLs/combs are standard); say so.

**Positioning (Lan/Yb):** telecom-leveraged, OPLL-free, fibre-integrated → attractive for transportable/integrated systems; a methods credential.

**Backing:** `docs/operating_point.md` (§1b, §3), `docs/reference/delivery/single_EOM_sequence.md`, `docs/reference/delivery/architecture_delivery_thermometry.md`.

---

## Paper P3 — Cooling physics: the cloud floor and the EIT-tolerant / RSC-fragile regime  ·  **P1 BACKBONE (not standalone)**

> **Status update 2026-06-17 — see `novelty_findings.md`.** All three pillars are established
> physics: the EIT-tolerant/RSC-fragile contrast is the well-known **EIT bandwidth advantage**; the
> inhomogeneous-light-shift cloud floor is named in the HCPCF literature (arXiv:1812.02887;
> magic-wavelength HCPCF; fibre-interferometer DLS dephasing); outside-Lamb-Dicke recoil-limited
> cooling is a developed subfield (Yu–Ni, PRA 97, 063423 (2018)); and the prospective host group
> already does in-fibre sideband cooling (Wang, PRR 4, L022058 (2022)). The geometry-specific floor
> is a useful computation but **not a novel-discovery standalone** — keep it as P1's floor budget.

**Working title:** *Radial-temperature limits of sideband cooling in a soft-confinement guided trap: the inhomogeneous-light-shift cloud floor and the EIT-tolerant, Raman-fragile regime.*

**Thesis:** In a guided trap with a soft radial mode the cooling floor is set by the radial cloud sampling the inhomogeneous 1064 light shift (the M3 effect); the floor rises with radial temperature (tail-dominated; the clk2 T_r-gated cloud all-in is **≈0.012 at 100 µK**, superseding the earlier semiclassical ≈0.0095); and **EIT cooling tolerates the radial spread** (its ~150 kHz bright feature covers the ν_z(r) swing) while **RSC is fragile** (its ~16 kHz sideband does not). Addresses the inhomogeneous-broadening limiter the HCPCF field cites.

**Type / venue:** cooling-physics — PRA / PR Applied. **P1's backbone** (the stand-alone option is withdrawn — mechanism is established; see status note).

**Status:** mostly modeling [V]; optionally bench-validated by P1's floor-vs-radial-T scan.

**Authorship:** Dondi (first), Minardi/Prevedelli.

**Figures (~3–4):** (1) the radial mechanism (M1 ν_z(r), M2 Ω(r), M3 differential shift) + profile (`realistic_floor.png`); (2) cloud floor vs radial T — the semiclassical MC (`mb_ensemble_figure.png`), tail-dominated ≈0.012@100 µK [v17; was 0.0095 semiclassical]; (3) the EIT-tolerant/RSC-fragile regime map (150 kHz EIT feature vs 16 kHz RSC sideband vs the ν_z(r) swing); (4, opt.) direct EIT-vs-RSC floor vs radial T.

**Outline:** (i) the field cites inhomogeneous broadening (trap light × radial distribution) — what actually sets the floor in a soft-radial guided trap? (ii) the radial physics (M1/M2/M3; why M3 dominates; the soft-radial η_r≈1 picture); (iii) the cloud floor — the MC sampling positions and the position-dependent rate → floor vs radial T; (iv) the regime map (EIT's broad bright feature covers the swing; RSC's narrow sideband doesn't — ties to Paper T's why-EIT spine); (v) discussion — and the **atom-general** point that the soft radial mode stays recoil-limited *regardless of line narrowness*, so even alkaline-earth narrow-line/clock cooling needs radial compression (the P4 / Sr-relevant result).

**In hand [V]:** v13 M1–M5, the differential-light-shift cloud floor, the semiclassical MC, the regime map. **Needs bench (optional):** floor-vs-radial-T scan; cloud-floor/coverage; direct EIT-vs-RSC comparison.

**Novelty/framing:** correct, useful **geometry-specific** floor budget — but the mechanism and qualitative conclusions are established (incl. by the prospective host group, Wang 2022). Not a discovery; serves as P1's quantitative floor analysis, cited.

**Positioning (Lan/Yb):** **the strongest Sr-relevant piece** — "the soft radial mode is recoil-limited regardless of line narrowness, so you still need compression" is exactly the point for Lan's Sr radial ground-state cooling; the regime map is platform-general.

**Backing:** `src/engines/radial_inhomogeneity.py`, `src/engines/radial_floor_mc.py`, `docs/reference/radial/radial_inhomogeneity_findings.md`, figures.

---

## Cross-paper notes

- **Order (revised 2026-06-17):** **P1 is the first-author anchor** (after the two-photon-linewidth go/no-go); **T and P3 fold into P1** as cited motivation/backbone (neither is a standalone — see `novelty_findings.md`); **P2** is a short standalone methods note; then P4 → applications.
- **T and P3 share the "why EIT, not RSC" spine** (rank-2 suppression + radial fragility) — both become **P1 sections**: T the design rationale (cited to Naber–Spreeuw 2016), P3 the floor budget (cited to the HCPCF / EIT-bandwidth literature).
- **P2 shares P1's critical measurement** (the two-photon linewidth); merge-vs-standalone is a PI call.
- **First-author paper for the Lan application: P1** (the experiment). The "write-now preprint before outreach" plan is **withdrawn** — T and P3 are not novel standalones. Lead the outreach with the **direct platform fit** (Wang 2022 — the host group's own in-fibre cooling) + the thesis-in-progress, not a manufactured-novelty note.
- **Universal honesty flags:** novelty lit-check before *any* abstract; never "first cooling in a fibre"; pitch the program as the **enabling cold field-insensitive source**, with "breakthrough" reserved for the downstream OD-vs-cooling / Rydberg-NLO path (consolidated doc §11).
