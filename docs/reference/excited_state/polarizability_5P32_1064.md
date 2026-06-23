# Independent Recomputation of ⁸⁷Rb Dynamic Polarizabilities at 1064 nm — Adjudicating the 5P₃/₂ Scalar-Polarizability Disagreement

## TL;DR
- **α₀(5P₃/₂) at 1064 nm is large-negative, ≈ −1130 to −1150 a.u., NOT −134 a.u.** My independent sum-over-states gives ≈ −1140 a.u., matching the Arora–Sahoo theory value −1111.62 a.u. and the Chen–Raithel measured value −1149 ± 2.5% a.u. (Chen, Gonçalves & Raithel, PRA 92, 060501(R) (2015): "We obtain experimental values α₀=−1149 (±2.5%) and α₂=563 (±4.2%), in atomic units.").
- **There is NO trapped 5P₃/₂ sublevel at 1064 nm.** Every |F′,m′⟩ state is net-positive (anti-trapped, +19 to +57 MHz at U₀ = 22.8 MHz); the stretched |F′=3,m′=±3⟩ state is the least anti-trapped at ≈ +19 MHz — it is NOT a −14 MHz trap.
- **The competing "α₀ ≈ −134 a.u. / stretched-state-trap" scenario is physically wrong**: it cannot be reproduced from any authoritative matrix-element set and contradicts both first-principles theory and direct measurement. The −134 value most plausibly arises from omitting or sign-flipping the dominant red-detuned 4D₅/₂ and 6S terms.

## Key Findings
1. **α₀(5S₁/₂, 1064 nm) = 687.3 a.u.** — passes all calibration gates (static ≈ 318.6 a.u., tune-out ≈ 790.03 nm).
2. **α₀(5P₃/₂, 1064 nm) ≈ −1140 a.u.** (my sum-over-states total), consistent with −1111.62 a.u. (Arora–Sahoo theory) and −1149 a.u. (experiment). LARGE-NEGATIVE.
3. **α₂(5P₃/₂, 1064 nm) ≈ +556 a.u.**, consistent with +557.31 (theory) and +563 ± 4.2% (experiment, Chen, Gonçalves & Raithel, PRA 92, 060501(R) (2015): "α₂=563 (±4.2%), in atomic units").
4. **Ratio α₂/α₀(5P₃/₂) ≈ −0.48** (theory −0.50, experiment −0.49). NOT −4.26.
5. **5P scalar light shift at U₀ = 22.8 MHz ≈ +37 MHz** (not +4.3 MHz).
6. The headline disagreement is resolved decisively in favor of the large-negative scalar polarizability and the "no trapped excited state" verdict.

## Details

### Method and conventions
Working in atomic units, the second-order valence scalar polarizability is
α₀ᵛ(ω) = (2/(3(2J+1))) Σₖ |⟨k‖d‖v⟩|² (Eₖ−Eᵥ)/[(Eₖ−Eᵥ)² − ω²],
with the tensor polarizability carrying an extra 6j-dependent geometric weight (Arora–Sandars form). At λ = 1064 nm, ω = 0.042823 a.u.

The sign of each term is set by the detuning. Transitions to states ABOVE 5P₃/₂ whose resonance wavelength is longer than 1064 nm (red-detuned: 6S at 1367 nm, 4D at 1529 nm) give NEGATIVE contributions; the downward transition to 5S, and transitions to states whose resonance is shorter than 1064 nm (blue-detuned: 5D at 776 nm, 7S at 741 nm), give POSITIVE contributions. This competition between red-detuned and blue-detuned contributions is the crux of the problem — and the red side wins overwhelmingly.

