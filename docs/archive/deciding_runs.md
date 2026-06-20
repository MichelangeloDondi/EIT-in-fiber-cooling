# Deciding-run evidence layer (2026-06-20)

> **Status: archived evidence, not authority.** The *verdicts and physics reasoning* live in the
> `docs/` findings (linked per entry); this file preserves the *raw results that produced them* —
> the numbers a future reader would need to audit or reproduce the decisions. The `/tmp` solver logs
> were ephemeral (machine reboots / `/tmp` wipes during the session) and are gone; the values below
> are transcribed from the runs as they completed. Regenerate with the named scripts to re-verify.

---

## 1. Clock m′=0 leg-swap — control↔probe (clk2.py gate)

**Verdict (live):** [`clock_leg_swap_finding.md`](../../clock_leg_swap_finding.md), CLAIMS LS2 — swap
**rejected**, config A holds ~3.8×. **Engine:** `clk2.py` (= `clock_combined_solve.py` + surgical
hooks; integrity-diff clean). **Point:** B=1.5 G, Dc=80, η=0.094 symmetric.

| run | config | ⟨n_z⟩ | frame-conflict | note |
|---|---|---|---|---|
| clean-Λ (Nf 6/8/10) | A (dark \|1,−1⟩) | **0.0072** | 0.00 | swap-hook validator |
| clean-Λ | B (swap, dark \|2,+1⟩) | **0.0022** | 0.00 | isolated diffusion lever (3.3×) |
| full repumped (rep2=A, Drep1=20, Drep2=5, OmR=0.25, Nf=8) | A | **0.0048** | 0.00 | hard-converged |
| full repumped (swap, rep2=A forced, Drep2=20, OmR=0.25) | B, Nf=6 | 0.0137 | 0.0 | tail 0.391 |
| " | B, Nf=8 | 0.0139 | 0.0 | tail 0.485 |
| " | B, Nf=10 | 0.0140 | 0.0 | tail **0.558** |

**Reading:** config A is flat/hard-converged at 0.0048; config B's Fock tail **rises monotonically**
(0.391 → 0.485 → 0.558 over Nf 6→8→10) → ⟨n⟩ diverges with truncation (best bounded ≈0.018) → A
favored ~3.8×. Cause: the F=2-interior dark leg forces rep2=A (the unique protecting repump), which
cannot clear \|2,+2⟩ → near-flat heating tail. **frame-conflict = 0** throughout ⇒ B's divergence is
physics, not a rotating-frame artifact. The EOM-Raman \|2,+2⟩ clearer was also tested and rejected
(window empty). *Convention note:* these are the η=0.094-symmetric deciding-run absolutes; the
convention-robust result is the **relative 3.8×** (not a new single-end floor).

## 2. F′=1 repump dwell — retires the high-dwell branch

**Verdict (live):** [`ANTITRAP_RESOLUTION.md`](../ANTITRAP_RESOLUTION.md), SSOT `repump_dwell_status`.
**Script:** `src/dwell.py` (clk2-native).

- Measured **P_e(F′1) = 8.4×10⁻⁶** (clk2 config A steady state), **5× below** the 4×10⁻⁵ low-dwell
  reference; F′2 residual 1.8×10⁻⁵ cross-checks the dark-state ~4×10⁻⁵.
- ⇒ firmly **low-dwell**; the grid high-dwell bracket (0.026–0.053) does not apply; the certified
  single-atom floor **0.008–0.010** stands, and the +0.003 squeezer increment is conservative.

## 3. Radial dynamic Monte-Carlo — the cloud is benign

**Verdict (live):** [`audit_radial_dynamic_MC.md`](../audit_radial_dynamic_MC.md),
`clock_EIT_consolidated.md` v16 §8. **Pipeline:** `src/radial_mc/` (data: `data/scan_400.npz`).

- Realized cooling floor sits **below** the quasi-static ceiling: the cooling rate W(r) peaks at the
  cold center, anti-correlated with n_ss(r) → cooling-rate-weighted limit cycle pulled cold.
- Suppression vs quasi-static **≈ 1.2 / 3.0 / 7.4×** at T_r = 25 / 100 / 400 µK (3-level engine →
  ratio result, not the clock magnitude). Frozen-position bound (0.0064/0.0126/0.0266) superseded as
  a realized ceiling. The anti-trap squeezer is de-risked (P_e(F′2) *falls* off-axis).

## 4. Regression re-pin anchors (qutip-5 stack)

**Live:** the `_regression` anchors in `src/eit_cooling_tool.py` + the pin in `requirements.txt`
(numpy 2.0.2 / scipy 1.13.1 / qutip 5.0.4). Archived here only as the **convergence-gate method**
that justified the re-benchmark: each new anchor confirmed the *converged unique* steady state —
residual ‖Lρ‖/‖ρ‖ ~1e-15, Tr ρ = 1 to ~1e-16, min-eigenvalue strictly ≥ 0 (PSD), Fock-tail
P(n=Nf−1) ≤ 3e-7 — so the old (qutip-4) values were under-converged, not the new ones wrong. The
re-benchmarked set moved e0→0.0022, e3→0.0030, dual→0.00587 (single 0.0075 unchanged).
