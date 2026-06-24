# Repo sync manifest — for Claude Code

Repo: `github.com/MichelangeloDondi/EIT-in-fiber-cooling`. Standing split: this chat decides/drafts;
Claude Code touches the repo. **Provenance matters** — Claude Code cannot see this chat's
`/mnt/user-data/outputs`. Items marked **[pull]** are files Michelangelo downloads from the chat and
drops into the repo; items marked **[repo-edit]** are edits Claude Code makes to files already in the
repo; items marked **[verify]** change nothing.

Do these as **two commits** (A = the ready docs; the re-pin verify is separate/trivial). Hold C and D.

---

## A — COMMIT NOW (ready, no unresolved dependency)

### A1. `clock_branching_check.py` — **[pull]**, NEW file (repo root, with the other `verify_*`/`audit_*` scripts)
The R2 tracked-number script for the cooling-excited-state dark-leg branching. Computes |F′2,0⟩ (clock)
and |F′2,2⟩ (stretched) renormalized dark-leg branching from first principles (6j × CG²), and
**self-gates**: it asserts the stretched value reproduces `verify_tagged_solve.py:32` (0.75/0.25) before
reporting the clock value (0.25/0.75).
- **Post-add validation (required):** run `python clock_branching_check.py` — the GATE assert must pass.
- **Commit rationale:** "Add clock_branching_check.py: first-principles |F′2,0⟩ vs |F′2,2⟩ dark-leg
  branching, gate-validated against verify_tagged_solve:32 (0.75/0.25); clock renorms to 0.25/0.75."

### A2. `clock_leg_swap_finding.md` — **[pull]**, NEW file (repo root, with the audit/finding docs)
Durable record of the control/probe leg-swap thread. **Status is [O] OPEN by design** — it records a
verified result (the |F′2,0⟩ branching reverses vs |F′2,2⟩; the isolated diffusion lever is 3.29×) AND a
**falsified** headline (the naive swap is 3.3× *worse* in the full repumped system; "swap wins" withdrawn).
It does not bake in an unresolved conclusion; it documents the open state and names the deciding run.
- **Commit rationale:** "Add clock_leg_swap_finding.md: |F′2,0⟩ branching reverses the diffusion lever
  (3.29× isolated) but the naive swap is 3.3× worse as-repumped; verdict OPEN pending the re-pointed
  deciding run. Supersedes stretched-scheme leg numbers; cross-refs clock_branching_check.py."

**Suggested commit A:** `git add clock_branching_check.py clock_leg_swap_finding.md` →
"Add clock leg-swap branching check + finding (branching reversal verified; swap verdict open)."

---

## B — VERIFY (closes the already-shipped re-pin; no file change) — **[verify]**

The regression re-pin already shipped this session (commit 74786c7). The one open tick: run **only the
`_regression` assertion block** (sub-second, *not* the 5 h full `--regression`) and confirm all seven
anchors assert green against the committed bands — pure transcription insurance that
e0→0.0022 / dual→0.00587 / e3→0.0030 (tolerances untouched) were typed correctly. If the diff review
already showed each band bracketing its measured value, this is covered — confirm and close.

---

## C — HOLD (ready except for a named upstream trigger; do NOT push yet)

### C1. `cloud_floor_spec.md` — HOLD until the reabsorption-brief revision lands
The chat copy is **correct but mid-revision**: the *safe* edit is in (band/Conclusion 1 withdrawn to
[O] after the red team; s(r)=19 µm fix; CPL tags), but the *positive* restructure (endogenous-T_r-via-
2b-static; the corrected §2c–§2e and Conclusions 2/4) was deliberately **held** pending the radial→axial
coupling **brief revision, which leads**. Pushing now commits a document that says "[O], under revision"
in several places and that you will immediately re-edit.
- **Trigger:** the reabsorption-brief revision is written → revise the spec against it → push **once**,
  complete. (The repo's *current* copy is stale and asserts the falsified "expected small" — so if you
  want an interim honesty fix, the minimal move is to mark the repo copy's reabsorption block `[O] —
  under revision, see chat` rather than ship the half-revised version. Your call; default is hold.)

### C2. Thermometry scheme reconciliation — `thermometry_audit.md` — **[repo-edit]**, HOLD until the leg-swap deciding run
The repo doc describes the park→read transfer for **m′=2 stretched** cooling (`|1,+1⟩ → |1,0⟩`,
Δm=−1). The cooling we run is **m′=0 clock** (confirmed) — so the transfer is from the clock dark leg,
**currently `|1,−1⟩ → |1,0⟩` (Δm=+1)**. Two reasons to hold rather than one-line patch now: (i) the exact
dark leg depends on the **unresolved leg-swap** (if the swap wins, dark → |2,+1⟩ and the transfer adapts
again); (ii) the doc likely carries **other** m′=2 assumptions that want a coherent pass, not a single
edit.
- **Trigger:** leg-swap deciding run resolves the dark leg → do one coherent m′=0 pass of the thermometry
  doc (park-transfer line + any other stretched-scheme residue). Fold into the leg-swap-resolution commit.

---

## D — NOT SAVED (exist only inline in the chat; save first if you want them tracked)

- **1560 nm 5P₃/₂ polarizability audit brief** — drafted in chat, never saved as a file. If you want it
  tracked (it pairs with the existing `Rb-87_5P3_2…1064nm…md`), ask the chat to emit
  `audit_brief_1560_polarizability.md` first, then it joins commit A as a **[pull]**. *(Also still gated
  on the apparatus question: is the in-fibre lattice 1064 or 1560? Moot for cooling if 1064.)*
- **Leg-swap reply to the external auditor** — inline only; the durable content is in A2 (the finding),
  so no separate file needed unless you want the correspondence archived.

---

## Order of operations
1. Commit A (A1 + A2), run the A1 gate, push.
2. Confirm B (the `_regression` assertion tick) — closes the re-pin thread.
3. Leave C1, C2 parked on their triggers. Leave the leg-swap **deciding run** parked on the Prevedelli
   σ⁺-forward polarization check (unchanged).
