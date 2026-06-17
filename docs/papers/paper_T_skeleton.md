# Paper T — skeleton & argument spine

**Working title (pick one):**
1. *A rank-2 selection-rule obstruction to Raman sideband cooling of alkali clock qubits* ← recommended
2. *Field-insensitive clock states resist Δm = 2 Raman sideband cooling: a J = ½ obstruction*
3. *Why electromagnetically-induced-transparency cooling is the field-insensitive route for alkali clock qubits*

**Target:** Physical Review A (full theory note), **arXiv-first**. Length ~5–7 pp, 2–3 figures.
**MANUSCRIPT:** `docs/papers/paper_T.tex` (+ `paper_T.bib`) — assembles the verified core; **compiles clean to 4 pp** (PRA revtex4-2). §III–V, §VII, abstract, table, FoM box are the computed core; §I/II/VI/VIII are first drafts; **all three figures done**; compiles to 5 pp.

**Status:** all load-bearing results are **[V]** (see CLAIMS.md: B4 + F7 + F8 + the FoM). UNBLOCKED.
**One-sentence thesis:** connecting a field-insensitive alkali clock pair with a single two-photon
momentum kick requires a rank-2 (Δm = 2) operator, which vanishes in a J = ½ ground manifold, so
Raman sideband cooling on that pair has an unimprovable coherence-per-scatter ceiling and a high
floor — EIT cooling, operating near-resonance, evades it.

---

## Abstract (draft, ~160 words)
Field-insensitive "clock" states of alkali atoms — the m_F sublevels with matched g_F m_F — are
the natural qubit and metrology basis, but cooling them directly to the motional ground state is
constrained. We show that Raman sideband cooling on a field-insensitive clock pair of ⁸⁷Rb is
obstructed by a selection rule: connecting the pair with a single two-photon momentum kick
requires a Δm = 2 (rank-2) operator, and the rank-2 component of a two-photon operator vanishes
identically in a J = ½ ground manifold, since the reduced matrix element requires the forbidden
triangle (½, 2, ½). The transition survives only through excited-state hyperfine mixing, with
amplitude ∝ Δ_HFS/Δ², so the coherence per spontaneously scattered photon is pinned at a figure of
merit of order Δ_HFS/Γ ≈ 5 — independent of detuning, and unimprovable. A Lamb-Dicke rate analysis
gives a cooling floor n̄ ≈ 0.45, robust to a factor-3 change in the scattering prefactor.
Electromagnetically-induced-transparency cooling on the same pair evades the obstruction by
operating near-resonance, reaching n̄ ≈ 0.005. The result identifies a general constraint on direct
sideband cooling of alkali clock qubits and singles out EIT as the field-insensitive route.

---

## Section-by-section spine

### 1. Introduction  *(no new compute)*
- Motivation: motional-ground-state cooling of neutral-atom clock/qubit states in tweezers,
  lattices, and fibres; the field-insensitive m_F pairs (matched g_F m_F) are the metrology basis.
- The tension: a single guided/retro two-photon operation that imparts one motional quantum
  between such a pair is, for the natural choices, a **Δm = 2** transition.
- State the result and the resolution (EIT). Forward-reference Fig. 2.

### 2. The clock pair and the Δm = 2 requirement  *(no new compute; cite Audit-C / B1–B3)*
- Define the ⁸⁷Rb pair |1,−1⟩ / |2,+1⟩ → |F′=2, m′=0⟩; both have g_F m_F = +½ ⇒ **field-insensitive
  at any B**, and 1st-order vector-light-shift immune (CLAIMS B1–B2).
- Show that a single-beam-axis (guided + retro) sideband operation connecting them carries Δm = 2.
- Contrast with the field-**sensitive** stretched pair |2,+2⟩/|2,+1⟩ (Δm = 1, allowed) — which is
  *not* a clock pair (CLAIMS F6); this sets up why one is "forced" onto Δm = 2.

### 3. The rank-2 obstruction  *(feeds from `audit_C_rank2.py`, CLAIMS B4 — the theoretical heart)*
- Adiabatically eliminate the excited manifold → effective two-photon ground operator
  T_eff = Σ_e (d·ε₂)|e⟩⟨e|(d·ε₁)/Δ_e. Decompose into irreducible tensors T^(K), K = 0,1,2.
- For Δm = 2, only **K = 2** contributes. The electronic part acts on J = ½:
  by Wigner-Eckart, ⟨J=½‖T^(2)‖J=½⟩ requires Δ(½, 2, ½) ⇒ 0 ≤ 2 ≤ 1, **false** ⇒ reduced matrix
  element = 0. Equivalently: a rank-2 electronic operator would need Δm_J = 2, impossible in J = ½
  (max |Δm_J| = 1).
