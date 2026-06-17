# Paper T — pre-submission checklist

> ⛔ **HOLD — DO NOT SUBMIT AS STANDALONE (2026-06-17).** The central result is **prior art**
> (Naber–Spreeuw, Phys. Rev. A 94, 013427 (2016)); the scope is also narrower than the manuscript
> claims (the m=0 clock transition is coolable). Paper T is **demoted to P1 motivation**. See
> `novelty_findings.md`. This checklist applies **only if/when** the verified core is repackaged as
> part of another paper.

**Status:** complete draft; compiles clean to 5 pp (Phys. Rev. A, revtex4-2). The science is
computed and verified (see `code/`). Everything below is editorial or administrative.

## Must do before posting

### Authorship & front matter
- [ ] Confirm author list and order with F. Minardi and M. Prevedelli; add affiliations.
- [ ] Acknowledgments: funding (grant numbers), group, useful discussions (the block is stubbed).
- [ ] Set corresponding author / email (currently M. Dondi).

### References — 5 entries flagged `VERIFY` in `paper_T.bib`
- [ ] `leong2020` — HCPCF Raman sideband cooling: supply exact authors / title / journal / vol / page.
- [ ] `chiu2025` — Lukin-group tweezer EIT cooling: supply exact authors / title / journal / vol / page.
- [ ] `xin2024` — EIT sideband cooling: supply exact authors / title / journal / vol / page.
- [ ] `steck_rb` / `steck_cs` / `steck_na` — confirm current revision numbers and years.
- [ ] `tiecke_k`, `gehm_li` — confirm.
- [ ] (Optional) cite the apparatus paper (Marchesini *et al.*, Opt. Continuum **3**, 1868 (2024))
      where the single-end tagged delivery is mentioned (sec VI); add tweezer-clock motivation
      refs in sec I if desired.

### Content review (your voice / your physics)
- [ ] Read sec I/II/VI/VIII — they are first drafts.
- [ ] Confirm the EIT floor numbers (0.0048 / 0.0072) match your latest clock-EIT solve.
- [ ] Internal review with Minardi before anything external (unpublished-work caveat).

## arXiv mechanics
- [ ] Primary category: **quant-ph**; cross-list: **physics.atom-ph**.
- [ ] Endorsement: confirm you (or Minardi) can submit to quant-ph.
- [ ] License: choose (arXiv default or CC-BY).
- [ ] Upload set: `paper_T.tex`, the three files in `figures/`, and **either** `paper_T.bib`
      **or** the generated `paper_T.bbl`. Safest: compile locally, then upload `paper_T.bbl`
      alongside the `.tex` so arXiv need not run BibTeX. **Delete `paper_TNotes.bib`** (a revtex
      build artifact) from the upload.
- [ ] Do one clean local compile from exactly the upload set before submitting.

## Optional polish
- [ ] A sentence in sec I or VI placing the result in your fibre-apparatus context.
- [ ] If you open-source `code/`, add a one-line data-availability / code pointer.

## Already verified — no action needed
- Rank-2 null  Σ g = 0  — exact  (`paper_T_fom.py`, `paper_T_generality.py`).
- FoM ≈ 5.6, independent of detuning  (`paper_T_fom.py`); floor n̄ ≈ 0.45 and the FoM ≳ 170
  threshold for n̄ ≈ 0.01  (`rsc_floor_rate_eqn.py`).
- Generality: universal null for I = 3/2 … 7/2; FoM 0.2 (Li) → 9.3 (Cs)  (`paper_T_generality.py`).
- Manuscript build: 0 undefined references/citations, 0 overfull boxes, 5 pages.
