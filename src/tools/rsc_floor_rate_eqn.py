"""
rsc_floor_rate_eqn.py -- the clock-RSC floor from a transparent Lamb-Dicke rate equation.

Makes Paper T section 5 self-contained: the floor follows from the coherence-per-scatter
FoM (computed in paper_T_fom.py, ~5.6) plus the standard sideband-cooling rates -- no need to
cite the raman_sbc engine (which is the obstruction-free idealization, n~0.0137).

Lamb-Dicke steady state for a red-sideband Raman drive with repump dissipation and the
FoM-limited off-resonant Raman-beam scatter:

    n_ss = A+ / (A- - A+)

    A-  (cooling, n->n-1)  = eta_sb^2 * Omega2 / Gamma_eff        [red sideband, repump-broadened]
    A+  (heating, n->n+1)  = R_sc * eta_rec^2  (+ n0 baseline)    [off-resonant Raman scatter recoil]
    R_sc (off-res scatter) = Omega2 / FoM                         [definition of the FoM]

Working in units of the carrier two-photon Rabi Omega2 = 1, and writing r = Gamma_eff/Omega2
(the repump-to-Raman rate ratio, the one real operating-point knob):

    A- = eta_sb^2 / r ,   A+ = eta_rec^2 / FoM   ->   n_ss = (eta_rec^2/FoM) / (eta_sb^2/r - eta_rec^2/FoM)

The absolute number is parameter-dependent (+/- a factor, as the resolution note states); the
DISQUALIFICATION -- n_ss = O(0.1-1) at the obstruction-bounded FoM, and FoM >~ 170 needed to
reach n~0.01 -- is robust across the reasonable parameter range.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import operating_point as op

FOM = 5.6                       # computed in src/paper_T_fom.py (rank-2-limited, detuning-flat)
ETA_SB = op.ETA_RETRO_2K          # sideband Lamb-Dicke parameter (2k retro Raman), 0.187
ETA_780 = op.ETA_780          # single-beam (1k) absorption recoil, 0.094
ETA_EM = getattr(op, "ETA_EM", 0.054)
N0 = 9.6e-4                     # clean resolved-sideband baseline (no obstruction), ~0.001

# per-off-resonant-scatter recoil: single-photon absorption (1k) + spontaneous emission
ETA_REC2 = ETA_780**2 + ETA_EM**2

def n_ss(fom, r, eta_sb=ETA_SB, eta_rec2=ETA_REC2, n0=N0):
    Am = eta_sb**2 / r                 # cooling rate (units Omega2=1)
    Ap = eta_rec2 / fom + n0 * Am      # heating: off-res scatter recoil + baseline diffusion
    return Ap / (Am - Ap) if Am > Ap else float("inf")

print("="*74)
print(" CLOCK-RSC FLOOR from a transparent Lamb-Dicke rate equation")
print("="*74)
print(" inputs:  FoM = %.1f (rank-2-limited, from paper_T_fom.py)" % FOM)
print("          eta_sb (2k sideband) = %.3f ;  eta_rec^2 = eta_780^2+eta_em^2 = %.4f" % (ETA_SB, ETA_REC2))
print("          r = Gamma_eff/Omega2 (repump:Raman ratio) -- the operating-point knob")
print("-"*74)
print(" n_ss at the obstruction-bounded FoM = %.1f, vs repump:Raman ratio r:" % FOM)
for r in (1.0, 2.0, 3.0, 5.0, 8.0):
    n = n_ss(FOM, r)
    print("     r = %4.1f :  n_ss = %.3f   (ground fraction %4.1f%%, T_z ~ %4.0f uK)"
          % (r, n, 100.0/(1.0+n), op.NU_Z_MHZ*1e6*4.79924e-5*(n+0.5)))
print("   -> O(0.1-1); the independent estimate 0.45 sits at r~5 (strong repump). NOT 0.0137.")
print("-"*74)
print(" contrast: the obstruction-FREE idealization (FoM -> infinity) collapses to the baseline:")
print("     FoM -> inf :  n_ss -> %.4f   (= raman_sbc 'clock' idealization, ~0.0137 regime)" % n_ss(1e6, 5.0))
print("-"*74)
print(" DISQUALIFICATION threshold -- FoM needed to reach a useful floor (r=5):")
for target in (0.1, 0.05, 0.01):
    # solve n_ss(F)=target for F:  eta_rec2/F = target/(1+target) * eta_sb^2/r
    r = 5.0
    F_need = ETA_REC2 / ((target/(1+target)) * ETA_SB**2 / r)
    print("     n_ss = %.2f  needs FoM >= %5.0f   (x%4.0f beyond the bounded %.1f)"
          % (target, F_need, F_need/FOM, FOM))
print("   -> recovering n~0.01 needs FoM ~ 170 (x30); the rank-2 ceiling permits ~5.6.")
print("="*74)
print(" RESULT: with the detuning-independent FoM ~ %.1f the floor is n_ss = O(0.1-1)" % FOM)
print(" (here ~0.2-0.5, bracketing the independent 0.45); the disqualification is robust to the")
print(" +/- factor in parameters. Only FoM >~ 170 -- physically unreachable for a J=1/2 Dm=2")
print(" Raman -- would recover ground-state cooling. EIT (near-resonant) reaches n~0.005.  [V]")
print("="*74)
