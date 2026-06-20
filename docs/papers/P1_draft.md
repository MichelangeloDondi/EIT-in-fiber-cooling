# P1 — manuscript draft (settled sections)

*Working draft of the settled (non-bench-gated) sections. §V (Results) is a placeholder pending the
bench. Honesty rails (outline §43–50) are applied throughout: AXIAL ground state, never bare "3D";
headline the certified low-dwell single-atom floor n̄_z ≈ 0.008–0.010 (NOT the withdrawn 0.012–0.019
double-count; the cloud-limited value is T_r-gated, ≈0.012 at 100 µK if the radial mode is cooled — squeezer de-risked, P_e falls off-axis; dynamic MC benign), claim n̄_z ≲ 0.01–0.02; "first EIT cooling in a fibre"
(not "first cooling" — Leong 2020 = RSC); the radial mode is an input/limit, not a result. Math in
LaTeX; convertible to PRA/PRApplied LaTeX once mature. Citations are author-year keys → `references.bib`.*

**Title.** Electromagnetically-induced-transparency cooling of a field-insensitive clock pair to the
axial motional ground state in a hollow-core fiber.

**Authors (confirm with Minardi).** M. Dondi, [Nasoni], [Marchesini], M. Prevedelli, F. Minardi.

---

## Abstract

We cool the axial motion of trapped $^{87}$Rb atoms to near the motional ground state inside a
kagome hollow-core photonic-crystal fiber (HCPCF), using electromagnetically-induced-transparency
(EIT) cooling on a magnetic-field-insensitive clock pair. The cooling transition is a $\Lambda$
system in which both ground legs, $|F{=}1,m{=}{-}1\rangle$ and $|F{=}2,m{=}{+}1\rangle$, share
$g_F m_F = +\tfrac{1}{2}$, so the dark resonance is first-order immune to magnetic field at any
field — the property that lets the dark state survive the inhomogeneous trap environment the cloud
samples. The EIT fields are delivered all-fiber from a single electro-optic modulator in a
common-mode configuration that makes the two-photon coherence intrinsic to the modulation, with no
optical phase-lock. A multilevel Lindblad model that accounts for every $5P_{3/2}$ hyperfine
channel and the $1064$ nm tensor light shift predicts a single-atom axial floor of $\bar n_z \approx
0.008$–$0.010$ at low repump dwell, with the cloud-limited value comparable when the radial mode is
cooled to $\lesssim 100\ \mu$K and reported as a function of the in-fiber radial temperature. The cooling is
one-dimensional: the shallow degenerate radial mode is not addressed by this scheme and is reported
as an input that bounds the achievable state. To our knowledge this is the first demonstration of
EIT cooling of atoms confined in a hollow-core fiber.

---

## I. Introduction

Atoms trapped inside hollow-core photonic-crystal fibers combine tight, diffraction-free transverse
confinement with an interaction length set by the fiber rather than a Rayleigh range, a combination
that has driven their use for optical memories, slow light, nonlinear optics at low photon number,
and in-fiber interferometry and clock work [Bajcsy 2011; Xin 2018; Wang 2022]. The recurring
limitation across these applications is motional: the strong guided trap imposes a large
differential light shift that, combined with thermal occupation of the trap modes, dephases the
internal states and curtails the usable interrogation time [Wang 2022]. Reaching the long
coherence times these platforms promise therefore requires cooling the atoms *in situ*, inside the
fiber, where free-space sub-Doppler techniques do not straightforwardly apply.

Two features motivate the specific scheme we adopt. First, for any metrological use the cooled
states should themselves be insensitive to the environment, which points to a **field-insensitive
clock pair**: the $|1,-1\rangle / |2,+1\rangle$ states of $^{87}$Rb both have
$g_F m_F = +\tfrac{1}{2}$, so their differential Zeeman shift vanishes identically at every field
[Breit–Rabi, computed], and — because the ground $5S_{1/2}$ manifold has no tensor polarizability —
the pair is also immune to the vector light shift for a suitably polarized lattice. Cooling
directly on this pair means the cold atoms are produced already in the basis a clock or
interferometer would use.

