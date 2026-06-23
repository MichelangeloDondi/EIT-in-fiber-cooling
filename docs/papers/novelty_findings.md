# Novelty findings — Paper T and Paper P3 (recorded 2026-06-17)

Both write-now theory candidates (Paper T, Paper P3) were red-teamed and novelty-checked.
**Both are built from established physics and are NOT viable as novel-discovery standalone
preprints.** Their correct, verified content is retained as P1 components (T = design rationale /
motivation, P3 = floor budget / backbone), properly cited. The genuinely novel contribution in
the program is the **experiment (P1)**, which is bench-gated on the 6.835 GHz two-photon linewidth.

Flags: `[V]` computed/verified in this repo · `[lit]` established in the literature (cited).
Backing computations: `src/tools/m0_vector_raman_check.py`, `src/tools/breit_rabi_sensitivity.py`.

---

## Paper T — rank-2 obstruction to Δm=2 clock-pair Raman cooling

The **physics is correct and verified** (rank-2 null `B4`, floor `F7/F8` in `CLAIMS.md`). What the
findings change is **scope** and **novelty**.

### T1 — Scope: the m=0 clock transition is NOT obstructed and IS coolable  [V]
`src/tools/m0_vector_raman_check.py`. The abstract's "matched g_F m_F" definition of clock pair *includes*
the m=0 pair |1,0⟩/|2,0⟩, which is connected by a **Δm=0** (not Δm=2) Raman; the Δm=0 amplitude runs
through the **rank-1 (vector)** channel, which is allowed in J=½.
- Δm=2 matched pair |1,−1⟩→|2,+1⟩ : Σ_F′ g = 0 (rank-2 null), G ∝ 1/Δ², FoM flat ≈ 5.6 — obstructed (reproduces the paper).
- m=0 |1,0⟩→|2,0⟩ (σ⁺σ⁺ counter-prop, Δk = 2k) : Σ_F′ g = −1/3 (no null), G ∝ 1/Δ, FoM = 78 / 826 / 2474 at Δ = 1 / 10 / 30 GHz — coolable (826 ≫ 170 at 10 GHz).

⇒ "EIT is **the** field-insensitive route" / "alkali clock qubits resist RSC" **overclaims**. The
correct narrow statement: only the **Δm=2 matched pairs (m≠0)** are rank-2-obstructed.

### T2 — The m=±1 magic pair is not *forced* by field-insensitivity  [V]
`src/tools/breit_rabi_sensitivity.py` (Breit–Rabi, ⁸⁷Rb ground). |dν/dB|:
- m=0 : 1.15 / 1.73 / 3.71 kHz/G at B = 1 / 1.5 / 3.23 G (quadratic K = 575 Hz/G²).
- m=±1 magic pair : first-order zero at B = 3.229 G (residual 862 Hz/G²); comparable/worse than m=0 *away* from the magic field.
- Dephasing at 1 mG field noise : m=0 @1.5 G = 1.7 Hz ; magic @3.229 G = 0.0004 Hz (~1000×).

⇒ m=0 at the 1–1.5 G cooling field (1.7–17 Hz for 1–10 mG noise) is **within the sub-100 Hz target
AND coolable**. The m=±1 magic pair is the **metrologically-optimal** field-insensitive choice
(~1000× field immunity at the magic field, drift/inhomogeneity-immune, direct cooling without a
transfer step) — **not a necessity**. Choosing it for magnetic insensitivity is reasonable and
standard; it is not forced.

### T3 — Prior art: the central result is already published  [lit, decisive]
**J. B. Naber, L. Torralbo-Campo, T. Hubert, R. J. C. Spreeuw, Phys. Rev. A 94, 013427 (2016)**
(arXiv:1605.05230), *Raman transitions between hyperfine clock states in a magnetic trap.*
Point-for-point against Paper T's core:
- Same pair |F=1,m=−1⟩/|F=2,m=+1⟩, the magic clock states at B = 3.23 G.
- Same geometry: Δm = +2 → σ⁺ (one laser) and σ⁻ (the other), through |F′=1,0⟩ and |F′=2,0⟩.
- Same null, same method (Wigner–Eckart + Clebsch–Gordan):
  ⟨1|r₋₁|e1⟩⟨0|r₁|e1⟩ = −⟨1|r₋₁|e2⟩⟨0|r₁|e2⟩ ⇒ the two paths interfere destructively.