- **m_I bookkeeping:** the dipole acts only on the electron (Δm_I = 0 per vertex), so Δm_F = 2 with
  |Δm_J| ≤ 1 demands Δm_I ≥ 1 — supplied **only** by the excited-state I·J coupling (which conserves
  m_F = m_J + m_I while mixing m_I, m_J). Hence the transition routes through excited hyperfine
  mixing, amplitude **∝ Δ_HFS/Δ²** (one 1/Δ from the resolvent; one Δ_HFS/Δ from the
  otherwise-cancelling sum over excited HFS levels).
- *Verified three ways (cite):* product-basis amplitude → exact zero in the degenerate-HFS limit;
  full-resolvent Δ-scaling; explicit Breit-Rabi + excited HFS+Zeeman diagonalization at 1.5 G →
  allowed 1/Δ coefficient = 1×10⁻⁴.

### 4. Coherence-per-scatter ceiling  *(feeds from `clock_RSC_resolution.md` FoM; NEEDS clean derivation)*
- Two-photon Rabi: Ω₂ph ∝ Ω₁Ω₂ · Δ_HFS/Δ² (rank-2, HFS-mediated). Off-resonant single-photon
  scatter per beam: R_sc ∝ Ω²Γ/Δ².
- **Key scaling:** FoM ≡ (coherent Raman rate)/(scatter rate) ∝ (Δ_HFS/Δ²)/(Γ/Δ²) = **Δ_HFS/Γ**,
  *independent of detuning*. Contrast the allowed case (FoM ∝ Δ/Γ, improvable by detuning).
  ⇒ the obstruction's quantitative bite: **you cannot detune your way out.**
- Numerically (computed in `src/paper_T_fom.py`, LaTeX-ready in `paper_T_core_derivation.md`):
  the null is **exact** — g(F′=1) = −g(F′=2) = −1/(4√3); the survivor G₂ = 22.7 MHz ∝ the
  F′=1,2 splitting; and **FoM ≈ 5.6** (radians of two-photon rotation per scattered photon),
  **flat across Δ = 1–30 GHz**. An earlier independent estimate gave ≈4 (A₂,∞ ≈ 16 MHz); both are
  O(few), differing only by the scatter-normalization convention. The ceiling = Δ_HFS/Γ.
- **Geometry lemma:** in the mirror-ladder (guided + retro) configuration the dark-state coupling
  forces one Raman beam onto the dark state (scatter ∝ Ω₋²); the *rate* Ω_R = Ω₊Ω₋ is a free knob,
  but the **FoM** is what is bounded — cranking the rate cranks the depumping scatter in lockstep.

### 5. Cooling-floor consequence  *(feeds from F7/F8; NEEDS transparent rate-equation)*
- Lamb-Dicke steady state n̄_ss = A₊/(A₋ − A₊). With FoM ≈ 4, the off-resonant scattering rate
  exceeds the Lamb-Dicke cooling rate by **11–23×**, so recoil heating from that scatter overwhelms
  the cooling: n̄_ss ≈ **0.45** (T_z ≈ 18 µK, 69 % ground), B-independent.
- **Robustness:** needs ×170 in the scatter prefactor to recover a useful floor; a ×3 uncertainty
  leaves it disqualified.
- **Note the engine:** `raman_sbc('clock')` returns 0.0137 (CLAIMS F8) — this is the
  **obstruction-free idealization** (free Raman Rabi, ~0 scatter), shown explicitly to be the floor
  of a model that omits the rank-2 suppression; it is *not* the physical floor. Use it as the
  "what you'd get if the obstruction didn't exist" reference, exactly as in Fig. 2.

### 6. Contrast: EIT cooling evades the obstruction  *(feeds from `tagged_solver.py`, CLAIMS F1)*
- EIT operates **near-resonance**, where the excited HFS is resolved and the dark-state cooling
  does not rely on a far-detuned Δm = 2 Raman; its floor already includes the scattering.
- On the *same* field-insensitive pair, the EIT solve floor is n̄ ≈ 0.0048 (dual) / 0.0072
  (single-tagged) — ~100× below the RSC floor (Fig. 2). This is the practical resolution.
- One line on why you cannot simply pull the Raman near-resonant: the scatter then diverges (you
  lose the FoM); EIT is the structured near-resonant solution (dark-state interference).

