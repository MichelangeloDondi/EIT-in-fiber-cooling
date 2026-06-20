# External audit — D1 (795 nm) fiber-buildability gate G1, given the PI's 780-guidance confirmation

**How to use:** hand to an external auditor / fresh chat. **This is NOT a re-evaluation of the D1
physics** — that is settled (S1–S4, External Audits A and B, `D1_hybrid_consolidated_findings.md`,
`EIT_brief_v11.md` §12; two independent rebuilds reproduced every number). It evaluates *one* thing: how
much the PI's new confirmation that the fiber guides **780 nm** well clears the **G1 fiber-buildability
gate** for a 795 nm variant, and what 795-specific characterization remains. House style: concise,
[V]/[I]/[O] tags, cite source + line, attack the [I] rows. Compute/verify, don't assert.

## Settled physics — INPUT, do not re-litigate (cite, don't re-derive)
- **Pruning theorem [V]:** a coherent cooling Λ must live on one line (same-line legs 6.835 GHz → one EOM
  bridges; cross-line 7.12 THz → comb-only). Three candidates: **H1** (cool D2 / repump D1), **H2** (cool
  D1 / repump D2), **full-D1**. (`D1_hybrid_consolidated_findings.md`, "Organizing theorem".)
- **No floor gain on any variant [V comparisons / I absolute]:** the floor is recoil/branching-limited and
  **line-independent** — b_leak is exactly 1/3 (m′=2), 2/3 (m′=0) on both lines (a 6j identity); GATE A
  coherent floor = **0.0072 [V]**, reproduced bit-for-bit. **full-D1 is dead** (F′=1 branching inverts
  5/6:1/6→1/6:5/6 → recycler 1.65× worse). H2 floor-neutral; H1 floor move <0.003.
- **The only real D1 advantage is inhomogeneous broadening, and it is isotope-tempered [V on the numbers /
  I on "sweepable"]:** ⁸⁷Rb's F′=2 antisymmetry protects the cooling resonance (|F′2,0⟩ shifts 0.30 MHz vs
  ⁸⁵Rb's 10.1 MHz) **[V, Audit B]**, so the "D2 smears the cooling line" motivation is **largely absent for
  ⁸⁷Rb**. The residual broadening lives in the F′=1 **repump** (~18 MHz), which D1 removes. Whether D2's
  repump broadening is **sweepable** by a power-broadened incoherent repump is **[I, Audit B — conditional
  on repump-parking]**, *not* verified: at source the rate penalty is **two-regime** — **mid-spread parking
  (Δ≈9 MHz off the cold F′=1 c.o.g.) ~10×, which is inside the demonstrated 16× floor-flat R window and
  holds the floor; worst-case parking (fully-shifted line, Δ≈18 MHz) ~37×, which is *outside* the 16×
  window.** So D1 is "not forced" **iff the repump parks mid-spread** (Audit B's own open Q5,
  `audit_B_adjudication.md:64`). Either way the cost is capture/rate/robustness, never the floor.
- **Hardware [V/I]:** no tapered amplifier (in-fiber EIT runs at ~0.1–1 µW); the 6.834678 GHz EOM ports to
  795 (line-independent HFS, no F′=3 forbidden zone — structurally *cleaner* than D2); cost H1 ~€3–6k, H2
  ~€6–12k (no-TA, pending quotes). The in-fiber cooling precedents (Wang radial ΛGM, Leong axial RSC) are
  **D1**.
- **Net verdict [settled]:** adoption is a **cost / cleanliness / fiber decision, never a floor one.** The
  D2 design is the validated baseline; D1 is an evaluated alternative.

**Consequence for this audit:** because D1 carries no floor gain — and the ⁸⁷Rb broadening advantage is at
best *conditionally* sweepable ([I], only if the repump parks mid-spread; see above) — **the fiber gate
decides *buildability*, not whether D1 helps.** If even the broadening advantage is [I]-conditional, the
case for D1 is *weaker*, not stronger: clearing it makes D1 an option
on cost/cleanliness grounds; it does not make D1 a performance imperative. Keep the stakes in view — do not
let "the fiber works at 795" be read as "so we should switch."

## The open gate — G1 (cite `S1_795nm_hardware_gate_memo.md` §3)
System: ⁸⁷Rb, kagome HCPCF, 48 µm core, **38 µm MFD @780**, w₀≈19 µm; 1064 nm lattice; D1–D2 gap 7.12 THz.
G1 archives the D1 line if **any** of three 795 requirements fail:
1. **[O] axial transmission (dB/m) + MFD @795** — does the kagome guide 795 with usable loss and a mode
   close to the 780 value? (A 795 IC resonance, or an MFD far from 38 µm, breaks the guided EIT condition
   / 780×795 overlap.)