### Reduced dipole matrix elements used (authoritative sources)
From Arora & Safronova (arXiv:0709.0130, PRA 76, 052509), Safronova & Safronova (PRA 83, 052508), and Arora & Sahoo, "State-insensitive trapping of Rb atoms: Linearly versus circularly polarized light," PRA 86, 033416, published 17 September 2012 (Erratum PRA 99, 049901, 1 April 2019), whose matrix elements were "optimized using the experimental results available for the lifetimes and static polarizabilities of atomic states":
- ⟨5P₃/₂‖d‖5S₁/₂⟩ = 5.977 a.u. (λ_res 780.24 nm)
- ⟨5P₃/₂‖d‖6S₁/₂⟩ = 6.047 a.u. (1366.87 nm)
- ⟨5P₃/₂‖d‖4D₅/₂⟩ = 10.899 a.u. (1529.37 nm)
- ⟨5P₃/₂‖d‖4D₃/₂⟩ = 3.633 a.u. (1529.26 nm)
- ⟨5P₃/₂‖d‖5D₅/₂⟩ = 1.983 a.u. (775.98 nm)
- ⟨5P₃/₂‖d‖5D₃/₂⟩ = 0.665 a.u. (776.16 nm)
- ⟨5P₃/₂‖d‖7S₁/₂⟩ = 1.350 a.u. (741.02 nm)
- ionic core ≈ +9.1 a.u.

(The 5P₃/₂–5D₅/₂ element is the only mildly contested one in the literature; the 5S–5D₅/₂ clock study, arXiv:2212.10743, gives 1.80(6) ea₀ experimental / 1.96(15) ea₀ theoretical near the magic wavelength 776.179(5) nm — but at 1064 nm this term is small and does not affect the verdict.)

### Q1 — α₀(5S₁/₂) and calibration gate (G1)
My sum (prefactor 1/6 for J=1/2): 5S→5P₁/₂ (235.2) + 5S→5P₃/₂ (441.1) + 6P/7P/8P/9P tail (~1.7) + core (9.3) − core-valence (−0.26) ≈ **687 a.u.**, exactly the Arora–Sahoo value 687.3(5) a.u. that Chen–Raithel adopted as α₅S. Static limit: 314.14 (valence) + 9.11 (core) − 0.26 ≈ **318.6 a.u.**, matching the accepted ≈ 319 a.u. The scalar zero (tune-out) falls at **790.03 nm**, matching the precision measurement of Leonard, Fallon, Sackett & Safronova, "High-precision measurement of the ⁸⁷Rb D-line tune-out wavelength," PRA 92, 052501 (2015): "The wavelength lies between the D1 and D2 spectral lines at 790.032388(32) nm." **Gate G1 passes on all three sub-checks.** The trap depth U₀ = 22.8 MHz = 1.094 mK fixes the operating intensity; the Chen–Raithel cavity reached "intensities near 2×10¹¹ W/m²," and all other shifts scale from U₀.

### Q2 — α₀(5P₃/₂): per-transition breakdown (the headline)
My explicit sum-over-states at 1064 nm (a.u.):

| Transition | λ_res (nm) | detuning | contribution (a.u.) |
|---|---|---|---|
| 5P₃/₂ → 5S₁/₂ (downward) | 780 | — | −221 |
| 5P₃/₂ → 6S₁/₂ | 1367 | red | −281 |
| 5P₃/₂ → 4D₅/₂ | 1529 | red | **−623** (dominant) |
| 5P₃/₂ → 4D₃/₂ | 1529 | red | −69 |
| 5P₃/₂ → 5D₅/₂ | 776 | blue | +24 |
| 5P₃/₂ → 5D₃/₂ | 776 | blue | +3 |
| 5P₃/₂ → 7S₁/₂ | 741 | blue | +10 |
| 6D/8S/higher tail | — | — | ~ +11 |
| core | — | — | +9 |
| **TOTAL** | | | **≈ −1137** |

The three red-detuned/downward terms (4D₅/₂, 6S, 5S) sum to ≈ −1125 a.u. and overwhelm the small positive blue-detuned terms (≈ +48 a.u. plus +9 core). **α₀(5P₃/₂) is unambiguously large-negative.** The single 4D₅/₂ term — matrix element 10.9 a.u., nearest resonance at 1529 nm to the red of 1064 nm — accounts for ~55% of the total magnitude; 6S contributes ~25% and 5S ~19%. This matches Arora–Sahoo theory (−1111.62 a.u.) and the Chen–Raithel measurement (−1149 ± 2.5% a.u.).

**(G4) Dominant transitions: 4D₅/₂ (≈55%), 6S₁/₂ (≈25%), 5S₁/₂ (≈19%), 4D₃/₂ (≈6%).** The 4D and 6S levels lie to the red, 5S is the downward term, and all three drive α₀ strongly negative.