### 7. Generality and scope  *(**DONE** — computed in `src/paper_T_generality.py`; table in `paper_T_core_derivation.md` §7)*
- The obstruction is generic to **J = ½ ground manifolds** driving Δm = 2: applies to the
  field-insensitive clock pairs of the alkalis (Rb, Cs, Na, K, …). FoM ≈ Δ_HFS/Γ differs per
  species (different excited-state HFS) → tabulate FoM for Rb-87, Cs-133, K-39/41, Na-23.
- Scope/caveats: rank-2 *electronic* null is exact; the floor is a Lamb-Dicke rate estimate
  (±factor on 0.45, but disqualification robust); assumes the standard guided/retro geometry.
- What does *not* transfer: alkaline-earth clock cooling (J = 0 ground; sidebands resolved on the
  narrow line) is a different regime — note it explicitly to pre-empt the obvious referee question.

### 8. Conclusion  *(no new compute)*
- A selection rule, not an engineering limit, blocks Δm = 2 Raman cooling of alkali clock qubits;
  the coherence-per-scatter is pinned and detuning-proof; EIT is the field-insensitive route.

---

## Figures
| Fig | Content | Source | Status |
|---|---|---|---|
| 1 | Level scheme: clock pair, Δm = 2 path, mirror-ladder geometry; F'=1,2 cancel (rank-2 null) | `figures/fig_level_scheme.py` | **DONE** |
| 2 | Floor comparison — EIT 0.0048 vs clock-RSC 0.45 (DISQUALIFIED, rank-2, ×33 lift from the 0.0137 idealization) vs stretched 0.00196; field-insensitive vs field-sensitive | `figures/fig_rsc_vs_eit.py` | **DONE** |
| 3 | FoM vs detuning: flat for Δm = 2 (rank-2) vs ∝ Δ/Γ for an allowed Raman — the "can't detune out" point | `figures/fig_fom_vs_detuning.py` | **DONE** |

---

## What is [V] vs what must be ADDED for publication
**Already computed [V]:**
- Rank-2 electronic null + the I·J routing (`audit_C_rank2.py`) — §3.
- **FoM derivation — DONE** (`src/paper_T_fom.py` + LaTeX-ready `paper_T_core_derivation.md`):
  exact null, Δ_HFS/Δ² survivor, detuning-independent FoM ≈ 5.6 — §3–§4.
- Floor ≈ 0.45 and its robustness; the 0.0137 obstruction-free idealization (`clock_RSC_resolution.md`, `raman_sbc.py`) — §5.
- EIT contrast floor 0.0048/0.0072 (`tagged_solver.py`) — §6.
- Fig. 2 — done.

**Must add (the writing/derivation work):**
1. ~~Clean analytic derivation of the FoM scaling~~ — **DONE** (`paper_T_core_derivation.md`); now
   just transcribe into the manuscript and add the $|m_J,m_I\rangle$-basis appendix.
2. ~~Transparent rate-equation reproducing n̄ ≈ 0.45~~ — **DONE** (`src/rsc_floor_rate_eqn.py`,
   written into §5 of `paper_T_core_derivation.md`): n̄ = O(0.1–1) at FoM ≈ 5.6, FoM ≳ 170 to
   recover; brackets the 0.45 and the 0.0137 idealization.
3. ~~Fig. 1 (level scheme + geometry)~~ — **DONE** (`figures/fig_level_scheme.py`). ~~Fig. 3~~ — **DONE**.
4. ~~Generality table (§7)~~ — **DONE** (`src/paper_T_generality.py`): null universal (Σg=0 for
   I=3/2–7/2); FoM 0.2 (Li) → 9.3 (Cs), all ≪170, sub-unity for the light alkalis. *(orig: plug excited-HFS
   splittings.)*
5. **Literature positioning** — see below.

---

## Positioning / novelty
- Distinct from prior **EIT-cooling-in-fibre / tweezer** work (Leong 2020 HCPCF RSC; Chiu/Lukin 2025
  tweezer EIT; Xin 2024 EIT-SC): those are *demonstrations*; this is a *selection-rule theory
  result* about why one cooling modality is blocked for clock qubits and another is not.
- Distinct from standard Raman-cooling FoM discussions (which assume an allowed transition): the
  novelty is the **rank-2 null in J = ½** and the resulting **detuning-proof** FoM ceiling.
- The honest framing is a constraint + resolution, broadly useful to the neutral-atom
  clock/qubit-cooling community — not specific to the fibre apparatus (that is P1/P2).

## Suggested writing order
§3 → §4 (the theoretical core, with derivation) → §5 (floor) → §6 (EIT contrast) → §2 (setup) →
§7 (generality) → §1/§8 (intro/conclusion) → abstract last. Build Fig. 1 alongside §2–3.