2. **[O] transverse transmission + PER @795** — the side-injection gate (for a side-π repump in H1/H2):
   does the cladding pass a clean π sheet with good polarization extinction at 795?
3. **[O] 780 + 795 + 1064 coexistence** — does 795 co-guide (no guidance gap where 780 has a window)
   without perturbing the 1064 trap?

## The new datum
**The PI (Minardi) confirms the fiber guides 780 nm well** (core/axial guidance — the D2 cooling baseline,
previously an assumption, now PI-confirmed).

## The audit task — map the 780 datum onto G1, and pressure-test the inference
For each requirement, grade how much the 780 confirmation clears it:

- **Req 1 (axial + MFD @795) — strongly supported, NOT closed. [I, the central inference to attack]**
  795 is 15 nm from 780; kagome inhibited-coupling transmission windows are broad (the fiber already
  co-guides 1064 *and* 780, i.e. it is intrinsically multi-band). So good 780 axial guidance makes good
  795 axial guidance **likely by proximity**, and MFD @795 ≈ 38 µm by proximity. **But pressure-test the
  inference:** kagome IC guidance has *narrow high-loss resonances* between the broad windows — a 15 nm
  neighbor is usually safe but not guaranteed. The auditor should require the fiber's *measured/spec
  transmission spectrum* to confirm 795 sits in a window, not on a resonance. **Falsify:** 795 on/near an
  IC resonance, or MFD @795 departs enough from 38 µm to break the 780×795 overlap.
- **Req 2 (transverse PER @795) — NOT addressed by the 780 datum. [O, stays open]** 780 *axial/core*
  guidance says nothing about *transverse cladding* transmission at 795 — this is a different optical path
  (side-injected sheet through the cladding). Even the 780 transverse gate is an open bench item
  (`EIT_brief_v11.md` §16, "kagome transverse transmission + PER at 780"). **Separate 795 measurement
  required.** Fallback if it fails: axial-only repump (the ~5×10⁶-site knee), as on D2 — not a kill, but a
  constraint.
- **Req 3 (780+795+1064 coexistence) — NOT confirmed. [O, stays open]** The 780 datum is 780 (±1064);
  the coexistence requirement is specifically that **795** co-guides without a gap where 780 has a window.
  Good-780 + good-1064 does not rule out a 795 gap between them. **Needs the 795 point on the spectrum.**

## Checkable questions (for the PI / the auditor)
1. **(PI)** Does the fiber's transmission spectrum place **795 in a low-loss window** (not on an IC
   resonance), and what is the **MFD @795**? *Falsify Req 1: 795 loss ≫ 780, or MFD far from 38 µm.*
2. **(PI)** **Transverse transmission + PER @795** for a side-injected π sheet. *Falsify Req 2 → axial-only
   repump fallback.*
3. **(PI)** **780 + 795 + 1064 simultaneous guidance** — confirm 795 co-guides and the 1064 trap is intact.
   *Falsify Req 3 → a 795 gap kills all hybrids regardless of cost.*
4. **(stakes check — the one that decides whether to bother)** Given the settled physics (no floor gain;
   ⁸⁷Rb broadening advantage sweepable, not forced), **does clearing G1 change the verdict, or does D1
   remain a cost/cleanliness alternative to the validated D2 baseline?** State explicitly so "the fiber is
   fine at 795" is not mis-read as a reason to pivot.

## Disposition
- **The 780 confirmation is genuinely useful but incremental:** it (a) firms up the **D2 baseline** (the
  cooling fiber guides 780 — was an assumption, now PI-confirmed), and (b) makes Req 1 of the D1 gate
  *likely* by proximity — but it leaves Reqs 2 and 3 open and does not, by itself, clear G1.
- **The minimal path to close G1:** the 795 transmission-spectrum point (Req 1 + Req 3 in one read) plus
  the 795 transverse PER (Req 2). Three numbers, one fiber-characterization request to the PI.
- **The physics verdict is unchanged regardless:** clearing G1 makes a 795 variant *buildable* (then a cost
  decision); failing it archives the D1 line. Neither changes that D1 carries **no floor gain** for ⁸⁷Rb.
- If the auditor concurs, the only forward action is the **795 fiber-characterization request** (the
  "C pending → PI" step already named in `D1_hybrid_consolidated_findings.md` process state) — not any
  further physics work.
