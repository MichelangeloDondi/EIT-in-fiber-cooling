# INDEX — authority router for EIT-in-fiber-cooling

*The single authoritative file per settled question, with its verdict. Read the named file before
acting; do **not** reconstruct an answer from intermediate or superseded files — that is the failure
this index exists to prevent. Last reconciled: 2026-06-22 (**v17** master — folded the four-subversion
delivery×tone matrix, the 1-/2-tone crossover T_r≈120 µK, and the dynamic box-MC confirmation of the
flat-top into the master, and added the PI `cloud_cooling_tool.py`; **no v16 *conclusion* changed** —
a coherence pass corrected stale *displayed* values only: §3 δ₂, §5 dual-floor range. Prior 2026-06-20
v16 floor-correction: SSOT double-count fix + SCOPE→CLAIMS deferral (PR #4); squeezer off-axis
rate-rise **disproven**). In-flux items are flagged §OPEN; do not cite those as final.*

---

## 1. Settled questions → authority → verdict

| question | authority file | verdict (one line) |
|---|---|---|
| **Cooling scheme + operating point** | `clock_EIT_consolidated.md` (**v17**) | D2 clock-EIT, m′=0 pair \|1,−1⟩/\|2,+1⟩ → \|F′2,0⟩, **config A** (dark on \|1,−1⟩); Δ≈45 MHz (flat 40–55), Ω_p/Ω_c≈0.10–0.12 (**0.12 nominal**; 0.10 is floor-optimal but ~1.4× slower cooling — §3), δ₂ servoed; ν_z=2π·430 kHz, U₀=1094 µK, η_z=0.094, η_eff(retro)=0.187; magic B=3.2288 G (interrogation), cooling 1–1.5 G. **Four subversions:** A/B (1-tone) / C/D (2-tone) × dual/retro — tone count set by radial temperature (1 tone <120 µK, 2 above; §4, §8). |
| **Leg assignment (config A vs B)** | `clock_leg_swap_finding.md` (**RESOLVED**) | The swap is **rejected; A holds** (3.8× advantage; B's F=2-interior dark leg can't clear \|2,+2⟩). |
| **Why EIT, not RSC** | `clock_EIT_consolidated.md` §I/§II | On the Δm=2 field-insensitive pair, RSC hits a **rank-2 destructive-interference obstruction** (Σg=0 → floor ~0.45); EIT escapes it. Cited as established (Naber 2016), not new. |
| **Excited state at 1064 (anti-trap potential)** | `Rb-87_5P3_2_Scalar_Polarizability_…md` | 5P₃/₂ **anti-trapped** at 1064 (α₀≈−1149 a₀³); **\|F′2,0⟩ pure scalar +38.1 MHz** (F′=2 tensor term vanishes → geometry-independent). |
| **Anti-trap FLOOR (m′=0)** | **`ANTITRAP_RESOLUTION.md`** | Repump-**dwell**-gated **~0.01–0.05, pinned not runaway**. Low-dwell (P_e_rep~4e-5) → faithful bulk **~0.01**; high-dwell (~3.5e-4) → ~0.03–0.05. The grid 0.03→0.10 growth is a **boundary artifact**, not a floor. Point-number for a chosen repump = workstation/sparse-iterative job. |
| **Floor budget / all-in** *(corrected; SSOT committed to PR #4 — see §3)* | `operating_point.py` (SSOT) **+ the §3 convention** | **single-atom on-resonance ≈ 0.008–0.010** (low-dwell, **CERTIFIED**). **High-dwell** = **RETIRED** (measured low-dwell: clk2 config-A P_e(F′1)=8.4×10⁻⁶, 5× below the 4×10⁻⁵ low-dwell ref → the 0.03–0.05 branch does not apply; certified floor stands). **Cloud-limited = [O]** = cooling(r) + squeezer integral. **Cooling half CHARACTERIZED** (dynamic MC: realized sits *below* quasi-static — W(r) peaks at the cold center, anti-correlated with n_ss(r) → frozen 0.0126 superseded, dynamics benign; **3-level engine ⇒ ratio result**, clock magnitude pending). **Squeezer half [O] but DE-RISKED** (clk2: P_e(F′2)(r) measured *falls* off-axis — M3 is a common shift, δ₂ preserved, dark state stays dark → heat rate R_sq falls to 0.32× at r=10; the "rate-rise" driver is **disproven**. Only the 1/W tail amplification remains, which the cooling dwell-weighting defeats → likely **cloud ≈ single-atom ≈ 0.008–0.010**; magnitude confirm = MC dwell-weighted integral, **not sign-deciding**). **Cloud all-in ≈ 0.007/0.012/0.022 at T_r=25/100/400 µK** [I, cross-engine], **T_r-gated** → cloud ≈ single-atom (~0.012) if radial-cooled to ~100 µK. Old **0.012–0.019** / **0.012–0.017** withdrawn (§3, §4). Single-atom edges = the two delivery configs (dual-end 0.0048 / single-tagged **0.0072**), each + 0.003 squeezer once. |
| **Realized floor < GATE A (0.003 vs 0.0072)** | `floor_gap_resolution.md` | GATE A (`clean_lambda=True`) and the realized floor are the **same solver in two modes**; the gap is recoiler-closure, not a reduced engine. |
| **D1 vs D2** | `D1_hybrid_consolidated_findings.md` | **D1 ruled out** — no floor gain, line-independent binding, F′1 inversion 1.65× worse; α₀(5P₁/₂,1064)≈−1254 a.u. (every-leg r=−1.78, worse than D2). Do not model D1. |
| **Retro geometry** | `retro_EIT_section.md` | Retro EIT **viable**; m′=2 + bare mirror favorable; dual-end vs retro is an **engineering trade**, not a physics result. Reflection rule is **optic-dependent** (name the optic before quoting Δm). |
| **Delivery / laser architecture** | `laser_architecture_comparison.md` + `single_EOM_full_sequence.md` | **All-fiber, single 1560 nm EOM → SHG 780**, common-mode (no OPLL). Dual-end carrier-suppressed (β=2.405) preferred; single-end tagged retro (2f_A=400 MHz down-shift) fallback. |
| **Thermometry** | `thermometry_audit.md` | Sideband-asymmetry on the Raman pair; η_R∝1/√ν_z floor–thermometer correlation (measure ν_z directly); m′=0 dark leg resolved \|1,−1⟩→\|1,0⟩ (Δm=+1). |
| **Alternatives sweep (all dead ends)** | `clock_EIT_consolidated.md` §10 (PART II) | Leg-swap, EOM-Raman clearer, D1 pivot/hybrid, D1-Raman repump, recoil-routing — **all closed**. Recurring lesson: **repump topology** decides leg/recycle questions, not the diffusion/branching lever. |

---

## 2. Do NOT mistake these (intermediate / superseded — look authoritative, are not)

- **`recycle_dwell_S3.py`** — a D1/hybrid recycle-**traffic** tool (N_cool/N_rep per leak). **NOT the anti-trap floor authority.** Its `n_floor=0.077…` Markov estimate is superseded by `ANTITRAP_RESOLUTION.md`. *(This exact mistake was made and caught 2026-06-20.)*
- **`antitrap_kernel_grid.py` grid steady-state runaway (0.03→0.10)** — a truncation/boundary **artifact** (`ANTITRAP_RESOLUTION.md:22–23`), not a physical floor. The closed-form **kernel** (0.031 m′=0, 0.018 F′1) IS valid; the grid *steady state* runaway is not.
- **`operating_point.py` `all_in_single_atom = (0.012, 0.019)`** [the OLD field] — was **double-counted** (`antitrap_leak_increment=0.007` is the *no-squeezer bulk* ≈ the solve floor). **FIXED 2026-06-20** (committed PR #4): the field is now `squeezer_increment_lowdwell = 0.003` (scalar) and `all_in_single_atom_lowdwell` = solve + squeezer ≈ **0.008–0.010**. **Any copy still showing (0.012, 0.019) or `antitrap_leak_increment` is pre-correction — discard.**
- **The `EIT_brief` lineage (`v11` / `v12` / `v17`)** — **superseded**; the **current master is `clock_EIT_consolidated.md` v17** (the v17 brief's four-subversion matrix + box-MC are folded into master §4/§8). The briefs are **not kept as files** — see git history for v11/v12 (D1 §12, the five-column comparison). Do not cite them for the current floor.
- **`clock_EIT_consolidated.md` v14 / v15 / v16** — superseded by the current **v17** master. Re-sync project knowledge from the live docs (use `INDEX.md` as the authority map).
- **Any `clock_leg_swap_finding.md` headed "[O] swap favored"** — the **RESOLVED** version ("swap rejected; A holds") supersedes it.
- **`v12_plan.md` / `D1_hybrid_plan.md` / `v12_decision.md`** — process scaffolding; conclusions are in v16 / the findings docs.

---

## 3. Load-bearing conventions (state these before quoting any floor number)

**The increment convention** *(the single cause of three contested floor numbers this session)*.
The solve floor (`clk2.py`, config A = 0.0048; `:234` puts one ground frequency on all internal
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
**design intent, not a result** — the adopted F′=1 EIT repump (`clk2.py:135`) sits on the exact leg
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

---

## 4. OPEN / in-flux — NOT settled, do not cite as final

- **✅ DONE `operating_point.py` double-count fix** (2026-06-20) — `antitrap_leak_increment=(0.007,0.012)` replaced by the squeezer increment (~0.003, once); `all_in_single_atom_lowdwell` = solve + squeezer ≈ 0.008–0.010 [I, low-dwell]; high-dwell + cloud carried as [O]. **Committed to PR #4** (claude/floor-correction, gate-green); the SSOT `SCOPE` now **defers detection/survival to CLAIMS D-/S-series** (no independent tier — an unintentional `[O]` metadata downgrade was reverted).
- **✅ DONE (2026-06-20) repump-dwell measurement** — clk2 config-A F′=1 dwell **P_e(F′1)=8.4×10⁻⁶**, 5× below the low-dwell ref (4×10⁻⁵) → **firmly low-dwell; high-dwell branch (0.03–0.05) retired**; certified ~0.008–0.010 stands (and the 0.003 squeezer increment is conservative). Proxy clk2 pe_F1 ~ grid P_e_rep is **[I]** (auditor to vet); F′2 residual 1.8×10⁻⁵ cross-checks dark-state ~4×10⁻⁵. The dense-ME high-dwell re-solve is now needed *only if the dwell proxy is contested*.
- **[O] radial squeezer integral — input now COMPUTED; only the dwell-weighted assembly remains.** P_e(F′2)(r) measured on clk2 (`radial_pe.py`): it **falls** off-axis (1.53→0.88 ×10⁻⁵ over r=0–10 µm; M3 common shift preserves δ₂/dark state), so R_sq(r)=P_e·kernel **falls to 0.32× at r=10** — the "rate-rise" half is **disproven**, not sign-uncertain. The remaining question is only whether the dwell-weighting beats the off-axis 1/W tail (it did for cooling). Fold R_sq(r) into the MC ⟨n⟩-ODE (anchored to faithful 0.003 on-axis) and dwell-weight; expected cloud ≈ single-atom ≈ 0.008–0.010. Brief: `audit_squeezer_integral_MC.md`.
- **✅ DONE (2026-06-20) Radial dynamic MC (S3)** — cooling half of the cloud: realized sits **below** quasi-static (W(r) peaks at the cold center, anti-correlated with n_ss(r)) → **frozen bound 0.0126 superseded; radial cooling dynamics are benign**. **3-level engine ⇒ RATIO result** (suppression ~1.2×/3.0×/7.4× at 25/100/400 µK *within its own bracket*), NOT the clock floor. Pipeline `mc.py`/`grid_build.py`/`engine.py` + fig `s3_radial_mc.png`. Provenance note: the brief's 0.0085 semiclassical-MC driver was **not in the file set** (asserted [V] in `clock_EIT_consolidated.md §8`, generating code absent). Clock-engine magnitude = clk2 per-radius re-run [O].
- **In-fiber radial temperature** — 556 µK (loaded/uncooled) vs ~100 µK (cooled upstream). Gates the cloud floor **and** P1 §IV.B.
- **Flat-top** — flatness spec ≤3% over ±6 µm (frozen, provisional; S3 relaxes it); ~1.3–1.7× mover *conditional on low-dwell repump*. Fiber feasibility (mode content @1064, walk-off over 2 m, contrast) → XLIM. Briefs: `flat_top_feasibility.md`, `flatness_spec_result.md`.
- **6.835 GHz two-photon linewidth** — the bench-gated binding measurement (sub-100 Hz?). P1 hinges on it.

---

## 5. Validated engines (src/)

| engine | role | gate |
|---|---|---|
| `clk2.py` | deciding-run solver = base + hooks (swap/rep2mode/clearer/want_fock) | config A = 0.0048; clean-Λ A=0.0072 / B=0.0022 |
| `clock_combined_solve.py` | the validated **base** clk2 is built on | clean-Λ = 0.0072 |
| `verify_tagged_solve.py` | tagged-EIT steady-state solver | — |
| `eit_cooling_tool.py` | PI **axial** tool (embeds the engine, self-checking; `--regression`) | dual ~0.0048 / single ~0.0072 (v17 preset, Nf=6 gate) |
| `cloud_cooling_tool.py` | PI **radial/cloud** tool (box flat-top + two-tone; `--regression`) | box→on-axis ∀T_r; 1-/2-tone crossover ~120 µK |
| `antitrap_kernel_grid.py` | anti-trap **kernel** (valid) + grid (steady-state runaway = artifact) | normal-trap grid = Fock = 0.0085 |
| `raman_sbc.py` | RSC engine (anchors the RSC-vs-EIT comparison) | — |
| `flatness_spec.py` | per-depth floor / flat-top flatness spec | s=1 → 0.00485 |
| `radial_pe.py` | per-radius P_e(F′2) on clk2 (squeezer-rate input) | P_e *falls* off-axis 1.53→0.88e-5 |
| `grid_avg_cloud.py` | Boltzmann cloud average of clk2 n̄(r) | 0.0056/0.0169/0.130 @ 25/100/400 µK |
| `dwell.py` | clk2 F′=1 repump-dwell measurement | P_e(F′1)=8.4e-6 → low-dwell |

---

*Maintenance: re-reconcile this index whenever a floor number, an authority file, or a convention
changes. The protective value is the §2 "do not mistake" list and the §3 conventions — keep those
current. Authoritative resolution docs (`ANTITRAP_RESOLUTION.md`, `floor_gap_resolution.md`) are now in
`docs/` (PR #4), since this index points to them as load-bearing.*