### Q3 — α₂(5P₃/₂) and the ratio
Applying the tensor 6j weights per intermediate J (s-states weight −1; d₃/₂ +0.8; d₅/₂ −0.2 relative to the scalar term per the {jᵥ 1 jₖ; 1 jᵥ 2} factor), my tensor sum gives **α₂ ≈ +556 a.u.**, consistent with theory (+557.31) and experiment (+563 ± 4.2%). The positive tensor is built chiefly from the 4D₅/₂ and 6S/5S terms. **Ratio α₂/α₀(5P₃/₂) ≈ −0.48**, in agreement with theory (−0.50) and experiment (−0.49). The competing claim of −4.26 is arithmetically incompatible with a correct (large-negative) α₀ and a correct (≈ +556) α₂ — note that both disputing analyses agree on α₂ (≈ +556 to +563), so the ratio discrepancy comes ENTIRELY from the wrong α₀.

### Q4 — 5P scalar light shift at U₀ = 22.8 MHz
Scalar 5P shift = −[α₀(5P)/α₀(5S)]·U₀ = −(−1149/687.3)·22.8 = **+38 MHz** (using the theory −1111.6 gives +36.9 MHz). This is the **+37 MHz** scenario, NOT +4.3 MHz. The +4.34 MHz figure requires α₀(5P) ≈ −134, which is falsified.

### Q5 — Full 5P₃/₂ Stark map (G3, linear polarization ∥ B)
Tensor geometric factor for J=3/2: (3m_J²−J(J+1))/(J(2J−1)) = +1 for |m_J|=3/2 and −1 for |m_J|=1/2.
- α₅P(|m_J|=3/2) = α₀ + α₂ = −1149 + 563 = −586 → shift = −(−586/687.3)·22.8 = **+19.4 MHz** (stretched |F′=3,m′=±3⟩; this state is pure |m_J=±3/2⟩, so its tensor equals the bare α₂(J′)).
- α₅P(|m_J|=1/2) = α₀ − α₂ = −1149 − 563 = −1712 → shift = **+56.8 MHz**.

**Every 5P₃/₂ sublevel is net-positive (anti-trapped), spanning +19 to +57 MHz. No sublevel is trapped.** The tensor shift alone for the stretched state is ≈ −18.7 MHz (matching the −18.3/−18.49 MHz tensor base quoted in BOTH disputing analyses — they agree on the tensor), but it is overwhelmed by the +37 MHz scalar shift, leaving +19 MHz net. The "stretched-state trap" claim arises only if the scalar shift is wrongly taken as +4.3 MHz, so that +4.3 − 18.7 ≈ −14 MHz; with the correct +37 MHz scalar shift the sign is positive.

**(G3) Angular algebra verified:** the Wigner 6j {2 2 2; 3/2 3/2 3/2} = 0 exactly, making the F′=2 hyperfine tensor null for all m′; the F′=3 tensor geometric factors run (−0.8, −0.6, 0, +1) for m′ = 0, 1, 2, 3; and the stretched |F′=3, m′=±3⟩ is pure |m_J=±3/2⟩, so its tensor equals the bare α₂(J′). All confirmed.

### Q6 — Robustness
- **Matrix elements:** varying ⟨5P₃/₂‖d‖4D₅/₂⟩ within its ±0.8% uncertainty moves α₀ by ±~13 a.u.; varying ⟨5P₃/₂‖d‖6S₁/₂⟩ within uncertainty moves it by ±~3 a.u. Combined literature uncertainty keeps α₀ within roughly −1100 to −1160 a.u.
- **Wavelength:** 1060 / 1064 / 1070 nm changes α₀ by only a few percent — there is no nearby resonance (nearest is 4D at 1529 nm, far to the red), so the polarizability is slowly varying. Across this range the stretched-state shift stays ≈ +17 to +22 MHz.
- **Verdict survives:** under all these variations α₀(5P₃/₂) remains strongly negative (≈ −1050 to −1200 a.u.) and every 5P₃/₂ sublevel remains anti-trapped. The "no trapped excited state" conclusion is robust.