- Same detuning law: their Eq. (2) carries 𝔇(Δ) = Δ₂₁/(Δ₁+Δ₂₁); "for large detuning the destructive
  interference essentially changes the scaling of Ω_R to ∼ 1/Δ₁²," pinned by the F′=1↔2 interval Δ₂₁.
- Same headline consequence: "one cannot reduce the effect of spontaneous emission by going to
  larger detunings." (They attribute the interference to an earlier ref [26]; may predate 2016.)

Paper T's additions — the rank-2 **tensor** language, the cooling FoM/floor, the alkali-series
generalization, the EIT contrast — are re-framing and corollary, not a new result. A PRA referee in
this area will know the 2016 paper.

**Bonus — Naber also de-risks the m′=0 thermometry.** The same paper's finding that the differential
AC-Stark *vanishes at an optimal laser intensity ratio* — on the exact |1,−1⟩↔|2,+1⟩ readout pair — is
the empirical characterization + nulling knob for the thermometry's differential-Stark bias (the
readout [O1]); and its rank-2 null tells the Δm=+2 readout it cannot detune scatter away. So the prior
art that demotes Paper T simultaneously sharpens the thermometry validation. See `../thermometry.md` §5.

### Decision (T)
**Demoted from standalone preprint → P1 design-rationale/motivation, cited to Naber–Spreeuw 2016.**
DO NOT submit standalone. The polished manuscript + package in `docs/papers/` are retained but
flagged **HOLD** (`SUBMISSION_CHECKLIST.md`); reuse their verified core as P1's motivation section.

---

## Paper P3 — inhomogeneous-light-shift radial cooling floor

The specific quantitative floor for *our* geometry is the user's computation; the **mechanism and
every qualitative conclusion are established** — some of it by the prospective-host group.

- **B1 — "EIT-tolerant / RSC-fragile"** = the established EIT cooling **bandwidth advantage**.
  Multi-mode ion-string cooling exploits exactly "a broad EIT bright feature covers a range of mode
  frequencies a narrow sideband cannot" (Lechner 2016; Jordan 2019; Qiao 2021; widely called one of
  EIT cooling's most compelling features). [lit]
- **B2 — inhomogeneous-light-shift cloud floor (the M3 effect)** is named in the HCPCF literature:
  Cs-in-HCPCF (arXiv:1812.02887) states the trap AC-Stark shift "adds an inhomogeneous broadening …
  [dependent on] the radial distribution of the atoms in the fiber," extendable "by transverse
  cooling"; the ~935 nm magic-wavelength HCPCF Cs work suppresses exactly this radial-distribution
  inhomogeneous broadening; the tightly-trapped fibre interferometer attributes its limit to "the
  DLS introduced by the FORT [leading] to the inhomogeneous dephasing." [lit]
- **B3 — outside-Lamb-Dicke, recoil-limited soft modes**: Yu, Hutzler, Ni *et al.*, PRA 97, 063423
  (2018) cool despite large η and large differential light shifts; Morigi *et al.* (1998) cooling
  outside the LD regime; Dy narrow-line tweezer cooling chirps to cover the inhomogeneous spread. [lit]
- **B4 — fit**: the prospective host group already does in-fibre sideband cooling for this purpose —
  **C.-C. Wang *et al.*, Phys. Rev. Research 4, L022058 (2022)**, in-fibre laser cooling to extend a
  HCPCF atom interferometer. [lit]

### Decision (P3)
**P1 backbone, not standalone.** Keep the geometry-specific floor budget (n̄_z ≈ 0.012 at 100 µK [v17 T_r-gated cloud; was 0.0095 semiclassical],
M1/M2/M3, MC ensemble) as P1's floor analysis; cite B1–B4. Do not pitch as a novel-discovery note.

---

## Strategic conclusion
- Neither T nor P3 is a novel-discovery standalone. **There is no theory shortcut to a first-author
  preprint here.**
- The novel contribution is the **experiment — P1** (EIT-SC to the axial ground state of a
  field-insensitive clock pair in HCPCF), bench-gated on the 6.835 GHz two-photon linewidth.
- **Revised plan:** anchor the first-author paper on **P1**; fold in **T** (cited motivation) and
  **P3** (cited backbone). Drop / reframe the "preprint-before-outreach" step for the Lan
  application; lead the outreach with the direct platform fit (Wang 2022) + the thesis-in-progress,
  not a manufactured-novelty note.
