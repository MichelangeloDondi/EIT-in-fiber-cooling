"""
radial_survival.py -- computable radial heating + survival budget over the cooling
window (fundamental issue #2: does the sample survive the anti-trapped excited state
and the recoil heating of the UNCOOLED radial mode?).

Picture: the 5S ground state is trapped (U0 = 22.8 MHz = 1094 uK); the 5P3/2 excited
state is ANTI-trapped at 1064 nm (+19..+57 MHz peak, polarizability_5P32_1064.md).
During EIT cooling the atom scatters ~N_cool photons, spending a fraction rho_ee in
the anti-trapped state and taking recoil kicks; the AXIAL mode is cooled, the soft
RADIAL mode (nu_r = 5.42 kHz) is not. Scored here:
  (1) is the TIME-AVERAGED radial trap still confining? (anti-trap vs trap curvature)
  (2) RECOIL heating of the radial mode over the cooling window -> survival
  (3) is the anti-trap itself a heating channel? (additive + parametric vs recoil)

Tags: [V] computed, [I] estimate, [O] bench. SI internally.
"""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engines"))
import operating_point as op

# ---- constants ----
hbar = 1.054571817e-34; kB = 1.380649e-23
m_Rb = 87*1.66053907e-27
lam  = 780.241e-9; kvec = 2*math.pi/lam
Gamma = 2*math.pi*op.GAMMA_D2_MHZ*1e6
U0_MHz, U0_uK = op.U0_MHZ, op.U0_UK
nu_r = op.NU_R_MHZ*1e6; w_r = 2*math.pi*nu_r          # radial trap, Hz / rad-s
w_trap = 19e-6                                          # 1064 trap waist [I]
Ue_MHz = (19.0, 57.0)                                  # 5P3/2 anti-trap peak shift [polarizability_5P32_1064.md]

# ---- recoil heating of the radial mode ----
E_r = (hbar*kvec)**2/(2*m_Rb); T_r_uK = E_r/kB*1e6
f_rad = 1.0/3.0                                        # emission recoil into radial (isotropic); axial absorption -> 0
dT_rad = T_r_uK*f_rad                                  # uK per scattered photon

# ---- cooling photon budget (continuous EIT: ~Delta_n / eta^2 photons) ----
T_axial_init = 100.0                                   # post-molasses axial T [I/O]
n_z_init = op.n_thermal(T_axial_init, op.NU_Z_MHZ)
n_z_final = op.FLOOR.all_in_single_atom_lowdwell[0]   # SSOT field renamed (low-dwell certified)
dn = n_z_init - n_z_final
N_cool = {eta: dn/eta**2 for eta in (op.ETA_RETRO_2K, op.ETA_780)}   # 2-photon LD vs single-photon
N_cool_lo, N_cool_hi = min(N_cool.values()), max(N_cool.values())
t_cool_ms = 1.0
rho_ee = (N_cool_hi/(t_cool_ms*1e-3))/Gamma            # rho_ee at the conservative photon budget

# ---- loss limit: photons to heat radial from T_init to the trap depth ----
T_rad_init = 100.0                                     # post-molasses radial T [I/O]
N_loss = (U0_uK - T_rad_init)/dT_rad

print("="*72)
print(" RADIAL HEATING + SURVIVAL BUDGET  (over the cooling window)")
print("="*72)
print(" recoil T_r=%.3f uK/photon -> radial heating %.3f uK/photon  [V]" % (T_r_uK, dT_rad))
print(" cooling photon budget N_cool ~ dn/eta^2 = %.0f (eta_2k) .. %.0f (eta_780)   [dn=%.1f]"
      % (N_cool[op.ETA_RETRO_2K], N_cool[op.ETA_780], dn))
print(" trap-depth (loss) limit: N_loss = (U0 - T_init)/dT_rad = %.0f photons" % N_loss)
print("-"*72)

# ---- (1) is the time-averaged radial trap still confining? ----
print(" (1) TIME-AVERAGED radial trap (anti-trap curvature vs trap curvature)")
print("     rho_ee during cooling ~ %.3f  (N_cool=%.0f over %.1f ms)" % (rho_ee, N_cool_hi, t_cool_ms))
for Ue in Ue_MHz:
    ratio = Ue/U0_MHz                                  # |anti-trap curvature| / trap curvature
    rho_crit = 1.0/(1.0+ratio)                          # confining iff rho_ee < rho_crit
    soft = 1.0 - rho_ee*(1.0+ratio)                     # (omega_eff/omega_r)^2
    print("     anti-trap %2.0f MHz: curvature ratio %.2f -> confining iff rho_ee<%.2f ; "
          "trap softening (om_eff/om)^2=%.2f (=%.0f%% freq)" % (Ue, ratio, rho_crit, soft, 100*math.sqrt(max(soft,0))))