Second, the choice of *cooling mechanism* is forced by the structure of this pair. The two ground
legs are separated by $\Delta m = 2$, and on such a pair conventional Raman sideband cooling (RSC)
encounters a rank-2 destructive-interference obstruction: the two excited-state pathways that would
return the atom to the dark leg interfere so that the sum of their amplitudes vanishes
($\Sigma_g = 0$), and the spontaneous-emission rate out of the cooling cycle cannot be suppressed by
detuning. The RSC floor consequently lifts to $\bar n \sim 0.45$ [computed]. This is an instance of
the destructive-interference structure analyzed by [Naber 2016] and we invoke it not as a new
result but as the *reason EIT is the route*: EIT cooling does not rely on a closed two-photon
Raman cycle on the dark pair, but on parking the carrier in a transparency window while a
light-shifted bright resonance enhances the red motional sideband. EIT cooling is, in addition,
intrinsically broadband (Fano-shaped), which tolerates the spread of trap frequencies a cloud in a
shallow transverse trap presents [Morigi 2018; Lechner 2016].

EIT cooling has not, to our knowledge, been demonstrated inside a hollow-core fiber: the in-fiber
cooling literature comprises Raman sideband cooling [Leong 2020], and the HCPCF cold-atom corpus is
otherwise light storage, slow light, and interferometry. We close that gap. This work demonstrates
EIT cooling of $^{87}$Rb to the **axial** motional ground state of a field-insensitive clock pair
inside a kagome HCPCF, delivered by an all-fiber single-EOM common-mode architecture. We state the
scope plainly: the scheme cools one motional dimension; the radial mode is reported as an input that
bounds the achievable state, not as a result.

---

## II. Scheme and cooling physics

### A. The field-insensitive $\Lambda$

The cooling $\Lambda$ is driven on the $D_2$ line with both legs terminating on the *same* excited
sublevel $|F'{=}2, m'{=}0\rangle$:

$$\text{probe } \sigma^+ : |1,-1\rangle \to |F'2,0\rangle, \qquad
  \text{control } \sigma^- : |2,+1\rangle \to |F'2,0\rangle .$$

The two-photon resonance is the $\Delta m = 2$ magic clock transition. Because both ground legs
carry $g_F m_F = +\tfrac{1}{2}$, the dark superposition is first-order magnetic-field insensitive at
any field; the residual second-order shift is $0.50$ kHz per unit ellipticity, and the ground
tensor polarizability is zero ($J=\tfrac12$). The two-photon detuning $\delta_2$ is *servoed* to the
dark resonance rather than held fixed, because it drifts with optical power and radial position. The
clock-magic field $B = 3.2288$ G is used only for the subsequent interrogation, not for cooling,
which may be run at any modest field ($1$–$1.5$ G).

### B. The cooling mechanism

EIT cooling places the Fano-narrowed bright resonance so that the red (cooling) motional sideband is
resonantly enhanced while the blue (heating) sideband is suppressed; the steady-state cooling rate
is the resulting net red–blue asymmetry, i.e. the Liouvillian gap. The bright state sits at the
light shift $\delta_B = \Omega_c^2/4\Delta$, and the cooling condition places it on the red sideband,
$\delta_B = \nu_z$. A non-obvious but decisive optimization is the **weaker-probe lever**: as the
probe/control ratio $\Omega_p/\Omega_c$ is lowered the cooling rate saturates while the floor keeps
falling, so the optimum sits at *weak* probe ($\Omega_p/\Omega_c \approx 0.10$–$0.12$), bounded below
only by the cooling-time/trap-lifetime budget, not at the "balanced" $\Lambda$ one might assume.

### C. No excited-state anti-trap

At $1064$ nm the $5P_{3/2}$ manifold is not trapped ($\alpha_0 = -1149\,a_0^3$,
$\alpha_2 = +563\,a_0^3$ [Chen; Gonçalves–Raithel]); crucially the cooling sublevel
$|F'2,0\rangle$ has a *pure scalar* shift of $+38.1$ MHz, because the $F'{=}2$ hyperfine tensor term
vanishes identically ($\{2\,2\,2; \tfrac32\tfrac32\tfrac32\} = 0$), so the shift is
geometry-independent. The ground $5S_{1/2}$ scalar polarizability is positive and $1064$ nm is red
of the $D$ lines, so the lattice lowers the ground state (this is the trap) and, conversely, blue
light raises it — the anchor that fixes every AC-Stark sign in the analysis.

### D. Multilevel model and operating point

The achievable state is computed with a multilevel Lindblad steady-state model: full Breit–Rabi
ground manifold, tensor-diagonalized $5P_{3/2}$, complete Clebsch–Gordan ladders, a static
multi-rotating frame, full hyperfine decay branching, and recoil. The model accounts for every
$5P_{3/2}$ hyperfine level; the parasitic $F'{=}0$, $F'{=}1$, $F'{=}3$ channels and the $1064$ nm
tensor light shift are folded into the in-trap detunings. The operating point is

$$\Delta \approx 45\ \text{MHz (flat optimum } 40\text{–}55), \quad
  \Omega_p/\Omega_c \approx 0.10\text{–}0.12, \quad
  \delta_2 \text{ servoed},$$

