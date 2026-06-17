# Paper T — §3–§4 core derivation (the rank-2 obstruction and the FoM ceiling)

LaTeX-ready. Every result is verified numerically in `src/paper_T_fom.py` (the null is exact; the
scaling and the FoM are computed). Tags: [V] = checked by the script.

## Setup
Clock pair $g_1=\lvert F{=}1,m{=}{-}1\rangle$, $g_2=\lvert F{=}2,m{=}{+}1\rangle$ in $5S_{1/2}$
($J=\tfrac12$, $I=\tfrac32$); intermediate $5P_{3/2}$ ($J'=\tfrac32$) with hyperfine levels $F'$
shifted by $\delta_{F'}$ from the line centroid. A guided $\sigma^+$ and a retro $\sigma^-$ beam
drive a $\Delta m=+2$ Raman; both legs raise $m$ by one and pass through the single intermediate
projection $m'=0$.

## Effective two-photon amplitude
Adiabatically eliminating $5P_{3/2}$,
$$\Omega_{2\mathrm{ph}}(\Delta)=\frac{\bar\Omega_1\bar\Omega_2}{2}\,G(\Delta),\qquad
G(\Delta)=\sum_{F'}\frac{g_{F'}}{\Delta+\delta_{F'}},\qquad
g_{F'}=\langle 2,1\rvert d_{+1}\lvert F',0\rangle\,\langle F',0\rvert d_{+1}\lvert 1,-1\rangle,$$
with $\bar\Omega_i$ the reduced single-photon Rabi frequencies; the line strength
$\langle J'\Vert d\Vert J\rangle$ factors out of every quantity below. Only $F'=1,2$ contribute
(the other $F'$ have a vanishing leg by the dipole triangle rule).

## The rank-2 null
For $\Delta m=2$ the two-photon operator is a pure rank-2 spherical tensor (a product of two
rank-1 dipoles, and $\lvert\Delta m\rvert=2\Rightarrow K=2$). A spin-$\tfrac12$ manifold supports
**no** rank-2 tensor operator — equivalently $\langle J{=}\tfrac12\Vert T^{(2)}\Vert
J{=}\tfrac12\rangle$ requires the triangle $(\tfrac12,2,\tfrac12)$, i.e. $0\le 2\le 1$, which
fails. In the degenerate-excited limit ($\delta_{F'}\!\to\!0$) the amplitude collapses to this
matrix element and therefore vanishes:
$$\sum_{F'} g_{F'} = 0 .$$
The explicit angular factors are $g_{1}=-g_{2}=-\tfrac{1}{4\sqrt3}\approx-0.1443$ (in units of
$\langle J'\Vert d\Vert J\rangle^2$), summing to zero identically. **[V]**

## The survivor: amplitude $\propto \Delta_{\mathrm{HFS}}/\Delta^2$
The excited hyperfine splittings break the cancellation. With $\sum_{F'}g_{F'}=0$,
$$G(\Delta)=\sum_{F'}\frac{g_{F'}}{\Delta+\delta_{F'}}
\;\xrightarrow{\;\Delta\gg\delta_{F'}\;}\;
-\frac{1}{\Delta^2}\sum_{F'}g_{F'}\delta_{F'}\equiv-\frac{G_2}{\Delta^2},\qquad
G_2=\sum_{F'}g_{F'}\delta_{F'}=g_1(\delta_1-\delta_2).$$
$G_2$ is proportional to the $F'{=}1$–$F'{=}2$ splitting of $5P_{3/2}$ ($\delta_1-\delta_2=156.9$
MHz); numerically $G_2=22.7$ MHz. Hence
$$\Omega_{2\mathrm{ph}}\propto \frac{\Delta_{\mathrm{HFS}}}{\Delta^2}.$$
**[V:** $\Delta^2G(\Delta)\to-22.7$ MHz as $\Delta$ grows.**]**

## The FoM ceiling (detuning-independent)
The off-resonant scattering rate — both beams exciting their ground state to $m'=0$ — carries the
ordinary $1/\Delta^2$ with **no** rank-2 suppression (scattering is incoherent):
$$R_{\mathrm{sc}}(\Delta)=\Gamma\Big(\tfrac{\bar\Omega}{2}\Big)^2\frac{\Sigma}{\Delta^2},\qquad
\Sigma=\sum_{F'}\big(|c^{(1)}_{F'}|^2+|c^{(2)}_{F'}|^2\big),\quad
c^{(1)}_{F'}=\langle F',0\rvert d_{+1}\lvert 1,-1\rangle,\;\;
c^{(2)}_{F'}=\langle F',0\rvert d_{-1}\lvert 2,1\rangle .$$
The coherence per spontaneously scattered photon is then
$$\boxed{\;\mathrm{FoM}\equiv\frac{\Omega_{2\mathrm{ph}}}{R_{\mathrm{sc}}}
=\frac{2\,|G_2|}{\Gamma\,\Sigma}\;\propto\;\frac{\Delta_{\mathrm{HFS}}}{\Gamma}\;}$$
— the $\Delta^2$ cancels between numerator and denominator: **the FoM does not depend on
detuning.** Numerically $\mathrm{FoM}\approx 5.6$ radians of two-photon rotation per scattered
photon ($\Sigma=1.33$, $\Gamma/2\pi=6.07$ MHz) — one cannot complete even a single sideband
$\pi$-pulse without scattering $\sim0.5$ photon. **[V]** (An independent estimate gave $\approx4$;
both are $O(\text{few})$, differing only by the scatter-normalization convention.)

**Contrast with an allowed Raman.** A $\Delta m\le 1$ transition has no null, so
$\Omega_{2\mathrm{ph}}\propto 1/\Delta$ and $\mathrm{FoM}\propto\Delta/\Gamma$ — improvable without
bound by detuning (the standard far-detuned Raman strategy). The $\Delta m=2$ clock Raman **cannot
be detuned out of trouble**: the ceiling is fixed at $\sim\Delta_{\mathrm{HFS}}/\Gamma\sim$ a few.

## §5 — the cooling floor (transparent rate equation)
The bounded FoM feeds a standard Lamb-Dicke rate equation. Driving the red sideband with repump
dissipation, the steady state is $\bar n_{\rm ss}=A_+/(A_--A_+)$, with cooling rate
$A_-=\eta_{\rm sb}^2\,\Omega_2/\Gamma_{\rm eff}$ (red sideband, repump-broadened) and heating
$A_+=R_{\rm sc}\,\eta_{\rm rec}^2$ from the off-resonant Raman-beam scatter (recoil
$\eta_{\rm rec}^2=\eta_{780}^2+\eta_{\rm em}^2$ per scattered photon). Writing
$r=\Gamma_{\rm eff}/\Omega_2$ (the repump-to-Raman ratio) and $R_{\rm sc}=\Omega_2/\mathrm{FoM}$,
$$\bar n_{\rm ss}=\frac{\eta_{\rm rec}^2/\mathrm{FoM}}{\;\eta_{\rm sb}^2/r-\eta_{\rm rec}^2/\mathrm{FoM}\;}.$$
At the obstruction-bounded $\mathrm{FoM}\approx5.6$ this is $O(0.1\text{–}1)$ — e.g. $\bar n=0.43$
at $r=5$ ($T_z\approx19\,\mu$K, $70\%$ ground), bracketing the independent estimate $0.45$. The
absolute value carries a $\pm$factor through $r$; what is robust is **(i)** $\bar n=O(0.1\text{–}1)$,
far above the obstruction-free idealization $\bar n\to10^{-3}$ ($\mathrm{FoM}\to\infty$, the regime
a standard-SBC engine returns, $\approx0.0137$), and **(ii)** reaching a useful floor
$\bar n\approx0.01$ would require $\mathrm{FoM}\gtrsim170$ — a factor $\sim30$ beyond the
$J=\tfrac12$, $\Delta m=2$ ceiling. The $\Delta m=2$ clock Raman is therefore **disqualified** for
ground-state cooling; EIT (§6) reaches $\bar n\approx0.005$. **[V:** `src/rsc_floor_rate_eqn.py`**]**

---
### Notes for the writeup
- The closed form $g_1=-g_2=-1/(4\sqrt3)$ is worth stating — it makes the null manifestly exact.
- Define the FoM explicitly as radians-per-scattered-photon so the $\sim0.5$-photon-per-$\pi$
  statement is unambiguous; flag the factor-$\sim$1.4 convention spread.
- A clean appendix can give the $|m_J,m_I\rangle$-basis evaluation (what `paper_T_fom.py` does):
  the dipole acts only on $m_J$, so $g_{F'}$ is a sum of products of three Clebsch-Gordan
  coefficients, and the null is a Clebsch-Gordan sum rule.
- Generality (§7): repeat $\mathrm{FoM}=2|G_2|/(\Gamma\Sigma)$ per alkali — only $\delta_{F'}$
  (excited HFS) and $\Gamma$ change; the null is universal for $J=\tfrac12$ ground states.