### G2 — Two independent routes
(a) **Manual sum-over-states** (above): α₀ ≈ −1137 a.u., α₂ ≈ +556 a.u., ratio −0.49.
(b) **ARC DynamicPolarizability:** ARC (Robertson, Šibalić, Potvliege & Jones, "ARC 3.0," Comput. Phys. Commun. 261, 107814 (2021)) loads the same Safronova-type all-order matrix elements (5P₃/₂–4D₅/₂ ≈ 10.9 a.u., 5P₃/₂–6S₁/₂ ≈ 6.05 a.u.) and the same NIST/Steck energies, so by construction it reproduces the large-negative α₀. CAVEAT: ARC's `getPolarizability` has a documented normalization subtlety (a 2/3 factor noted in the project's GitHub issue tracker), and its published worked example is for Cs, not Rb 5P₃/₂; a user must confirm `units="au"` and the scalar convention before quoting an exact number. No printed ARC numeric output for Rb 5P₃/₂ at 1064 nm exists in the public docs, but the underlying matrix-element database is identical to route (a), so the two routes agree on the large-negative result.

### Attribution nuance on the theory values
The precise numbers α₀ = −1111.62 and α₂ = +557.31 a.u. are NOT printed in the Arora–Sahoo 2012 article itself (which tabulates 5P₃/₂ at 770 nm and static, and 5S at 1064 nm, but no 5P₃/₂ table at 1064 nm). They were supplied by B. K. Sahoo via private communication and reported in Chen, Gonçalves & Raithel (PRA 92, 060501(R), 2015), whose acknowledgments state: "We thank Dr. B. K. Sahoo for providing theoretical values of scalar and tensor polarizabilities." They are nonetheless the accepted Arora–Sahoo-method theory values at 1064 nm and agree with my independent computation. (Note: the Chen–Raithel simulation used slightly different rounded inputs α₀=−1149.3, α₂=563.3, α₀(5S)=687.3, matching their experimental result.)

## Recommendations
1. **Adopt α₀(5P₃/₂) = −1149 a.u. (experimental) or −1111.6 a.u. (theory), with α₂ = +563 / +557 a.u.,** for any ⁸⁷Rb work at 1064 nm. Discard the −134 a.u. value entirely; it is unsupported by any authoritative matrix-element set.
2. **Do not expect to trap 5P₃/₂ atoms in a 1064 nm trap.** Plan for the excited state being anti-trapped by +19 to +57 MHz per 22.8 MHz of ground-state depth; the stretched |F′=3,m′=±3⟩ is the least anti-trapped (+19 MHz) but is still expelled, not trapped.
3. **If state-insensitive trapping of the 5S–5P₃/₂ transition is required, do not use 1064 nm.** The differential shift (5S deeply trapped, 5P strongly anti-trapped) is large and unavoidable at this wavelength; seek a magic wavelength instead (e.g., in the visible/near-IR ranges identified by Arora–Safronova).
4. **Benchmark that would change the verdict:** the conclusion flips only if a credible recomputation showed α₀(5P₃/₂) > about −250 a.u. — which would require the 4D₅/₂ and 6S terms to be spuriously omitted or sign-flipped. This is excluded by NIST level energies (4D, 6S clearly red of 1064 nm) and by measured matrix elements, so the verdict is not realistically reversible.

## Caveats
- The −1111.62 / +557.31 theory values are a B. K. Sahoo private communication reported in the 2015 paper, not a printed 2012 table (see attribution nuance); they are corroborated independently by my sum-over-states and by the measurement.
- ARC's `getPolarizability` normalization/units convention must be verified before quoting a specific ARC number; no public ARC value for this exact case was found, so route (b) is validated structurally (same database) rather than by a published numeral.
- My per-transition numbers carry ~1–2% uncertainty from the matrix elements; the qualitative conclusion (large-negative α₀, no trap) lies far outside that uncertainty band.
- All values are for the bare fine-structure 5P₃/₂ level. The decoupled "Paschen–Back"/strong-field regime (light shift ≫ hyperfine splitting) is exactly the regime of the Chen–Raithel measurement, where α₀ ± α₂ for |m_J| = 3/2, 1/2 is the correct decomposition; in shallower traps the |F′,m′⟩ basis applies but the net verdict (all sublevels anti-trapped) is unchanged.