with the total Rabi pinned to the EIT condition $\Omega_{\rm tot} = \sqrt{4\Delta\,\nu_z}$.

**Constants.** $\nu_z = 2\pi\times 430$ kHz (stiff, axial); $\nu_r = 2\pi\times 5.42$ kHz (shallow,
degenerate radial); trap depth $U_0 = 22.8$ MHz $= 1094\ \mu$K; lattice spacing $532$ nm;
$\eta_z(780) = 0.094$, $\eta_{\rm eff}$ (retro, $2k$) $= 0.187$; $\Gamma_{D2}/2\pi = 6.07$ MHz;
$A_{\rm HFS} = 6834.683$ MHz; clock-magic field $3.2288$ G; cooling field $1$–$1.5$ G.

---

## III. Methods and apparatus

### A. All-fiber laser architecture

The EIT fields are generated all-fiber from a single electro-optic modulator driven at the $6.835$
GHz ground hyperfine splitting and frequency-doubled to $780$ nm [Marchesini 2024]; there is no
optical phase-lock loop, because the two-photon coherence between the probe and control is intrinsic
to the modulation (the two fields are sidebands of a common carrier). This common-mode generation is
an established technique for in-fiber two-photon delivery [Xin 2018]; the contribution here is its
EIT-specific implementation and characterization. Two delivery geometries realize the same atomic
operating point:

- **Dual-end, carrier-suppressed (preferred).** One arm carries the control as a clean tone; the
  other carries the probe via a phase EOM driven to the first $J_0$ zero ($\beta = 2.405$), which
  suppresses the carrier and leaves the $\sigma^+$ probe as the upper $J_1$ sideband. Opposite-end
  injection, no single-sideband modulator or filter cavity. This is the shorter, co-located-arm
  geometry and the stronger common-mode case for two-photon coherence.
- **Single-end tagged retro (fallback).** Control carrier and probe co-propagate; a double-passed
  acousto-optic tag ($2f_A = 400$ MHz, down-shifting) separates the retro-reflected return, and a
  quarter-wave plate in the retro arm flips the helicity to generate the $\sigma^+$ probe. The
  down-shift is essential — an up-shift would crash the rejected return-control into $F'{=}3$. This
  geometry routes the differential path through the full fiber and is the weaker common-mode case.

### B. Loading chain (front-end, data-complete)

The front end is data-complete [Nasoni thesis]: a 2D→3D MOT loads $\sim 10^8$ $^{87}$Rb $\sim 7$ mm
from the kagome tip; sub-Doppler molasses reaches $13.9\ \mu$K; injection couples $80$–$96\%$ into
the kagome core; and $\sim 10^5$ atoms are loaded into the in-fiber dipole trap, with conveyor-belt
transport available to move the sample into the fiber.

### C. In-fiber thermal state (input)

Loading and compression set the in-fiber thermal state, which the cooling then acts on. The axial
mode loads near $\sim 92\ \mu$K ($\bar n_z \approx 4.5$); EIT cools this, so the loaded axial
temperature sets the cooling *time*, not the floor. The radial mode is the concern: it is shallow,
degenerate, and **not addressed by this scheme**, and at the loaded compression it is hot
($\bar n_r \gg 1$). We treat the in-fiber radial temperature as an input and a limit (§IV), not a
result, and note that any reduction of it (upstream gray-molasses cooling, or a flattened transverse
trap) acts directly on the achievable floor.

### D. Detection and thermometry

Single-atom fluorescence is swamped by the $48\ \mu$m core, so detection is ensemble optical depth.
The motional state is read by sideband-asymmetry thermometry on the Raman pair, with an estimated
resolution of order $\pm 33\%$ on $(1-P_0)$ per $\sim 2000$ shots. A correlation between the floor
and the thermometer — both scale with $\eta_R \propto 1/\sqrt{\nu_z}$ — means $\nu_z$ should be
measured directly (§V) rather than inferred. Because the thermometry resolution is of order
$10^{-2}$, we claim $\bar n_z \lesssim 0.01$–$0.02$ and do not quote the sub-floor solve value,
which the apparatus cannot resolve.

---

## IV. Achievable-state model

### A. The axial floor budget

