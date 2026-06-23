"""Breit-Rabi: dnu/dB for the 87Rb ground clock pairs. m=0 vs the m=+-1 magic pair."""
import numpy as np
DHF = 6834.682610      # MHz, 5S1/2 ground hyperfine splitting
gJ  = 2.0023311
gI  = -0.0009951414
muB = 1.399624         # MHz/G  (mu_B/h)
I   = 1.5

def E(F, m, B):
    # Breit-Rabi energy (MHz/h) for F = I +- 1/2
    x = (gJ - gI)*muB*B/DHF
    pm = +1 if F == 2 else -1
    return -DHF/(2*(2*I+1)) + gI*muB*m*B + pm*(DHF/2)*np.sqrt(1 + 4*m*x/(2*I+1) + x**2)

def nu_m0(B):   return E(2,0,B)  - E(1,0,B)        # |1,0>-|2,0> clock
def nu_pm1(B):  return E(2,+1,B) - E(1,-1,B)       # |1,-1>-|2,+1> magic pair

def slope(f, B, h=1e-4):  # MHz/G
    return (f(B+h)-f(B-h))/(2*h)

print("="*70)
print(" 87Rb ground clock pairs: field sensitivity  |dnu/dB|  (Hz/G)")
print("="*70)
print(" %6s | %14s | %16s" % ("B (G)", "m=0  |1,0>-|2,0>", "m=+-1 |1,-1>-|2,+1>"))
print(" "+"-"*60)
for B in (0.5, 1.0, 1.5, 3.229, 5.0):
    s0  = abs(slope(nu_m0,  B))*1e6   # Hz/G
    sp1 = abs(slope(nu_pm1, B))*1e6
    print(" %6.3f | %14.0f | %16.1f" % (B, s0, sp1))
print(" "+"-"*60)

# m=0 quadratic coefficient (Hz/G^2): nu = nu0 + K B^2
K = (nu_m0(1.0)-nu_m0(0.0))*1e6   # Hz at 1 G ~ K*1^2
print(" m=0 quadratic coeff  K = %.1f Hz/G^2   (slope = 2K*B)" % K)

# find magic field for m=+-1 (dnu/dB = 0)
from scipy.optimize import brentq
Bmag = brentq(lambda B: slope(nu_pm1,B), 2.5, 4.0)
# residual curvature at magic: nu ~ nu_mag + 0.5*beta*(B-Bmag)^2
h=1e-3
beta = (nu_pm1(Bmag+h)-2*nu_pm1(Bmag)+nu_pm1(Bmag-h))/h**2 * 1e6  # Hz/G^2
print(" m=+-1 magic field B_mag = %.4f G ;  residual curvature = %.1f Hz/G^2" % (Bmag, beta))
print("    -> at B_mag, |dnu/dB| = %.2f Hz/G (first-order zero); leading shift ~0.5*beta*dB^2" % (abs(slope(nu_pm1,Bmag))*1e6))

print("="*70)
print(" DEPHASING for field noise dB (Hz):  linear pairs ~ |dnu/dB|*dB")
print(" %8s | %12s | %12s | %16s" % ("dB", "m=0 @1.5G", "m=0 @3.23G", "magic @B_mag (quad)"))
for dB_mG in (0.1, 1.0, 10.0):
    dB = dB_mG/1000.0
    d_m0_15  = abs(slope(nu_m0,1.5))*1e6*dB
    d_m0_323 = abs(slope(nu_m0,3.229))*1e6*dB
    d_mag    = 0.5*abs(beta)*dB**2
    print(" %5.1f mG | %9.2f Hz | %9.2f Hz | %12.4f Hz" % (dB_mG, d_m0_15, d_m0_323, d_mag))
print("="*70)
