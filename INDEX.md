# INDEX — authority router for EIT-in-fiber-cooling

*The single authoritative file per settled question, with its verdict. Read the named file before
acting; do **not** reconstruct an answer from intermediate or superseded files — that is the failure
this index exists to prevent. Last reconciled: 2026-06-22 (**v17** master — folded the four-subversion
delivery×tone matrix, the 1-/2-tone crossover T_r≈120 µK, and the dynamic box-MC confirmation of the
flat-top into the master, and added the PI `cloud_cooling_tool.py`; **no v16 *conclusion* changed** —
a coherence pass corrected stale *displayed* values only: §3 δ₂, §5 dual-floor range. Prior 2026-06-20
v16 floor-correction: SSOT double-count fix + SCOPE→CLAIMS deferral (PR #4); squeezer off-axis
rate-rise **disproven**). In-flux items are flagged §OPEN; do not cite those as final.*

> **Auditing a number? The path is four steps.** (1) Find it in **§1b** (canonical values, one place) or in **[`CLAIMS.md`](CLAIMS.md)** (every headline number → evidence tier `[V]`/`[I]`/`[O]` → the script that establishes it). (2) Note the **convention** in **§3** that decides *which* number a script reports (solve vs all-in, single-atom vs cloud, field vs state-energy δ₂) — most apparent disagreements in this project's history were convention mismatches, not physics. (3) Open the script named in **§5** (validated engines + their gate values) and run it. (4) Run the gates: `python audit/check.py` (the repo consistency gate) and the two `python src/engines/{eit_cooling_tool,cloud_cooling_tool}.py --regression` floors. Engine outputs land in `outputs/` (gitignored), so a clone-and-run stays clean. The `[O]` items in **§4** are *not* settled — do not cite them as final.

---

## 1. Settled questions → authority → verdict

| question | authority file | verdict (one line) |
|---|---|---|
| **Cooling scheme + operating point** | `clock_EIT_consolidated.md` (**v17**) | D2 clock-EIT, m′=0 pair \|1,−1⟩/\|2,+1⟩ → \|F′2,0⟩, **config A** (dark on \|1,−1⟩); Δ≈45 MHz (flat 40–55), Ω_p/Ω_c≈0.10–0.12 (**0.12 nominal**; 0.10 is floor-optimal but ~1.4× slower cooling — §3), δ₂ servoed; ν_z=2π·430 kHz, U₀=1094 µK, η_z=0.094, η_eff(retro)=0.187; magic B=3.2288 G (interrogation), cooling 1–1.5 G. **Four subversions:** A/B (1-tone) / C/D (2-tone) × dual/retro — tone count set by radial temperature (1 tone <120 µK, 2 above; §4, §8). |
| **Leg assignment (config A vs B)** | `docs/reference/scheme/clock_leg_swap_finding.md` (**RESOLVED**) | The swap is **rejected; A holds** (3.8× advantage; B's F=2-interior dark leg can't clear \|2,+2⟩). |
| **Why EIT, not RSC** | `clock_EIT_consolidated.md` §I/§II | On the Δm=2 field-insensitive pair, RSC hits a **rank-2 destructive-interference obstruction** (Σg=0 → floor ~0.45); EIT escapes it. Cited as established (Naber 2016), not new. |
| **Excited state at 1064 (anti-trap potential)** | `docs/reference/excited_state/polarizability_5P32_1064.md` | 5P₃/₂ **anti-trapped** at 1064 (α₀≈−1149 a₀³); **\|F′2,0⟩ pure scalar +38.1 MHz** (F′=2 tensor term vanishes → geometry-independent). |
| **Anti-trap FLOOR (m′=0)** | **`docs/reference/floor/ANTITRAP_RESOLUTION.md`** | Repump-**dwell**-gated **~0.01–0.05, pinned not runaway**. Low-dwell (P_e_rep~4e-5) → faithful bulk **~0.01**; high-dwell (~3.5e-4) → ~0.03–0.05. The grid 0.03→0.10 growth is a **boundary artifact**, not a floor. Point-number for a chosen repump = workstation/sparse-iterative job. |
| **Floor budget / all-in** *(corrected; SSOT committed to PR #4 — see §3)* | `operating_point.py` (SSOT) **+ the §3 convention** | **single-atom on-resonance ≈ 0.008–0.010** (low-dwell, **CERTIFIED**). **High-dwell** = **RETIRED** (measured low-dwell: clk2 config-A P_e(F′1)=8.4×10⁻⁶, 5× below the 4×10⁻⁵ low-dwell ref → the 0.03–0.05 branch does not apply; certified floor stands). **Cloud-limited = [O]** = cooling(r) + squeezer integral. **Cooling half CHARACTERIZED** (dynamic MC: realized sits *below* quasi-static — W(r) peaks at the cold center, anti-correlated with n_ss(r) → frozen 0.0126 superseded, dynamics benign; **3-level engine ⇒ ratio result**, clock magnitude pending). **Squeezer half [O] but DE-RISKED** (clk2: P_e(F′2)(r) measured *falls* off-axis — M3 is a common shift, δ₂ preserved, dark state stays dark → heat rate R_sq falls to 0.32× at r=10; the "rate-rise" driver is **disproven**. Only the 1/W tail amplification remains, which the cooling dwell-weighting defeats → likely **cloud ≈ single-atom ≈ 0.008–0.010**; magnitude confirm = MC dwell-weighted integral, **not sign-deciding**). **Cloud all-in ≈ 0.007/0.012/0.022 at T_r=25/100/400 µK** [I, cross-engine], **T_r-gated** → cloud ≈ single-atom (~0.012) if radial-cooled to ~100 µK. Old **0.012–0.019** / **0.012–0.017** withdrawn (§3, §4). Single-atom edges = the two delivery configs (dual-end 0.0048 / single-tagged **0.0072**), each + 0.003 squeezer once. |
| **Realized floor < GATE A (0.003 vs 0.0072)** | `docs/reference/floor/floor_gap_resolution.md` | GATE A (`clean_lambda=True`) and the realized floor are the **same solver in two modes**; the gap is recoiler-closure, not a reduced engine. |
| **D1 vs D2** | `docs/reference/excited_state/D1_hybrid_findings.md` | **D1 ruled out** — no floor gain, line-independent binding, F′1 inversion 1.65× worse; α₀(5P₁/₂,1064)≈−1254 a.u. (every-leg r=−1.78, worse than D2). Do not model D1. |
| **Retro geometry** | `docs/archive/scheme_comparison.md` (reflection rule) | Retro EIT **viable**; m′=2 + bare mirror favorable; dual-end vs retro is an **engineering trade**, not a physics result. Reflection rule is **optic-dependent** (name the optic before quoting Δm). |
| **Delivery / laser architecture** | `docs/reference/delivery/laser_architecture_comparison.md` + `docs/reference/delivery/single_EOM_sequence.md` | **All-fiber, single 1560 nm EOM → SHG 780**, common-mode (no OPLL). Dual-end carrier-suppressed (β=2.405) preferred; single-end tagged retro (2f_A=400 MHz down-shift) fallback. |
| **Thermometry** | `docs/thermometry.md` (consolidated) | Sideband-asymmetry on the cooling pair \|1,−1⟩↔\|2,+1⟩ **directly** (no park — both field-insensitive), Blackman-shaped, calibrated R. **Open:** the readout is **Δm=+2**, and that pair's transition-specific spectral env (nearby-line Fano, red/blue AC-Stark) is **relabeled from the Δm=0 audit, not re-derived** — needs a multilevel Δm=+2 readout sim (`docs/thermometry.md` §5). |
| **Alternatives sweep (all dead ends)** | `clock_EIT_consolidated.md` §10 (PART II) | Leg-swap, EOM-Raman clearer, D1 pivot/hybrid, D1-Raman repump, recoil-routing — **all closed**. Recurring lesson: **repump topology** decides leg/recycle questions, not the diffusion/branching lever. |

---

## 1b. Canonical numbers (SSOT) — reference this; do not restate

*All rows are the **m′=0 clock** scheme at the **v17 operating point** (Δ=+45, OmR=0.12 nominal, 2f_A=400). Quote with the convention + solver shown; do **not** mix with the superseded m′=2 audit numbers (note at end).*

| quantity | value | scheme / point | solver (convergence) | tier |
|---|---|---|---|---|
| axial floor, dual-end (**all contaminants, coherent**) | **~0.005–0.006** | m′=0, OmR 0.10→0.12 | `eit_cooling_tool` (F′0–3 as coherent ladder edges + repumps ⊗ Fock): 0.0051@0.10 / **0.0059@0.12** converged; 0.0048 at the Nf=6 gate | [V] |
| ↳ clean base / clk2-raw (no F′1-spoiler, no F′3) | **~0.0014–0.0021** | m′=0, Δ=45 | `eit_cooling_tool` base (contaminants off) 0.0014 · clk2 (F′1-repump-only engine) ~0.0021 | [V] |
| axial floor, single-tagged | **~0.0072** | m′=0, 2f_A=400 | `tagged_solver` / clk2 | [V] |
| certified single-atom all-in | **0.008–0.010** | m′=0, low-dwell | solve + 0.003 squeezer (once) | [V]/[I] |
| cloud floor, Gaussian | **0.007 / 0.012 / 0.022** | T_r = 25/100/400 µK | clk2 quasi-static × 3-level MC | [I] |
| cloud floor, flat-top (box) | **cooled 0.0072 (100µK) [V, Nf-conv]; uncooled ≥0.021 and rising (556µK) [O]** | dead-wall: flat-top collapses the cloud far below **Gaussian (0.024/0.099)** at every T_r (the lever, holds qualitatively); cooled-cloud floor settled, hot-cloud digit Nf-divergent. **The Nf=6 0.0118 is RETRACTED (under-resolved — see footnote).** | `cloud_multilevel_union` (eit-tool coherent⊗Fock on the radial grid); cooled 0.0072 Nf-converged (+1.4% Nf6→Nf8); uncooled ≥0.021 @Nf8 (drift +79% & growing → cluster-pending); single-rate closure **[V]** at the r=0–3 floor-bearing core (r=0 0.92/0.98, r=3 0.97/0.99; 98%-resolved) | cooled **[V]** / hot **[O]** cluster-pending #4 |
| δ₂ set-point | **−0.10 dual / −0.19 single** | **field convention** (probe−transition) | ccs3 / clk2 (see §3) | [V] |
| Δ (single-photon) | **+45 MHz** (flat 40–55) | m′=0 | clk2 / tagged | [V] |
| Ω_p/Ω_c (OmR) | **0.12 nominal** (0.10 floor-optimal, ~1.4× slower) | m′=0 | §3 | [V] |
| 1-/2-tone crossover | **T_r ≈ 120 µK** | Gaussian | `cloud_cooling_tool` | [I] |

*The all-contaminant 0.0048–0.0059 is a **coherent** solve (F′1/F′3 are Hamiltonian ladder edges, `eit_cooling_tool.py:730–736`), not a federated sum — the "+0.0034 F′1" is a coherent toggle. **Scope of "coherent F′1":** the cooling-beam spoiler (control→F′1 *and* probe→F′1) carries **both** the coherent coupling *and* full m-resolved spontaneous decay + recoil (`:817–879`) — not coupling-only; the lone F′1 approximation is the **single-end** parasitic retro-carrier leak (~88 MHz, F=2→F′1), a linearized dissipator laddered to F′2/F′3 only (flagged, not in ⟨n_z⟩; SCOPE §6), and the **dual-end headline sets `with_rejected=False`** (no rejected tones) so its F′1 is fully coherent. clk2-raw (0.0021, F′1-repump-only) + a perturbative F′1 (+0.0034) would give ~0.0055 additive; the coherent solve lands **below** that (0.0048) → sub-additive, and that coherent solve **is** the m′=0 verification of the additivity (the m′=0 analog of the m′=2 `combined_solve`). So m′=0 single-atom additivity is **not** open; the open m′=0 seam is the cloud × multilevel union (§4).*

*Cloud × multilevel union — the hot-end retraction (2026-06-23). The grid8→compare run showed the Nf=6 **hot**-cloud floor was itself **under-resolved**: the Nf6→Nf8 floor drift is **+1.4% (cooled 100 µK box)** but **+79% (uncooled 556 µK box)** and growing, with per-radius n_ss drift rising off-axis (r=18 +27%, r=21 +30%) — exactly the radii (n_ss > 1 at r ≥ 12) that dominate the hot-cloud weighting. So **one under-resolved grid produced two wrong-looking-right results**: the 0.0118 floor *and* the expectation that off-axis W-suppression would converge the hot floor (**FALSIFIED** — those radii carry real floor weight; the 3-level baseline and Nf=6 both under-resolved them, so it looked consistent). **Retraction:** the **cooled** box floor **0.0072 is settled [V]** (Nf-converged); the **uncooled** box floor is a **non-converged lower bound ≥0.021 @Nf8 [O]**; the **Nf=6 0.0118 is retracted** (under-resolved — **not** merely re-tagged). The flat-top-collapses-the-cloud **lever holds qualitatively** at every T_r, but "collapses to ≈ on-axis" holds **only for the cooled cloud**. **Acceptance bar for the uncooled digit:** settled when the hot-box floor's successive-Nf drift is < few % at the off-axis radii (requires Nf ≫ 8 → cluster). This is the §3 recurring-failure-mode class — an instrument read out of its resolved range.*

*The `eit_cooling_tool --regression` gate runs **Nf=6 for speed** and prints ~0.0048 (the eit-tool **underconverged** at the operating OmR=0.12); the **converged operating-point floor is ~0.0059**. The gate is a fast smoke test, **not** the converged floor. (Separately, clk2's `__main__` anchor 0.0048 is at Δ=80/OmR=0.25 — a different point; do not equate it with the gate value.)*

*Superseded m′=2 audit — do **not** mix into the rows above: `combined_solve.py` 0.0206/0.0178, δ₂ −0.15 (field) / +0.20 (state-energy), at Δ=40/OmR=0.25/2f_A=220 — the swapped scheme the leg-swap finding **rejected**. Its [I1] additivity closure is for **that** scheme. The m′=0 single-atom headline is the **`eit_cooling_tool` coherent all-contaminant solve** (F′1/F′3 are coherent ladder edges) — its sub-additivity vs clk2-raw + perturbative-F′1 is the m′=0's own verification, so it is **not** underwritten by the m′=2 result and is **not** open. The one m′=0 additivity seam that remains open is the **cloud × multilevel union** (§4).*

---

## 2. Do NOT mistake these (intermediate / superseded — look authoritative, are not)

- **`recycle_dwell_S3.py`** — a D1/hybrid recycle-**traffic** tool (N_cool/N_rep per leak). **NOT the anti-trap floor authority.** Its `n_floor=0.077…` Markov estimate is superseded by `ANTITRAP_RESOLUTION.md`. *(This exact mistake was made and caught 2026-06-20.)*
- **`antitrap_kernel_grid.py` grid steady-state runaway (0.03→0.10)** — a truncation/boundary **artifact** (`ANTITRAP_RESOLUTION.md:22–23`), not a physical floor. The closed-form **kernel** (0.031 m′=0, 0.018 F′1) IS valid; the grid *steady state* runaway is not.
- **`operating_point.py` `all_in_single_atom = (0.012, 0.019)`** [the OLD field] — was **double-counted** (`antitrap_leak_increment=0.007` is the *no-squeezer bulk* ≈ the solve floor). **FIXED 2026-06-20** (committed PR #4): the field is now `squeezer_increment_lowdwell = 0.003` (scalar) and `all_in_single_atom_lowdwell` = solve + squeezer ≈ **0.008–0.010**. **Any copy still showing (0.012, 0.019) or `antitrap_leak_increment` is pre-correction — discard.**
- **The `EIT_brief` lineage (`v11` / `v12` / `v17`)** — **superseded**; the **current master is `clock_EIT_consolidated.md` v17** (the v17 brief's four-subversion matrix + box-MC are folded into master §4/§8). The briefs are **not kept as files** — see git history for v11/v12 (D1 §12, the five-column comparison). Do not cite them for the current floor.
- **`clock_EIT_consolidated.md` v14 / v15 / v16** — superseded by the current **v17** master. Re-sync project knowledge from the live docs (use `INDEX.md` as the authority map).
- **Any `docs/reference/scheme/clock_leg_swap_finding.md` headed "[O] swap favored"** — the **RESOLVED** version ("swap rejected; A holds") supersedes it.
- **`v12_plan.md` / `D1_hybrid_plan.md` / `v12_decision.md`** — process scaffolding; conclusions are in v16 / the findings docs.

---

## 3. Load-bearing conventions (state these before quoting any floor number)

**The increment convention** *(the single cause of three contested floor numbers this session)*.
The solve floor (`src/engines/clk2.py`, config A = 0.0048; `:234` puts one ground frequency on all internal
states) is **traffic-in, anti-trap-potential-out** — i.e. the *no-squeezer* quantity. The only
honest thing to add is the **squeezer heat** = faithful − no-squeezer ≈ **0.003** (= the recoil
bound). **Do NOT add the no-squeezer bulk (~0.007)** — that double-counts the traffic floor. The
single-atom on-resonance floor **IS the faithful bulk ~0.01**, *not* solve + bulk. Re-emit any
all-in as a tagged sum: `solve [traffic-in/potential-out] + squeezer [+~0.003, increment] →
on-resonance ~0.008–0.010 (low-dwell)`. **High-dwell** breaks the decomposition (clk2 must be
re-solved; the grid 0.026–0.053 upper is the contaminated-Fock *artifact*, not a value). **Cloud**
is **not** on-resonance + flat increment — it needs the radial integral `⟨cooling(r) + squeezer(r)⟩`,
and **both halves now favor the cold center**: cooling realized sits *below* quasi-static (W(r)
W-weighted, peaks cold), and the squeezer is **DE-RISKED** — P_e(F′2)(r) *falls* off-axis (the M3
shift is **common** to both legs, δ₂ unchanged, dark state preserved) so R_sq=P_e·kernel falls to
**0.32× at r=10 µm**; the off-axis **rate-rise is DISPROVEN**, not sign-uncertain. Result: cloud
all-in ≈ **0.007/0.012/0.022** at T_r=25/100/400 µK [I, cross-engine], **T_r-gated**. Only the
dwell-weighted magnitude confirm remains (**[O], not sign-deciding**).

**The repump-dwell caveat.** The anti-trap floor is **dwell-gated ~0.01–0.05**. Low-dwell (~0.01) is
**design intent, not a result** — the adopted F′=1 EIT repump (`src/engines/clk2.py:135`) sits on the exact leg
`ANTITRAP_RESOLUTION.md` flags as the dwell bottleneck. Only **RSC-to-\|F=2,m=0⟩** forces low dwell
*structurally*. The F′=1 dwell is now **MEASURED** (clk2 config-A P_e(F′1)=8.4×10⁻⁶, 5× below the 4×10⁻⁵ low-dwell ref) → **firmly low-dwell; the 0.03–0.05 high-dwell branch is RETIRED**, the certified ~0.008–0.010 stands, and the 0.003 squeezer increment is conservative.

**The η convention.** η_z=0.094 is **symmetric**; the 3.8× config-A advantage is **relative**. Don't
misread the dual-end 0.0048 against the single-tagged **0.0072**.

**The OmR convention.** Operating nominal is Ω_p/Ω_c=**0.12** (SSOT `OP.OmR`); the dual-end floor and
the cooling-time/semiclassical scans are characterized at the low-probe edge **0.10** (the §6
optimum). The dual floor is F′1-dominated and ~OmR-robust at ~0.005 across 0.10–0.12, so the label is
harmless — but **don't read 0.10 as the operating point** (0.10 was also the OmR of the superseded
v12 Δ=55/OmR=0.10 point; the §5 floor table is at Δ=45 now).

**The δ₂ sign convention.** Canonical is the **field convention** (δ₂ = probe − transition; CLAUDE.md +
the public `eit_cooling_tool.py`): the servoed two-photon-detuning optimum is **slightly negative** —
**≈ −0.10 (dual) / −0.19 (single) at the v17 point** — because it tracks the ≈ −0.2 MHz e3-Stark shift
of the dark resonance. **`tagged_solver.py` uses the opposite parameterization** (the |g2⟩ *state
energy*, `+d2·P(g2,g2)`), so it reports the same servo point with the **opposite sign** — its optimum
is **d2 = +0.20** (verified). Same physics; **quote δ₂ negative** in the field convention. Magnitudes
vary with the operating point (OmR, 2f_A, B): the canonical v17 numbers are −0.10/−0.19; older delivery
docs at 2f_A=300 / B=1 G read ≈ −0.13/−0.25.

**The solve-vs-all-in label.** "single-atom 0.005/0.0072" (clk2) = **solve only** (potential-out);
"all-in" = solve + anti-trap + cloud. The word "single-atom" is **overloaded** between files — always
state which quantity.

**Honesty rails (headline).** Report **AXIAL** ground state (not 3D); claim **n̄_z ≲ 0.01–0.02**;
"**first EIT cooling in a fibre**" (Leong 2020 = RSC); radial mode is an **input/limit**, not a result.

**The recurring failure mode (and its guard).** The single most common error in this project is *a
setting valid at one operating point reused where it is not* — caught ≥5×: the Nf=6 gate floor
(0.0048) read as the converged floor (it is 0.0059); the 7× three-level cloud elevation carried from
the cold end to the hot end (it is 27×); the README "refs/ never committed" claimed but unenforced in
`.gitignore`; the closure-check window tuned for on-axis W reused at off-axis r=9 (it resolved 1.6%,
giving fit-noise); and the **Nf=6 hot-cloud floor 0.0118**, believed because Nf=6 under-resolved the
very off-axis radii (n_ss > 1 at r ≥ 12) that dominate the hot-cloud weight — so one under-resolved
grid produced **two** wrong-looking-right results (the floor *and* the "W-suppression converges the
hot floor" expectation, FALSIFIED; the 0.0118 is retracted, §1b). **The principle behind all five:**
*a number is not trustworthy until the instrument that produced it has demonstrated it resolves the
regime that dominates the number* — the closure prints its resolved fraction; the floor must show
< few-% successive-Nf drift at the radii that carry its weight. **Guard:** an instrument must
**self-report its valid range** so it cannot pass silently out of range (e.g. `cloud_multilevel_union`'s
closure now prints the resolved fraction), and **every number carries the qualifiers it was computed
under** (Nf, T_r, operating point, convention).

---

## 4. OPEN / in-flux — NOT settled, do not cite as final

- **✅ DONE `operating_point.py` double-count fix** (2026-06-20) — `antitrap_leak_increment=(0.007,0.012)` replaced by the squeezer increment (~0.003, once); `all_in_single_atom_lowdwell` = solve + squeezer ≈ 0.008–0.010 [I, low-dwell]; high-dwell + cloud carried as [O]. **Committed to PR #4** (claude/floor-correction, gate-green); the SSOT `SCOPE` now **defers detection/survival to CLAIMS D-/S-series** (no independent tier — an unintentional `[O]` metadata downgrade was reverted).
- **✅ DONE (2026-06-20) repump-dwell measurement** — clk2 config-A F′=1 dwell **P_e(F′1)=8.4×10⁻⁶**, 5× below the low-dwell ref (4×10⁻⁵) → **firmly low-dwell; high-dwell branch (0.03–0.05) retired**; certified ~0.008–0.010 stands (and the 0.003 squeezer increment is conservative). Proxy clk2 pe_F1 ~ grid P_e_rep is **[I]** (auditor to vet); F′2 residual 1.8×10⁻⁵ cross-checks dark-state ~4×10⁻⁵. The dense-ME high-dwell re-solve is now needed *only if the dwell proxy is contested*.
- **[O] radial squeezer integral — input now COMPUTED; only the dwell-weighted assembly remains.** P_e(F′2)(r) measured on clk2 (`radial_pe.py`): it **falls** off-axis (1.53→0.88 ×10⁻⁵ over r=0–10 µm; M3 common shift preserves δ₂/dark state), so R_sq(r)=P_e·kernel **falls to 0.32× at r=10** — the "rate-rise" half is **disproven**, not sign-uncertain. The remaining question is only whether the dwell-weighting beats the off-axis 1/W tail (it did for cooling). Fold R_sq(r) into the MC ⟨n⟩-ODE (anchored to faithful 0.003 on-axis) and dwell-weight; expected cloud ≈ single-atom ≈ 0.008–0.010. Brief: `audit_squeezer_integral_MC.md`.
- **✅ DONE (2026-06-20) Radial dynamic MC (S3)** — cooling half of the cloud: realized sits **below** quasi-static (W(r) peaks at the cold center, anti-correlated with n_ss(r)) → **frozen bound 0.0126 superseded; radial cooling dynamics are benign**. **3-level engine ⇒ RATIO result** (suppression ~1.2×/3.0×/7.4× at 25/100/400 µK *within its own bracket*), NOT the clock floor. Pipeline `mc.py`/`grid_build.py`/`engine.py` + fig `s3_radial_mc.png`. Provenance note: the brief's 0.0085 semiclassical-MC driver was **not in the file set** (asserted [V] in `clock_EIT_consolidated.md §8`, generating code absent). Clock-engine magnitude = clk2 per-radius re-run [O].
- **In-fiber radial temperature** — 556 µK (loaded/uncooled) vs ~100 µK (cooled upstream). Gates the cloud floor **and** P1 §IV.B.
- **Flat-top** — flatness spec ≤3% over ±6 µm (frozen, provisional; S3 relaxes it); ~1.3–1.7× mover *conditional on low-dwell repump*. Fiber feasibility (mode content @1064, walk-off over 2 m, contrast) → XLIM. Briefs: `flat_top_feasibility.md`, `flatness_spec_result.md`.
- **6.835 GHz two-photon linewidth** — the bench-gated binding measurement (sub-100 Hz?). P1 hinges on it.
- **[O] two figure regens (compute-bound) — flagged by the 2026-06 figure red-team.** `fig_retro_flatness` plots ~0.0049 (the config-A on-axis floor) for the single-ended tagged 2f_A=400 floor, whose canonical value is **0.0072** (`operating_point.md` §3) — magnitude stale; removed from the master, disclosed in Ch 03. `fig_delta2_landscape` shows δ₂=+0.25 (tagged_solver state-energy sign); canonical is **−0.19 field** (§3). Both need a `tagged_solver` re-run (numpy<2 / cluster, ~min/solve) to refresh the *pixels* — the captions already carry the canonical numbers. *(The cloud-floor figure gap is **closed**: `fig_cloud_floor_multilevel.py`, baked from §1b, now in the master + Ch 06.)*

---

## 5. Validated engines (all in `src/engines/`)

Support tools (diagnostics, paper-T computations, sensitivity checks) live in `src/tools/`.

| engine | role | gate |
|---|---|---|
| `clk2.py` | deciding-run solver = base + hooks (swap/rep2mode/clearer/want_fock) | config A = 0.0048; clean-Λ A=0.0072 / B=0.0022 |
| `clock_combined_solve.py` | the validated **base** clk2 is built on | clean-Λ = 0.0072 |
| `tagged_solver.py` | validated tagged-EIT steady-state solver (single-ended retro) | constants gate-checked by `audit/check.py` |
| `eit_cooling_tool.py` | PI **axial** tool (embeds the engine, self-checking; `--regression`) | dual ~0.0048 / single ~0.0072 (v17 preset, Nf=6 gate) |
| `cloud_cooling_tool.py` | PI **radial/cloud** tool (box flat-top + two-tone; `--regression`) | box→on-axis ∀T_r **[3-level engine; the multilevel hot-cloud digit is non-converged, §1b]**; 1-/2-tone crossover ~120 µK |
| `antitrap_kernel_grid.py` *(not shipped — analysis in `ANTITRAP_RESOLUTION.md` + git history)* | anti-trap **kernel** (valid) + grid (steady-state runaway = artifact) | normal-trap grid = Fock = 0.0085 |
| `raman_sbc.py` | RSC engine (anchors the RSC-vs-EIT comparison) | — |
| `cloud_multilevel_union.py` | cloud × multilevel union: eit-tool n_ss(r)/W(r) on the radial grid → dead-wall MC (modes: grid/grid8/compare/closure/nf/defang) | engine sound (produced the citable cooled floor **and** exposed its own hot divergence): cooled box-cloud **0.0072 @100µK [V, Nf-conv]**; uncooled @556µK Nf-divergent → **≥0.021 @Nf8, cluster-pending** (the Nf=6 0.0118 retracted as under-resolved); closure HOLDS r=0–3 (0.92/0.98, 0.97/0.99; 98%-resolved) |

*Support tools in `src/tools/` (import engines; not in the validated set): `flatness_spec.py` (per-depth floor spec), `radial_pe.py` (per-radius P_e on clk2), `grid_avg_cloud.py` (Boltzmann cloud average), `dwell.py` (F′=1 repump dwell), `detection_snr.py`, `rsc_floor_rate_eqn.py`, `paper_T_fom.py`, and others.*

---

## 6. Document map — every doc, grouped (so nothing is orphaned)

*New-reader order: [`README.md`](README.md) (the front door — map + the narrative chapter guide) → the [`docs/guide/`](docs/guide/) chapters → [`START_HERE_simulations.md`](START_HERE_simulations.md) → this index → the master. §1 above gives the authority + verdict per **settled question**; this map lists **every** file by topic. The repo is three layers: **narrate** (the README chapter guide + `docs/guide/`), **run** (`START_HERE` + `src/`), **reference** (this index → master → `docs/reference/` → `CLAIMS`/`SCOPE`).*

**Governance / entry**
- [`README.md`](README.md) — **the front door**: map, headline, the narrative chapter guide, trust gates · [`START_HERE_simulations.md`](START_HERE_simulations.md) — run/tune the two PI tools
- [`CLAIMS.md`](CLAIMS.md) — audited ledger (number → tier → script) · [`SCOPE.md`](SCOPE.md) — what the model covers / omits · [`CLAUDE.md`](CLAUDE.md) — working guide
- **Subsystem READMEs:** [`audit/`](audit/) — constants gate-check (`check.py`) · [`src/radial_mc/`](src/radial_mc/README_radial_mc.md) — the S3 radial-MC subsystem · [`figures/`](figures/) — publication figures

**The narrative — chapters (`docs/guide/`)** *(pedagogical; narrates over the master, links here for canonical numbers; the cover, headline, and chapter TOC are now in [`README.md`](README.md))*
- [`01 · apparatus & sequence`](docs/guide/01_apparatus_and_sequence.md) · [`02 · cooling scheme`](docs/guide/02_cooling_scheme.md) · [`03 · laser & delivery`](docs/guide/03_laser_and_delivery.md) · [`04 · operating point`](docs/guide/04_operating_point.md)
- [`05 · axial floor`](docs/guide/05_axial_cooling_floor.md) · [`06 · cloud floor & dead-wall`](docs/guide/06_cloud_floor_and_deadwall.md) · [`07 · thermometry & analysis`](docs/guide/07_thermometry_and_analysis.md) · [`08 · running & optimising`](docs/guide/08_running_and_optimizing.md)

**Authorities (`docs/`)**
- [`docs/clock_EIT_consolidated.md`](docs/clock_EIT_consolidated.md) — **THE MASTER (v17)**: technical state + conceptual path
- [`docs/operating_point.md`](docs/operating_point.md) — operating-point notes (SSOT = `src/engines/operating_point.py`) · [`docs/thermometry.md`](docs/thermometry.md) — **consolidated thermometry authority** (readout method + spec)

**Reference · scheme (`docs/reference/scheme/`)**
- [`clock_RSC_resolution.md`](docs/reference/scheme/clock_RSC_resolution.md) — why EIT, not RSC (rank-2 obstruction)
- [`clock_leg_swap_finding.md`](docs/reference/scheme/clock_leg_swap_finding.md) — config A vs B (**RESOLVED**: A holds ~3.8×)

**Reference · delivery (`docs/reference/delivery/`)**
- [`laser_architecture_comparison.md`](docs/reference/delivery/laser_architecture_comparison.md) — single 1560 nm EOM → SHG, all-fiber
- [`single_EOM_sequence.md`](docs/reference/delivery/single_EOM_sequence.md) · [`full_sequence_config.md`](docs/reference/delivery/full_sequence_config.md) — full pulse sequence on one EOM · [`architecture_delivery_thermometry.md`](docs/reference/delivery/architecture_delivery_thermometry.md) — laser/delivery overview

**Reference · floor / anti-trap (`docs/reference/floor/`)**
- [`ANTITRAP_RESOLUTION.md`](docs/reference/floor/ANTITRAP_RESOLUTION.md) — anti-trap floor (dwell-gated ~0.01–0.05) · [`floor_gap_resolution.md`](docs/reference/floor/floor_gap_resolution.md) — GATE A vs realized floor (one solver, two modes)

**Reference · radial / cloud (`docs/reference/radial/`)**
- [`radial_inhomogeneity_findings.md`](docs/reference/radial/radial_inhomogeneity_findings.md) · [`radial_survival_findings.md`](docs/reference/radial/radial_survival_findings.md) — radial-cloud floor + survival
- [`audit_radial_dynamic_MC.md`](docs/reference/radial/audit_radial_dynamic_MC.md) · [`audit_squeezer_integral_MC.md`](docs/reference/radial/audit_squeezer_integral_MC.md) — dynamic-MC audits (cooling / squeezer halves)
- [`flat_top_feasibility.md`](docs/reference/radial/flat_top_feasibility.md) · [`flatness_spec_result.md`](docs/reference/radial/flatness_spec_result.md) — flat-top mode feasibility + flatness spec

**Reference · thermometry / detection (`docs/reference/thermometry/`)**
- [`thermometry_findings.md`](docs/reference/thermometry/thermometry_findings.md) — detailed falsification audit (readout-pair superseded; see `thermometry.md` §1) · [`detection_findings.md`](docs/reference/thermometry/detection_findings.md) — detection / SNR

**Reference · excited-state (`docs/reference/excited_state/`)**
- [`polarizability_5P32_1064.md`](docs/reference/excited_state/polarizability_5P32_1064.md) — 5P₃/₂ scalar polarizability / anti-trap at 1064 · [`D1_hybrid_findings.md`](docs/reference/excited_state/D1_hybrid_findings.md) — D1 route (**ruled out**)

**Papers (`docs/papers/`)**
- [`P1_draft.md`](docs/papers/P1_draft.md) — P1, the in-fibre cooling paper
- [`paper_T_skeleton.md`](docs/papers/paper_T_skeleton.md) + [`paper_T_core_derivation.md`](docs/papers/paper_T_core_derivation.md) — **Paper T** = the rank-2 RSC-**obstruction theory** paper (*not* thermometry, despite the "T")
- [`per_paper_outlines.md`](docs/papers/per_paper_outlines.md) · [`novelty_findings.md`](docs/papers/novelty_findings.md) · [`paper_planning_memo.md`](docs/papers/paper_planning_memo.md) · [`SUBMISSION_CHECKLIST.md`](docs/papers/SUBMISSION_CHECKLIST.md)

**Archive (`docs/archive/`)** *(superseded but preserved; superseded briefs live in git history)*
- [`scheme_comparison.md`](docs/archive/scheme_comparison.md) · [`configuration_tradeoffs.md`](docs/archive/configuration_tradeoffs.md) — v12 snapshots *(numbers superseded by the master, reasoning kept)* · [`CONSOLIDATION_PLAN.md`](docs/archive/CONSOLIDATION_PLAN.md) — PR#4 consolidation record · [`archive/README.md`](docs/archive/README.md) — anti-museum policy

---

*Maintenance: re-reconcile this index whenever a floor number, an authority file, or a convention
changes. The protective value is the §2 "do not mistake" list and the §3 conventions — keep those
current. The findings docs are grouped under `docs/reference/<topic>/`; the authorities
(master, `operating_point.md`, `thermometry.md`) stay at `docs/`; the pedagogical narrative is
the README chapter guide + `docs/guide/`. When a doc moves, fix its links and re-run the link/orphan checker.*
