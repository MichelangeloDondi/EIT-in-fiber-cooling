"""
detection_snr.py  --  computable in-fibre detection budget for the kagome-HCPCF
clock-EIT experiment.  Turns "can you measure any of it?" (fundamental issue #4)
into numbers, and identifies the viable method.

Question: state-selective readout (F=2 -> F'=3) of atoms INSIDE a 48 um hollow
core.  Three routes are scored here:
  (A) absorption / optical depth (OD) of a guided probe   -- the natural method
  (B) fluorescence collected into the guided mode          -- intrinsically weak
  (C) the co-propagating readout beam as background        -- why forward fluor. fails

Tags: [V] computed here, [I] estimate, [O] bench input to be measured.
Numbers internal in SI; reported in convenient units.
"""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engines"))
import operating_point as op

# ---- constants ----
hbar = 1.054571817e-34
c    = 2.99792458e8
kB   = 1.380649e-23
h    = 2*math.pi*hbar
m_Rb = 87*1.66053907e-27
lam  = 780.241e-9
kvec = 2*math.pi/lam
Gamma = 2*math.pi*op.GAMMA_D2_MHZ*1e6          # rad/s, from SSOT
Isat = 1.67e-3/1e-4                            # 1.67 mW/cm^2 cycling -> W/m^2 (=16.7)
w_mode = 19e-6                                 # 780 nm mode field radius (MFD 38 um) [I from fibre spec]

# ---- derived single-atom / mode quantities ----
A_mode  = math.pi*w_mode**2                    # m^2
sigma0  = 3*lam**2/(2*math.pi)                 # resonant cycling cross-section, m^2
E_ph    = h*c/lam                              # J per 780 photon
E_r     = (hbar*kvec)**2/(2*m_Rb); T_r = E_r/kB*1e6   # recoil temp per photon, uK
NA_eff  = lam/(math.pi*w_mode)                 # guided-mode divergence (effective NA)
eta_1dir = NA_eff**2/4                          # dipole->guided-mode coupling, ONE direction
OD_atom  = sigma0/A_mode                        # optical depth per atom on resonance

# ---- readout assumptions ----
s        = 1.0                                  # saturation parameter during readout [I]
QE       = 0.6                                  # detector quantum efficiency [I]
T_fibre  = 0.5                                  # 780 transmission over the readout path [I/O]
R_sc     = (Gamma/2)*s/(1+s)                     # scattering rate per atom, /s
T_rad0   = 100.0                                 # initial radial temperature, uK [I/O]
U0       = op.U0_UK                              # trap depth, uK (SSOT)

# photons an atom can scatter before it is lost from the trap (recoil heating of
# the soft radial mode) or pumped out of the cycle (off-resonant F'=2 leak):
dT_rad_per_photon = T_r/3.0                      # emission recoil into radial (~1/3 isotropic)
N_recoil_loss = (U0 - T_rad0)/dT_rad_per_photon
Delta_32 = 2*math.pi*266.65e6                    # F'=3 - F'=2 splitting, rad/s
p_leak   = (Gamma/(2*Delta_32))**2 * 0.5         # off-resonant F'2 excitation x branch to F=1
N_cycle_leak = 1.0/p_leak
N_scatter = min(N_recoil_loss, N_cycle_leak)     # usable photons per atom per shot

# ============================================================================
print("="*72)
print(" IN-FIBRE DETECTION BUDGET  (F=2 -> F'=3 readout, 48 um kagome core)")
print("="*72)
print(" mode: w=%.0f um  A_mode=%.2e cm^2   sigma0=%.2e cm^2   OD/atom=%.2e"
      % (w_mode*1e6, A_mode*1e4, sigma0*1e4, OD_atom))
print(" recoil T_r=%.3f uK/photon -> radial heating ~%.3f uK/photon" % (T_r, dT_rad_per_photon))
print(" usable scatter/atom: recoil-loss %.0f  vs  cycle-leak %.0f  -> N_scatter=%.0f"
      % (N_recoil_loss, N_cycle_leak, N_scatter))
print("-"*72)

# ---- (A) ABSORPTION / OD ----
print(" (A) ABSORPTION (OD) of a guided probe  [the natural in-fibre method]")
for N in (1e3, 4e3, 1e4):
    print("     N_atoms=%6.0f  ->  OD=%.2f   (transmission e^-OD = %.1f%%)"
          % (N, N*OD_atom, 100*math.exp(-N*OD_atom)))
N_for_OD1 = 1.0/OD_atom
# probe photons needed for a given OD resolution (shot-noise on transmitted+reference)
for dOD in (0.03, 0.01):
    N_probe = (math.e + 1)/dOD**2                # ~ (e^OD + 1)/dOD^2 at OD~1
    print("     OD resolution dOD=%.2f needs ~%.1e detected probe photons = %.1f fJ  (trivial)"
          % (dOD, N_probe, N_probe*E_ph*1e15))
print("     => OD~1 at N~%.0f atoms; probe photons are ~free, so absorption is NOT" % N_for_OD1)
print("        photon-limited. Floor on a per-shot population fraction f is the")
print("        atom-number/projection noise sqrt(f(1-f)/N), not detection. [V]")
print("-"*72)

# ---- (B) GUIDED-MODE FLUORESCENCE ----
print(" (B) FLUORESCENCE into the guided mode")
print("     NA_eff=%.4f -> eta_couple=%.2e per direction" % (NA_eff, eta_1dir))
N_coll_atom = N_scatter*eta_1dir*QE*T_fibre
print("     collected photons / atom / shot (backward, 1 dir) = %.3f" % N_coll_atom)
print("     => <1 photon per atom: fluorescence is INTRINSICALLY an ensemble method,")
print("        photon-starved at the single-atom level. [V]")
print("-"*72)

# ---- (C) READOUT-BEAM BACKGROUND ----
print(" (C) READOUT-BEAM BACKGROUND (why forward fluorescence fails)")
P_read = Isat*s*A_mode                            # W guided
ph_read = P_read/E_ph                             # readout photons/s in the mode
for N in (1e4,):
    sig_back = N*R_sc*eta_1dir                     # backward fluorescence into guided mode, /s
    print("     readout beam in mode: %.1f nW = %.2e photons/s (same wavelength as the signal)"
          % (P_read*1e9, ph_read))
    print("     fluorescence (N=%.0f) into guided mode: %.2e photons/s" % (N, sig_back))
    print("     FORWARD detection: signal/background = %.1e  -> readout swamps it (~%.0fx)."
          % (sig_back/ph_read, ph_read/sig_back))
    print("     BACKWARD detection rejects the (forward) readout by direction; residual")
    print("     background is then fibre BACKSCATTER x readout (HCPCF backscatter at 780 = [O]).")
print("="*72)
print(" CONCLUSION")
print("  - In-fibre detection should be ABSORPTION (OD): OD~1 at N~%.0f atoms, shot-noise on" % N_for_OD1)
print("    plentiful probe light -> detection is NOT the bottleneck (atom-number noise is).")
print("  - Guided-mode fluorescence is intrinsically ensemble (<1 photon/atom); forward is")
print("    swamped by the same-wavelength readout beam, backward is backscatter-limited [O].")
print("  - Single-atom in-fibre detection is NOT available -> the experiment is an ENSEMBLE OD")
print("    measurement (consistent with the 1D/ensemble scope; ties to the OD-vs-cooling item).")
print("  - Bench inputs to close it [O]: loaded N_atoms (sets OD), 780 transmission over the")
print("    readout path, and (for any fluorescence route) the HCPCF backscatter fraction.")
print("="*72)