With every $5P_{3/2}$ contaminant and the optimized repumpers included, the model gives an axial
single-atom floor of $\bar n_z \approx 0.005$ (dual-end) and $\approx 0.0072$ (single-end tagged).
The contaminant budget is closed and ranked: the common, $\Lambda$-closing $F'{=}1$ level dominates
($+0.0034$, a residual dark-state coupling of $-0.31$ suppressed only by the $\sim 212$ MHz
detuning), $F'{=}3$ is secondary ($+0.0010$, control-only), and $F'{=}0$ is negligible ($+0.0001$).
The increments are non-additive; $F'{=}1$ sets the scale. The cooling cycle is repump-recycle-limited:
per spontaneous leak the recycler runs $\sim 3$ cooling and $\sim 7$ repump scattering events, so the
$\approx 0.005$ floor is set by the recycle recoil rather than the cooling or the leak. We note that
EIT cooling decisively outperforms RSC on a cloud in this geometry: at $100\ \mu$K the EIT bright
feature ($\sim 150$ kHz) covers $\sim 99\%$ of the cloud versus $\sim 19\%$ for an RSC sideband.

### B. Anti-trap, radial inhomogeneity, and the all-in floor

The all-in floor adds two effects to the solve floor, under one stated convention — the convention
matters, because conflating its terms inflated an earlier headline. The solve floor uses the ground
trap frequency for *every* internal state (traffic-in, potential-out), so it omits the heating from
excursions onto the $1064$ nm anti-trapped $5P_{3/2}$ manifold. First, then, the **anti-trap squeezer
heat**: the genuine increment is the squeezer term, faithful $-$ no-squeezer $\approx 0.003$, counted
*once* — explicitly **not** the bare recoil ($\eta^2+\eta_{\rm em}^2\approx 0.012$) nor the
no-squeezer bulk ($\approx 0.007$), both of which are already inside the solve floor. This gives a
**single-atom on-resonance floor $\bar n_z \approx 0.008$–$0.010$**. The increment is
repump-dwell-gated, and the dwell is fixed by the engine rather than assumed: the full multilevel
(clock) steady state gives an excited repump population $P_e(F'1) = 8.4\times 10^{-6}$, a factor
$\sim\!5$ below the low-dwell reference, placing the system firmly in the low-dwell regime — so the
$\sim 0.03$–$0.05$ high-dwell bracket does not apply and the floor stands at $\approx 0.008$–$0.010$.
(Low dwell is additionally structurally guaranteed for an RSC-to-$|2,0\rangle$ repump.)

Second, the **radial inhomogeneity**. The shallow, degenerate radial trap means the cloud samples a
range of trap intensities $s(r)=\exp(-2r^2/w^2)$, hence axial frequencies $\nu_z(r)=\nu_{z0}\sqrt{s}$
and — through the $+38.1$ MHz scalar shift of $|F'2,0\rangle$ — an inhomogeneous dark-resonance shift
$\Delta_{\rm eff}(r)=\Delta_0+c(1-s)$, $c=60.9$ MHz, which degrades the dark state off-axis. This is
an established mechanism (inhomogeneous dark-resonance / differential-light-shift dephasing
[1711.00732; DLS-clock literature; nanofiber gradient dephasing]), applied to this geometry, not
claimed as new. The realized cloud floor is this per-radius cooling floor integrated over the radial thermal
distribution, with the squeezer folded into the same $\nu_z(r)$/$\Delta_{\rm eff}(r)$ distribution — a
radial integral, *not* a flat increment. A quasi-static Boltzmann average of the multilevel per-radius
floor over the anharmonic trap sets a conservative ceiling $\bar n_z \approx 0.006$/$0.017$/$0.13$ at
radial temperatures $T_r = 25$/$100$/$400\ \mu$K; the steep $T_r$-dependence — at $400\ \mu$K only
$\sim\!50\%$ of the cloud is trapped — makes the in-fiber radial temperature the controlling input. A
dynamic treatment lies below this ceiling: the cooling rate $W(r)$ peaks at the cold trap center and
collapses off-axis, anti-correlated with the per-radius floor, so the realized limit cycle is the
cooling-rate-weighted average $\oint W\,n_{\rm ss}\,/\oint W$, pulled toward the center (an
orbit-level Monte-Carlo gives a $1.2$–$7.4\times$ suppression of the ceiling across $25$–$400\ \mu$K).
The anti-trap squeezer contributes little off-axis, for a reason specific to this pair: the
dark-resonance shift $\Delta_{\rm eff}(r)$ is *common* to both legs (both terminate on
$|F'2,0\rangle$), so it leaves the two-photon detuning — and hence the dark state — intact, and the
excited population driving the squeezer excursions *falls* off-axis with the weakening field rather
than rising. Combining these, the cloud-limited floor is estimated at $\bar n_z \approx
0.007$/$0.012$/$0.022$ at $T_r = 25$/$100$/$400\ \mu$K — comparable to the single-atom floor when the
radial mode is cooled to $\lesssim 100\ \mu$K, degrading only if it is left warm. (The suppression
factor is computed on a reduced three-level cooling model and transferred as a ratio; a clock-engine
dwell-weighted squeezer integral — which the disproven off-axis rate-rise now de-risks — is the one
remaining refinement.) An earlier "$0.012$–$0.019$" band is withdrawn, as it added the no-squeezer
bulk to the solve floor (a double-count). The radial mode — not the axial floor — is thus the true
figure of merit; reducing it (upstream radial cooling; a flattened transverse profile) is the lever
(§VI).

### C. Field-insensitivity and the binding noise axis

The cooling pair is first-order field-immune (both $g_F m_F = +\tfrac12$) and vector-light-shift
immune; the residual is the $0.50$ kHz/ellipticity second-order shift. The binding noise axis is the
two-photon linewidth: the floor doubles at a linewidth of $\approx 0.26$ kHz, so a sub-$100$ Hz
two-photon coherence buys $\sim 2.6\times$ margin. This sets the single decisive bench measurement
(§V).

---

## V. Results

*[Placeholder — bench-gated. To be written last. Until then §IV supplies the predicted bounds.]*
The measurement sequence, in gating order: (i) $\nu_z$ and trap depth by direct carrier–sideband
splitting (gates Lamb–Dicke, sideband resolution, the floor, and the thermometry calibration); (ii)
in-fiber detection SNR (gates observability); (iii) the **$6.835$ GHz two-photon linewidth** — the
deciding measurement (sub-$100$ Hz?); (iv) the EIT-cooling demonstration via red/blue sideband
asymmetry $\to \bar n_z$, compared to the §IV model; (v) in-fiber radial temperature after
loading/compression and sample survival $N$ versus cooling time. The whole result hinges on (iii):
if the two-photon linewidth does not clear sub-$100$ Hz, the central result does not materialize.

---

## VI. Discussion and outlook

What is achieved is the axial motional ground state of a field-insensitive clock pair, in-fiber, with
an all-fiber laser; what is not is the radial and hence three-dimensional ground state, nor
single-atom resolution. We emphasize the scope honestly: $\bar n_z \lesssim 0.01$–$0.02$ is a
one-dimensional result, the radial occupation is large and uncooled, and sample survival under
cooling is a live concern tied to the trap-depth ratio.

The axial scheme itself is, within the model, optimal against a broad family of alternatives: a
systematic search — the opposite leg assignment, a frequency-selective Raman clearer of the
stretched-state leak, double-EIT, tripod/quadrupod extensions, sequential EIT$\leftrightarrow$RSC,
and a coherent two-photon repump — each either breaks the field-insensitivity that motivates the
pair, fails on repump topology, or improves only the axial floor, which already sits below the
radial-inhomogeneity term. The recurring lesson is that on this pair the repump topology, not the
diffusion or branching intuition, decides a leg-assignment question. The consequence for the program
is that the leverage has moved off the axial $\Lambda$ entirely and onto the radial mode.

The path to a three-dimensional state is therefore radial: degenerate-Raman or gray-molasses cooling
of the transverse motion upstream of, or interleaved with, the axial stage; or — more
structurally — flattening the transverse trap profile so the inhomogeneity that bounds the floor is
removed at its source, which would benefit any cooling scheme at once. The platform implications are
direct: a cold, field-insensitive source produced inside the fiber is the enabling step for in-fiber
clocks and interferometry, and fits naturally with the HCPCF/EOM-Raman architecture developed for
in-fiber atom optics [Xin 2018; Wang 2022].

---

## VII. Conclusion

We have demonstrated electromagnetically-induced-transparency cooling of $^{87}$Rb inside a kagome
hollow-core photonic-crystal fiber, to the axial motional ground state of a magnetic-field-insensitive
clock pair, using an all-fiber single-EOM common-mode architecture — to our knowledge the first EIT
cooling of atoms in a hollow-core fiber. The cooled state has $\bar n_z \lesssim 0.01$–$0.02$ and is
produced directly in a field-insensitive clock basis. The cooling is one-dimensional; the shallow
radial mode is the next frontier, and the natural routes to it — transverse cooling and a flattened
trap profile — are identified.

---

## References

*To compile from `references.bib`. Author-year keys used above: Bajcsy 2011; Xin 2018; Wang 2022;
Marchesini 2024; Naber 2016; Morigi 2018; Lechner 2016; Leong 2020; Chen / Gonçalves–Raithel
(5P3/2 polarizability); 1711.00732 (multimode EIT); plus the DLS-clock and nanofiber-gradient
dephasing references for §IV.B.*
