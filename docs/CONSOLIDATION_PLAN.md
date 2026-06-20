> **[EXECUTED 2026-06-20]** PR #4 (`claude/floor-correction`) landed gate-green: SSOT now uses `squeezer_increment_lowdwell` (0.003 scalar) → all-in 0.008–0.010, master is **v16**, SCOPE defers detection/survival to CLAIMS. **This is a historical plan** — references below to v15 / `antitrap_leak_increment` / 0.012–0.019 describe the PRE-correction state. Current authority map: `INDEX.md`.

# Consolidation plan / discussion — session 2026-06-20 (floor correction + radial analysis)

**For Claude Code.** Two chats produced new work this session (this decision chat + the radial-MC
chat). The important part: a **correction that supersedes content already in the repo** — PR #2's v15
and the committed `operating_point.py` both headline a floor number this session found to be wrong.
So consolidation = propagate the correction + land the new analysis + re-sync, not just file-sync.
Below: the critical flag, the same-name rule (your explicit question), the artifact inventory, a
proposed PR structure, and the branch decisions I need from you (you hold the repo state; I hold the
new artifacts).

---

## 0. CRITICAL — the repo's floor number is wrong as committed

`operating_point.py` (`antitrap_leak_increment=(0.007,0.012)`, `all_in_single_atom ~ (0.012,0.019)`)
and `docs/clock_EIT_consolidated.md` **v15** both headline **0.012–0.019**. This session (two-instance
audit) found that's a **double-count**: the 0.007 increment ≈ the no-squeezer bulk ≈ the solve floor,
so `solve + increment` counts the clean floor twice; the 0.012 upper edge ≈ the bare recoil
η²+η_em², already inside the solve. Corrected, under one convention (solve = traffic-in/potential-out;
add the squeezer heat = faithful − no-squeezer ≈ 0.003, **once**):

- **certified single-atom floor 0.008–0.010** (low-dwell);
- **high-dwell branch RETIRED** — measured: clk2 config-A P_e(F′1)=8.4×10⁻⁶, 5× below the low-dwell ref;
- **cloud benign** — clk2 clock-unit quasi-static 0.0056/0.0169/0.130 at T_r=25/100/400 µK; MC shows
  realized < quasi-static; squeezer de-risked (P_e(F′2) *falls* off-axis, rate-rise disproven);
  cloud all-in ~0.007/0.012/0.022, **T_r-gated**;
- old **0.012–0.019 withdrawn**.

The corrected `operating_point.py` is in `/outputs` (runs clean). **`clock_EIT_consolidated.md` v15 →
v16 still needs drafting** (the §8 floor section + the cloud table). v15 was written *early* this
session, before the correction — it is not a reliable doc as committed. I can draft v16; flag if you
want it before or after the branch decision.

---

## 1. Same-name / different-content rule — YES, keep exactly one per name

Your question: *for files with the same name, can we keep only one even if they differ?* **Yes, and you
should — never carry same-name-different-content duplicates.** Three cases:

1. **Versions of one artifact** (same path, different content — `operating_point.py` old vs corrected;
   v14/v15/v16 of the consolidated doc): commit the new one; **git history preserves the old**. The
   repo holds ONE per path, always. No duplicate files.
2. **Project knowledge** flattens to basenames, so same-name-different-content *is* the staleness trap
   that bit us this session (I grabbed a stale intermediate). Fix: **clear stale PK and re-sync from
   the repo** after the commits land → PK then holds one canonical per name (the latest). Do not
   hand-upload old + new together.
3. **Different artifacts sharing a basename** (the repo-root `README.md` vs the radial-MC pipeline's
   `README.md`): git keeps both by *path* — no collision — but PK collides on the basename. **Rename
   one for PK** (e.g. `README_radial_mc.md`), exactly as was already done for
   `README_eit_cooling_tool.md`. Check for other basename clashes when you stage the MC pipeline.

---

## 2. Artifact inventory (what's new in /outputs and the radial-MC chat)