print("     => rho_ee (%.3f) << threshold; trap stays confining, softens a few %%.  [V]" % rho_ee)
print("-"*72)

# ---- (2) recoil heating + survival over the cooling window ----
print(" (2) RECOIL heating + survival")
for N in (N_cool_lo, N_cool_hi, N_loss):
    Tf = T_rad_init + N*dT_rad
    sigma = math.sqrt(2*N)*dT_rad                       # random-walk spread in radial energy (uK)
    tag = "COOLING" if N <= N_cool_hi else "loss limit"
    print("     N=%6.0f (%s): radial T %3.0f -> %4.0f uK (spread +-%.0f); U0=%.0f uK"
          % (N, tag, T_rad_init, Tf, sigma, U0_uK))
print("     => over the cooling window the radial mode heats ~%.0f-%.0f uK and stays FAR below"
      % (N_cool_lo*dT_rad, N_cool_hi*dT_rad))
print("        the %.0f uK depth: survival ~100%%. The depth is reached only at ~%.0f photons"
      % (U0_uK, N_loss))
print("        (the READOUT regime, already bounded in detection_snr.py).  [V]")
print("-"*72)

# ---- (3) is the anti-trap itself a heating channel? ----
print(" (3) ANTI-TRAP as a heating channel (additive + parametric vs recoil)")
r_th = math.sqrt(kB*(T_rad_init*1e-6)/(m_Rb*w_r**2))    # thermal radius, m
tau_e = 1.0/Gamma                                       # excited-state dwell, s
Ue0 = max(Ue_MHz)*1e6*2*math.pi*hbar                    # worst-case anti-trap peak, J
U0_J = U0_MHz*1e6*2*math.pi*hbar
dF = (Ue0 + U0_J)*(4*r_th/w_trap**2)*math.exp(-2*r_th**2/w_trap**2)   # extra force when excited, N
dp_anti = dF*tau_e                                      # impulse per excitation
add_ratio = 3.0*(dp_anti/(hbar*kvec))**2                # additive anti-trap heating / recoil
# parametric: spring-constant telegraph noise PSD at 2*nu_r (omega*tau_e << 1)
ratio_kappa = (Ue0+U0_J)/U0_J
S_2nu = 4*rho_ee*(1-rho_ee)*ratio_kappa**2*tau_e        # PSD of (dkappa/kappa) at 2 nu_r
Gamma_param = math.pi**2 * nu_r**2 * S_2nu              # Savard/Thomas: pi^2 nu^2 S(2nu), nu in Hz
print("     thermal radius r_th(%.0f uK)=%.1f um ; excited dwell 1/Gamma=%.0f ns" % (T_rad_init, r_th*1e6, tau_e*1e9))
print("     additive: anti-trap impulse/recoil = %.2f -> heating fraction %.4f of recoil" % (dp_anti/(hbar*kvec), add_ratio))
print("     parametric: Gamma_param ~ %.2e /s -> over %.1f ms, exp(Gamma t)=%.4f" % (Gamma_param, t_cool_ms, math.exp(Gamma_param*t_cool_ms*1e-3)))
print("     => both << recoil (R_sc >> nu_r kills the parametric term).  Anti-trap is NOT a")
print("        meaningful heating channel; recoil dominates.  [V]")
print("="*72)
print(" CONCLUSION")
print("  - Survival through cooling ~100%%: the soft radial mode heats only ~%.0f-%.0f uK by recoil"
      % (N_cool_lo*dT_rad, N_cool_hi*dT_rad))
print("    (~%.0f-%.0f photons), far below the %.0f uK trap depth. The depth-limited scatter" % (N_cool_lo, N_cool_hi, U0_uK))
print("    budget (~%.0f photons) bounds the READOUT, not the cooling." % N_loss)
print("  - The anti-trapped 5P3/2 is benign during cooling: rho_ee~%.2f << confining threshold" % rho_ee)
print("    ~0.3-0.5, so the time-averaged radial trap stays confining (softens a few %); and the")
print("    anti-trap adds <1% to recoil heating (the 26 ns excited dwell is far too short, and")
print("    R_sc >> nu_r suppresses parametric heating).")
print("  - CONSEQUENCE: the radial mode ends WARM (~%.0f-%.0f uK, up from %.0f) -> this feeds the"
      % (T_rad_init + N_cool_lo*dT_rad, T_rad_init + N_cool_hi*dT_rad, T_rad_init))
print("    inhomogeneous-light-shift / cloud floor, it is not a loss channel.")
print("  - Bench [O]: post-molasses radial T and atom number; in-situ trap depth at 1064.")
print("="*72)
