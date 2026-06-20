# archive/ — results of lasting value, not the live record

This is the narrow tier between the **live authoritative docs** (`docs/`, routed by
[`docs/INDEX.md`](../INDEX.md)) and **git history** (which already holds every superseded file
version). It exists for results that have **standalone explanatory or evidential value but no
live home** — and for nothing else.

## Inclusion test (the anti-museuming rule)

> Archive *X* **only if deleting *X* would lose understanding or reproducibility that neither git
> history nor the live docs already preserve.**

If git history holds it (any superseded file version), or a live doc already carries the
conclusion and its evidence pointer, it does **not** belong here. That single test excludes the
usual museum exhibits:

- superseded file versions (v14/v15 of the master doc, old `operating_point.py`) → **git history**;
- redundant or intermediate drafts, drop folders (`files-NN/`), duplicate INDEX copies → **discard**;
- process scratch (`sync_manifest.md`, the consolidation saga) → **not a result**;
- regenerable logs whose conclusions are already in the live docs → **regenerate, don't hoard**.

## Promotion (the inverse operation)

If an archived result later becomes load-bearing, **promote it to `docs/`** and route it from
`INDEX.md`. (This is the direction the floor-correction INDEX already describes for
`ANTITRAP_RESOLUTION.md` / `floor_gap_resolution.md`, which were promoted *out* of archive because
they became load-bearing.)

## Gate scope & the banner rule

`audit/check.py` deliberately does **not** scan `archive/` — archived snapshots legitimately
contain withdrawn numbers (e.g. the pre-correction `0.012–0.019` all-in band). To keep that honest,
**any archived doc that carries superseded numbers MUST open with a dated `SUPERSEDED` banner**
pointing to the current authority (`docs/INDEX.md` / the SSOT / v16). A reader who lands here out of
context must learn in the first line that this is not live.

## Index

- [`D2_baseline_consolidation.md`](D2_baseline_consolidation.md) — 2026-06-19 snapshot of the
  **adopted-D2-scheme + alternatives-sweep disposition**: *why* D2 m′=0 clock cooling was kept over
  D1, RSC, and the control↔probe leg-swap. SUPERSEDED-banner'd (its `0.012–0.019` headline is the
  withdrawn double-count). `INDEX.md` does not route to it; kept as the provenance record of *why we
  did not go elsewhere* — the rationale a returning collaborator or paper-writer would want.
- [`deciding_runs.md`](deciding_runs.md) — the **evidence layer** behind the live verdicts: the raw
  results of the clk2 leg-swap A-vs-B gate, the F′=1 repump-dwell measurement, and the radial
  dynamic-MC suppression. The conclusions live in the `docs/` findings; the *numbers that produced
  them* are captured here (the `/tmp` gate logs were ephemeral and are gone).