**A. Floor correction — HIGH priority, mergeable, independent of fmix:**
- `operating_point.py` (corrected) → replaces repo `operating_point.py` *(git history keeps the old)*
- `clock_EIT_consolidated.md` **v16** → supersedes v15 *(needs drafting — see §0)*
- `P1_draft.md` (settled paper sections, corrected §IV.B) → new, `docs/` or `paper/`
- `INDEX.md` → `docs/INDEX.md` — the authority router (the durable fix for the staleness trap)
- **promote** `ANTITRAP_RESOLUTION.md`, `floor_gap_resolution.md` from archive → `docs/` (INDEX points
  at them as load-bearing; they should not live in archive)

**B. Analysis artifacts (briefs + scripts):**
- briefs: `audit_squeezer_integral_MC.md`, `audit_radial_dynamic_MC.md`, `flat_top_feasibility.md`,
  `flatness_spec_result.md` → `docs/`
- scripts: `flatness_spec.py`, `dwell.py`, `radial_pe.py`, `grid_avg_cloud.py` → `src/`
  (the floor computations; each gates on a known anchor — see headers)

**C. Radial-MC pipeline (from the radial-MC chat):**
- `mc.py`, `grid_build.py`, `engine.py`, `make_figure.py` → `src/` (a `radial_mc/` subdir is clean)
- `s3_radial_mc.png` → `figures/`; data `grid_cache.npz`, `scan_400.npz` → `data/` (or .gitignore if
  regenerable — they are, from `grid_build.py`)
- the MC `README.md` → rename for PK (case 3 above)

**D. clk2.py note:** my /outputs copy has a tiny additive change (the `want_pops` return split into
F′1/F′2, used for the dwell measurement). The **repo's gate-validated clk2.py is canonical**; the split
is optional — fold it only if you want the dwell-readout reproducible in-repo, and re-run the gate if so.

---

## 3. Proposed PR structure (for your call — §4)

The floor correction must NOT wait behind PR #2's fmix gate. Cleanest is a **new PR off `main`**
(`claude/floor-correction`), mergeable-now like PR #3 was, carrying §2.A + §2.B + §2.C. **But** v16
supersedes the v15 you just committed to PR #2 — so v15 on PR #2 becomes redundant. Options for you to
weigh:

- **(a)** New floor PR off main with v16; merge it; then **rebase PR #2** onto new main — PR #2's v15
  diff drops out, PR #2 keeps only the two D1 audits (which v16 should reference). Fmix stays parked.
- **(b)** Since PR #2 already has v15, put v15→v16 *on PR #2's branch* and unblock it from fmix by
  splitting fmix to its own PR. (Heavier surgery; depends how entangled fmix is on that branch.)
- **(c)** Something else you see from the actual branch state.

I lean **(a)** — it keeps the important correction on a fast, independent path and leaves the parked
fmix work parked. The D1 audits (PR #2) are unaffected either way.

---

## 4. Decisions I need from you (you hold the repo state)

1. **Branch structure** — (a)/(b)/(c) above? Where does v16 land so it supersedes v15 cleanly without
   blocking on fmix?
2. **Paths** — confirm `docs/` for the briefs + INDEX + promoted resolutions; `src/radial_mc/` for the
   pipeline; `figures/` + `data/` (or gitignore the .npz)?
3. **Basename clashes** — does staging the MC `README.md` (and any other pipeline file) collide with an
   existing repo basename? Rename for PK accordingly.
4. **v16 timing** — want me to draft v16 now (so the floor PR is complete), or stage the corrected
   `operating_point.py` + INDEX first and add v16 next?
5. **fmix** — still your call (parked). It only matters here insofar as it gates PR #2; the floor
   correction routes around it.

---

## 5. Final step — re-sync project knowledge (the durable fix)

After the floor PR (and PR #2/#3) land: **clear the stale project knowledge and re-upload from the
repo.** That replaces every stale version in one step (the v14→v16, the old operating_point.py, the old
leg-swap note), eliminates same-name-different-content collisions (§1), and makes `docs/INDEX.md` the
in-PK authority map. This is the move that prevents a repeat of this session's stale-file error — more
than any individual deletion.
